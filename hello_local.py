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
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:4b")
QUESTION = "用一句话解释什么是正向部署工程师。"


def chat(prompt: str) -> dict:
    payload = {
        "model": MODEL,
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
        data = chat(QUESTION)
    except urllib.error.URLError as e:
        print(f"连不上 {HOST}：{e.reason}", file=sys.stderr)
        print("检查：1) Ollama 是否已启动（ollama serve）2) 模型是否已下载（ollama pull qwen3:4b）", file=sys.stderr)
        return 2

    print(data.get("message", {}).get("content", "").strip())
    print(f"模型: {data.get('model', MODEL)}")
    print("输入 token:", data.get("prompt_eval_count"), "输出 token:", data.get("eval_count"))
    print(f"本地推理耗时: {data.get('total_duration', 0) / 1e9:.1f} 秒（不产生费用）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
