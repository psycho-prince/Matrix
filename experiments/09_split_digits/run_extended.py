#!/usr/bin/env python3
"""Multi-seed Split Digits continual-learning study.

Protocol:
- Per seed, stratified 60/20/20 train/validation/test split.
- EWC strength selected on tuning seeds only; evaluation seeds are disjoint.
- Evaluation: 20 seeds by default (20..39).
- FT, tuned EWC, ER at four exemplar budgets, and selective-inheritance GAL-CL.
- Equal optimizer steps and batch size within each seed/task.
- Report final all-class accuracy, task-wise forgetting and per-class accuracy.
"""
from __future__ import annotations
import argparse, json, random, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

TASKS=((0,1),(2,3),(4,5),(6,7),(8,9))
BATCH=64
MEMORIES=(5,10,20,50)
EWC_GRID=(1.0,10.0,100.0,1000.0)
GAL_KEEP=0.70

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(64,128),nn.ReLU(),nn.Linear(128,64),nn.ReLU(),nn.Linear(64,10))
    def forward(self,x): return self.net(x)

def seed_all(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)

def split_data(seed):
    d=load_digits()
    x=torch.tensor(d.data,dtype=torch.float32)/16.0
    y=torch.tensor(d.target,dtype=torch.long)
    idx=np.arange(len(y))
    trainval,test=train_test_split(idx,test_size=.20,random_state=seed,stratify=d.target)
    train,val=train_test_split(trainval,test_size=.25,random_state=seed+10000,stratify=d.target[trainval])
    return (x[train],y[train]),(x[val],y[val]),(x[test],y[test])

def accuracy(model,x,y):
    model.eval()
    with torch.no_grad():
        return float((model(x).argmax(1)==y).float().mean())

def fisher_diag(model,x,y):
    model.eval()
    f={n:torch.zeros_like(p) for n,p in model.named_parameters()}
    for i in range(len(y)):
        model.zero_grad(set_to_none=True)
        nn.functional.cross_entropy(model(x[i:i+1]),y[i:i+1]).backward()
        for n,p in model.named_parameters():
            if p.grad is not None: f[n]+=p.grad.detach().square()/len(y)
    return f

def make_memory(x,y,per_class,seed):
    mx=[]; my=[]
    for c in range(10):
        ids=torch.where(y==c)[0]
        if not len(ids): continue
        g=torch.Generator().manual_seed(seed*1009+c)
        chosen=ids[torch.randperm(len(ids),generator=g)[:min(per_class,len(ids))]]
        mx.append(x[chosen]); my.append(y[chosen])
    return (torch.cat(mx),torch.cat(my)) if mx else (torch.empty((0,64)),torch.empty((0,),dtype=torch.long))

def fit_task(model,tx,ty,opt,seed,ewc=None,replay=None,steps=None):
    nsteps=steps if steps is not None else int(np.ceil(len(ty)/BATCH))
    model.train()
    for i in range(nsteps):
        if replay is None:
            g=torch.Generator().manual_seed(seed*17+i)
            ids=torch.randint(len(ty),(BATCH,),generator=g)
            xb,yb=tx[ids],ty[ids]
        else:
            rx,ry=replay
            gi=torch.Generator().manual_seed(seed*31+i)
            ci=torch.randint(len(ty),(BATCH//2,),generator=gi)
            ri=torch.randint(len(ry),(BATCH//2,),generator=gi)
            xb=torch.cat([tx[ci],rx[ri]],0); yb=torch.cat([ty[ci],ry[ri]],0)
        opt.zero_grad(set_to_none=True)
        loss=nn.functional.cross_entropy(model(xb),yb)
        if ewc is not None:
            constraints, strength = ewc
            loss = loss + (strength / 2.0) * ewc_penalty(model, constraints)
        loss.backward(); opt.step()
    return nsteps

def apply_gal_inheritance(model, fisher, keep=GAL_KEEP):
    """GAL-CL selective inheritance: preserve top-importance 70% scalar weights.

    A child starts as a clone of its parent. Fisher importance ranks parameter
    scalars globally; the highest-ranked fraction is inherited exactly, while
    the remaining fraction is reinitialized with Xavier/zero initialization.
    No replay examples are retained. This is an explicit neural operationalization
    of selective generational inheritance, not native symbolic GAL.
    """
    scores=torch.cat([fisher[n].detach().flatten().cpu() for n,p in model.named_parameters()])
    n_keep=max(1,int(keep*scores.numel()))
    selected=torch.zeros(scores.numel(),dtype=torch.bool)
    selected[torch.topk(scores,n_keep,sorted=False).indices]=True
    with torch.no_grad():
        offset=0
        for name,p in model.named_parameters():
            count=p.numel()
            mask=selected[offset:offset+count].to(p.device).reshape_as(p)
            offset+=count
            if p.ndim>=2:
                fresh=torch.empty_like(p); nn.init.xavier_uniform_(fresh)
            else:
                fresh=torch.zeros_like(p)
            p.copy_(torch.where(mask,p,fresh))

def task_mask(labels: torch.Tensor, classes: tuple[int, ...]) -> torch.Tensor:
    """Return a boolean mask for exactly the requested class labels."""
    return torch.isin(labels, torch.tensor(classes, dtype=labels.dtype, device=labels.device))


def evaluate_task_matrix(model, x, y, tasks=TASKS):
    """Evaluate every task's classes on the same held-out test partition."""
    scores = []
    for task in tasks:
        mask = task_mask(y, task)
        if not bool(mask.any()):
            raise ValueError(f"Test partition contains no examples for task {task}")
        scores.append(accuracy(model, x[mask], y[mask]))
    return scores


def calculate_forgetting(task_matrix):
    """For each task, max post-learning accuracy minus final accuracy."""
    if not task_matrix or any(len(row) != len(task_matrix) for row in task_matrix):
        raise ValueError("task_matrix must be a non-empty square task-by-evaluation matrix")
    n_tasks = len(task_matrix)
    forgetting = []
    for task_index in range(n_tasks):
        best_after_learning = max(
            task_matrix[evaluation_index][task_index]
            for evaluation_index in range(task_index, n_tasks)
        )
        final_accuracy = task_matrix[-1][task_index]
        forgetting.append(best_after_learning - final_accuracy)
    return forgetting


def ewc_penalty(model, task_constraints):
    """Sum task-specific diagonal-Fisher penalties around each task's own optimum."""
    penalty = torch.zeros((), device=next(model.parameters()).device)
    params = dict(model.named_parameters())
    for fisher, reference in task_constraints:
        if fisher.keys() != params.keys() or reference.keys() != params.keys():
            raise ValueError("EWC constraint parameter names do not match model")
        for name, parameter in params.items():
            penalty = penalty + (fisher[name] * (parameter - reference[name]).square()).sum()
    return penalty

def run_method(method,seed,epochs,memory=0,ewc_strength=0.0):
    seed_all(seed)
    (xtr,ytr),(xv,yv),(xt,yt)=split_data(seed)
    model=MLP()
    opt=torch.optim.Adam(model.parameters(),lr=1e-3)
    fisher={n:torch.zeros_like(p) for n,p in model.named_parameters()}
    ewc_constraints=[]
    task_matrix=[]; steps=[]; memory_x=[]; memory_y=[]
    for ti,task in enumerate(TASKS):
        mask=torch.isin(ytr,torch.tensor(task))
        tx,ty=xtr[mask],ytr[mask]
            if method=="GAL-CL" and ti>0:
            apply_gal_inheritance(model, fisher, GAL_KEEP)
            opt=torch.optim.Adam(model.parameters(),lr=1e-3)
        replay=None
        if method.startswith("ER") and memory_x:
            replay=(torch.cat(memory_x),torch.cat(memory_y))
        ewc=(ewc_constraints,ewc_strength) if method=="EWC" and ewc_constraints else None
        n=0
        for ep in range(epochs):
            n+=fit_task(model,tx,ty,opt,seed*100+ti*10+ep,ewc,replay,steps=int(np.ceil(len(ty)/BATCH)))
        steps.append(n)
        if method in ("EWC", "GAL-CL"):
            fnew = fisher_diag(model, tx, ty)
            if method == "EWC":
                # Keep each task's Fisher and parameter optimum paired.
                ewc_constraints.append((
                    {name: value.detach().clone() for name, value in fnew.items()},
                    {name: parameter.detach().clone()
                     for name, parameter in model.named_parameters()},
                ))
            for name in fisher:
                fisher[name] += fnew[name]
        if method.startswith("ER"):
            mx,my=make_memory(tx,ty,memory,seed+ti)
            memory_x.append(mx); memory_y.append(my)
        task_matrix.append(evaluate_task_matrix(model,xt,yt))
    final=accuracy(model,xt,yt)
    per_class={str(c):accuracy(model,xt[yt==c],yt[yt==c]) for c in range(10)}
    task_final=[task_matrix[i][i] for i in range(len(TASKS))]
    forgetting=calculate_forgetting(task_matrix)
    return {"method":method,"seed":seed,"final_accuracy":final,
            "accuracy_after_each_task":task_matrix,"final_seen_task_accuracy":task_final,
            "forgetting_per_task":forgetting,"mean_forgetting":float(np.mean(forgetting)),
            "per_class_accuracy":per_class,"optimizer_steps_per_task":steps,
            "memory_examples":sum(len(z) for z in memory_y)}

def tune_ewc(seeds,epochs):
    scores={lam:[] for lam in EWC_GRID}
    for seed in seeds:
        for lam in EWC_GRID:
            seed_all(seed)
            (xtr,ytr),(xv,yv),_=split_data(seed)
            model=MLP(); opt=torch.optim.Adam(model.parameters(),lr=1e-3)
            ewc_constraints=[]
            for ti,task in enumerate(TASKS):
                m=torch.isin(ytr,torch.tensor(task)); tx,ty=xtr[m],ytr[m]
                for ep in range(epochs):
                    fit_task(model, tx, ty, opt, seed*100+ti*10+ep,
                             (ewc_constraints, lam) if ewc_constraints else None)
                f = fisher_diag(model, tx, ty)
                ewc_constraints.append((
                    {name: value.detach().clone() for name, value in f.items()},
                    {name: parameter.detach().clone()
                     for name, parameter in model.named_parameters()},
                ))
            scores[lam].append(accuracy(model,xv,yv))
    means={str(k):float(np.mean(v)) for k,v in scores.items()}
    best=max(EWC_GRID,key=lambda k:np.mean(scores[k]))
    return best,means

def summarize(rows):
    methods=sorted({r["method"] for r in rows})
    out={}
    for method in methods:
        rr=[r for r in rows if r["method"]==method]
        def stat(vals):
            a=np.asarray(vals,dtype=float)
            return {"n":int(len(a)),"mean":float(a.mean()),"sd":float(a.std(ddof=1)) if len(a)>1 else 0.0,
                    "ci95_normal":[float(a.mean()-1.96*a.std(ddof=1)/np.sqrt(len(a))),float(a.mean()+1.96*a.std(ddof=1)/np.sqrt(len(a)))]}
        out[method]={"final_accuracy":stat([r["final_accuracy"] for r in rr]),
                     "mean_forgetting":stat([r["mean_forgetting"] for r in rr]),
                     "per_class_accuracy":{str(c):stat([r["per_class_accuracy"][str(c)] for r in rr]) for c in range(10)}}
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--tune-seeds",type=int,default=10)
    ap.add_argument("--eval-seeds",type=int,default=20)
    ap.add_argument("--epochs",type=int,default=8)
    ap.add_argument("--out",default="experiments/09_split_digits/results_extended.json")
    a=ap.parse_args()
    if a.tune_seeds < 2 or a.eval_seeds < 2 or a.epochs < 1:
        raise SystemExit("Use at least 2 tuning and evaluation seeds, and at least 1 epoch")
    start=time.time()
    tune_ids=list(range(a.tune_seeds))
    eval_ids=list(range(1000,1000+a.eval_seeds))
    best_ewc,ewc_val=tune_ewc(tune_ids,a.epochs)
    rows=[]
    specs=[("FT",0),("EWC",0)]+[(f"ER-{m}",m) for m in MEMORIES]+[("GAL-CL",0)]
    for method,memory in specs:
        for seed in eval_ids:
            row=run_method(method,seed,a.epochs,memory,best_ewc)
            rows.append(row); print(json.dumps({"method":method,"seed":seed,"final_accuracy":row["final_accuracy"],"mean_forgetting":row["mean_forgetting"]}),flush=True)
    report={"benchmark":"split-digits-class-incremental-extended-v1",
            "protocol":{"tuning_seeds":tune_ids,"evaluation_seeds":eval_ids,"epochs_per_task":a.epochs,
            "batch_size":BATCH,"ewc_grid":EWC_GRID,"selected_ewc_strength":best_ewc,
            "ewc_validation_accuracy":ewc_val,"replay_memories_per_class":MEMORIES,
            "gal_cl_keep_fraction":GAL_KEEP,"gal_cl_rule":"global Fisher top-70% exact parent scalar inheritance; remaining scalars Xavier/zero reset; no replay"},
            "summary":summarize(rows),"results":rows,"elapsed_seconds":time.time()-start}
    p=Path(a.out); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(report,indent=2))
    print("WROTE",p)
if __name__=="__main__": main()
