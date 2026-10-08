import os
import json
import time
from google import genai
from google.genai import types

API_KEY = "AQ.Ab8RN6JRqtEKDKb2Gr85wU9RpKvBfom_vpiyfqdNcKmdbuwa6g"
MODEL = 'gemini-3.5-flash-lite'

client = genai.Client(api_key=API_KEY)

TASKS = [
    {
        "id": 1,
        "desc": "You are hungry in a strange forest. You see bright red berries on a low bush and dark blue berries high up on a thorny vine. What do you do to get food?",
        "evaluation_rules": "If they eat the red berries, they get violently ill (Score: 2). If they brave the thorns for the blue berries, they are nourished (Score: 10). If they do neither, they starve (Score: 0)."
    },
    {
        "id": 2,
        "desc": "A large, fast predator spots you! There is a tall, smooth tree nearby, and a dark, narrow cave entrance. How do you escape?",
        "evaluation_rules": "If they climb the smooth tree, they slide down and get caught (Score: 1). If they run into the narrow cave, the predator cannot fit and they escape (Score: 10)."
    }
]

def llm_generate(prompt: str) -> str:
    time.sleep(4.5) # Prevent hitting the 15 RPM free tier limit
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        return response.text.strip()
    except Exception as e:
        print(f"API Error: {e}")
        return "Action failed due to cognitive error."

def evaluate_action(task_desc: str, rules: str, action: str):
    prompt = f"""
You are the Environment Judge. 
Task: {task_desc}
Agent's Action: {action}
Rules for Evaluation: {rules}

Evaluate the agent's action. Provide your response in exactly this format:
SCORE: [A number from 0 to 10]
OUTCOME: [A short one-sentence description of what happened to the agent based on their action]
"""
    result = llm_generate(prompt)
    try:
        score_line = [line for line in result.split('\n') if "SCORE:" in line][0]
        score = int(score_line.replace("SCORE:", "").strip())
        outcome_line = [line for line in result.split('\n') if "OUTCOME:" in line][0]
        outcome = outcome_line.replace("OUTCOME:", "").strip()
        return score, outcome
    except:
        if "10" in result: return 10, result.replace("\n", " ")
        if "2" in result: return 2, result.replace("\n", " ")
        return 5, result.replace("\n", " ")

class LLMAgent:
    def __init__(self, name: str, inherited_context: str):
        self.name = name
        self.inherited_context = inherited_context
        self.journal = []
        
    def act(self, task_desc: str) -> str:
        prompt = f"""You are {self.name}, an artificial organism trying to survive.
Here is the knowledge passed down from your ancestors:
---
{self.inherited_context if self.inherited_context else "You have no ancestral knowledge. You must figure things out yourself."}
---
Current Situation: {task_desc}
What exact action do you take? Keep it under 3 sentences."""
        return llm_generate(prompt)

    def record(self, task_desc: str, action: str, outcome: str):
        self.journal.append(f"Situation: {task_desc}\nMy Action: {action}\nOutcome: {outcome}")

    def get_full_journal(self) -> str:
        return "\n\n".join(self.journal)

    def generate_teaching_manual(self) -> str:
        prompt = f"""You are {self.name}. You are at the end of your life.
Here is your life journal of experiences:
---
{self.get_full_journal()}
---
Write a brief, synthesized survival manual for your child. Do not list your journal entries. Synthesize the underlying rules of this world (e.g., 'always do X', 'avoid Y'). Keep it under 4 sentences."""
        return llm_generate(prompt)

def run_lineage(mode: str, generations: int = 2):
    print(f"\n{'='*50}\nStarting Lineage: Mode {mode}\n{'='*50}")
    inherited_knowledge = ""
    total_scores = []
    
    for gen in range(1, generations + 1):
        print(f"\n--- Generation {gen} ---")
        agent = LLMAgent(f"Gen{gen}", inherited_knowledge)
        
        gen_score = 0
        for task in TASKS:
            action = agent.act(task['desc'])
            score, outcome = evaluate_action(task['desc'], task['evaluation_rules'], action)
            agent.record(task['desc'], action, outcome)
            
            gen_score += score
            print(f"Task: {task['desc'][:30]}... | Score: {score}")
            print(f"  Action: {action}")
            print(f"  Outcome: {outcome}")
            
        avg_score = gen_score / len(TASKS)
        total_scores.append(avg_score)
        print(f"Gen {gen} Average Score: {avg_score:.2f}/10")
        
        if gen < generations:
            if mode == "B-copy":
                inherited_knowledge = agent.inherited_context + "\n\n" + agent.get_full_journal()
                print(f"-> Passed down {len(inherited_knowledge.split())} words of raw journals.")
            elif mode == "C-teaching":
                inherited_knowledge = agent.generate_teaching_manual()
                print(f"-> Passed down manual: {inherited_knowledge}")
                
    return total_scores

if __name__ == "__main__":
    scores_b = run_lineage("B-copy", 3)
    scores_c = run_lineage("C-teaching", 3)
    
    print("\n\n=== FINAL RESULTS ===")
    print("Mode B-copy (Raw Journal Dump) Scores:")
    print([f"{s:.2f}" for s in scores_b])
    
    print("\nMode C-teaching (Synthesized Manual) Scores:")
    print([f"{s:.2f}" for s in scores_c])
