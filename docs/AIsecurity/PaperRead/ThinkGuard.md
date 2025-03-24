---
url: http://arxiv.org/abs/2502.13458
tags:
  - guardrail
  - LRM
---

# ThinkGuard

> [!abstract]- [ThinkGuard: Deliberative Slow Thinking Leads to Cautious Guardrails](http://arxiv.org/abs/2502.13458)
>
> Ensuring the safety of large language models (LLMs) is critical as they are deployed in real-world applications. Existing guardrails rely on rule-based filtering or single-pass classification, limiting their ability to handle nuanced safety violations. To address this, we propose ThinkGuard, a critique-augmented guardrail model that distills knowledge from high-capacity LLMs by generating structured critiques alongside safety labels. Fine-tuned on critique-augmented data, the captured deliberative thinking ability drastically enhances the guardrail's cautiousness and interpretability. Evaluated on multiple safety benchmarks, ThinkGuard achieves the highest average F1 and AUPRC, outperforming all baselines. Compared to LLaMA Guard 3, ThinkGuard improves accuracy by 16.1% and macro F1 by 27.0%. Moreover, it surpasses label-only fine-tuned models, confirming that structured critiques enhance both classification precision and nuanced safety reasoning while maintaining computational efficiency.

## 概述 (Content)

现有的防护栏主要依赖基于规则的过滤或单次分类，难以处理复杂的、细微的安全性违规问题。ThinkGuard 通过引入批判性增强的防护栏模型，从高容量 LLMs（更强大的模型）中提取知识，生成结构化的批评和安全性标签，从而显著提高了防护栏的谨慎性和可解释性。

## 方法 (How)

ThinkGuard 的核心方法是将“慢思考”引入 LLMs 的安全性评估中，通过多步骤的评估过程，使模型能够进行更深入、更谨慎的决策。具体而言，该方法包括以下几个关键步骤：

- **数据构建**：使用结构化的提示格式，从高容量的LLMs（如GPT-4o, DPSK-LLaMA-70B）中生成 <u>详细的批评</u> 和安全性分类，构建包含标签和批评的训练数据集。
- **模型训练**：使用 LLaMA Guard 3-8B 作为基础模型；采用标签增强的监督微调策略，将分类损失和批评生成损失相结合，训练一个较小的防护栏模型，使其能够同时进行分类和生成解释。
	- $L = L_{cls}+L_{critique} = - \sum_{i}y_{i}\log P(y_{i}|x_{i}, r_{i}) - \sum_{t}\log P(c_{t}|c_{<t}, x_{i}, r_{i}, y_{i})$

- **推理与决策**：在推理阶段，模型首先预测安全性标签，然后识别违反的安全性类别，并生成批评以解释其决策。

## 贡献 (Contribution)

ThinkGuard在多个安全性基准测试中取得了最高的平均F1分数和AUPRC，显著优于所有基线模型。与LLaMA Guard 3相比，ThinkGuard在准确性上提高了16.1%，在宏F1上提高了27.0%。此外，它还超越了仅使用标签进行微调的模型，证明了 <u>结构化批评能够增强分类精度和细微的安全性推理能力</u> 。

- 提出了一种新的防护栏模型架构，能够通过批判性思维提高安全性评估的准确性。
- 通过结构化批评 <u>增强了模型的可解释性</u> ，使人类更容易理解和信任模型的决策。
- 在 <u>保持计算效率</u> 的同时，实现了与标准链式思考微调相当的性能。

## 总结 (Summary)

该论文生成数据集、训练模型的推理分析能力值得参考；仍存在一些不足：

- 该模型的性能高度依赖于训练数据的质量，如果批评内容不完整或与安全性指南不一致，模型可能会继承偏见和不一致性
- 生成结构化批评会引入 <u>额外的计算开销</u> ，需要在推理深度和效率之间进行进一步优化
