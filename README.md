# hello-llm

FDE 讲义 M0 的预习产出：第一次调用 LLM API，并读出本次调用的 token 用量。

## 用途

问模型一个问题，打印回答与 token 用量。
M3 的成本估算、M4 的 ROI 计算，都从这里的 usage 字段开始。

两条路线，任选其一：

| 脚本 | 模型来源 | 需要 Key | 费用 |
|---|---|---|---|
| `hello_local.py` | 本地 Ollama（qwen3:4b） | 不需要 | 0 |
| `hello.py` | Anthropic 官方 API | 需要 | 按量计费 |

## 如何运行（免费路线，推荐先跑通）

```bash
brew install ollama
ollama serve              # 保持这个终端开着；或直接启动 Ollama 应用
ollama pull qwen3:4b      # 约 2.5GB，只需一次

.venv/bin/python hello_local.py
```

## 如何运行（官方 API 路线）

```bash
export ANTHROPIC_API_KEY="你的 key"   # 只在当前终端有效
.venv/bin/python hello.py
```

不指定 `LLM_MODEL` 时，`hello.py` 会向服务端查询账号下最新的模型，避免模型名过期。

## 预期输出

```
正向部署工程师是……
输入 token: 18 输出 token: 46
```

## 安全约定

- `.env` 与 `.venv/` 已在 `.gitignore` 中，不会被提交。
- key 只放环境变量，永远不写进代码。
- 提交前用 `git status` 确认没有密钥文件。
- 一旦泄露：立刻在控制台吊销旧 key 再生成新的——只删 Git 历史是不够的。

## 环境说明

- 解释器：Homebrew Python 3.14.6（满足讲义「3.11 或更高」）
- 已装依赖：`anthropic 2.6.0`、`scikit-learn 1.9.1`（M3 的 RAG 基线要用）
- 重新建环境：`python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`

## 下一步

M2 会把这里的脚本演进成 `ticket-assistant` 服务模板：分层结构、FastAPI 接口、
Docker 打包、不依赖外部 API 的单元测试。
