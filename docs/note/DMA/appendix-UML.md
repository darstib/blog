---
tags:
  - notes
comments: true
---

> [!quote] [_Understanding Machine Learning: From Theory to Algorithms_](https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/copy.html) 

比较难读，参考知乎上的笔记 [UML Reading Notes](https://www.zhihu.com/column/c_1779928788929331200)。

## A Gentle Start


- Domian Set: $\mathcal{X}$
- Label Set: $\mathcal{Y}$
- Data Set: $S = \{(x_{1}, y_{1}), \dots, (x_m, y_m)\}~(\forall~i~\in [m], x_{i}, y_{i} \in \mathcal{X\times Y})$
- Hypothesis: $h:\mathcal{X \rightarrow Y} \in \mathcal{H}$
- Ground truth: $f:\mathcal{X\rightarrow Y}~(\forall~i~\in~[m],f(x_i) = y_{i})$
- Subset: $A \subset \mathcal{X}$
- Data Distribution: D
	- $D(A)$ 表示对于 $x \in \mathcal{X}$，$x \in A$ 的概率
- Error rate: $L_{\mathcal{D},f}(h)\stackrel{\mathrm{def}}{=}\mathbb{P}_{x\sim\mathcal{D}}[h(x)\neq f(x)]\stackrel{\mathrm{def}}{=}\mathcal{D}(\{x:h(x)\neq f(x)\})$
	- 即 h 在分布 D 上的错误率
- Empirical Risk: $L_s(h) = \frac{|\{i \in [m]:h(x_i)\neq y_{i}\}|}{m}$
	- 即 h 在数据集 S 上的错误率

- Theorem 1.1 (The Realizability Assumption)
	- 认为存在 $h^* \in \mathcal{H}$ 使得 $L_{D, f}(h^*) = 0 = L_S(h^*)$
	- 即假设在待学习的模型空间中存在一个完美的模型能够拟合 f
- Theorem 1.2
	- 对于有限集 $\mathcal{H}$，如果在 D 上独立同分布的数据集 S 的长度满足 $m\geq \frac{\log(|\mathcal{H}| / \delta)}{\epsilon}$
	- 那么有 $1-\delta$ 的概率得到 $L_{D, f}(h_S) \leq \epsilon$
	- 即在足够大的数据集上学习到的模型有较大概率能够有较好的表现。

## PAC learning

- Definition 2.1 (PAC Learnability)
	- 存在函数 $m_{\mathcal{H}}: (0, 1)^2 \rightarrow \mathbb{N}$，当 $|S|=m \geq m_\mathcal{H}(\epsilon, \delta)$ 且有 $1-\delta$ 的概率得到 h 满足 $L_{D, f}(h) \leq \epsilon$
	- 则称这个 $\mathcal{H}$ 是 PAC learnable
- Corollary 2.2
	- 每一个有限的 $\mathcal{H}$ 都 PAC learnable
	- $m_\mathcal{H}(\epsilon, \delta) \leq \left\lceil  \frac{\log(|\mathcal{H| / \delta})}{\epsilon}  \right\rceil$
- Definition 2.3 (Agnostic PAC Learnability)
	- 如果没有 Theorem 1.1 条件，但
	- 存在函数 $m_{\mathcal{H}}: (0, 1)^2 \rightarrow \mathbb{N}$，当 $|S|=m \geq m_\mathcal{H}(\epsilon, \delta)$ 且有 $1-\delta$ 的概率得到 h 满足 $L_{\mathcal{D}}(h)\leq\min_{h'\in\mathcal{H}}L_{\mathcal{D}}(h')+\epsilon$
	- 则称这个 $\mathcal{H}$ 是 Agnostic PAC learnable
	- 更加一般化的定义

## Uniform Convergence

- Definition 3.1 ($\epsilon-Representative$)
	- 训练集 S 是 $\epsilon-Representative$ 当且仅当：
	- $\forall~h~\in~\mathcal{H}, |L_S(h)-L_D(h)| \leq \epsilon$
- Definition 3.3 (Uniform Convergence)
	- $\mathcal{H}$ 具有一致收敛性当且仅当：
	- 存在一个函数 $m_\mathcal{H}^{UC}: (0, 1)^2 \rightarrow \mathbb{N}$，对于任意 $\epsilon, \delta, D$，只要 $|S| = m \geq m_\mathcal{H}^{UC}(\epsilon, \delta)$
	- 那么训练集 S 有 $1-\delta$ 概率为 $\epsilon-Representative$ 
- 可以推导出：有限假设类 $\mathcal{H}$ 在 Agnostic PAC 模型下是可学习的

## Bias-Complexity tradeoff

- Theorem 5.1 (No-Free-Lunch)
	- $\forall m < \frac{|\mathcal{X}|}{2}, \exists ~f \text{ with } L_{D}(f) = 0$ while $S \sim D^m$: $L_{D}(A(S))\geq \frac{1}{8}$ with probability of at least $\frac{1}{7}$
	- 即如果训练数据集太小了，总能找到一个分布使得：有能够很好地学习这个分布的假设，但较大概率会得到较差的结果
- Corollary 5.2
	- Let $\mathcal{X}$ be an infinite domain set and $\mathcal{H}$ be the set of all $f:\mathcal{X} \rightarrow \{0, 1\}$. Then $\mathcal{H}$ is not PAC learnable.
	- 也就是说如果不对假设空间 $\mathcal{H}$ 引入先验知识（以限制空间大小），那么 $\mathcal{H}$ 是 PAC 不可学习的
- Error decomposition
	- $L_{D}(h_{S}) = \epsilon_{app} + \epsilon_{est}$ where: $\epsilon_{app} = \min_{h \in\mathcal{H}}L_{D}(h), \epsilon_{est}=L_{D}(h_{S}) - \epsilon_{app}$
	- 近似误差 (Approximation Error, $\epsilon_{app}$) 
		- 代表了在 $\mathcal{H}$ 中能够达到的最小的风险，显然提高 $\mathcal{H}$ 的复杂度有利于降低 $\epsilon_{app}$
	- 估计误差 (Estimation Error, $\epsilon_{est}$)
		- 代表了在 $S$ 上训练得到的假设 $h_{S}$ 与最优假设之间的风险差距，这源于数据集与真实世界之间信息量的差距
		- 显然增大样本量 $m:=|S|$ （相对而言，就是降低 $H$ 的复杂度）有利于降低 $\epsilon_{est}$
- 这引出了欠拟合与过拟合的问题，需要在偏差和复杂度之间做出权衡

## VC-Dimension

> 前面提到：“每一个有限的 $\mathcal{H}$ 都 PAC 可学习的”；那无限的 $\mathcal{H}$ 呢？

- DEFINITION 6.2 (Restriction of $\mathcal{H}$ to $C$)
	- Let $\mathcal{H}$ be a class of functions from $\mathcal{X}$ to $\{0, 1\}$ and let $C = \{c_1, \dots, c_m\} \subset \mathcal{X}$. The restriction of $\mathcal{H}$ to $C$ is the set of functions from $C$ to $\{0, 1\}$ that can be derived from $\mathcal{H}$. That is,

		$$ \mathcal{H}_C = \{(h(c_1), \dots, h(c_m)) : h \in \mathcal{H}\}, $$

	- where we represent each function from $C$ to $\{0, 1\}$ as a vector in $\{0, 1\}^{|C|}$.

If the restriction of $\mathcal{H}$ to $C$ is the set of all functions from $C$ to $\{0, 1\}$, then we say that $\mathcal{H}$ *shatters* the set $C$. Formally:

- DEFINITION 6.3 (Shattering)
	- A hypothesis class $\mathcal{H}$ shatters a finite set $C \subset \mathcal{X}$ if the restriction of $\mathcal{H}$ to $C$ is the set of all functions from $C$ to $\{0, 1\}$. That is, $|\mathcal{H}_C| = 2^{|C|}$.
- DEFINITION 6.5 (VC-dimension)
	- The VC-dimension of a hypothesis class $\mathcal{H}$, denoted $\text{VCdim}(\mathcal{H})$, is the maximal size of a set $C \subset \mathcal{X}$ that can be shattered by $\mathcal{H}$. If $\mathcal{H}$ can shatter sets of arbitrarily large size we say that $\mathcal{H}$ has infinite VC-dimension.
- THEOREM 6.6
	- Let $\mathcal{H}$ be a class of infinite VC-dimension. Then, $\mathcal{H}$ is not PAC learnable.
- 结论：下面的描述等价
	- $\mathcal{H}$ 是 PAC 可学习的
	- $\mathcal{H}$ 的 VC 维有限
	- $\mathcal{H}$ 具有一致收敛属性
	- 任何 ERM（经验风险最小化）规则都是成功的学习器