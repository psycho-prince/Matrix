"""Controlled symbolic knowledge lifecycle across generations."""
from __future__ import annotations
from dataclasses import asdict, dataclass, replace
import hashlib, json, random
from collections import defaultdict

@dataclass(frozen=True)
class FactKey:
    subject: str
    relation: str
    context: str

@dataclass(frozen=True)
class Claim:
    key: FactKey
    value: str
    source_agent: str
    source_generation: int
    evidence_id: str
    confidence: float
    verified: bool = False
    lineage: tuple[str, ...] = ()

class KnowledgeStore:
    def __init__(self, agent_id: str, generation: int):
        self.agent_id, self.generation = agent_id, generation
        self.claims: list[Claim] = []
        self.audit: list[dict] = []

    def acquire(self, key, value, evidence_id, confidence=0.7):
        if not value or not evidence_id or not 0 <= confidence <= 1:
            raise ValueError("invalid claim")
        claim = Claim(key, value, self.agent_id, self.generation, evidence_id, confidence)
        self.claims.append(claim)
        self.audit.append({"event":"acquired","evidence_id":evidence_id,"value":value})
        return claim

    def verify(self, claim, heldout_oracle):
        if claim not in self.claims:
            raise ValueError("claim does not belong to this store")
        passed = heldout_oracle.get(claim.key) == claim.value
        updated = replace(claim, verified=passed)
        self.claims[self.claims.index(claim)] = updated
        self.audit.append({"event":"verified" if passed else "rejected","evidence_id":claim.evidence_id})
        return updated

    def answer(self, key, verified_only=True):
        candidates = [c for c in self.claims if c.key == key and (c.verified or not verified_only)]
        values = {c.value for c in candidates}
        if not candidates:
            return {"status":"unknown","answer":None,"evidence":[]}
        if len(values) != 1:
            return {"status":"conflict","answer":None,"evidence":sorted(c.evidence_id for c in candidates)}
        chosen = max(candidates, key=lambda c:(c.verified,c.confidence,c.evidence_id))
        return {"status":"answered","answer":chosen.value,"evidence":[c.evidence_id for c in candidates]}

    def inherit(self, child_id, child_generation, mode):
        if mode not in {"verified_only","all_memory","noisy_transfer","none"}:
            raise ValueError("unknown inheritance mode")
        child = KnowledgeStore(child_id, child_generation)
        selected = ([c for c in self.claims if c.verified] if mode=="verified_only"
                    else list(self.claims) if mode in {"all_memory","noisy_transfer"} else [])
        for c in selected:
            child.claims.append(Claim(c.key,c.value,c.source_agent,c.source_generation,
                c.evidence_id,c.confidence,False,c.lineage+(self.agent_id,)))
        child.audit.append({"event":"inherited","mode":mode,"count":len(selected),"from":self.agent_id})
        return child

def _world():
    names={"France":"Paris","Japan":"Tokyo","Kenya":"Nairobi","Brazil":"Brasilia",
           "Nepal":"Kathmandu","Canada":"Ottawa","Egypt":"Cairo","Norway":"Oslo",
           "Peru":"Lima","Ghana":"Accra","India":"New Delhi","Chile":"Santiago"}
    return {FactKey(k,"capital","geography"):v for k,v in names.items()}

def run_experiment(seed_start=7300,seeds=40,generations=4):
    if seeds<1 or generations<2: raise ValueError("need >=1 seed and >=2 generations")
    modes=("none","verified_only","all_memory","noisy_transfer")
    truth=_world(); keys=list(truth); aggregate={m:defaultdict(int) for m in modes}; raw=[]
    for seed in range(seed_start,seed_start+seeds):
        order=list(keys); random.Random(seed).shuffle(order); train,heldout=order[:8],order[8:]
        for mode in modes:
            store=KnowledgeStore(f"{mode}-s{seed}-g0",0)
            for i,key in enumerate(train):
                value=truth[key] + ("-noise" if i in (1,5) else "")
                store.acquire(key,value,f"s{seed}-g0-e{i}",0.9)
            for claim in list(store.claims): store.verify(claim,truth)
            rows=[]
            for gen in range(generations):
                correct=answered=conflicts=0
                for key in keys:
                    result=store.answer(key)
                    answered += result["status"]=="answered"
                    conflicts += result["status"]=="conflict"
                    correct += result["status"]=="answered" and result["answer"]==truth[key]
                rows.append({"generation":gen,"known_answers":answered,"correct":correct,
                             "conflicts":conflicts,"accuracy_all_world":correct/len(keys),
                             "coverage":answered/len(keys)})
                for metric,value in (("correct",correct),("answered",answered),("conflicts",conflicts)):
                    aggregate[mode][metric]+=value
                if gen<generations-1:
                    child=store.inherit(f"{mode}-s{seed}-g{gen+1}",gen+1,mode)
                    for j,key in enumerate(heldout[:2]):
                        if not any(c.key==key for c in child.claims):
                            child.acquire(key,truth[key],f"s{seed}-g{gen+1}-new{j}",0.85)
                            child.verify(child.claims[-1],truth)
                    store=child
            raw.append({"seed":seed,"mode":mode,"generations":rows,
                        "final_claims":len(store.claims),"final_verified":sum(c.verified for c in store.claims),
                        "audit_events":len(store.audit)})
    denom=seeds*generations*len(keys); summary={}
    for mode in modes:
        a=aggregate[mode]
        summary[mode]={"accuracy_all_world":a["correct"]/denom,"coverage":a["answered"]/denom,
            "conflict_rate":a["conflicts"]/denom,"answered":a["answered"],
            "correct":a["correct"],"total_probes":denom}
    report={"schema_version":1,"experiment":"gal2_generational_knowledge_lifecycle",
        "design":{"seed_start":seed_start,"seeds":seeds,"generations":generations,
                  "world_facts":len(keys),"training_facts":8,"new_facts_per_child":2,"arms":list(modes)},
        "summary":summary,"raw_results":raw,
        "interpretation":"Symbolic software test only. Held-out oracle verifies claims but is not used to answer. Fresh acquisition is separated from inheritance. No claim of general intelligence."}
    canonical=json.dumps(report,sort_keys=True,separators=(",",":")).encode()
    report["results_sha256"]=hashlib.sha256(canonical).hexdigest()
    return report

if __name__=="__main__": print(json.dumps(run_experiment(),indent=2))
