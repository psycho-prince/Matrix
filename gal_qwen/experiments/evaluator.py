"""Structured pilot evaluator for GAL × Qwen experiments."""

import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from gal_qwen.ollama_adapter import OllamaAdapter

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "datasets" / "world_v1.json"
RESULTS = ROOT / "results"

ANSWER_SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "string"}},
    "required": ["answer"],
    "additionalProperties": False,
}


def canonical_answer(value):
    return " ".join(str(value).strip().lower().split()).rstrip(".!?")


def build_prompt(question, facts, rules, condition):
    instructions = (
        "Answer questions about this fictional experimental world. "
        "Use only supplied information. Do not guess. "
        "If information is insufficient, answer UNKNOWN."
    )

    if condition == "no_memory":
        context = "No world facts or rules have been supplied."
    else:
        fact_text = "\n".join(
            f"{f['subject']} | {f['relation']} | {f['object']}"
            for f in facts
        )
        rule_text = "\n".join(
            f"{r['id']}: {r['description']}"
            for r in rules
        )
        context = (
            "WORLD FACTS:\n" + fact_text
            + "\n\nWORLD RULES:\n" + rule_text
        )

    return f"{instructions}\n\n{context}\n\nQUESTION: {question}"


def classify_result(result, expected):
    if result.get("done_reason") == "length":
        return "truncated", False, None

    if result.get("done") is not True:
        return "inference_error", False, None

    if result.get("parse_error") is not None:
        return "invalid_json", False, None

    response = result.get("response")

    if not isinstance(response, dict):
        return "invalid_json", False, None

    answer = response.get("answer")

    if not isinstance(answer, str) or not answer.strip():
        return "invalid_json", False, None

    predicted = canonical_answer(answer)
    correct = predicted == canonical_answer(expected)

    return "correct" if correct else "incorrect", correct, predicted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--condition",
        choices=["no_memory", "context_baseline"],
        required=True,
    )
    parser.add_argument("--model", default="qwen3:4b")
    parser.add_argument("--num-predict", type=int, default=128)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.num_predict < 1:
        raise SystemExit("--num-predict must be positive")

    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    client = OllamaAdapter(model=args.model)

    models = client.list_models()
    model_info = next(
        (m for m in models if m["name"] == args.model),
        None,
    )
    if model_info is None:
        raise SystemExit(f"Model not installed: {args.model}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    run_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    output_file = RESULTS / f"pilot_{args.condition}_{run_id}.jsonl"

    counts = {
        "correct": 0,
        "incorrect": 0,
        "truncated": 0,
        "invalid_json": 0,
        "inference_error": 0,
    }

    print(f"Run ID: {run_id}")
    print(f"Condition: {args.condition}")
    print(f"Model: {args.model}")
    print(f"Model digest: {model_info.get('digest')}")
    print(f"Dataset: {dataset['world_id']}")
    print(f"Output: {output_file}\n")

    with output_file.open("x", encoding="utf-8") as output:
        for item in dataset["ground_truth"]:
            prompt = build_prompt(
                item["question"],
                dataset["facts"],
                dataset["rules"],
                args.condition,
            )
            prompt_hash = hashlib.sha256(
                prompt.encode("utf-8")
            ).hexdigest()

            try:
                result = client.generate_structured_with_metadata(
                    prompt=prompt,
                    schema=ANSWER_SCHEMA,
                    temperature=0.0,
                    num_predict=args.num_predict,
                    seed=args.seed,
                )
                status, is_correct, predicted = classify_result(
                    result, item["answer"]
                )
            except Exception as exc:
                result = {"inference_exception": repr(exc)}
                status = "inference_error"
                is_correct = False
                predicted = None

            counts[status] += 1

            record = {
                "run_id": run_id,
                "timestamp_utc": timestamp,
                "condition": args.condition,
                "dataset_id": dataset["world_id"],
                "question_id": item["question_id"],
                "question": item["question"],
                "expected_answer": item["answer"],
                "predicted_answer": predicted,
                "status": status,
                "correct": is_correct,
                "prompt_sha256": prompt_hash,
                "model_requested": args.model,
                "model_returned": result.get("model"),
                "model_digest": model_info.get("digest"),
                "temperature": 0.0,
                "seed": args.seed,
                "num_predict": args.num_predict,
                "inference": result,
            }

            output.write(json.dumps(record, ensure_ascii=False) + "\n")
            output.flush()

            print(
                f"{item['question_id']} | "
                f"Expected: {item['answer']} | "
                f"Got: {predicted} | Status: {status}"
            )

    valid = counts["correct"] + counts["incorrect"]

    print("\n===== PILOT SUMMARY =====")
    for status, count in counts.items():
        print(f"{status}: {count}")

    print(f"Total questions: {len(dataset['ground_truth'])}")
    print(f"Valid completed answers: {valid}")

    if valid:
        print(f"Accuracy among valid answers: {counts['correct'] / valid:.3f}")
    else:
        print("Accuracy: unavailable")

    print(f"Raw results: {output_file}")
    print("Engineering pilot only; not a statistical conclusion.")


if __name__ == "__main__":
    main()
