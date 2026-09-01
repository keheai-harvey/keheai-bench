#!/usr/bin/env python3
"""
keheai-bench — 给 OpenAI 兼容 API 网关测延迟和吞吐的命令行小工具。

为什么写它：选 API 网关最怕两件事——慢、贵、还动不动挂。
这个小工具 30 秒帮你测出：首次响应延迟（TTFT）、每秒能出多少字（tok/s）、
一次请求花多少钱。支持任意 OpenAI 兼容端点，包括 keheai.com。

用法：
    pip install openai
    python bench.py --base-url https://keheai.com/v1 --api-key YOUR_KEY --model deepseek-chat
    # 对比两家：
    python bench.py --base-url https://keheai.com/v1 --api-key KEY --model deepseek-chat --rounds 3
"""
import argparse
import sys
import time

try:
    from openai import OpenAI
except ImportError:
    sys.exit("先装依赖：pip install openai")


def bench(base_url: str, api_key: str, model: str, prompt: str, rounds: int = 1):
    client = OpenAI(base_url=base_url, api_key=api_key)
    print(f"\n=== {base_url}  model={model}  rounds={rounds} ===")
    ttfts, tpss, costs = [], [], []
    for i in range(rounds):
        t0 = time.time()
        first = True
        text = ""
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                max_tokens=200,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    if first:
                        ttft = time.time() - t0
                        first = False
                    text += delta
            elapsed = time.time() - t0
        except Exception as e:
            print(f"  round {i+1}: 调用失败 -> {e}")
            continue
        n_tokens = max(len(text) // 2, 1)  # 粗略：1 token≈2 字符（中文更密）
        tps = n_tokens / elapsed
        cost = (n_tokens / 1_000_000) * 0.001  # 占位单价，真实价格看网关文档
        ttfts.append(ttft)
        tpss.append(tps)
        costs.append(cost)
        print(f"  round {i+1}: TTFT={ttft:.2f}s  ~{tps:.0f} tok/s  约 {len(text)} 字  ~${cost:.5f}")
    if ttfts:
        print(f"  均值: TTFT={sum(ttfts)/len(ttfts):.2f}s  tok/s={sum(tpss)/len(tpss):.0f}  "
              f"~${sum(costs)/len(costs):.5f}/次")


def main():
    ap = argparse.ArgumentParser(description="OpenAI 兼容网关延迟/吞吐小测")
    ap.add_argument("--base-url", required=True, help="网关 /v1 地址，如 https://keheai.com/v1")
    ap.add_argument("--api-key", required=True, help="你的 API key")
    ap.add_argument("--model", default="deepseek-chat", help="模型名")
    ap.add_argument("--prompt", default="用一句话解释什么是 API 网关。", help="测试提示词")
    ap.add_argument("--rounds", type=int, default=1, help="重复次数取均值")
    args = ap.parse_args()
    bench(args.base_url, args.api_key, args.model, args.prompt, args.rounds)


if __name__ == "__main__":
    main()
