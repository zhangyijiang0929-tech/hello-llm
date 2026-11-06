"""M0 练习（免费路线）：调用本地 Ollama 的 HTTP 接口，零成本跑通第一次 LLM 调用。

为什么能这么写：Ollama 的 /api/chat 就是一个普通 HTTP POST 接口。
这正是讲义 0.4 「HTTP 与 REST」的内容——你在用 urllib 手写一个 POST 请求，
和 curl 做的事完全一样，只是换成了 Python。

准备：
    brew install ollama
    ollama serve            # 或直接打开 Ollama 应用
    ollama pull qwen3:4b    # 约 2.5GB；机器内存小可换 qwen3:1.7b

运行：
    .venv/bin/python hello_local.py

成功后会打印回答，以及本次调用的 token 用量（Ollama 返回 prompt_eval_count / eval_count）。
这两个数字就是讲义里 cost = token × 单价 的那个 token。
"""

import json
import os
import sys
import urllib.error
import urllib.request

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:1.5b")
QUESTION = "用一句话解释什么是正向部署工程师。"


def available_models() -> list[str]:
    """列出本机已下载的模型，用于在默认模型缺失时自动降级。"""
    with urllib.request.urlopen(f"{HOST}/api/tags", timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return [m["name"] for m in data.get("models", [])]


def pick_model() -> str:
    """优先用 OLLAMA_MODEL；没设置或未下载时，退回本机已有的第一个模型。"""
    models = available_models()
    if MODEL in models:
        return MODEL
    if models:
        print(f"提示：本机没有 {MODEL}，改用已下载的 {models[0]}（想用别的：export OLLAMA_MODEL=模型名）", file=sys.stderr)
        return models[0]
    raise RuntimeError("本机还没有下载任何模型，先执行：ollama pull qwen2.5:1.5b")


def chat(prompt: str, model: str) -> dict:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    req = urllib.request.Request(
        f"{HOST}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    try:
        model = pick_model()
        data = chat(QUESTION, model)
    except urllib.error.URLError as e:
        print(f"连不上 {HOST}：{e.reason}", file=sys.stderr)
        print("检查：1) Ollama 是否已启动（ollama serve）2) 模型是否已下载（ollama pull qwen2.5:1.5b）", file=sys.stderr)
        return 2
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2

    print(data.get("message", {}).get("content", "").strip())
    print(f"模型: {data.get('model', model)}")
    print("输入 token:", data.get("prompt_eval_count"), "输出 token:", data.get("eval_count"))
    print(f"本地推理耗时: {data.get('total_duration', 0) / 1e9:.1f} 秒（不产生费用）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
