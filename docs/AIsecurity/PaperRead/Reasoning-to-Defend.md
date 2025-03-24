---
url: http://arxiv.org/abs/2502.12970
tags:
- LRM
---

> [!abstract]- [Reasoning-to-Defend: Safety-Aware Reasoning Can Defend Large Language Models from Jailbreaking](http://arxiv.org/abs/2502.12970)
>
> The reasoning abilities of Large Language Models (LLMs) have demonstrated remarkable advancement and exceptional performance across diverse domains. However, leveraging these reasoning capabilities to enhance LLM safety against adversarial attacks and jailbreak queries remains largely unexplored. To bridge this gap, we propose Reasoning-to-Defend (R2D), a novel training paradigm that integrates safety reflections of queries and responses into LLMs' generation process, unlocking a safety-aware reasoning mechanism. This approach enables self-evaluation at each reasoning step to create safety pivot tokens as indicators of the response's safety status. Furthermore, in order to improve the learning efficiency of pivot token prediction, we propose Contrastive Pivot Optimization(CPO), which enhances the model's ability to perceive the safety status of dialogues. Through this mechanism, LLMs dynamically adjust their response strategies during reasoning, significantly enhancing their defense capabilities against jailbreak attacks. Extensive experimental results demonstrate that R2D effectively mitigates various attacks and improves overall safety, highlighting the substantial potential of safety-aware reasoning in strengthening LLMs' robustness against jailbreaks.

## 概述 (Content)

现有的防御方法主要依赖于外部检测或监督微调信号，忽略了LLM本身在生成过程中的推理能力对安全性的作用。该论文提出了一种新的训练范式 Reasoning-to-Defend (R2D)，将 <u>查询和响应的安全反思整合到 LLM 的生成过程中</u> ，从而解锁安全感知的推理机制，提升 LLM 对越狱攻击的防御能力。

> [!todo]-
>
> - [x] 背景
> - [x] 目的

## 方法 (How)

- **安全感知推理蒸馏（SwaRD）：** 首先，通过 SwaRD 训练 LLM，使其具备分阶段思考的能力。这种分阶段的推理过程由 LLM 自身逐步评估，形成关于每个步骤是安全、不安全还是需要进一步改进的“pivot tokens”；
- **对比枢轴优化（CPO）：** 在推理过程中，LLMs 逐步预测安全状态标记（pivot tokens），通过对比学习优化模型对这些标记的感知能力，从而提高模型对对话安全状态的感知能力。

使用 $DeepSeek-R1_{70B}$ 和 $QwQ_{p-32B}$ 作为推理模型（M_R），并从 Alpaca 和 AdvBench 中收集推理轨迹数据，对非推理模型（如 Llama v3-8B、Qwen v2.5-14B 等）进行训练。

> [!todo]-
>
> - [ ] 方法
> - [ ] 模型
> - [ ] 数据集

## 贡献 (Contribution)

- R2D 显著降低了多种越狱攻击的成功率，相比非防御 LLMs，R2D 平均降低了 56%的攻击成功率；
- 与现有的防御基线相比，R2D 至少降低了 10%的攻击成功率；
- R2D 在保持模型有用性的同时，有效避免了过度拒绝现象。

> [!todo]-
>
> - [x] 结果
> - [ ] 解决了什么问题

## 总结 (Summary)

1. 论文提出的 R2D 训练范式为增强 LLMs 的安全性提供了一种新的思路。通过引入**安全意识推理机制**，模型在推理过程中能够动态调整回答策略，从而更有效地抵御越狱攻击。同时，CPO 方法也为优化模型对安全状态的感知能力提供了有效手段，有助于提升模型的鲁棒性。
2. 论文中主要关注的是通过从推理模型中蒸馏推理能力来提高安全性，而不是采用强化学习和测试时扩展等方法，未来可以研究如何将安全感知推理整合到 ReFT 类型的方法中。

> [!todo]-
>
> - [x] 没解决什么问题/进一步研究的方向
> - [x] 对我有什么用？

## 旁注 (note)

> [!cite]- Page 1
> 
> To bridge this gap, we propose Reasoning-toDefend (R2D), a novel training paradigm that integrates safety reflections of queries and responses into LLMs’ generation process, unlocking a safety-aware reasoning mechanism.
> 
> > [!note]
> >
> > 提出 R2D 训练范式，提高模型在推理过程中的安全意识。
> ^NDXAXHH5aDKKF6LRJp1

> [!cite]- Page 1
> 
> Furthermore, in order to improve the learning efficiency of pivot token prediction, we propose Contrastive Pivot Optimization (CPO), which enhances the model’s ability to perceive the safety status of dialogues.
> 
>> [!note]
>>
>> 在模型推理过程中插入安全状态标记（如<safe>或<unsafe>），通过对比学习优化模型对这些标记的感知能力
> ^8QXLD47NaDKKF6LRJp1

> [!cite]- Page 1
> 
> LLMs dynamically adjust their response strategies during reasoning, significantly enhancing their defense capabilities against jailbreak attacks.
> 
> > [!note]
> >
> > 推理过程中动态调整回答。
> ^EMIZWAIIaDKKF6LRJp1

> [!cite]- Page 1
> 
> R2D effectively mitigates various attacks and improves overall safety, highlighting the substantial potential of safety-aware reasoning in strengthening LLMs’ robustness against jailbreaks.1
> ^EJVVEBRFaDKKF6LRJp1

> [!cite]- Page 1
> 
> External1  arXiv:2502.12970v1 [cs.CL] 18 Feb 2025 detection methods usually rely on content regular expression matching, perplexity filtering (Jain et al., 2023; Alon and Kamfonas, 2023), prompt perturbation (Robey et al., 2023) or external guardrail models (Inan et al., 2023) to discover potential jailbreaking risks. Supervised-enhancement methods (Liu et al., 2024c; Dai et al., 2024; Mu et al., 2024) mainly rely on safe supervised fine-tuning (SFT), direct preference optimization (DPO, Rafailov et al., 2023), reinforcement learning from human feedback (RLHF, Ouyang et al., 2022). Other learning-based approaches like toxic content unlearning (Zhang et al., 2024; Lu et al., 2024), and safety-aware decoding (Xu et al., 2024; Hazra et al., 2024) can also be attributed to this category.
> 
> > [!note]
> >
> > 现有防御方式有：外部防御，监督强化，(基于学习的方式)
> ^EUPLTUKPaDKKF6LRJp1

> [!cite]- Page 2
> 
> Supervised-enhancement methods (Liu
> ^4YGW3JF7aDKKF6LRJp2

> [!cite]- Page 2
> 
> learning-based approaches
> ^83RVDVAJaDKKF6LRJp2

> [!cite]- Page 2
> 
> proposed R2D integrates the safety reflections into each step of the reasoning process of LLMs, eliminating the necessity of external guardrails.
> 
> > [!note]
> >
> > 通过使用 R2D 策略，使得模型在每一步思考后进行反思，使用 pivot 标记，以影响模型的后续推理。
> ^NAIL8NNJaDKKF6LRJp2

> [!cite]- Page 2
> 
> Specifically, R2D equips LLM with reasoning abilities first with Safety-aware Reasoning Distillation (SwaRD), enabling LLMs with staged thinking tendency. The staged reasoning process is further step-wise evaluated by the LLM itself, forming pivot tokens about whether an individual step is safe, unsafe, or requires refinement afterward, which is enhanced with the proposed Contrastive Pivot Optimization (CPO)
> ^WUD34ET5aDKKF6LRJp2

> [!cite]- Page 2
> 
> learning from reasoning trajectories instead of hard refusal prevents LLMs from over-refusal in safe scenarios, which is crucial for maintaining the capabilities for normal usage.
> 
> > [!note]
> >
> > 从推理轨迹中去学习能够较好的防止模型过度拒绝回答。
> ^5JFS99LCaDKKF6LRJp2

> [!cite]- Page 2
> 
> We also include XSTest (Röttger et al., 2024) in our experiments to investigate whether R2D leads to potential overrefusal.
> 
> > [!note]
> >
> > 使用 XSTest 测试模型在 “过度拒绝”中的表现。
> ^62CTRNBYaDKKF6LRJp2

> [!cite]- Page 2
> 
> safety-aware reasoning does not lead to loss of performance for normal usage
> ^IT8T354SaDKKF6LRJp2

> [!cite]- Page 2
> 
> safety-aware reasoning to defend LLMs against jailbreak attacks, and effectively avoid over-refusal phenomenon for normal usage
> 
> > [!note]
> >
> > 使用 safety-aware reasoning 来提高模型抵抗越狱攻击的能力，同时减少过度拒绝。
> ^9898PWUFaDKKF6LRJp2

> [!cite]- Page 2
> 
> training paradigm named R2D, where original non-reasoning LLMs are trained to reason using SwaRD, while also learning to detect and mitigate safety risks in the process using the proposed CPO.
> ^IRBPFFILaDKKF6LRJp2

> [!cite]- Page 3
> 
> In the field of safety, some works also focus on reasoning-based self-reflection, which is proved to be valid as discussed in Self-Reminder (Xie et al., 2023) and backtracking (Zhang et al., 2025a), where LLMs critique themselves given current prompts and responses.
> ^GF4TZXA5aDKKF6LRJp3

> [!cite]- Page 3
> 
> The safety-aware reasoning capabilities are enhanced through reasoning distillation. Moreover, we introduce contrastive pivot optimization to further improve LLMs’ awareness of safety at each step.
> 
> > [!note]
> >
> > 强调 reasoning distillation 和 CPO 的使用。
> ^AXUWQVWEaDKKF6LRJp3

> [!cite]- Page 3
> 
> Specifically, during R2D’s inference, it generates an inner reasoning process with step-wise self-evaluation, forming safety-aware PIVOT TOKENS of each step of responses, and indicating whether this step is safe (marked as [SAFE]), unsafe (marked as [UNSAFE]) or requires further refinement (marked as [RETHINK]).
> 
> > [!note]
> >
> > 在推理过程中进行自评估，使用三种标签来标记，影响模型的推理。
> ^EDDSFLW2aDKKF6LRJp3

> [!cite]- Page 3
> 
> After the reasoning and generation are finished, the [UNSAFE] reasoning process and answers are kept invisible from users, maintaining the safety of the conversations.
> 
> > [!note]
> >
> > 标记为不安全的内容不展示给用户
> ^4TQN3WE8aDKKF6LRJp3

> [!cite]- Page 4
> 
> reasoning trajectories are utilized in the Safety-aware Reasoning Distillation (SwaRD) process, where a non-reasoning LLM acquires reasoning skills from a safety perspective.
> 
> > [!note]
> >
> > SwaRD 使得非推理模型获得在安全方面的推理能力。
> ^XP8HRB6LaDKKF6LRJp4

> [!cite]- Page 5
> 
> Subsequently, a guardrail model (Inan et al., 2023) is employed to perform safety-aware tagging, ensuring that each reasoning step is accompanied by more precise and contextually appropriate PIVOT TOKENS. This process helps align the predicted PIVOT TOKENS with safety protocols by evaluating the reasoning trajectory for potential risks at each step. The tagged PIVOT TOKENS, along with their corresponding reasoning trajectories, are then aggregated to construct the safety-aware reasoning dataset, denoted as DR
> ^ZMFK875BaDKKF6LRJp5

> [!cite]- Page 8
> 
> Our experimental results and ablation studies show that by leveraging these reasoning capabilities, R2D-enabled LLMs consistently achieve lower ASRs compared to those using previous defense approaches, validating the effectiveness of the different components of R2D
> 
> > [!note]
> >
> > 通过 ablation study 来研究不同策略对模型的实际影响。
> ^QAA2WZ95aDKKF6LRJp8


