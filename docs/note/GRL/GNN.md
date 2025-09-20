# Graph Neural Network

- [AI 算法工程师手册 - GNN](https://www.huaxiaozhuan.com/深度学习/chapters/11_GNN.html)
	- [第三方备份](https://www.bookstack.cn/read/huaxiaozhuan-ai/1d6b4f71c978a00a.md)

很多领域的数据关系可以表示为图结构，如计算机视觉、分子化学、模式识别、目标检测等，这些图结构往往比较复杂，基本的 Graph Embedding （可以认为是将图“压缩”为实值向量）会损失较多信息，难以捕捉到图的细节。

关于图的任务可以分为两大类：

- 基于图的任务 (graph-focused) ：例如分子化合物整个图结构的意义高于单独的原子和化学键
- 基于节点的任务 (node-focused) ：例如目标检测、网页分类任务需要关注局部，整体信息过于嘈杂

论文《The graph neural network model》提出了 `GNN` 模型，该模型扩展了 `RNN` 和马尔科夫链技术，适合处理图结构的数据。`GNN` 是基于消息扩散机制 `information diffusion mechanism` 。图由一组处理单元来处理，每个处理单元对应于图的一个顶点。GNN 既适合 graph-focused 任务，也适合 node-focused 任务。

> [!todo] 感觉要先看 CNN/RNN。

## GNN



## GraphSAGE

> [!quote]- 动机
> 
> GraphSAGE 提出的前提是因为基于直推式(transductive)学习的图卷积网络无法适应工业界的大多数业务场景。我们知道的是，基于直推式学习的图卷积网络是通过拉普拉斯矩阵直接为图上的每个节点学习 embedding 表示，每次学习是针对于当前图上所有的节点。然而在实际的工业场景中，图中的结构和节点都不可能是固定的，会随着时间的变化而发生改变。在这样的场景中，直推式学习的方法就需要不断的重新训练才能够为新加入的节点学习 embedding，导致在实际场景中无法投入使用。

斯坦福大学提出了一种归纳(inductive)学习的 GCN 方法——《Graph Sample and Aggregage:GraphSAGE》，即**通过聚合邻居信息的方式为给定的节点学习 embedding**。不同于直推式(transductive)学习，GraphSAGE 是通过学习聚合节点邻居生成节点 Embedding 的函数的方式，为任意节点学习 embedding，进而将 GCN 扩展成归纳学习任务。

### 概览

![GCN overview](https://raw.githubusercontent.com/darstib/public_imgs/utool/2509/05_250905-181135.png)

> 这张图找了很久来源，一直觉得可能是哪篇论文的配图（很多文章中使用但是没写来源）最后疑似出自 [Food Discovery with Uber Eats: Using Graph Learning to Power Recommendations](https://www.uber.com/en-SG/blog/uber-eats-graph-learning/) ；但是好像还是不知道公式是从哪里来的。

上面是一个 xxx 的算法流程公式解析，核心自然是中间的公式。

- $h^{0}_{v}$ 表示节点 v 使用自身的特征 $\mathbf{x}_{v}$ 初始化的表示
- $h_{v}^{k}$ 表示第 k 层卷积后的节点表示，其更新来自两部分：
	- 对 k-1 层得到的邻居表征求平均 ($\sum_{u\in N(v)}\frac{h_u^{k-1}}{|N(v)|}$)，再进行线性变换 ($W_{k}$)
	- 对 k-1 层得到的表征 $h_{v}^{k-1}$ 作线性变换 ($B_{k}$)
	- 相加后用 sigmoid 函数激活
- $z_{v} = h_{v}^{last}$ 表示最后的结果输出

![GraphSAGE algorithm](https://raw.githubusercontent.com/darstib/public_imgs/utool/2509/05_1757074885950.png)

简而言之，利用采样降低计算复杂度，依据边关系聚合邻居节点信息以及自身信息，作非线性变换。通过多层堆叠，节点能够从全局角度利用到邻居信息；同时 GraphSAGE 支持归纳学习 (inductive learning) ，聚合邻居节点生成 embedding 更适合图结构不断变化的工业场景。

### 采样

GraphSAGE 的采样过程如下：

1. 使用一小批节点 B 初始化 $B^{K}$
2. 对于 k 从 $K\rightarrow 1$ ：
	- 使用 $B^{k}$ 初始化 $B^{k-1}$
	- 以 $B^{k}$ 中的节点作为中心节点，对邻居进行随机定量采样
		- “随机”使得相似的节点具有相同的表达形式
		- “定量”是为了方便批量训练，每个 batch 等大
		- “采样”是为了避免搜索全图导致计算复杂度高
	- 将采样的邻居加入 $B^{k-1}$
3. 得到 $\{B^{k}\}_{k\in [K]}$ ，以此为第 k 层卷积操作时需要计算的点。

### 聚合

由于邻居节点是无序的，所以希望构造的聚合函数具有**对称性(即输出的结果不因输入排序的不同而改变)**，同时拥有**较强的表达能力**。如何对于采样到的节点集进行聚合，介绍的4种方式：

- Mean 聚合：首先会对邻居节点按照**element-wise**进行均值聚合，然后将当前节点k-1层得到特征 $h_{v}^{k-1}$ ​与邻居节点均值聚合后的特征 $MEAN(h_{u}^{k}∣u \in N(v))$ **分别**送入全连接网络后**相加**得到结果。
- Convolutional 聚合：这是一种基于GCN聚合方式的变种，首先对邻居节点特征和自身节点特征求均值，得到的聚合特征送入到全连接网络中。与Mean不同的是，这里**只经过一个全连接层**。
- LSTM聚合：由于LSTM可以捕捉到序列信息，因此相比于Mean聚合，这种聚合方式的**表达能力更强**；但由于LSTM对于输入是有序的，因此该方法不具备**对称性**。作者对于无序的节点进行随机排列以调整LSTM所需的有序性。
- Pooling聚合：对于邻居节点和中心节点进行一次非线性转化，将结果进行一次基于**element-wise**的**最大池化**操作。该种方式具有**较强的表达能力**的同时还具有**对称性**。

注意到采样和聚合的顺序时相反的，我们希望信息逐层从边缘向中心节点聚集，最后得到中心节点的表征。
