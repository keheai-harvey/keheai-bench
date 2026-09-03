# keheai-bench

给 **OpenAI 兼容 API 网关**测延迟和吞吐的命令行小工具。30 秒测出两项真实指标：首次响应多快（TTFT）、每秒出多少字（tok/s）。

选 API 网关最怕两件事：**慢、动不动挂**。这个小工具用同一段提示词，横向比出几家网关的真实手感。

## 安装

```bash
pip install openai
```

## 用法

```bash
# 测任意 OpenAI 兼容端点（硅基流动、DeepSeek 官方、你自建的 New-API 都能测）
python bench.py --base-url https://你的网关/v1 --api-key YOUR_KEY --model deepseek-chat --rounds 3

# 对比本地自建网关
python bench.py --base-url http://localhost:8000/v1 --api-key EMPTY --model deepseek-chat
```

## 支持任何 OpenAI 兼容端点

不止某一家。硅基流动、DeepSeek 官方、你自建的 New-API、keheai.com，把 `--base-url` 换掉就行。

## 为什么写这个

很多同学想自建 OpenAI 兼容网关（Claude Code / Cursor / CherryStudio 都能直接改 base_url 接），但上游一挂就傻眼。这个小工具用来验证"切换到底快不快、稳不稳"——自己跑一下比看文档实在。

> 说明：本工具只测延迟和吞吐，**不估算成本**（各网关定价不同，硬估只会误导）。

## 欢迎贡献

欢迎提 PR 加更多指标（如首字率、错误率统计）或更多模型。

## License

MIT
