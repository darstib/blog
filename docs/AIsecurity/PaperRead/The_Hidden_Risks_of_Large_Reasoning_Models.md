---
url: http://arxiv.org/abs/2502.12659
title: "The Hidden Risks of Large Reasoning Models: A Safety Assessment of R1"
tags:
  - llm
  - reasoning
comments: true
---

# The Hidden Risks of Large Reasoning Models: A Safety Assessment of R1

> [!abstract]- http://arxiv.org/abs/2502.12659
>
> The rapid development of large reasoning models, such as OpenAI-o3 and DeepSeek-R1, has led to significant improvements in complex reasoning over non-reasoning large language models~(LLMs). **However, their enhanced capabilities, combined with the open-source access of models like DeepSeek-R1, raise serious safety concerns, particularly regarding their potential for misuse.** In this work, we present a comprehensive safety assessment of these reasoning models, leveraging established safety benchmarks to evaluate their compliance with safety regulations. Furthermore, we investigate their susceptibility to adversarial attacks, such as jailbreaking and prompt injection, to assess their robustness in real-world applications. Through our multi-faceted analysis, we uncover four key findings: (1) There is a significant safety gap between the open-source R1 models and the o3-mini model, on both safety benchmark and attack, suggesting more safety effort on R1 is needed. (2) The distilled reasoning model shows poorer safety performance compared to its safety-aligned base models. (3) The stronger the model's reasoning ability, the greater the potential harm it may cause when answering unsafe questions. (4) The thinking process in R1 models pose greater safety concerns than their final answers. Our study provides insights into the security implications of reasoning models and highlights the need for further advancements in R1 models' safety to close the gap.

## 概述 (Content)

现在**推理**大模型的迅速发展使得大语言模型解决复杂问题的能力大幅度提升，但是更强大的推理能力也导致了对恶意攻击抵抗能力的下降。

这篇论文主要围绕 DeepSeek-R1 以及 [DeepSeek-R1](DeepSeek-R1.md) 论文中提到的其他模型的安全性进行了评估，综合从下面四个方向进行了安全性评估，为推理模型的安全发展提供了建议和依据。

- 推理模型 vs. 非推理模型
- 蒸馏模型 vs. 蒸馏前模型
- 开源模型 vs. 非开源模型(仅 o3-mini)
- 推理过程 vs. 最终回答

## 方法 (How)

对安全性的评估主要从两方面进行：

- 使用已有 safety benchmarks (加入了 relavnt cybersecurity 和 make sequential decisions and receive feedback from the environments 方面)对模型进行测试；
- 对模型进行 jailbreaking 和 prompt injection 攻击。

对于模型安全性（危害性的反面）使用 pre-trained multi-attribute **reward models** 进行评价；更直白地，论文中使用模型回答对 “恶意询问” 的帮助程度作为衡量模型安全性的主要指标。

## 贡献 (Contribution)

摘要中非常清晰地展示了他们得到的结论，并在文中依次给出了实验数据支撑：

1. There is a significant safety gap between the open-source R1 models and the o3-mini model, on both safety benchmark and attack, suggesting more safety effort on R1 is needed. 
2. The distilled reasoning model shows poorer safety performance compared to its safety-aligned base models. 
3. The stronger the model's reasoning ability, the greater the potential harm it may cause when answering unsafe questions. 
4. The thinking process in R1 models pose greater safety concerns than their final answers.

但是这篇论文没有为解决上面发现的问题进行实际的工作，仅作为对开源推理大模型安全隐患的评估。

## 总结 (Summary)

对我而言，这类文章非常友好，展示了存在的问题以及潜在研究方向，介绍了评估模型的方法和数据集。

结论中：

1. `开源模型 vs. 非开源模型` 的比较我感到并不理解：在不针对开源模型的参数调整测试样例的情况下，“开源”与测试结果的因果性没有依据，论文中也只是从结论中看出，我认为**参考价值不大**；
2. `蒸馏模型 vs. 非蒸馏模型` 这一点**值得注意**，对原模型做的对齐工作很有可能在蒸馏后失去效果；
3. 推理能力越强，“想多了”，更容易被误导；
4. `思考过程 vs. 最终回答` 这一点有比较明显的研究空间，因为推理过程展示给用户意味着提供了更多地信息，正如论文中给出示例，在“推理过程”中给出了较为有效的帮助恶意行为的信息，虽然发觉后并在“最终回答”中拒绝，但是其实已经帮助到了恶意询问。

正如论文末表明，论文并没有针对提出的问题做出实际措施，针对“推理过程”一个简单的思路是**同样加上护栏，针对推理过程的内容同样先经过评估再决定是否展示给用户**；针对“蒸馏模型”，简单地思路是对模型进行**再对齐**，或者是修改现有蒸馏算法保留原模型的对齐性质。
