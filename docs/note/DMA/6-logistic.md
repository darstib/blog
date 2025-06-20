> [!help]-  推荐阅读 [Visual Information Theory](https://colah.github.io/posts/2015-09-Visual-Information/)

## 回归问题回顾 (page 4-5)

在进入分类模型之前，我们先回顾一下“回归”的概念。回归的目标是预测一个连续值的输出。

> [!example]+ 房价预测示例 (page 4)
>
> 假设我们有房屋面积与销售价格的数据，我们希望找到一个函数来拟合这些数据，以便预测新房屋的价格。
>
> 一个简单的模型是线性回归，例如：
>
> $$
> h(x) = \theta_0 + \theta_1 x_1 + \theta_2 x_2
> $$
>
> 其中 $x_1$ 可以是面积，$x_2$ 可以是房间数量等特征，$\theta_i$ 是我们需要学习的模型参数。我们的目标是找到一条（或一个超平面）线，使其能最好地“穿过”数据点，最小化预测值与真实值之间的误差。

> [!note]+ 多项式拟合与模型复杂度 (page 5)
>
> 我们可以使用更高阶的多项式来拟合数据。这张图展示了使用不同阶数 $M$ 的多项式函数去拟合一组数据点的效果。
>
> - **M=0, M=1**: 模型过于简单，无法捕捉数据的潜在趋势，导致**欠拟合（Underfitting）**。
> - **M=3**: 模型与数据的拟合程度较好，能够反映数据的基本分布。
> - **M=9**: 模型过于复杂，为了迁就每一个数据点而导致函数曲线剧烈波动。虽然它在训练数据上表现完美，但对新数据的预测能力（泛化能力）会很差，这被称为**过拟合（Overfitting）**。
>
> 这个例子告诉我们，在机器学习中选择合适的模型复杂度至关重要。

## 逻辑斯蒂分布与 Sigmoid 函数

逻辑斯蒂回归模型的名字来源于它所使用的**逻辑斯蒂分布（Logistic Distribution）**。

### 逻辑斯蒂分布 (page 6)

> [!definition]+ 逻辑斯蒂分布
>
> 设 $X$ 是一个连续随机变量，如果它服从逻辑斯蒂分布，其**累积分布函数（CDF）** 和 **概率密度函数（PDF）** 定义如下：
>
> - **分布函数**:
>
> $$
> F(x) = P(X \le x) = \frac{1}{1 + e^{-(x-\mu)/\gamma}}
> $$
>
> - **密度函数**:
>
> $$
> f(x) = F'(x) = \frac{e^{-(x-\mu)/\gamma}}{\gamma(1+e^{-(x-\mu)/\gamma})^2}
> $$
>
> 其中，$μ$ 是位置参数，决定了分布的中心位置；$γ > 0$ 是形状参数，决定了分布的“胖瘦”程度。
>
> 
> 其密度函数 $f(x)$ 呈钟形，而分布函数 $F(x)$ 是一条S形的曲线，被称为**Sigmoid曲线**。该分布函数关于点 $(μ, 1/2)$ 中心对称。

### Sigmoid 函数与 tanh 函数 (page 7)

在机器学习中，我们常用到两种与逻辑斯蒂分布密切相关的函数：Sigmoid 函数和 tanh 函数。它们通常被用作神经网络中的激活函数。

> [!wiki]+ Sigmoid 函数
>
> Sigmoid函数是逻辑斯蒂分布函数在 $μ=0, γ=1$ 时的特殊形式。
>
> - **公式**:
>
> $$
> f(z) = \frac{1}{1+e^{-z}}
> $$
>
> - **输出范围**: $(0, 1)$，这个特性使得它非常适合用来表示概率值。
> - **导数**: $f'(z) = f(z)(1-f(z))$。其导数可以用自身来表示，这在反向传播算法中计算梯度时非常方便。

> [!wiki]+ 双曲正切函数 (tanh)
>
> - **公式**:
>
> $$
> f(z) = \tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}
> $$
>
> - **输出范围**: $[-1, 1]$。与Sigmoid相比，tanh是零中心化的（zero-centered），这在某些场景下有助于加速模型收敛。
> - **导数**: $f'(z) = 1 - (f(z))^2$。
>
> 实际上，tanh函数是Sigmoid函数经过线性变换得到的：$\tanh(z) = 2 \cdot \text{sigmoid}(2z) - 1$。

## 二项逻辑斯蒂回归 (Binomial Logistic Regression) (page 8-11)

逻辑斯蒂回归虽然名字里有“回归”，但它实际上是一个经典的**分类模型**。它主要用于二分类问题，也可以扩展到多分类。

### 模型定义 (page 8)

逻辑斯蒂回归模型是一个由条件概率 $P(Y|X)$ 表示的分类模型。假设 $Y$ 的取值为0和1。

> [!definition]+ 二项逻辑斯蒂回归模型
>
> 对于给定的输入向量 $x$，模型输出类别为1和0的条件概率如下：
>
> $$
> P(Y=1|x) = \frac{\exp(w \cdot x + b)}{1 + \exp(w \cdot x + b)}
> $$
>
> $$
> P(Y=0|x) = \frac{1}{1 + \exp(w \cdot x + b)}
> $$
>
> - $w$ 是权值向量，$b$ 是偏置。
> - 为了简化表达，我们可以将偏置 $b$ 看作是权值向量的一个分量，同时在输入向量 $x$ 中增加一个恒为1的分量。这样，模型可以写成：
>
> $$
> w \leftarrow (w^{(1)}, \dots, w^{(n)}, b)^T, \quad x \leftarrow (x^{(1)}, \dots, x^{(n)}, 1)^T
> $$
>
> 模型就变为：
>
> $$
> P(Y=1|x) = \frac{\exp(w \cdot x)}{1 + \exp(w \cdot x)}
> $$
>
> $$
> P(Y=0|x) = \frac{1}{1 + \exp(w \cdot x)}
> $$

这正是将线性回归的输出 $w \cdot x$ 送入Sigmoid函数得到的结果。

### 模型解释：对数几率 (page 9)

逻辑斯蒂回归的一个优美之处在于其物理解释。

> [!wiki]+ 几率 (Odds) 与对数几率 (Log-odds)
>
> - **几率 (Odds)**：一个事件发生的概率 $p$ 与它不发生的概率 $1-p$ 之比，即 $\frac{p}{1-p}$。
> - **对数几率 (Log-odds or logit)**：对几率取对数，即 $\text{logit}(p) = \log\frac{p}{1-p}$。
>
> 对于逻辑斯蒂回归模型，我们将 $p = P(Y=1|x)$ 代入，可以得到：
>
> $$
> \log \frac{P(Y=1|x)}{1 - P(Y=1|x)} = \log \frac{\frac{\exp(w \cdot x)}{1+\exp(w \cdot x)}}{\frac{1}{1+\exp(w \cdot x)}} = \log(\exp(w \cdot x)) = w \cdot x
> $$
>
> 这个结果表明，在逻辑斯蒂回归模型中，**输出Y=1的对数几率是输入x的线性函数**。这便是“对数几率回归”这个名字的由来。

模型的决策过程可以看作：

1. 对输入 $x$ 进行线性变换：$z = w \cdot x$
2. 通过激活函数（Sigmoid）将 $z$ 转换为概率：$p = \text{sigmoid}(z)$

### 模型参数估计：极大似然法 (page 10-11)

模型的参数 $w$ 如何确定呢？答案是使用**极大似然估计（Maximum Likelihood Estimation, MLE）**。

> [!theorem]+ 似然函数
>
> 我们的目标是找到一组参数 $w$，使得在这些参数下，观测到我们现有训练数据的概率最大。
>
> 假设 $P(Y=1|x) = \pi(x)$，则 $P(Y=0|x) = 1-\pi(x)$。对于一个样本 $(x_i, y_i)$，其概率可以统一写成：
>
> $$
> P(y_i|x_i; w) = [\pi(x_i)]^{y_i} [1-\pi(x_i)]^{1-y_i}
> $$
>
> （当 $y_i=1$ 时，为 $\pi(x_i)$；当 $y_i=0$ 时，为 $1-\pi(x_i)$）
>
> 对于整个包含 $N$ 个独立同分布样本的数据集，其似然函数为所有样本概率的乘积：
>
> $$
> L(w) = \prod_{i=1}^N P(y_i|x_i; w) = \prod_{i=1}^N [\pi(x_i)]^{y_i} [1-\pi(x_i)]^{1-y_i}
> $$

为了计算方便，我们通常最大化对数似然函数 $\log L(w)$：

$$
\begin{align}
\log L(w) &= \sum_{i=1}^N \left[ y_i \log \pi(x_i) + (1-y_i) \log(1-\pi(x_i)) \right] \\
&= \sum_{i=1}^N \left[ y_i \log \frac{\pi(x_i)}{1-\pi(x_i)} + \log(1-\pi(x_i)) \right] \\
&= \sum_{i=1}^N \left[ y_i (w \cdot x_i) - \log(1+\exp(w \cdot x_i)) \right]
\end{align}
$$

我们的任务就是找到使这个对数似然函数 $\log L(w)$ 达到最大的 $w$ 值。这是一个无约束的凸优化问题，可以通过**梯度下降法**或更高效的**拟牛顿法**等数值优化算法来求解。

## 多项逻辑斯蒂回归 (Multinomial Logistic Regression) (page 12)

当分类任务的类别数 $K > 2$ 时，我们需要将二项逻辑斯蒂回归推广到多项。这种模型也被称为**Softmax回归**。

> [!definition]+ 多项逻辑斯蒂回归模型
>
> 设 $Y$ 的取值集合为 $\{1, 2, \dots, K\}$。模型形式如下：
>
> $$
> P(Y=k|x) = \frac{\exp(w_k \cdot x)}{1 + \sum_{j=1}^{K-1} \exp(w_j \cdot x)}, \quad k=1, 2, \dots, K-1
> $$
>
> $$
> P(Y=K|x) = \frac{1}{1 + \sum_{j=1}^{K-1} \exp(w_j \cdot x)}
> $$
>
> 这里我们为前 $K-1$ 个类别分别学习一个权值向量 $w_k$，而第 $K$ 个类别作为基准（reference class），其权值向量被固定为零向量。这样做是为了保证所有类别的概率之和为1。

> [!note]+ Softmax 函数
>
> 多项逻辑斯蒂回归的另一种等价且更常见的形式是使用Softmax函数：
>
> $$
> P(Y=k|x) = \frac{\exp(w_k \cdot x)}{\sum_{j=1}^{K} \exp(w_j \cdot x)}
> $$
>
> 在这种形式下，我们为每个类别都学习一个权值向量，分母是所有类别的 "score" 的指数之和，起到了归一化的作用。

## 损失函数：交叉熵 (page 13-16)

前面我们通过极大似然估计导出了逻辑斯蒂回归的目标函数。现在我们从另一个角度——信息论——来理解它，这就需要引入KL散度和交叉熵的概念。

### KL散度 (page 13-14)

> [!definition]+ Kullback-Leibler (KL) 散度 (page 13)
>
> KL散度，又称**相对熵（Relative Entropy）**，用于衡量两个概率分布之间的差异。
>
> 对于离散随机变量 $X$ 上的两个概率分布 $P(x)$（真实分布）和 $Q(x)$（模型近似分布），KL散度定义为：
>
> $$
> KL(P||Q) = \sum_x P(x) \log \frac{P(x)}{Q(x)}
> $$

> [!theorem]+ KL散度的性质 (page 14)
>
> 1. **非负性**: $KL(P||Q) \ge 0$。当且仅当 $P=Q$ 时，等号成立。
> 2. **不对称性**: $KL(P||Q) \neq KL(Q||P)$。它不是一个严格意义上的“距离”。
>
> 非负性的证明可以借助**Jensen不等式**[^1]：
>
> $$
> KL(P||Q) = \sum_x P(x) \log \frac{P(x)}{Q(x)} = - \sum_x P(x) \log \frac{Q(x)}{P(x)} \ge -\log\left(\sum_x P(x) \frac{Q(x)}{P(x)}\right) = -\log\left(\sum_x Q(x)\right) = -\log(1) = 0
> $$

[^1]: **Jensen不等式**: 对于凸函数 $f$，有 $E[f(X)] \ge f(E[X])$。在这里，$-\log(x)$ 是一个凸函数。

### 交叉熵 (page 15-16)

> [!definition]+ 交叉熵 (Cross-Entropy)
>
> KL散度可以被分解为：
>
> $$
> \begin{align}
> KL(P||Q) &= \sum_x P(x) (\log P(x) - \log Q(x)) \\
> &= \sum_x P(x)\log P(x) - \sum_x P(x)\log Q(x) \\
> &= -H(P) + H(P, Q)
> \end{align}
> $$
>
> 其中 $H(P) = -\sum_x P(x)\log P(x)$ 是真实分布 $P$ 的**信息熵**，而 $H(P, Q) = -\sum_x P(x)\log Q(x)$ 就是**交叉熵**。
>
> 在机器学习中，真实数据分布 $P$ 是固定的，因此其信息熵 $H(P)$ 是一个常数。我们的目标是让模型分布 $Q$ 尽可能地接近 $P$，即最小化 $KL(P||Q)$。这等价于**最小化交叉熵 $H(P, Q)$**。

> [!note]+ 极大似然与最小化交叉熵的等价性 (page 16)
>
> 让我们回到逻辑斯蒂回归的对数似然函数。最大化对数似然函数 $\max \log L(w)$ 等价于最小化它的负数 $\min (-\log L(w))$：
>
> $$
> \min \left( -\sum_{i=1}^N \left[ y_i \log \pi(x_i) + (1-y_i) \log(1-\pi(x_i)) \right] \right)
> $$
>
> 这个形式正是**交叉熵损失函数（Cross-Entropy Loss）**。其中，$y_i$ 可以看作是样本 $i$ 的真实标签分布（one-hot编码），而 $(\pi(x_i), 1-\pi(x_i))$ 是模型预测的概率分布。
>
> 因此，**对逻辑斯蒂回归进行极大似然估计，本质上就是在最小化模型预测分布与真实标签分布之间的交叉熵。**

## 最大熵模型 (Maximum Entropy Model) (page 17-27)

最大熵模型是另一种强大的对数线性模型，它与逻辑斯蒂回归有着深刻的联系。

> [!extra]- 推荐观看[最大熵对机器学习为什么非常重要？](https://www.bilibili.com/video/BV1cP4y1t7cP)

### 最大熵原理 (page 17-18)

> [!theorem]+ 最大熵原理
>
> 学习概率模型时，在所有满足已知约束条件的模型集合中，选取**熵**最大的模型作为最好的模型。
>
> - **熵的定义**: 对于离散随机变量 $X$ 的概率分布 $P(X)$，其熵为：
>
> $$
> H(P) = - \sum_x P(x) \log P(x)
> $$
>
> - **直观理解**:
>     1. 模型必须满足我们从数据中观测到的所有“事实”（约束条件）。
>     2. 对于未知的部分，我们不做任何主观假设，即使其“最不确定”或“最随机”。
>     3. 熵是衡量“不确定性”或“随机性”的数学指标。熵最大的分布，就是在满足约束的前提下，最均匀、最不偏不倚的分布。

> [!example]+ 抛硬币的例子 (page 19)
>
> 假设一个随机变量有5个取值 $\{A, B, C, D, E\}$。
>
> - **无先验知识**: 唯一的约束是 $\sum P(y_i) = 1$。根据最大熵原理，我们会得到一个均匀分布：$P(A)=P(B)=...=P(E)=1/5$。
> - **加入先验**: 如果我们知道一个事实，比如 $P(A)+P(B)=3/10$。那么在满足 $\sum P(y_i)=1$ 和 $P(A)+P(B)=3/10$ 这两个约束下，最大熵的解是：$P(A)=P(B)=3/20$，$P(C)=P(D)=P(E)=7/30$。在这个解中，A和B是等可能的，C、D、E也是等可能的，体现了在各自小团体内的“最大熵”。
> 
> 我们可以使用最大熵模型来求解，见 slide page 28 。

### 最大熵模型的定义 (page 20-22)

在实际应用中，我们构建最大熵模型来学习条件概率 $P(Y|X)$。

1. **经验分布和特征函数 (page 20)**:
    - 从训练数据 $T = \{(x_1, y_1), \dots, (x_N, y_N)\}$ 中，我们可以计算**经验联合分布** $\tilde{P}(x, y)$ 和**经验边缘分布** $\tilde{P}(x)$。
    - 我们定义**特征函数/指示函数** $f(x, y)$ 来刻画数据中的某些“事实”。它通常是一个二值函数：
        $$
        f(x, y) = \begin{cases} 1, & \text{x 与 y 满足某一事实} \\ 0, & \text{否则} \end{cases}
        $$

2. **约束条件 (page 21)**:
    - 最大熵模型的核心思想是让模型预测的“事实”与我们在训练数据中观测到的“事实”保持一致。这通过匹配**特征函数的期望值**来实现。
    - 特征 $f$ 在**经验分布**下的期望值：$E_{\tilde{P}}(f) = \sum_{x,y} \tilde{P}(x,y)f(x,y)$。
    - 特征 $f$ 在**模型**下的期望值：$E_{P}(f) = \sum_{x,y} \tilde{P}(x)P(y|x)f(x,y)$。
    - 约束就是：$E_{\tilde{P}}(f_i) = E_{P}(f_i)$，对所有我们关心的特征 $f_i$ 成立。

3. **最优化问题 (page 22)**:
    - **目标**: 最大化模型的**条件熵**:
        $$
        H(P) = H(Y|X) = \sum_{x,y} \tilde{P}(x)P(y|x) \log P(y|x)
        $$
    - **约束**:
        $$
        C = \{ P \in \mathcal{P} \mid E_P(f_i) = E_{\tilde{P}}(f_i), \quad i=1, \dots, n \}
        $$

### 最大熵模型的学习与推导 (page 23-27)

我们期望通过调整条件概率 $P(y|x)$ 来构建条件熵最大的模型（即这里的最大熵模型）。这是一个带约束的最优化问题，我们使用**拉格朗日乘子法**来求解。

$$
\begin{aligned}
\max_{P\in C}&H(P)=-\sum_{x,y}\widetilde{P}(x)P(y|x)\log P(y|x)\\
&s.t.E_{\tilde{P}}(f_i)=E_p(f_i),i=1,2,\cdots,n \\
&\sum_yP(y|x)=1\end{aligned}
\implies 
\begin{aligned}
\min_{P\in C}&-H(P)=\sum_{x,y}\widetilde{P}(x)P(y|x)\log P(y|x) \\
&s.t.E_{\tilde{P}}(f_i)-E_P(f_i),=0, i=1,2,\cdots,n\\
&1 - \sum_yP(y|x)=0
\end{aligned}
$$

1. **构建拉格朗日函数**: 将约束最优化问题转化为无约束的对偶问题。
	$$
	\begin{aligned}\mathcal{L}(P,w)&\equiv-H(P)+w_0\left(1-\sum_yP(y|x)\right)+\sum_{i=1}^nw_i(E_{\tilde{P}}(f_i)-E_P(f_i))\\&=\sum_{x,y}\widetilde{P}(x)P(y|x)\log P(y|x)+w_0\left(1-\sum_yP(y|x)\right)\\&+\sum_{i=1}^{n}w_i\left(\sum_{x,y}\widetilde{P}(x,y)f_i(x,y)-\sum_{x,y}\widetilde{P}(x)P(y|x)f_i(x,y)\right)\end{aligned}
	$$

2. **求解对偶问题**:
    - 先对 $P(y|x)$ 求极小值（通过求导并令其为0）。
    - 解得 $P(y|x)$ 具有如下指数形式：
        $$
        P_w(y|x) = \frac{\exp\left(\sum_{i=1}^n w_i f_i(x,y)\right)}{\sum_y \exp\left(\sum_{i=1}^n w_i f_i(x,y)\right)}
        $$
    - 这个形式被称为**对数线性模型**或**Gibbs分布**。$w_i$ 是特征 $f_i$ 的权重（即拉格朗日乘子）。分母 $Z_w(x) = \sum_y \exp(\dots)$ 是归一化因子，也叫**配分函数（Partition Function）**。
3. **再对 $w$ 求极大值**: 得到模型的具体形式后，再求解对偶函数的外部极大化问题，即寻找最优的参数 $w^*$。

> [!extra]+ 最大熵模型与逻辑斯蒂回归的关系
>
> 观察最大熵模型的最终形式，它与多项逻辑斯蒂回归（Softmax回归）的形式是完全一样的！可以证明，当为二分类的逻辑斯蒂回归选择特定的特征函数时，它就等价于一个最大熵模型。它们是“一体两面”的。

### 对偶函数的极大化与极大似然估计的等价性 (page 31-32)

$$
\begin{aligned}L_{\tilde{P}}(P_{w})&=\sum_{x,y}\tilde{P}(x,y)\log P_{w}(y|x)\\
&=\sum_{x,y}\tilde{P}(x,y)\sum_{i=1}^nw_if_i(x,y)-\sum_{x,y}\tilde{P}(x,y)\log Z_w(x\\
&=\sum_{x,y}\tilde{P}(x,y)\sum_{i=1}^nw_if_i(x,y)-\sum_x\tilde{P}(x)\log Z_w(x)\end{aligned}
\iff 
\begin{aligned}\Psi(w)&=\sum_{x,y}\tilde{P}(x)P_w(y|x)\log P_w(y|x)+\\&\sum_{i=1}^nw_i\left(\sum_{x,y}\tilde{P}(x,y)f_i(x,y)-\sum_{x,y}\tilde{P}(x)P_w(y|x)f_i(x,y)\right)\\&=\sum_{x,y}\tilde{P}(x,y)\sum_{i=1}^nw_if_i(x,y)+\sum_{x,y}\tilde{P}(x)P_w(y|x)\left(\log P_w(y|x)-\sum_{i=1}^nw_if_i(x,y)\right)\\&=\sum_{x,y}\tilde{P}(x,y)\sum_{i=1}^nw_if_i(x,y)-\sum_{x,y}\tilde{P}(x)P_w(y|x)\log Z_w(x)\\&=\sum_{x,y}\tilde{P}(x,y)\sum_{i=1}^nw_if_i(x,y)-\sum_x\tilde{P}(x)\log Z_w(x)\end{aligned}
$$

## 模型学习的最优化算法 (page 34-59，考试不涉及)

逻辑斯蒂回归和最大熵模型的学习都归结为以（对数）似然函数为目标函数的最优化问题。由于目标函数是光滑的凸函数，有很多高效的优化算法可以使用。

### 梯度下降/上升法 (page 36-37, 60-63)

> [!tip]+ 梯度下降法 (Gradient Descent)
>
> - **思想**: 梯度是函数值增长最快的方向，负梯度就是函数值下降最快的方向。从一个初始点开始，沿着负梯度方向一小步一小步地迭代，最终会收敛到函数的极小值点。
> - **更新规则**:
>
> $$
> w^{(k+1)} = w^{(k)} - \eta \nabla f(w^{(k)})
> $$
>
> - $\eta$ 是学习率，控制每一步的步长。
> - **梯度上升法**用于求极大值，只需将减号变为加号。
> - **随机梯度下降/上升 (SGD/SGA)**: 每次迭代只用一个样本来计算梯度并更新参数，而不是整个数据集。这大大加快了计算速度，尤其适用于大规模数据集。

### 牛顿法与拟牛顿法 (page 38-49)

梯度下降法只利用了一阶导数信息，收敛速度可能较慢。牛顿法利用二阶导数信息，收敛更快。

> [!tip]+ 牛顿法 (Newton's Method)
>
> - **思想**: 在当前点对目标函数进行二阶泰勒展开，用一个二次曲面来近似原函数，然后直接跳到这个二次曲面的极小点。
> - **更新规则**:
>
> $$
> w^{(k+1)} = w^{(k)} - H_k^{-1} g_k
> $$
>
> - $g_k$ 是梯度，$H_k$ 是**Hessian矩阵**（二阶偏导数矩阵）。
> - **优点**: 收敛速度快（二次收敛）。
> - **缺点**: Hessian矩阵计算量大、存储开销大，求逆更是困难。且要求Hessian矩阵正定，否则可能不收敛。

> [!tip]+ 拟牛顿法 (Quasi-Newton Method)
>
> - **思想**: 为了克服牛顿法的缺点，不再直接计算Hessian矩阵及其逆，而是用一个矩阵来**近似**Hessian矩阵的逆。
> - **核心**: 满足**拟牛顿条件（Secant Equation）**，并通过迭代来更新这个近似矩阵。
> - **著名算法**:
>     - **DFP算法**: 直接更新Hessian的逆矩阵 $G_k$。
>     - **BFGS算法**: 更新Hessian矩阵的近似 $B_k$，被认为是目前最有效的拟牛顿法之一。

### 改进的迭代尺度法 (IIS) (page 50-56)

IIS是专门为最大熵模型设计的一种优化算法。

> [!tip]+ 改进的迭代尺度法 (Improved Iterative Scaling, IIS)
>
> - **思想**: 在每一步迭代中，不是直接优化对数似然函数 $L(w)$，而是寻找并优化它的一个下界函数。通过迭代地提升这个下界，来保证原函数值也是不断增大的。
> - **过程**:
>     1. 寻找 $L(w+\delta) - L(w)$ 的一个易于优化的下界 $A(\delta|w)$。
>     2. 对 $A(\delta|w)$ 的每一维 $\delta_i$ 单独求解，找到使 $A$ 增大的 $\delta_i$。
>     3. 更新 $w \leftarrow w + \delta$，然后重复此过程直到收敛。
> - **求解**: 求解 $\delta_i$ 的方程可能是非线性的，需要用牛顿法等数值方法求解。

在实际应用中，由于BFGS等拟牛顿法具有更好的收敛性和普适性，它们通常是训练逻辑斯蒂回归和最大熵模型的首选。

## 习题

### 习题 6.2

> [!question]
>
> 写出逻辑斯谛回归模型学习的梯度下降算法。

在 logistic 回归模型中，似然函数为 $\prod_{i=1}^N[\pi(x_i)]^{y_i}[1-\pi(x_i)]^{1-y_i}$，

对数似然函数为：

$$
\begin{aligned}
L(w)&=\sum_{i=1}^N[y_i\log\pi(x_i)+(1-y_i)\log(1-\pi(x_i))]\\
&=\sum_{i=1}^N[y_i\log\frac{\pi(x_i)}{1-\pi(x_i)}+\log(1-\pi(x_i))]\\
&=\sum_{i=1}^N[y_i(w\cdot x_i)-\log(1+\exp(w\cdot x_i))]
\end{aligned}
$$

由于梯度下降算法解决的是最小优化问题，所以：

- **逻辑斯谛回归模型学习的梯度下降算法**
	- **输入**：目标函数 $f(w) = -L(w)$，梯度函数 $g(w)= \nabla f(w)$，计算精度 $\varepsilon$
	- **输出**：最优参数 $\hat{w} \Rightarrow$ 最优模型 $P(Y=1|x)=\frac{\exp(\hat{w}\cdot x)}{1+\exp(\hat{w}\cdot x)}$, $P(Y=0|x)=\frac{1}{1+\exp(\hat{w}\cdot x)}$

**算法步骤**：

1. 取初值 $w^{(0)}\in\mathbb{R}^{n+1}$，$k=0$；
2. 计算 $f(w^{(k)})$；
3. 计算梯度 $g_k=g(w^{(k)})$，当 $||g_k||<\varepsilon$ 时，停止迭代，令 $\hat{w}=w^{(k)}$；否则令 $p_k=-g_k$，
   一维搜索：求解 $\lambda_k$ 使 $f(w^{(k)}+\lambda_kp_k)=\min_{\lambda\geq0}f(w^{(k)}+\lambda p_k)$
4. 令 $w^{(k+1)}=w^{(k)}+\lambda_kp_k$，计算 $f(w^{(k+1)})$，
   当 $||f(w^{(k+1)})-f(w^{(k)})||<\varepsilon$ 或 $||w^{(k+1)}-w^{(k)}||<\varepsilon$ 时，
   停止迭代，$\hat{w}=w^{(k+1)}$；
5. 否则，令 $k=k+1$，回到步骤 3。

### 习题 6.3

> [!question]+
>
> 写出最大熵模型的 DFP 算法。

对于最大熵模型：

**目标函数**:

$$
\begin{aligned}
\min_{w\in\mathbb{R}^n}f(w)=\sum_x\tilde{P}(x)\log\sum_y\exp\left(\sum_{i=1}^nw_if_i(x,y)\right)-\sum_{x,y}\tilde{P}(x,y)\sum_{i=1}^nw_if_i(x,y)
\end{aligned}
$$

**梯度**:

$$
\begin{aligned}
g(w)=\left(\frac{\partial f(w)}{\partial w_1},\frac{\partial f(w)}{\partial w_2},\ldots,\frac{\partial f(w)}{\partial w_n}\right)^T
\end{aligned}
$$

**最大熵模型的 DFP 算法**：

- **输入**：特征函数 $f_1,f_2,\cdots,f_n$，目标函数 $f(w)$，梯度 $g(w)=\nabla f(w)$，精度要求 $\varepsilon$
- **输出**：最优参数 $\hat{w}$

**算法步骤**：

1. 选取初始点 $w^{(0)}$，取 $G_0$ 为正定矩阵，一般取单位矩阵，令 $k=0$；
2. 计算 $g_k=g(w^{(k)})$，若 $\|g_k\|<\varepsilon$，则停止计算，得近似解 $\hat{w}=w^{(k)}$；否则进行第 3 步；
3. 计算 $p_k=-G_k g_k$；
4. 一维搜索：求 $\lambda_k$ 使得 $f(w^{(k)}+\lambda_k p_k) = \min_{\lambda \geq 0} f(w^{(k)}+\lambda p_k)$；
5. 计算 $w^{(k+1)}=w^{(k)}+\lambda_k p_k$；
6. 计算 $g_{k+1}=g(w^{(k+1)})$，若 $\|g_{k+1}\|<\varepsilon$，则停止计算，得近似解 $\hat{w}=w^{(k+1)}$；否则按下式求出 $G_{k+1}$：（其中，$y_k=g_{k+1}-g_k, \delta_k=w^{(k+1)}-w^{(k)}$）

$$
\begin{aligned}
G_{k+1}=G_k+\frac{\delta_k\delta_k^T}{\delta_k^T y_k}-\frac{G_k y_k y_k^T G_k}{y_k^T G_k y_k}
\end{aligned}
$$

7. 令 $k=k+1$，回到步骤 3