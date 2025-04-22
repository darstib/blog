---
url: http://arxiv.org/abs/2502.12970
tags:
- LRM
comments: true
---

> [!abstract]- [Reasoning-to-Defend: Safety-Aware Reasoning Can Defend Large Language Models from Jailbreaking](http://arxiv.org/abs/2502.12970)
>
> The reasoning abilities of Large Language Models (LLMs) have demonstrated remarkable advancement and exceptional performance across diverse domains. However, leveraging these reasoning capabilities to enhance LLM safety against adversarial attacks and jailbreak queries remains largely unexplored. To bridge this gap, we propose Reasoning-to-Defend (R2D), a novel training paradigm that integrates safety reflections of queries and responses into LLMs' generation process, unlocking a safety-aware reasoning mechanism. This approach enables self-evaluation at each reasoning step to create safety pivot tokens as indicators of the response's safety status. Furthermore, in order to improve the learning efficiency of pivot token prediction, we propose Contrastive Pivot Optimization(CPO), which enhances the model's ability to perceive the safety status of dialogues. Through this mechanism, LLMs dynamically adjust their response strategies during reasoning, significantly enhancing their defense capabilities against jailbreak attacks. Extensive experimental results demonstrate that R2D effectively mitigates various attacks and improves overall safety, highlighting the substantial potential of safety-aware reasoning in strengthening LLMs' robustness against jailbreaks.

## 概述 (Content)

现有的防御方法主要依赖于外部检测或监督微调信号，忽略了LLM本身在生成过程中的推理能力对安全性的作用。该论文提出了一种新的训练范式 Reasoning-to-Defend (R2D)，将 <u>查询和响应的安全反思整合到 LLM 的生成过程中</u> ，从而解锁安全感知的推理机制，提升 LLM 对越狱攻击的防御能力。

## 方法 (How)

- **安全感知推理蒸馏（SwaRD）：** 首先，通过 SwaRD 训练 LLM，使其具备分阶段思考的能力。这种分阶段的推理过程由 LLM 自身逐步评估，形成关于每个步骤是安全、不安全还是需要进一步改进的“pivot tokens”；
- **对比枢轴优化（CPO）：** 在推理过程中，LLMs 逐步预测安全状态标记（pivot tokens），通过对比学习优化模型对这些标记的感知能力，从而提高模型对对话安全状态的感知能力。

$$
L_{\mathrm{CPO}}=-\mathbb{E}_{X,Y\sim D_R}\left[\log\sigma\left(\log P_M(t_+|Y,X)-\log P_M(t_-|Y,X)\right)\right]
$$

> [!question]+
>
> 奇怪的是对比学习一般用于二分类，论文中对于如何得到 `[Safe] [UnSafe] [Rethink]` 三种标签没有详细说明，感觉欠考虑……


使用 $DeepSeek-R1_{70B}$ 和 $QwQ_{p-32B}$ 作为推理模型（M_R），并从 Alpaca 和 AdvBench 中收集推理轨迹数据，对非推理模型（如 Llama v3-8B、Qwen v2.5-14B 等）进行训练。

## 贡献 (Contribution)

- R2D 显著降低了多种越狱攻击的成功率，相比非防御 LLMs，R2D 平均降低了 56%的攻击成功率；
- 与现有的防御基线相比，R2D 至少降低了 10%的攻击成功率；
- R2D 在保持模型有用性的同时，有效避免了过度拒绝现象。

## 总结 (Summary)

1. 论文提出的 R2D 训练范式为增强 LLMs 的安全性提供了一种新的思路。通过引入**安全意识推理机制**，模型在推理过程中能够动态调整回答策略，从而更有效地抵御越狱攻击。同时，CPO 方法也为优化模型对安全状态的感知能力提供了有效手段，有助于提升模型的鲁棒性。
2. 论文中主要关注的是通过从推理模型中蒸馏推理能力来提高安全性，而不是采用强化学习和测试时扩展等方法，未来可以研究如何将安全感知推理整合到 ReFT 类型的方法中。
