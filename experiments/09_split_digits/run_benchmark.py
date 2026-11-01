#!/usr/bin/env python3
"""Budget-matched class-incremental benchmark on sklearn Digits.

FT/EWC/ER receive the same optimizer-step count and batch size per task.
ER uses half current-task examples and half replay examples in each batch.
"""
from __future__ import annotations
import argparse, json, random, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

TASKS = [(0,1),(2,3),(4,5),(6,7),(8,9)]
METHODS = ("FT","EWC","ER")
BATCH_SIZE = 64

class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(64,128),nn.ReLU(),nn.Linear(128,64),nn.ReLU(),nn.Linear(64,10))
    def forward(self,x): return self.net(x)

def seed_all(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)

def accuracy(model,x,y):
    model.eval()
    with torch.no_grad():
        return float((model(x).argmax(1)==y).float().mean().item())

def train_standard(model,loader,opt,ewc):
    model.train(); steps=0
    for xb,yb in loader:
        opt.zero_grad()
        loss=nn.functional.cross_entropy(model(xb),yb)
        if ewc is not None:
            fisher,means,strength=ewc
            penalty=sum((fisher[n]*(p-means[n]).pow(2)).sum() for n,p in model.named_parameters())
            loss=loss+(strength/2.0)*penalty
        loss.backward(); opt.step(); steps+=1
    return steps

def train_er(model,tx,ty,rx,ry,opt,seed,ewc):
    """Same number of 64-example optimizer steps as standard training."""
    steps=int(np.ceil(len(ty)/BATCH_SIZE))
    gen=torch.Generator().manual_seed(seed+7919)
    model.train()
    for _ in range(steps):
        ci=torch.randint(len(ty),(BATCH_SIZE//2,),generator=gen)
        ri=torch.randint(len(ry),(BATCH_SIZE//2,),generator=gen)
        xb=torch.cat([tx[ci],rx[ri]],0)
        yb=torch.cat([ty[ci],ry[ri]],0)
        opt.zero_grad()
        loss=nn.functional.cross_entropy(model(xb),yb)
        if ewc is not None:
            fisher,means,strength=ewc
            penalty=sum((fisher[n]*(p-means[n]).pow(2)).sum() for n,p in model.named_parameters())
            loss=loss+(strength/2.0)*penalty
        loss.backward(); opt.step()
    return steps

def estimate_fisher(model,x,y):
    model.eval(); fisher={n:torch.zeros_like(p) for n,p in model.named_parameters()}
    for i in range(len(y)):
        model.zero_grad()
        nn.functional.cross_entropy(model(x[i:i+1]),y[i:i+1]).backward()
        for n,p in model.named_parameters():
            if p.grad is not None: fisher[n]+=p.grad.detach().pow(2)/len(y)
    return fisher

def run_one(method,seed,epochs,memory_per_class,ewc_strength):
    seed_all(seed)
    d=load_digits()
    x=torch.tensor(d.data,dtype=torch.float32)/16.0
    y=torch.tensor(d.target,dtype=torch.long)
    idx=np.arange(len(y))
    train_idx,test_idx=train_test_split(idx,test_size=.30,random_state=seed,stratify=d.target)
    xtr,ytr=x[train_idx],y[train_idx]; xte,yte=x[test_idx],y[test_idx]
    model=MLP(); opt=torch.optim.Adam(model.parameters(),lr=1e-3)
    fisher={n:torch.zeros_like(p) for n,p in model.named_parameters()}
    means={n:p.detach().clone() for n,p in model.named_parameters()}
    memory_x=[]; memory_y=[]; per_task=[]; step_counts=[]; processed=[]
    for ti,task in enumerate(TASKS):
        mask=torch.tensor(np.isin(ytr.numpy(),task))
        tx,ty=xtr[mask],ytr[mask]
        loader=DataLoader(TensorDataset(tx,ty),batch_size=BATCH_SIZE,shuffle=True,
                          generator=torch.Generator().manual_seed(seed+sum(task)))
        ewc=(fisher,means,ewc_strength) if method=="EWC" else None
        total_steps=0
        for ep in range(epochs):
            if method=="ER" and memory_x:
                rx,ry=torch.cat(memory_x),torch.cat(memory_y)
                total_steps+=train_er(model,tx,ty,rx,ry,opt,seed+ti*100+ep,ewc)
            else:
                total_steps+=train_standard(model,loader,opt,ewc)
        if method=="EWC":
            fnew=estimate_fisher(model,tx,ty)
            for n in fisher: fisher[n]+=fnew[n]
            means={n:p.detach().clone() for n,p in model.named_parameters()}
        if method=="ER":
            for cls in task:
                cidx=torch.where(ty==cls)[0]
                take=min(memory_per_class,len(cidx))
                gen=torch.Generator().manual_seed(seed*100+cls)
                chosen=cidx[torch.randperm(len(cidx),generator=gen)[:take]]
                memory_x.append(tx[chosen]); memory_y.append(ty[chosen])
        step_counts.append(total_steps)
        processed.append(total_steps*BATCH_SIZE)
        per_task.append(accuracy(model,xte,yte))
    return {"method":method,"seed":seed,"final_accuracy":accuracy(model,xte,yte),
            "accuracy_after_each_task":per_task,"optimizer_steps_per_task":step_counts,
            "training_examples_processed_per_task":processed}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seeds",type=int,default=3)
    ap.add_argument("--epochs",type=int,default=8)
    ap.add_argument("--memory-per-class",type=int,default=20)
    ap.add_argument("--ewc-strength",type=float,default=100.0)
    ap.add_argument("--out",default="experiments/09_split_digits/results.json")
    args=ap.parse_args()
    if args.seeds<1 or args.epochs<1: raise SystemExit("seeds and epochs must be >=1")
    start=time.time(); rows=[]
    for method in METHODS:
        for seed in range(args.seeds):
            row=run_one(method,seed,args.epochs,args.memory_per_class,args.ewc_strength)
            rows.append(row); print(json.dumps(row),flush=True)
    report={"benchmark":"sklearn-digits-5-task-class-incremental-budget-matched",
            "methods":list(METHODS),"seeds":args.seeds,"epochs_per_task":args.epochs,
            "batch_size":BATCH_SIZE,"er_batch_composition":"32 current + 32 replay",
            "memory_per_class":args.memory_per_class,"ewc_strength":args.ewc_strength,
            "results":rows,"elapsed_seconds":time.time()-start}
    path=Path(args.out); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2)); print("WROTE",path)
if __name__=="__main__": main()
