## QARM: Quantitative Alignment Multi-Modal Recommendation at Kuaishou

> [!info]
>
> - [QARM: Quantitative Alignment Multi-Modal Recommendation at Kuaishou](https://arxiv.org/abs/2411.11739)
> - [快手QARM:量化对齐多模态推荐](https://zhuanlan.zhihu.com/p/14936185173)

受限于训练的计算成本&推理时的时延约束, 工业界多模态推荐普遍采用两阶段级联范式:

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2604/22_1776871505399.png)

1. 首先预训练多模态大模型，为下游服务提供统一的多模态表征
2. 然后以多模态表征作为下游推荐模型额外的信息输入去辅助学习真实的 User-Item 协同交互

这种两阶段的级联范式能取得一些效果提升, 但还是存在着一些缺点:

+ **表征不匹配问题:** 预训练的多模态模型是以 NLP/CV 任务监督学习, 如图像文本匹配的自监督任务, 而推荐模型是 ID 特征主导的, 由真实的 User-Item 交互数据来驱动学习, 这就导致两类任务目标相对独立, 缺乏一致目标；
+ **表征不更新问题:** 生成的多模态表征是静态的, 总是存储在缓存中, 作为推荐模型的额外固定输入, 无法通过推荐模型梯度更新, 这对下游任务训练更加不友好

为了缓解这两个问题, 快手提出了量化对齐的多模态推荐方法 (Quantitative Alignment Multi-Modal Recommendation, QARM)。

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2604/22_1776871471840.png)

### Item Alignment

对于多模态表征不匹配问题，近年来业界广泛所采用的一个思路是: **使用推荐任务自己场景内的数据来微调多模态模型**；通过构造正负样本/生成高质量的 Item2Item 的 Pair 对 (Trigger Item, Target Item) 数据集来做微调。

QARM 使用到的是 Item Pair；Item Pair 的获取方式通常基于 U2I/I2I 召回模型构造。在生成高质量的 Item Pair数据集 $\mathcal{D}$ 后，由 MLLM 依据多模态输入 token 得到 Batch 内的多模态表征 $\mathrm{M}_{\mathrm{trigger}}/\mathrm{M}_{\mathrm{target}}\in\mathbb{R}^{|\mathcal{B}|\times d}$：

$$
\begin{aligned}
\mathbf{M_{trigger}}=\mathrm{MLLM}(\mathbf{T_{trigger}^{text}},\mathbf{T_{trigger}^{audio}},\mathbf{T_{trigger}^{image}})\\
\mathbf{M_{target}}=\mathrm{MLLM}(\mathbf{T_{target}^{text}},\mathbf{T_{target}^{audio}},\mathbf{T_{target}^{image}})\\
\mathcal{L}_{\mathrm{align}}=\text{Batch-Contrastive}(\mathbf{M}_{\mathrm{trigger}},\mathbf{M}_{\mathrm{target}},\mathcal{B})
\end{aligned}
$$

然后在 Batch 内优化 Item Pair 对齐损失，适配下游任务的协同信号。

### Quantitative Code

对于多模态表征不更新问题，业界一种最直接&广泛应用的 trick, 是对多模态表征量化压缩来构造语义相似 Item 的 ID list, 然后以 ID List 作为该 item 的语义特征输入到推荐模型。论文中提到了两种量化方案：

**Vector Quantized, VQ**

> 记上述得到的所有多模态表征的集合为 M，某一物品的表征为$ m \in M, m \in \mathbb{R}^{d} $。

我们知道 VQ 需要码本；作者认为前面得到的表征已经足够反映物品的信息，直接使用 M 作为码本：

$$
V = M
$$

随后的做法是利用 TopK 最近邻搜索，找到 V 中与 m 最近邻的 K 个向量的 index 作为 m 的量化编码：

$$
v_1,v_2,\ldots,v_K=\text{TopKCode}(V,m,K)
$$

**Residual Quantized, RQ**

对于 RQ 的基本思路这里不进行复述；这篇论文使用的不是 RQ-VAE，而是后来被称为 RQ-Kmeans 的做法：

1. 对于 RQ 中的** L 层码本**，在每一层都通过 Kmeans 聚类实现：
   - 在第 k 层，我们的表征集合为$ M^{k-1} $；使用 Kmeans 聚类得到 N 个聚类中心$ R^k $
   - 对于$ M^{k-1} $中的每个表征，寻找$ R^k $中的最近邻向量，并减去得到$ M^k $

$$
\begin{aligned}&\mathbf{R}^{1}=\mathrm{Kmeans}(\mathbf{M},N),\quad\mathbf{M}^{1}=\mathbf{M}-\mathrm{NearestRep}(\mathbf{M},\mathbf{R}^{1})\\&\mathbf{R}^{2}=\mathrm{Kmeans}(\mathbf{M}^{1},N),\quad\mathbf{M}^{2}=\mathbf{M}^{1}-\mathrm{NearestRep}(\mathbf{M}^{1},\mathbf{R}^{2})\\&\ldots,\quad\mathbf{R}^{L}=\mathrm{Kmeans}(\mathbf{M}^{L-1},N)\end{aligned}
$$

2. 获得码本后，量化编码的获取方式就是正常的 RQ

$$
\begin{aligned}&r_{1}=\mathrm{NearestCode}(\mathbf{R}^{1},\mathbf{m},1),\quad\mathbf{m}^{1}=\mathbf{m}-\mathbf{R}_{r_{1}}^{1}\\&r_{2}=\mathrm{NearestCode}(\mathbf{R}^{2},\mathbf{m}^{1},1),\quad\mathbf{m}^{2}=\mathbf{m}^{1}-\mathbf{R}_{r_{2}}^{1}\\&\ldots,\quad r_{L}=\mathrm{NearestCode}(\mathbf{R}^{L},\mathbf{m}^{L-1},1)\end{aligned}
$$

> 接下来的部分与 OneRec 无关，暂且放下

## OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment

> [!info]
>
> [OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment](https://arxiv.org/abs/2502.18965)

### 沙漏现象

沙漏现象指的是：在 `RQ-VAE` 中，中间 `level` 的 `tokens` 的分布变得非常不均匀：某些 `tokens` 被频繁使用、某些 `tokens` 被很少使用。这会导致如下问题：

- 表达效率低下：如果某些 `tokens` 被很少使用，那么它们对应的 `codebook` 向量就得不到充分的训练，浪费了模型容量。
- 模型性能下降：模型在预测这些低频 `tokens` 时会遇到困难。

沙漏现象的原因：

- 数据分布的特性：在推荐系统中，视频的 `embeddings` 分布并非均匀的。它们往往形成一些大而宽的聚类（如，“娱乐”、“体育”）、以及小而密的聚类（如，特定的游戏）。
- `first-level` 量化：`first-level codebook` 负责捕获最宏观的语义信息。由于聚类数量少（宏观类别少），`first-level codebook` 能够被相对均匀地使用。
- `middle-level` 的困境：经过 `first-level` 量化之后，残差数据的分布变得非常复杂和分散。它需要捕获每个宏观类别内部的大量细分信息。然后，`middle-level codebook` 的容量是固定的。它难以同时很好地覆盖到所有宏观类别内部的细分结构。

  导致的结果是：`middle-level codebook` 只有少数几个热门的 `code vector` 被频繁地用于补偿各种宏观类别下常见的残差，而大部分 `code vector` 很少被使用到。这造成了 `middle-level codebook` 的利用率极低。
- `tail-level` 量化：到了最后一个 `level`，任务变得相对单纯：它只需要修复前面 `levels` 量化后剩余的、非常细微的残差。这些细微的残差的分布相对均匀，因为 `tail-level codebook` 又能够被均匀地使用。

出于 RQ-VAE 的“沙漏现象”，论文中选择使用 multi-level balanced quantitative mechanism，具体而言使用到了 residual K-Means quantization algorithm。对于 RQ 部分不再复述，我们关注 codebook 的构建。

论文中使用了 Balanced K-means Clustering algorithm 进行 itemset partitioning；

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2604/23_260423-095327.png)

简单而言，对于物品集 $\mathcal V$，码本的第 $l \in \{1, \dots, L\}$ 层，希望聚为 K 个类（$w = |V|/K$ ）

1. 随机分配聚类中心 $C_l=\{\mathbf{c}_1^l,\ldots,\mathbf{c}_K^l\}$，初始化 $\mathcal U = \mathcal V$
2. 对于 $k \in \{1, \dots, K\}$，找到 $c_k^l$ 在 $\mathcal U$中最近的