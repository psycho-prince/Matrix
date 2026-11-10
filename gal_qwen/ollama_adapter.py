"""Ollama adapter with structured inference and reproducibility metadata."""

import json
import urllib.request
import urllib.error


class OllamaAdapter:
    def __init__(
        self,
        model="qwen3:4b",
        base_url="http://127.0.0.1:11434",
        timeout=120,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({})
        )

    def _request(self, endpoint, payload=None):
        url = f"{self.base_url}{endpoint}"

        if payload is None:
            request = urllib.request.Request(url)
        else:
            request = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"Ollama HTTP {exc.code}: {detail}"
            ) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Cannot connect to Ollama: {exc}"
            ) from exc

    def list_models(self):
        return self._request("/api/tags").get("models", [])

    def generate_structured_with_metadata(
        self,
        prompt,
        schema,
        temperature=0.0,
        num_predict=128,
        seed=42,
    ):
        result = self._request(
            "/api/chat",
            {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Answer the question using the available "
                            "information. Return only the requested "
                            "structured output."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                "format": schema,
                "stream": False,
                "think": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": num_predict,
                    "seed": seed,
                },
            },
        )

        message = result.get("message", {})
        raw_content = message.get("content", "")

        parsed = None
        parse_error = None

        try:
            parsed = json.loads(raw_content)
        except (json.JSONDecodeError, TypeError) as exc:
            parse_error = str(exc)

        return {
            "response": parsed,
            "raw_response": raw_content,
            "thinking": message.get("thinking"),
            "model": result.get("model"),
            "created_at": result.get("created_at"),
            "done": result.get("done"),
            "done_reason": result.get("done_reason"),
            "total_duration_ns": result.get("total_duration"),
            "load_duration_ns": result.get("load_duration"),
            "prompt_eval_count": result.get("prompt_eval_count"),
            "prompt_eval_duration_ns": result.get(
                "prompt_eval_duration"
            ),
            "eval_count": result.get("eval_count"),
            "eval_duration_ns": result.get("eval_duration"),
            "parse_error": parse_error,
        }

    def generate_with_metadata(self, prompt, temperature=0.0):
        result = self._request(
            "/api/generate",
            {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": 128,
                    "seed": 42,
                },
            },
        )

        return {
            "response": result.get("response", "").strip(),
            "model": result.get("model"),
            "created_at": result.get("created_at"),
            "total_duration_ns": result.get("total_duration"),
            "load_duration_ns": result.get("load_duration"),
            "prompt_eval_count": result.get("prompt_eval_count"),
            "prompt_eval_duration_ns": result.get(
                "prompt_eval_duration"
            ),
            "eval_count": result.get("eval_count"),
            "eval_duration_ns": result.get("eval_duration"),
            "done": result.get("done"),
            "done_reason": result.get("done_reason"),
        }

    def generate(self, prompt, temperature=0.0):
        return self.generate_with_metadata(prompt, temperature)["response"]
