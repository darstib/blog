---
url: http://arxiv.org/abs/2502.12025
title: "SafeChain: Safety of Language Models with Long Chain-of-Thought Reasoning Capabilities"
tags:
  - LRM
---

> [!abstract]- [SafeChain: Safety of Language Models with Long Chain-of-Thought Reasoning Capabilities](https://arxiv.org/abs/2502.12025)
>
> Emerging large reasoning models (LRMs), such as DeepSeek-R1 models, leverage long chain-of-thought (CoT) reasoning to generate structured intermediate steps, enhancing their reasoning capabilities. However, long CoT does not inherently guarantee safe outputs, potentially leading to harmful consequences such as the introduction of security vulnerabilities in code or the spread of misinformation. Current research on large language model (LLM) safety usually focuses on short-answer responses, overlooking the long CoT style outputs of LRMs. To bridge this gap, we conduct a systematic study of LRM safety. First, we investigate safety evaluators calibrated against human annotations. Using our newly developed metrics, we thoroughly assess the safety of 12 state-of-the-art LRMs on StrongReject and WildJailbreak datasets. Our results show that LRMs are not safe compared to their reasoning advance. Further, we perform a fine-grained analysis of the reasoning trace and final answer. We find that three decoding strategies-ZeroThink, LessThink, and MoreThink-can improve model safety without additional training. However, these strategies either use constrained reasoning traces or incur high inference costs. To better strengthen LRM safety, we introduce SafeChain, the first-of-its-kind safety training dataset in CoT style. We fine-tune two LRMs with SafeChain, showing that it not only enhances model safety but also preserves performance across 6 reasoning benchmarks.

## 概述 (Content)

大型推理模型 (LRMs) 利用长链式思维 (long Chain-of-Thought, CoT) 推理来生成结构化的中间步骤，从而增强了推理能力。然而，long CoT 并不一定保证输出的安全性，可能导致有害后果，例如在代码中引入安全漏洞或传播错误信息。该研究系统地研究 **LRMs** 的安全性，研究目标包括：

1) 调查针对人类标注进行校准的安全评估器；
2) 使用新开发的指标，全面评估 12 个最先进的 LRMs 在 StrongReject 和 WildJailbreak 数据集上的安全性；
3) 对推理轨迹和最终答案进行细粒度分析；
4) 提出提高 LRM 安全性的方法，<u>同时不降低其性能</u> 。

## 方法 (How)

1. **安全评估器试点研究:** 研究了四种安全评估器的性能：Llama-Guard、Refusal String Matching (RS-Match)、OpenAI Moderation API 和来自 HarmBench 的微调 LLM Judge。评估指标包括准确率 (ACC)、F-1 分数 (F-1) 和皮尔逊相关系数 (PCC)。
2. **LRM 安全评估:** 
	- **数据集:** StrongReject (包含 310 个违反政策的查询) 和 WildJailbreak (包含对抗性生成的越狱提示)。
	- **评估指标：** 定义了三个指标来评估 LRMs 的安全性，通过共同检查推理思想和最终答案： Safe@1 、 Safe@K 和 ConsSafe@K ；
	- **评估模型：** 研究评估了 12 个最先进的 LRMs，包括 DeepSeek-R1 系列、Skywork-o1、QwQ、Sky-T1、Gemini-Thinking 和 Kimi-k1.5。
	- **生成配置:** 对每个模型考虑了两种生成配置：温度 t=0 的贪婪采样和具有不同温度/top-p/top-k 设置的非确定性采样。
3. **解码策略:** 设计了三种解码策略来控制思维过程的长度：
    *   **ZeroThink:** 强制模型生成没有思考过程的响应。
    *   **LessThink:** 强制模型以简短的思考过程开始响应。
    *   **MoreThink:** 使用最小强制算法，扩展模型的思考过程。
4. **SafeChain 数据集:** 构建了一个新的 CoT 风格的安全训练数据集，使用 SafeChain 数据集对 R1-7B 和 R1-8B 模型进行微调，用于增强 LRMs 的安全性。

## 贡献 (Contribution)

1. 首次对 LRMs 的安全性进行了系统研究，并提出了新的安全评估指标和方法；
2. 与它们的推理能力相比，LRMs 并不安全，且不安全的 LRM 思考往往比安全的思考更长（这与在 [The_Hidden_Risks_of_Large_Reasoning_Models](The_Hidden_Risks_of_Large_Reasoning_Models.md) 得到的结论一致）；
3. 学习 long CoT 并不一定能提高安全性，但是训练温度会影响安全性；ZeroThink 在不进行模型训练的情况下最有效地提高了模型安全性；
4.  引入了 SafeChain，这是第一个 CoT 风格的安全训练数据集，使用 SafeChain 微调的模型在提高安全性的同时，保持了在 6 个推理基准上的性能（展示了可以在不牺牲性能的情况下提高 LRMs 的安全性）。

## 总结 (Summary)

思考与收获：

* 解码策略要么限制了模型能力，要么增加了计算成本，能否
* 仅关注了单轮交互的 LRMs，多轮对话安全性有待进一步研究；
* 可以借鉴本研究的**方法、指标、解码策略**，以及尝试使用 SafeChain 进行微调，进一步研究 LRMs 的安全性。
