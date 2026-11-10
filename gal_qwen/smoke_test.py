"""Connectivity and inference smoke test."""

from gal_qwen.ollama_adapter import OllamaAdapter


def main():
    client = OllamaAdapter(model="qwen3:4b")

    print("===== OLLAMA MODEL CHECK =====")

    models = client.list_models()
    installed = {model["name"] for model in models}

    for name in sorted(installed):
        print(name)

    if client.model not in installed:
        raise SystemExit(
            f"Required model not installed: {client.model}"
        )

    print("\n===== QWEN INFERENCE TEST =====")

    prompt = (
        "Reply with exactly this text and nothing else: "
        "GAL_QWEN_OK"
    )

    response = client.generate(prompt)

    print("Model response:", repr(response))

    if response != "GAL_QWEN_OK":
        raise SystemExit("Smoke test failed: unexpected response")

    print("\nSMOKE TEST PASSED")


if __name__ == "__main__":
    main()
