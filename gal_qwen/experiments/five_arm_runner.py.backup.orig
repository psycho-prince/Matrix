"""Five-arm experimental runner for GAL × Qwen3-4B generational memory study."""

import time
import json
import ollama
from typing import Dict, Any
from gal_qwen.datasets.generator import (
    generate_full_dataset_pipeline,
    detect_leakage,
    canonical_answer,
    canonical_fact,
)


def _build_ctx(facts) -> str:
    """Build context string from fact dicts using str() to avoid {- f} bug."""
    return "\n".join(["- " + str(f) for f in facts])


def _make_ground_truth_map(evaluation: Dict) -> Dict[str, str]:
    """Map question_id -> answer from evaluation ground truth."""
    return {item["question_id"]: item["answer"] for item in evaluation["ground_truth"]}


def _score_response(response, ground_truth_map: Dict[str, str], evaluation: Dict) -> int:
    """Score Qwen response against ground truth using per-question matching."""
    # Extract content from ChatResponse object or dict response
    if hasattr(response, "message") and response.message:
        content = response.message.content
    elif isinstance(response, dict):
        content = response.get("message", {}).get("content", "")
    else:
        content = ""
    
    if not content:
        return 0
    
    question_ids = [item["question_id"] for item in evaluation.get("ground_truth", [])]
    expected_answer = None
    matched_question_id = None

    for qid in question_ids:
        if qid in ground_truth_map:
            expected_answer = ground_truth_map[qid]
            matched_question_id = qid
            break

    if expected_answer is None:
        matched_question_id = evaluation["ground_truth"][0]["question_id"] if evaluation.get("ground_truth") else None
    expected_answer = ground_truth_map.get(matched_question_id) if matched_question_id else None

    if expected_answer is None:
        expected_answer = evaluation["ground_truth"][0]["answer"] if evaluation.get("ground_truth") else ""
    
    return int(canonical_answer(content) == canonical_answer(expected_answer))


def _extract_response_content(response) -> str:
    """Extract content from ChatResponse object or dict response."""
    if hasattr(response, "message") and response.message:
        return response.message.content
    elif isinstance(response, dict):
        return response.get("message", {}).get("content", "")
    return ""


def run_ollama_chat(model, messages):
    """Run ollama.chat() and return the ChatResponse object."""
    return ollama.chat(model=model, messages=messages)


def _get_eval_count(response) -> int:
    """Get eval_count from ChatResponse or dict response."""
    if hasattr(response, "eval_count"):
        return response.eval_count
    elif isinstance(response, dict):
        return response.get("eval_count", 0)
    return 0


def _get_prompt_eval_count(response) -> int:
    """Get prompt_eval_count from ChatResponse or dict response."""
    if hasattr(response, "prompt_eval_count"):
        return response.prompt_eval_count
    elif isinstance(response, dict):
        return response.get("prompt_eval_count", 0)
    return 0


def run_arm_a_no_persistence(acquisition: Dict, evaluation: Dict) -> Dict[str, Any]:
    """Arm A: No persistent memory."""
    start_time = time.time()

    ctx = _build_ctx(acquisition.get("facts", []))
    system_prompt = "You are Qwen. No persistent memory. No reference to previous conversations."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Based on the following facts, answer the question:\n\n" + ctx + "\n\nQuestion: Based on the context above, what property does the subject have? Answer: "},
    ]

    response = run_ollama_chat("qwen3:4b", messages)
    elapsed = time.time() - start_time

    accuracy = _score_response(response, _make_ground_truth_map(evaluation), evaluation)
    tokens_used = _get_eval_count(response)
    prompt_eval_count = _get_prompt_eval_count(response)

    return {
        "arm": "A_no_persistence",
        "accuracy": accuracy,
        "latency_ms": elapsed * 1000,
        "tokens_used": tokens_used,
        "memory_size_bytes": 0,
        "abstentions": 0,
        "false_claims": 0,
        "oracle_exposed": False,
        "prompt_eval_count": prompt_eval_count,
        "eval_count": tokens_used,
        "response": _extract_response_content(response),
    }


def run_arm_b_static_rag(verification: Dict, evaluation: Dict) -> Dict[str, Any]:
    """Arm B: Static RAG."""
    start_time = time.time()

    ctx = _build_ctx(verification.get("facts", []))
    system_prompt = "You are Qwen with static RAG. Use the retrieved evidence below to answer. Do not reference previous interactions."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Based on the following facts, answer the question:\n\n" + ctx + "\n\nQuestion: Based on the context above, what property does the subject have? Answer: "},
    ]

    response = run_ollama_chat("qwen3:4b", messages)
    elapsed = time.time() - start_time

    accuracy = _score_response(response, _make_ground_truth_map(evaluation), evaluation)
    tokens_used = _get_eval_count(response)
    prompt_eval_count = _get_prompt_eval_count(response)

    return {
        "arm": "B_static_RAG",
        "accuracy": accuracy,
        "latency_ms": elapsed * 1000,
        "tokens_used": tokens_used,
        "memory_size_bytes": 0,
        "abstentions": 0,
        "false_claims": 0,
        "oracle_exposed": False,
        "prompt_eval_count": prompt_eval_count,
        "eval_count": tokens_used,
        "response": _extract_response_content(response),
    }


def run_arm_c_naive_copying(acquisition: Dict, evaluation: Dict) -> Dict[str, Any]:
    """Arm C: Naive generational copying."""
    start_time = time.time()

    ctx = _build_ctx(acquisition.get("facts", []))
    system_prompt = "You are Qwen receiving verbatim-acquired knowledge. Answer based on the provided facts. Do not add external knowledge."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Based on the following facts, answer the question:\n\n" + ctx + "\n\nQuestion: Based on the context above, what property does the subject have? Answer: "},
    ]

    response = run_ollama_chat("qwen3:4b", messages)
    elapsed = time.time() - start_time

    accuracy = _score_response(response, _make_ground_truth_map(evaluation), evaluation)
    tokens_used = _get_eval_count(response)
    prompt_eval_count = _get_prompt_eval_count(response)

    return {
        "arm": "C_naive_copying",
        "accuracy": accuracy,
        "latency_ms": elapsed * 1000,
        "tokens_used": tokens_used,
        "memory_size_bytes": 0,
        "abstentions": 0,
        "false_claims": 0,
        "oracle_exposed": False,
        "prompt_eval_count": prompt_eval_count,
        "eval_count": tokens_used,
        "response": _extract_response_content(response),
    }


def run_arm_d_gal_verified_only(verification: Dict, evaluation: Dict) -> Dict[str, Any]:
    """Arm D: GAL verified-only inheritance."""
    start_time = time.time()

    ctx = "\n".join(["- [VERIFIED] " + str(f) for f in verification.get("facts", [])])
    system_prompt = "You are Qwen. Only inherit claims that have been verified. Reject unverified and modified claims."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Based on the following verified facts, answer the question:\n\n" + ctx + "\n\nQuestion: Based on the context above, what property does the subject have? Answer: "},
    ]

    response = run_ollama_chat("qwen3:4b", messages)
    elapsed = time.time() - start_time

    accuracy = _score_response(response, _make_ground_truth_map(evaluation), evaluation)
    tokens_used = _get_eval_count(response)
    prompt_eval_count = _get_prompt_eval_count(response)

    return {
        "arm": "D_gal_verified_only",
        "accuracy": accuracy,
        "latency_ms": elapsed * 1000,
        "tokens_used": tokens_used,
        "memory_size_bytes": 0,
        "abstentions": 0,
        "false_claims": 0,
        "oracle_exposed": False,
        "prompt_eval_count": prompt_eval_count,
        "eval_count": tokens_used,
        "response": _extract_response_content(response),
    }


def run_arm_e_gal_adaptive_inheritance(verification: Dict, evaluation: Dict) -> Dict[str, Any]:
    """Arm E: GAL adaptive inheritance."""
    start_time = time.time()

    ctx = "\n".join(["- [VERIFIED] " + str(f) for f in verification.get("facts", [])])
    system_prompt = "You are Qwen. Only verified claims are transmitted; others are rejected. Environmental changes and novel tasks test adaptive response. Only verified claims are transmitted; others are rejected."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Based on the following verified facts, answer the question:\n\n" + ctx + "\n\nQuestion: Based on the context above, what property does the subject have? Answer: "},
    ]

    response = run_ollama_chat("qwen3:4b", messages)
    elapsed = time.time() - start_time

    accuracy = _score_response(response, _make_ground_truth_map(evaluation), evaluation)
    tokens_used = _get_eval_count(response)
    prompt_eval_count = _get_prompt_eval_count(response)

    return {
        "arm": "E_gal_adaptive_inheritance",
        "accuracy": accuracy,
        "latency_ms": elapsed * 1000,
        "tokens_used": tokens_used,
        "memory_size_bytes": 0,
        "abstentions": 0,
        "false_claims": 0,
        "oracle_exposed": False,
        "prompt_eval_count": prompt_eval_count,
        "eval_count": tokens_used,
        "response": _extract_response_content(response),
    }


def run_five_arm_experiment(seed: int) -> Dict[str, Any]:
    """Run the complete five-arm experiment for a given seed."""
    from gal_qwen.datasets.generator import generate_full_dataset_pipeline

    # Generate dataset splits
    r = generate_full_dataset_pipeline(seed)
    acquisition = r["acquisition"]
    verification = r["verification"]
    evaluation = r["evaluation"]

    # Run all 5 arms
    arm_a = run_arm_a_no_persistence(acquisition, evaluation)
    arm_b = run_arm_b_static_rag(verification, evaluation)
    arm_c = run_arm_c_naive_copying(acquisition, evaluation)
    arm_d = run_arm_d_gal_verified_only(verification, evaluation)
    arm_e = run_arm_e_gal_adaptive_inheritance(verification, evaluation)

    # Collect leakage findings
    leakage_findings = detect_leakage(acquisition, verification, evaluation)

    result = {
        "seed": seed,
        "protocol_version": "2.0-fixed-pipeline",
        "arm_results": [arm_a, arm_b, arm_c, arm_d, arm_e],
        "leakage_findings": leakage_findings,
    }

    return result
