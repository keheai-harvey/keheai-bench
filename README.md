# keheai-bench

给 **OpenAI 兼容 API 网关**测延迟和吞吐的命令行小工具。30 秒看出一家网关：首次响应多快（TTFT）、每秒出多少字（tok/s）、一次请求花多少钱。

选 API 网关最怕三件事：**慢、贵、动不动挂**。这个小工具帮你用同一段提示词、同一句话，横向比出几家网关的真实手感。

## 安装

```bash
pip install openai
```

## 用法

```bash
# 测 keheai（免费试用额度注册即发，见下）
python bench.py --base-url https://keheai.com/v1 --api-key YOUR_KEY --model deepseek-chat --rounds 3

# 对比你自己搭的本地网关
python bench.py --base-url http://localhost:8000/v1 --api-key EMPTY --model deepseek-chat
```

## 为什么写这个

很多同学想自建 OpenAI 兼容网关（Claude Code / Cursor / CherryStudio 都能直接改 base_url 接），但上游一挂就傻眼。
keheai 的做法是**双上游自动故障切换**：主上游硅基流动，备 DeepSeek 官方，一家挂了另一家顶上，调用方无感。
这个小工具就是用来验证"切换到底快不快、稳不稳"的——自己跑一下比看文档实在。

- 免费试用：注册即发约 33 万 tokens 额度 → https://keheai.com/register
- 明示上游、不用于训练、故障自动切换，适合中小团队当稳定出口

## 支持任何 OpenAI 兼容端点

不止 keheai。硅基流动、DeepSeek 官方、你自建的 New-API，把 `--base-url` 换掉就行。
欢迎提 PR 加更多模型或指标（如首字率、错误率统计）。

## License

MIT
