"""M0 练习：第一次调用 LLM API。

运行：
    export ANTHROPIC_API_KEY="你的 key"
    .venv/bin/python hello.py

说明：
- key 只从环境变量读取，永远不要写进代码或提交到 Git。
- 不指定 LLM_MODEL 时，自动向服务端查询最新可用模型，避免把模型名写死。
"""

import os
import sys

import anthropic


def pick_model(client: anthropic.Anthropic) -> str:
    """取服务端最新的可用模型，避免硬编码过期模型名。"""
    models = client.models.list(limit=50).data
    if not models:
        raise RuntimeError("账号下没有可用模型，请检查账户状态")
    return max(models, key=lambda m: m.created_at).id


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            '缺少环境变量 ANTHROPIC_API_KEY。先执行：export ANTHROPIC_API_KEY="你的 key"',
            file=sys.stderr,
        )
        return 2

    client = anthropic.Anthropic()
    model = os.environ.get("LLM_MODEL") or pick_model(client)

    resp = client.messages.create(
        model=model,
        max_tokens=300,
        messages=[
            {"role": "user", "content": "用一句话解释什么是正向部署工程师。"}
        ],
    )

    print(resp.content[0].text)
    print(f"模型: {model}")
    print("输入 token:", resp.usage.input_tokens, "输出 token:", resp.usage.output_tokens)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
