---
tags:
  - notes
comments: true
---

# Graph Representation Learning

图表示学习 (Graph Representation Learning, GRL) 期望将结点（甚至整个图）映射为**向量**表示的时候尽可能多地保留图的**拓扑信息**。图表示学习主要分为**基于图结构的表示学习**和**基于图特征的表示学习**。

以空手道社交网络 (Karate Graph) 为例，基于已有聚类算法的聚类效果如图 (a) 所示，期望寻找的潜在二维表征 (laten representation) 如图 (b) 所示。

![proposed method learns a latent space representation of social interactions in R^d](https://raw.githubusercontent.com/darstib/public_imgs/utool/2509/05_250905-132831.png)

GRL 主要分为两大类：

- 图嵌入方法 (Graph Embedding, GE)
- 图神经网络 (Graph Neural Networks, GNNs)

## 基本符号

- $V$：所有顶点/节点集合
	- $u, v \in V$：一般用于表示节点（有时表示向量）
	- $i, j \in [|V|]$：一般用于表示节点标识符 (ID)
	- $N(v)/ne[v]$：表示节点 v 的所有邻接节点的集合
	- $\vec{l}_{v} \in \mathbb{R}^{n_{v}}$：表示节点 v 的标签信息
	- $\mathbf{x}_{v} \in \mathbb{R}^{|S|}$：表示节点的特征
- $E$：所有边的结合，包括有向边或无向边
	- $(u, v) \in E$：一般用于表示节点 u, v 之间的边
	- $E_{v} / co[v]$：表示包含节点 v 的边的集合
	- $\vec{l}_{u, v} \in \mathbb{R}^{n_{e}}$：表示边 (u, v) 的标签信息
- $G = (V, E)$ ：最基本的图，由点和边构成

上面只是一般情况，实际符号可能不同，有声明情况下以声明为准。
