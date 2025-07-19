---
url: http://arxiv.org/abs/2502.12659
tags:
  - LRM
comments: true
---

> [!abstract]- [Comprehensible Artificial Intelligence on Knowledge Graphs: A survey](http://arxiv.org/abs/2404.03499)
>
> Artificial Intelligence applications gradually move outside the safe walls of research labs and invade our daily lives. This is also true for Machine Learning methods on Knowledge Graphs, which has led to a steady increase in their application since the beginning of the 21st century. However, in many applications, users require an explanation of the Artificial Intelligences decision. This led to increased demand for Comprehensible Artificial Intelligence. Knowledge Graphs epitomize fertile soil for Comprehensible Artificial Intelligence, due to their ability to display connected data, i.e. knowledge, in a human- as well as machine-readable way. This survey gives a short history to Comprehensible Artificial Intelligence on Knowledge Graphs. Furthermore, we contribute by arguing that the concept Explainable Artificial Intelligence is overloaded and overlapping with Interpretable Machine Learning. By introducing the parent concept Comprehensible Artificial Intelligence, we provide a clear-cut distinction of both concepts while accounting for their similarities. Thus, we provide in this survey a case for Comprehensible Artificial Intelligence on Knowledge Graphs consisting of Interpretable Machine Learning on Knowledge Graphs and Explainable Artificial Intelligence on Knowledge Graphs. This leads to the introduction of a novel taxonomy for Comprehensible Artificial Intelligence on Knowledge Graphs. In addition, a comprehensive overview of the research on Comprehensible Artificial Intelligence on Knowledge Graphs is presented and put into the context of the taxonomy. Finally, research gaps in the field of Comprehensible Artificial Intelligence on Knowledge Graphs are identified for future research.

## 概述 (Content)

这篇综述探讨了在知识图谱(KG)背景下的可理解人工智能(CAI)。随着 AI，特别是基于 KG 的机器学习方法在现实世界（如医疗、工业、自动驾驶等）中的广泛应用，尤其是涉及安全关键领域时，对模型决策过程的理解变得至关重要。然而，许多先进的 AI 模型（如深度神经网络）本质上是“黑盒”，难以理解。这催生了对 CAI 研究的需求。当前，“可说明 AI”(XAI)的概念常常被宽泛使用，与“可解释机器学习”(IML)的概念界限模糊。该论文旨在**解决这种概念混淆**，通过引入**CAI 作为顶层概念**，清晰地**区分 IML（旨在构建本身透明的白盒模型）和 XAI（旨在解释现有黑盒模型的决策过程）**。、

论文认为，KG 因其结构化、包含语义且人机均可读的特性，是发展 CAI 的理想基础，并：

1. 梳理 KG 上 CAI 的历史和必要性；
2. 提出一个新的 CAI on KGs 的分类法；
3. 基于该分类法全面回顾 IML 和 XAI 在 KG 上的现有研究；
4. 指出该领域的研究空白和未来方向。

特别地，论文将**重点放在将KG作为AI模型的输入**进行研究，认为这种方式比将 <u>KG 作为输出</u> 更能促进可解释性。

## 方法 (How)

核心方法是**提出并应用一个新的分类法 (taxonomy)** 来组织和分析这些文献，包含四个维度： 

![table2](https://raw.githubusercontent.com/darstib/public_imgs/utool/2504/22_1745334166982.png)

1. **表示 (Representation):** KG 的表示方式（符号 SB、子符号 SSB、神经符号 NSB）；
2. **基础 (Foundation):** 底层的机器学习方法（如平移学习 TL、基于规则的学习 RBL、神经网络 ANN、强化学习 RL 等）；
3. **任务 (Task):** AI 模型在 KG 上执行的具体任务（如链接预测 LP、节点聚类 NC、图聚类 GC、推荐 R 等）；
4. **可理解性 (Comprehensibility):** 方法属于 IML 还是 XAI。

## 贡献 (Contribution)

主要贡献在于： 

1. 论证研究**焦点：** 提供了将研究重点放在“KG 作为输入”而非“KG 作为输出”的理由，认为前者更有利于实现模型的可解释性和说明性。
2. **概念澄清与构建：** 引入了**可理解人工智能(CAI)** 作为顶层概念，并对其两个主要分支——**可解释机器学习(IML)** 和**可说明人工智能(XAI)**——给出了清晰的定义和区分，解决了现有文献中 XAI 概念过载和与 IML 混淆的问题。强调了 IML 是构建内在可解释的模型，而 XAI 是为现有模型提供事后解释。 
3. 提出**新分类法：** 专门针对**知识图谱上的 CAI**，提出了一个包含表示、基础、任务和可理解性类型四个维度的新颖分类法。这个分类法为组织、理解和比较该领域的各种方法提供了一个系统的框架。 
4. 全面的**文献回顾：** 基于提出的分类法和IML/XAI的划分，对KG上的CAI研究现状进行了全面而结构化的综述，系统地梳理了 [IML（规则挖掘、路径发现、嵌入方法）](https://raw.githubusercontent.com/darstib/public_imgs/utool/2504/22_250422-230624.png)和[XAI（基于规则、分解、代理模型、图生成）](https://raw.githubusercontent.com/darstib/public_imgs/utool/2504/22_250422-230559.png)的主要研究路线和代表性工作。 
5. 指出**研究空白：** 明确指出了当前研究中存在的**空白和未来潜在的研究方向**，例如缺乏针对链接预测的 XAI 方法、IML 在聚类任务上应用较少、现有方法未能充分利用 KG 的丰富语义信息、缺乏标准化的 XAI 评估指标、以及需要改进 IML 模型解释的沟通方式等。

## 总结 (Summary)

该综述系统地梳理了知识图谱上可理解人工智能的研究现状，提出了新的概念框架和分类法。尽管取得了显著进展，但作者也指出了该领域仍存在的挑战和未来研究方向，下面是我比较感兴趣的部分：

- [ ] **语义利用不足：** 大多数现有方法（尤其是 XAI）并未充分利用 KG 特有的语义信息（如节点标签、边标签、方向、本体论）；
- [ ] **评估标准化缺失：** 如何客观、公正地比较不同 XAI 方法的性能和解释质量，仍然是一个悬而未决的问题。亟需建立标准化的评估基准和指标；
- [ ] **IML 解释传达：** IML 模型虽然“白盒”，但其决策过程的解释往往对非专家用户不够友好，需要研究更有效的、面向特定利益相关者的解释沟通策略和可视化界面；
- **性能与可解释性的权衡：** 如何在保证高预测性能的同时，实现高水平的可解释性/可说明性，仍然是该领域的核心挑战之一。
- **方法查找：** 可以根据论文提出的分类法，快速定位特定类型（如基于规则的 IML、基于代理模型的 XAI）或特定任务（如链接预测的可解释性）的相关工作。