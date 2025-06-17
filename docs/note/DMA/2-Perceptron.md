# 第二章 感知机

## 感知机模型 (page 2-4)

感知机（Perceptron）是一种简单的人工神经网络，由F. Rosenblatt 于 1957 年提出，它被视为一种最简单的前馈神经网络，本质上是一个二元线性分类器。

感知机的基本思想是：

- **输入**：实例的特征向量。
- **输出**：实例的类别，通常取值为 +1 或 -1。
- **作用**：感知机对应于输入空间中的一个分离超平面，将实例划分为正负两类。它属于判别模型。

### 感知机模型定义 (page 3)

> [!definition]+ 定义 2.1 (感知机)
>
> 假设输入空间（特征空间）是 $X \subseteq \mathbb{R}^n$，输出空间是 $Y = \{+1, -1\}$。输入 $x \in X$ 表示实例的特征向量，对应于输入空间（特征空间）的点；输出 $y \in Y$ 表示实例的类别。由输入空间到输出空间的函数如下：
>
> $$
> f(x) = \text{sign}(w \cdot x + b) \quad (2.1)
> $$
>
> 称为感知机。其中，$w$ 和 $b$ 为感知机模型参数，$w \in \mathbb{R}^n$ 叫作**权值（weight）**或**权值向量（weight vector）**，$b \in \mathbb{R}$ 叫作**偏置（bias）**，$w \cdot x$ 表示 $w$ 和 $x$ 的内积。$\text{sign}$ 是符号函数，即
>
> $$
> \text{sign}(x) = \begin{cases} +1, & x \ge 0 \\ -1, & x < 0 \end{cases}
> $$

### 感知机几何解释 (page 4)

感知机的几何解释是，它对应于特征空间（输入空间）中的一个**分离超平面 $S$**。

- **线性方程**：超平面 $S$ 的方程为 $w \cdot x + b = 0$。
- **法向量与截距**：
    - $w$ 是超平面 $S$ 的法向量（normal vector）。
    - $b$ 是超平面 $S$ 的截距（bias）。
- **分类**：这个超平面将输入空间划分为两个区域，分别对应于正类（+1）和负类（-1）。

## 数据集的线性可分性 (page 5)

线性可分性是感知机算法能够成功收敛的前提。

> [!definition]+ 定义 2.2 (数据集的线性可分性)
>
> 给定一个数据集 $T = \{(x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)\}$，其中 $x_i \in X = \mathbb{R}^n$, $y_i \in Y = \{+1, -1\}$, $i = 1, 2, \dots, N$。如果存在某个超平面 $S: w \cdot x + b = 0$，能够将数据集的正实例点和负实例点完全正确地划分到超平面的两侧，即对所有 $y_i = +1$ 的实例 $i$，有 $w \cdot x_i + b > 0$，对所有 $y_i = -1$ 的实例 $i$，有 $w \cdot x_i + b < 0$，则称数据集 $T$ 为**线性可分数据集（linearly separable data set）**；否则，称数据集 $T$ **线性不可分**。

简单来说，如果一个数据集可以通过一个直线（二维空间）或超平面（高维空间）完全分开，使得不同类别的点分别位于超平面的两侧，那么这个数据集就是线性可分的。

## 感知机学习策略 (page 6-7)

感知机学习的目标是找到一个能够将训练数据集完全正确划分的分离超平面。为了达到这个目标，我们需要定义一个损失函数，并通过优化算法最小化这个损失函数。

### 损失函数的选择 (page 6)

损失函数用于衡量模型的预测值与真实值之间的差距。在感知机中，我们希望找到一个损失函数，能够衡量误分类点的情况。

- **自然选择**：误分类点的数目。
    - **问题**：这个损失函数不是关于 $w, b$ 的连续可导函数，因此不宜通过梯度下降等优化方法进行优化。
- **另一选择**：误分类点到超平面的总距离。
    - 一个点 $(x_0, y_0)$ 到超平面 $w \cdot x + b = 0$ 的距离为：
        $$
        \frac{|w \cdot x_0 + b|}{||w||}
        $$
    - 对于误分类点 $(x_i, y_i)$，其特点是 $-y_i(w \cdot x_i + b) \geq 0$。这是因为：
        - 当 $y_i = +1$ 时，如果被误分类，则 $w \cdot x_i + b \le 0$，所以 $y_i(w \cdot x_i + b) \le 0$，即 $-y_i(w \cdot x_i + b) \ge 0$。
        - 当 $y_i = -1$ 时，如果被误分类，则 $w \cdot x_i + b \ge 0$，所以 $y_i(w \cdot x_i + b) \le 0$，即 $-y_i(w \cdot x_i + b) \ge 0$。
    - 误分类点 $(x_i, y_i)$ 到超平面的距离为：
        $$
        -\frac{1}{||w||} y_i(w \cdot x_i + b)
        $$
    - 所有误分类点到超平面的总距离（忽略 $||w||$，因为不影响优化）：
        $$
        -\sum_{x_i \in M} y_i(w \cdot x_i + b)
        $$
        其中 $M$ 为误分类点的集合。

### 感知机学习的损失函数 (page 7)

给定训练数据集 $T = \{(x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)\}$，其中 $x_i \in X = \mathbb{R}^n$, $y_i \in Y = \{+1, -1\}$, $i = 1, 2, \dots, N$。感知机 $\text{sign}(w \cdot x + b)$ 学习的损失函数定义为：

$$
L(w, b) = - \sum_{x_i \in M} y_i(w \cdot x_i + b) \quad (2.4)
$$

其中 $M$ 为误分类点的集合。

> [!note]+ 损失函数的性质 (page 7)
>
> 1.  **非负性**：损失函数 $L(w, b)$ 是非负的。
> 2.  **最小值**：如果没有误分类点，即 $M$ 为空集，损失函数值为 0。
> 3.  **与分类情况的关系**：误分类点越少，损失函数值越小；误分类点离超平面越近，损失函数值越小。
> 4.  **可导性**：对于一个特定的样本点，当它被误分类时，其损失项 $y_i(w \cdot x_i + b)$ 是参数 $w, b$ 的线性函数。当它被正确分类时，损失项为 0。因此，对于给定的训练数据集 $T$，损失函数 $L(w, b)$ 是关于 $w, b$ 的连续可导函数。这使得我们可以使用梯度下降法进行优化。

## 感知机学习算法 (page 8-16)

感知机学习算法旨在最小化损失函数 $L(w, b)$。这是一个无约束的最优化问题。

### 优化方法：随机梯度下降法 (page 8)

感知机学习算法采用**随机梯度下降法**（Stochastic Gradient Descent, SGD）来优化损失函数。

> [!note]+ 随机梯度下降的步骤 (page 8)
>
> 1.  **初始化**：首先任意选择一个超平面，即选择初始的权值向量 $w$ 和偏置 $b$。
> 2.  **迭代更新**：然后不断极小化目标函数（损失函数 $L(w, b)$）。在每次迭代中：
>    - **计算梯度**：计算损失函数 $L(w, b)$ 对 $w$ 和 $b$ 的梯度：
>        $$
>        \nabla_w L(w, b) = - \sum_{x_i \in M} y_i x_i
>        $$
>        $$
>        \nabla_b L(w, b) = - \sum_{x_i \in M} y_i
>        $$
>    - **选取误分类点**：在训练集中选取一个**误分类点** $(x_i, y_i)$。
>    - **更新参数**：使用梯度下降规则更新 $w$ 和 $b$：
>        $$
>        w \leftarrow w + \eta y_i x_i
>        $$
>        $$
>        b \leftarrow b + \eta y_i
>        $$
>        其中 $\eta$ 是**学习率（learning rate）**，表示每次更新的步长，通常是一个介于 0 到 1 之间的正数（$0 < \eta \le 1$）。
       
### 感知机学习算法的原始形式 (page 10)

> [!tip]+ 算法 2.1 (感知机学习算法的原始形式)
>
> **输入**：训练数据集 $T = \{(x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)\}$，其中 $x_i \in X = \mathbb{R}^n$, $y_i \in Y = \{-1, +1\}$, $i = 1, 2, \dots, N$；学习率 $\eta$ ($0 < \eta \le 1$)；
>
> **输出**：$w, b$；感知机模型 $f(x) = \text{sign}(w \cdot x + b)$.
>
> 1.  选取初值 $w_0, b_0$。
> 2.  在训练集中选取数据 $(x_i, y_i)$。
> 3.  如果 $y_i(w \cdot x_i + b) \le 0$（即 $(x_i, y_i)$ 是一个误分类点），则更新 $w$ 和 $b$：
>    $$
>    w \leftarrow w + \eta y_i x_i
>    $$
>    $$
>    b \leftarrow b + \eta y_i
>    $$
> 4.  转至 (2)，直至训练集中没有误分类点。
>
> **注**：原始形式对应后面介绍的对偶形式。

### 算法讨论 (page 11)

针对算法 2.1，我们需要思考几个问题：
1.  **解是否唯一？** 感知机算法的解不唯一。
2.  **初值对算法的解是否有影响？** 不同的初值会得到不同的解。
3.  **是否收敛？** 对于**线性可分的数据集**，感知机算法是收敛的，即经过有限次迭代后，能够找到一个分离超平面。

### 算法示例 (page 12-16)

通过一个具体例子来演示感知机学习算法的原始形式。

> [!example]+ **例 2.1**：
>
> - 正例：$x_1 = (3, 3)^T$, $x_2 = (4, 3)^T$
>- 负例：$x_3 = (1, 1)^T$

**解**：
我们根据算法 2.1 求解 $w, b$，设定学习率 $\eta = 1$。
1.  **初始化**：取初值 $w_0 = (0, 0)^T$, $b_0 = 0$。
2.  **第一次迭代**：
    - 选取 $x_1 = (3, 3)^T, y_1 = +1$。
    - 计算 $y_1(w_0 \cdot x_1 + b_0) = 1 \cdot ((0, 0) \cdot (3, 3) + 0) = 0$。由于 $0 \le 0$，这是一个误分类点。
    - 更新 $w, b$：
        $w_1 = w_0 + y_1 x_1 = (0, 0)^T + 1 \cdot (3, 3)^T = (3, 3)^T$
        $b_1 = b_0 + y_1 = 0 + 1 = 1$
    - 得到线性模型：$w_1 \cdot x + b_1 = 3x^{(1)} + 3x^{(2)} + 1$。

3.  **第二次迭代**：
    - 检查所有点是否正确分类：
        - 对 $x_1 = (3, 3)^T, y_1 = +1$: $y_1(w_1 \cdot x_1 + b_1) = 1 \cdot (3 \cdot 3 + 3 \cdot 3 + 1) = 19 > 0$。正确分类。
        - 对 $x_2 = (4, 3)^T, y_2 = +1$: $y_2(w_1 \cdot x_2 + b_1) = 1 \cdot (3 \cdot 4 + 3 \cdot 3 + 1) = 22 > 0$。正确分类。
        - 对 $x_3 = (1, 1)^T, y_3 = -1$: $y_3(w_1 \cdot x_3 + b_1) = -1 \cdot (3 \cdot 1 + 3 \cdot 1 + 1) = -7 < 0$。这是一个误分类点。
    - 选取 $x_3 = (1, 1)^T, y_3 = -1$。
    - 更新 $w, b$：
        $w_2 = w_1 + y_3 x_3 = (3, 3)^T + (-1) \cdot (1, 1)^T = (2, 2)^T$
        $b_2 = b_1 + y_3 = 1 + (-1) = 0$
    - 得到线性模型：$w_2 \cdot x + b_2 = 2x^{(1)} + 2x^{(2)}$。

这个过程会继续下去，直到所有点都被正确分类。在附件的例子中，经过多次迭代，最终在 $k=7$ 次更新后（迭代次数从0开始计数，实际更新了7次），得到了最终的参数 $w_7 = (1, 1)^T, b_7 = -3$。

- **最终线性模型**：$w_7 \cdot x + b_7 = x^{(1)} + x^{(2)} - 3$。
- **分离超平面**：$x^{(1)} + x^{(2)} - 3 = 0$。
- **感知机模型**：$f(x) = \text{sign}(x^{(1)} + x^{(2)} - 3)$。

通过这个例子，我们可以得出结论：

- **算法的解不唯一**：不同的误分类点选取顺序可能导致最终得到不同的分离超平面，但它们都能够将数据集正确划分。
- **不同的初值得到的解可能不同**：即使误分类点选取顺序相同，不同的初值也会影响最终的解。
- **算法的收敛性**：对于线性可分数据集，经过有限次迭代，感知机算法一定会收敛，找到一个能将训练数据集完全正确划分的分离超平面及感知机模型。

## 感知机学习算法的收敛性 (page 17-22)

感知机算法的收敛性是一个重要的理论性质，特别是对于线性可分数据集。

### 扩充权重向量 (page 17)

为了简化数学表达，我们可以将偏置 $b$ 并入到权重向量 $w$ 中，形成**扩充权重向量（augmented weight vector）**。

记作：$\hat{w} = (w^T, b)^T$，$\hat{x} = (x^T, 1)^T$。
此时，$\hat{w} \in \mathbb{R}^{n+1}$, $\hat{x} \in \mathbb{R}^{n+1}$。
原始的超平面方程 $w \cdot x + b = 0$ 可以写成扩充形式的内积：
$$
\hat{w} \cdot \hat{x} = w \cdot x + b = 0
$$

### Novikoff 定理 (page 17)

Novikoff 定理（Novikoff's theorem）是感知机算法收敛性的一个重要定理。

> [!theorem]+ 定理 2.1 (Novikoff)
>
> 设训练数据集 $T = \{(x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)\}$ 是线性可分的，其中 $x_i \in X = \mathbb{R}^n$, $y_i \in Y = \{-1, +1\}$, $i = 1, 2, \dots, N$。则：
>
> 1.  存在满足条件 $||\hat{w}_{\text{opt}}|| = 1$ 的超平面 $\hat{w}_{\text{opt}} \cdot \hat{x} = \hat{w}_{\text{opt}} \cdot x + b_{\text{opt}} = 0$ 将训练数据集完全正确分开；且存在 $\gamma > 0$，对所有 $i = 1, 2, \dots, N$，均有
>    $$
>    y_i(\hat{w}_{\text{opt}} \cdot \hat{x}_i) = y_i(\hat{w}_{\text{opt}} \cdot x_i + b_{\text{opt}}) \ge \gamma \quad (2.8)
>    $$
> 2.  令 $R = \max_{1 \le i \le N} ||\hat{x}_i||$，则感知机算法 2.1 在训练数据集上的误分类次数 $k$ 满足不等式
>    $$
>    k \le \left(\frac{R}{\gamma}\right)^2 \quad (2.9)
>    $$
>         

### 收敛性证明 (page 18-21)

> [!proof]- 证明感知机算法的收敛性主要依赖于上述 Novikoff 定理。

**第一部分证明 (1)**：
由于训练数据集是线性可分的，根据定义 2.2，存在一个超平面可以将训练数据完全正确分开。我们可以选取这样一个分离超平面，使其对应的扩充权重向量为 $\hat{w}_{\text{opt}}$，并且满足 $||\hat{w}_{\text{opt}}|| = 1$（可以通过对任意分离超平面的法向量进行归一化实现）。

由于所有样本点都能被正确分类，对于任意样本 $(x_i, y_i)$，均有 $y_i(w_{\text{opt}} \cdot x_i + b_{\text{opt}}) > 0$。
由于数据集是有限的，我们可以找到一个最小的正值 $\gamma$，使得：
$$
\gamma = \min_i \{y_i(\hat{w}_{\text{opt}} \cdot \hat{x}_i)\} > 0
$$
因此，对于所有 $i$，都有 $y_i(\hat{w}_{\text{opt}} \cdot \hat{x}_i) \ge \gamma$。

**第二部分证明 (2)**：
我们来推导两个重要的不等式 (2.12) 和 (2.13)。
假设感知机算法从 $\hat{w}_0 = 0$ 开始迭代。如果第 $k$ 个误分类实例是 $(x_i, y_i)$，那么在第 $k$ 次更新之前，扩充权重向量为 $\hat{w}_{k-1}$。此时误分类的条件是 $y_i(\hat{w}_{k-1} \cdot \hat{x}_i) \le 0$ (2.10)。
根据更新规则，新的扩充权重向量为：
$$
\hat{w}_k = \hat{w}_{k-1} + \eta y_i \hat{x}_i \quad (2.11)
$$

**首先证明 (2.12)**：
考虑 $\hat{w}_k$ 与 $\hat{w}_{\text{opt}}$ 的内积：
$$
\hat{w}_k \cdot \hat{w}_{\text{opt}} = (\hat{w}_{k-1} + \eta y_i \hat{x}_i) \cdot \hat{w}_{\text{opt}}
$$
$$
= \hat{w}_{k-1} \cdot \hat{w}_{\text{opt}} + \eta y_i (\hat{x}_i \cdot \hat{w}_{\text{opt}})
$$
根据 (2.8) 式，我们知道 $y_i(\hat{w}_{\text{opt}} \cdot \hat{x}_i) \ge \gamma$，因此 $\eta y_i (\hat{x}_i \cdot \hat{w}_{\text{opt}}) \ge \eta \gamma$。
所以，
$$
\hat{w}_k \cdot \hat{w}_{\text{opt}} \ge \hat{w}_{k-1} \cdot \hat{w}_{\text{opt}} + \eta \gamma
$$
这是一个递推关系。由于初始 $\hat{w}_0 = 0$，我们可以递推得到：
$$
\hat{w}_k \cdot \hat{w}_{\text{opt}} \ge \hat{w}_{k-1} \cdot \hat{w}_{\text{opt}} + \eta \gamma \ge \hat{w}_{k-2} \cdot \hat{w}_{\text{opt}} + 2 \eta \gamma \ge \dots \ge k \eta \gamma \quad (2.12)
$$

**接着证明 (2.13)**：
考虑 $|| \hat{w}_k ||^2$：
$$
||\hat{w}_k||^2 = ||\hat{w}_{k-1} + \eta y_i \hat{x}_i||^2
$$
$$
= ||\hat{w}_{k-1}||^2 + 2 \eta y_i (\hat{w}_{k-1} \cdot \hat{x}_i) + \eta^2 ||y_i \hat{x}_i||^2
$$
由于 $y_i^2 = 1$，所以 $||y_i \hat{x}_i||^2 = ||\hat{x}_i||^2$。
又因为 $(x_i, y_i)$ 是一个误分类点，根据 (2.10) 式，$y_i(\hat{w}_{k-1} \cdot \hat{x}_i) \le 0$。
所以，
$$
||\hat{w}_k||^2 \le ||\hat{w}_{k-1}||^2 + \eta^2 ||\hat{x}_i||^2
$$
根据 $R = \max_{1 \le i \le N} ||\hat{x}_i||$，有 $||\hat{x}_i||^2 \le R^2$。
因此，
$$
||\hat{w}_k||^2 \le ||\hat{w}_{k-1}||^2 + \eta^2 R^2
$$
同样是递推关系，由于初始 $\hat{w}_0 = 0$，可以递推得到：
$$
||\hat{w}_k||^2 \le ||\hat{w}_{k-1}||^2 + \eta^2 R^2 \le ||\hat{w}_{k-2}||^2 + 2\eta^2 R^2 \le \dots \le k \eta^2 R^2 \quad (2.13)
$$

**最后结合 (2.12) 和 (2.13)**：
利用柯西-施瓦茨不等式（Cauchy-Schwarz inequality）：$|\hat{w}_k \cdot \hat{w}_{\text{opt}}| \le ||\hat{w}_k|| \cdot ||\hat{w}_{\text{opt}}||$。
由于 $||\hat{w}_{\text{opt}}|| = 1$，且 $\hat{w}_k \cdot \hat{w}_{\text{opt}} \ge k \eta \gamma > 0$（因为 $k, \eta, \gamma$ 都是正数），所以 $\hat{w}_k \cdot \hat{w}_{\text{opt}} = |\hat{w}_k \cdot \hat{w}_{\text{opt}}|$。
因此，
$$
k \eta \gamma \le \hat{w}_k \cdot \hat{w}_{\text{opt}} \le ||\hat{w}_k|| \cdot ||\hat{w}_{\text{opt}}|| = ||\hat{w}_k||
$$
结合 (2.13) 式，我们有 $|| \hat{w}_k || \le \sqrt{k \eta^2 R^2} = \eta R \sqrt{k}$。
所以，
$$
k \eta \gamma \le \eta R \sqrt{k}
$$
两边平方（因为都是正数）：
$$
k^2 \eta^2 \gamma^2 \le k \eta^2 R^2
$$
由于 $k > 0$ 且 $\eta > 0$，可以两边同除以 $k \eta^2$：
$$
k \gamma^2 \le R^2
$$
最终得到误分类次数 $k$ 的上界：
$$
k \le \left(\frac{R}{\gamma}\right)^2
$$

### 收敛性定理的结论 (page 22)

上述收敛性定理表明：

- **误分类次数有上界**：当训练数据集是线性可分时，感知机学习算法原始形式的迭代次数 $k$ 是有上界的。这意味着算法会在有限次迭代后收敛。
- **多解性与依赖性**：感知机算法存在许多解，这些解：
    - **依赖于初值**：不同的初始 $w, b$ 会导致找到不同的分离超平面。
    - **依赖于误分类点的选择顺序**：在每次迭代中，如果存在多个误分类点，选择不同的点进行更新，也会影响最终找到的分离超平面。
- **寻求唯一分离超平面**：如果需要得到一个唯一的、最好的分离超平面，需要增加额外的约束条件，例如支持向量机（Support Vector Machine, SVM）就是在此基础上发展起来的，它寻找间隔最大的分离超平面。
- **线性不可分数据集**：如果数据集是线性不可分的，感知机算法的迭代将会震荡，无法收敛到一个确定的分离超平面。在这种情况下，需要使用其他模型，如软间隔支持向量机或多层感知机。

## 感知机学习算法的对偶形式 (page 23-27)

感知机学习算法除了原始形式外，还有其对偶形式。对偶形式的基本想法是将权重向量 $w$ 和偏置 $b$ 表示为实例 $x_i$ 和标记 $y_i$ 的线性组合的形式，通过求解其系数来求得 $w$ 和 $b$。

### 基本思想 (page 23)

在原始形式中，每次遇到一个误分类点 $(x_i, y_i)$，我们更新 $w$ 和 $b$：
$$
w \leftarrow w + \eta y_i x_i
$$
$$
b \leftarrow b + \eta y_i
$$
这意味着，最终的 $w$ 和 $b$ 可以表示为所有参与更新的误分类点 $(x_j, y_j)$ 的加权和。

设某个实例 $(x_j, y_j)$ 由于误分类而进行更新的次数为 $\alpha_j$。如果学习率 $\eta=1$，那么最终的 $w$ 和 $b$ 可以写成：
$$
w = \sum_{j=1}^N \alpha_j y_j x_j
$$
$$
b = \sum_{j=1}^N \alpha_j y_j
$$
其中，$\alpha_j \ge 0$ 是非负整数，表示第 $j$ 个实例点被误分类的次数。当 $\eta=1$ 时，$\alpha_j$ 就是第 $j$ 个实例点由于误分类而进行更新的次数。

### 对偶形式算法 (page 24)
 
> [!tip]+ 算法 2.2 (感知机学习算法的对偶形式)
>
> **输入**：线性可分的数据集 $T = \{(x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)\}$，其中 $x_i \in \mathbb{R}^n, y_i \in \{-1, +1\}, i = 1, 2, \dots, N$；学习率 $\eta$ ($0 < \eta \le 1$)；
>
> **输出**：$\alpha, b$；感知机模型 $f(x) = \text{sign}\left(\sum_{j=1}^N \alpha_j y_j x_j \cdot x + b\right)$，其中 $\alpha = (\alpha_1, \alpha_2, \dots, \alpha_N)^T$。
>
> 1.  初始化 $\alpha \leftarrow 0, b \leftarrow 0$。
> 2.  在训练集中选取数据 $(x_i, y_i)$。
> 3.  如果 $y_i \left(\sum_{j=1}^N \alpha_j y_j x_j \cdot x_i + b\right) \le 0$（即 $(x_i, y_i)$ 是一个误分类点），则更新 $\alpha_i$ 和 $b$：
>    $$
>    \alpha_i \leftarrow \alpha_i + \eta
>    $$
>    $$
>    b \leftarrow b + \eta y_i
>    $$
> 4.  转至 (2)，直至训练集中没有误分类数据。

### 对偶形式的优点 (page 25)

对偶形式的主要优点是：

- **计算效率**：在对偶形式中，我们不需要直接计算和更新 $w$ 向量，而是更新 $\alpha_i$。在进行判别 $y_i(\sum \alpha_j y_j x_j \cdot x_i + b)$ 时，内积 $x_j \cdot x_i$ 可以预先计算并存储在一个矩阵中，这个矩阵就是**Gram 矩阵（Gram matrix）**。
    - Gram 矩阵 $G = [x_i \cdot x_j]_{N \times N}$。
    - 在每次迭代中，只需要查找 Gram 矩阵中对应的内积值，可以加速计算，特别是当数据维度很高时。

### 对偶形式算法示例 (page 26-27)

继续使用例 2.1 的数据来演示对偶形式算法。

**例 2.2**：数据与例 2.1 相同：正例 $x_1 = (3, 3)^T, x_2 = (4, 3)^T$，负例 $x_3 = (1, 1)^T$。学习率 $\eta = 1$。

1.  **初始化**：$\alpha = (0, 0, 0)^T, b = 0$。

2.  **计算 Gram 矩阵**：
    - $x_1 \cdot x_1 = 3 \cdot 3 + 3 \cdot 3 = 18$
    - $x_1 \cdot x_2 = 3 \cdot 4 + 3 \cdot 3 = 21$
    - $x_1 \cdot x_3 = 3 \cdot 1 + 3 \cdot 1 = 6$
    - $x_2 \cdot x_2 = 4 \cdot 4 + 3 \cdot 3 = 25$
    - $x_2 \cdot x_3 = 4 \cdot 1 + 3 \cdot 1 = 7$
    - $x_3 \cdot x_3 = 1 \cdot 1 + 1 \cdot 1 = 2$
    Gram 矩阵 $G = [x_i \cdot x_j]_{3 \times 3}$：
    $$
    G = \begin{bmatrix}
    18 & 21 & 6 \\
    21 & 25 & 7 \\
    6 & 7 & 2
    \end{bmatrix}
    $$

3.  **迭代过程**：
    
    迭代过程与原始形式类似，只是更新参数从 $w, b$ 变为 $\alpha, b$。
    每次选取一个误分类点 $(x_i, y_i)$，根据公式 $y_i \left(\sum_{j=1}^N \alpha_j y_j (x_j \cdot x_i) + b\right) \le 0$ 判断是否误分类。如果误分类，则更新 $\alpha_i \leftarrow \alpha_i + \eta$ 和 $b \leftarrow b + \eta y_i$。

    例如，初始时 $k=0$，$\alpha=(0,0,0)^T, b=0$。
    选取 $x_1=(3,3)^T, y_1=+1$。
    计算 $y_1(\sum \alpha_j y_j (x_j \cdot x_1) + b) = 1 \cdot (0 + 0) = 0 \le 0$，误分类。
    更新 $\alpha_1 \leftarrow \alpha_1+1 = 1$, $b \leftarrow b+y_1 = 0+1=1$。
    此时 $\alpha=(1,0,0)^T, b=1$。

    这个过程会一直迭代，直到没有误分类点。最终得到的结果与原始形式一致：
    - 最终的 $\alpha = (2, 0, 5)^T, b = -3$。
    - 此时可以计算出最终的 $w$ 和 $b$：
        $w = \alpha_1 y_1 x_1 + \alpha_2 y_2 x_2 + \alpha_3 y_3 x_3$
        $w = 2 \cdot (+1) \cdot (3, 3)^T + 0 \cdot (+1) \cdot (4, 3)^T + 5 \cdot (-1) \cdot (1, 1)^T$
        $w = (6, 6)^T + (0, 0)^T + (-5, -5)^T = (1, 1)^T$
        $b = \alpha_1 y_1 + \alpha_2 y_2 + \alpha_3 y_3 = 2 \cdot (+1) + 0 \cdot (+1) + 5 \cdot (-1) = 2 - 5 = -3$
    - 分离超平面：$x^{(1)} + x^{(2)} - 3 = 0$。
    - 感知机模型：$f(x) = \text{sign}(x^{(1)} + x^{(2)} - 3)$。

**结论**：对偶形式与原始形式的结果一致，迭代步骤也是互相对应的。与原始形式一样，感知机学习算法的对偶形式也是收敛的，并且存在多个解。

---

## 习题

### 习题 2.1

> [!question]+ 2.1
>
> Minsky 与 Papert 指出：感知机因为是线性模型，所以不能表示复杂的函数,如异或(XOR)。验证感知机为什么不能表示异或。

根据异或（XOR）的定义，$\oplus$ 运算真值表如下：

| $x_{1}$ | $x_{2}$ | $x_{1} \oplus x_{2}$ |
|:-------:|:-------:|:--------------------:|
| 0       | 0       | 0                    |
| 0       | 1       | 1                    |
| 1       | 0       | 1                    |
| 1       | 1       | 0                    |

在以 $(x_{1}, x_{2})$ 为基的二维空间中作图：

<div style="text-align: center;"><img src="https://raw.githubusercontent.com/darstib/public_imgs/utool/tuchuang/17408187980341740818797248.png" alt="img" style="width: 50%;"><p></p></div>

```python title="xor function"
import matplotlib.pyplot as plt

X = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y = [0, 1, 1, 0]

class_0_x = [X[i][0] for i in range(len(X)) if Y[i] == 0]
class_0_y = [X[i][1] for i in range(len(X)) if Y[i] == 0]
class_1_x = [X[i][0] for i in range(len(X)) if Y[i] == 1]
class_1_y = [X[i][1] for i in range(len(X)) if Y[i] == 1]

plt.figure(figsize=(6, 5))
plt.scatter(class_0_x, class_0_y, color="red", marker="o", label="XOR = 0")
plt.scatter(class_1_x, class_1_y, color="blue", marker="x", label="XOR = 1")

plt.plot(
    [-0.4, 1.5], [1.8, 0.5], linestyle="--", color="gray", label="try 1"
) 
plt.plot(
    [-0.6, 1.5], [-1.5, 1.5], linestyle="--", color="lightgray", label="try 2"
) 
plt.plot(
    [-0.5, 1.2], [-0.2, 1.2], linestyle="--", color="darkgray", label="try 3"
) 

plt.xlim(-0.2, 1.2)
plt.ylim(-0.2, 1.2)
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("XOR function")
plt.legend()
plt.grid(True)
plt.show()

```

我们可以直觉上发现无法用一个超平面（在这里是一条二维平面上的直线）将两类样本完全分开，可以认为异或问题是线性不可分的（反证法如下）。而感知机是线性模型，因此感知机不能够表示异或。

> [!proof] 反证法：感知机不能够表示异或

依据课本定义，我们构建简单的感知机模型如下：
 
$f(x)=sign(wx+b)$，其中 $sign(x)=\begin{cases}+1, & x\geq 0 \\ -1, & x<0\end{cases}$ 。假设感知机能够表示异或，
 
$$\begin{aligned}&1.\text{ 根据}x_1=0,x_2=0,f(x)=0\text{,则}w\cdot x+b<0\text{,可得}b<0\text{;}\\
&2.\text{ 根据}x_1=0,x_2=1,f(x)=1\text{,则}w_2+b>0\text{,结合}b<0\text{,可得}w_2>-b>0;\\
&3.\text{ 根据}x_1=1,x_2=0,f(x)=1\text{,则}w_1+b>0\text{,结合}b<0\text{,可得}w_1>-b>0;\\
&4.\text{ 根据}x_1=1,x_2=1\text{,并结合}w_1+b>0\text{、}w_2 > 0\text{,则}w_1+w_2+b>0 \implies f(x)=1，\text{矛盾。}\end{aligned}$$
 
因此假设不成立，感知机不能够表示异或。

### 习题 2.3

> [!question] 2.3
>
> 证明以下定理：样本集线性可分的充分必要条件是正实例点集所构成的凸壳与负实例点集所构成的凸壳互不相交。

> [!definition] 凸壳的定义
>
> 设集合 $S \subset R^n$，是由 $R^n$ 中的k个点所组成的集合，即 $S={x1_​,x_2​,⋯,x_k​}$。定义 S 的凸壳 conv(S)为：
> 
> $$\mathrm{conv}(S)=\left\{x=\sum_{i=1}^k\lambda_ix_i\right|\sum_{i=1}^k\lambda_i=1,\lambda_i\geqslant0,i=1,2,\cdots,k\}$$
> 
>> [!help]
>> 
>> 依据我的直观理解，**凸壳**中的元素是原集合中的向量张成空间的一小部分。由于权重之和为 1，（如果将这些元素视为有质量物体，根据质心可分布的位置）结合二维空间不难发现这个**一小部分**应该是所有元素在欧式空间中分布后，两两直线相连后所能包裹的最大空间，且一定是一个凸多面（形）体，我想这也是其称为 **凸壳**的原因。

记 S 中正实例子集为 $S_{+}$，负实例子集为 $S_{-}$, $g(x)=wx+b$。
#### 必要性（线性可分 => 凸壳不相交）

对于线性可分的数据集合，存在一个超平面 $wx+b=0$ 完全分离 $S_{+},S_{-}$ 。记 $g(x) = wx+b$，则：

$$
\begin{align}
&\forall s_{+} \in conv(S_{+}):g(s_{+i})>0, \lambda_{i}>0 \\
&ws_{+} = w \sum_{i=1}^{|S_{+}|}\lambda _{i}s_{+i} \\
& =\sum_{i=1}^{|S_{+}|} \lambda _{i}(g(s_{+i})-b) \\
& =(\sum_{i=1}^{|S_{+}|} \lambda _{i}g(s_{+i})) - b \\
\end{align}
\implies g(s_{+}) = ws_{+}+b = \sum_{i=1}^{|S_{+}|} \lambda _{i}g(s_{+i}) > 0
$$

同理可得 $\forall s_{-} \in S_{-}, g(s_{-}) = ws_{-}+b < 0$ 。

> [!proof] 线性可分 => 凸壳不相交

假设存在 $s \in S_{+} \cap S_{-}$，那么 $s \in S_{+} \land s \in S_{-} \implies g(s)>0 \land g(s)<0$，显然矛盾，假设不成立，故凸壳不相交。

#### 充分性（凸壳不相交 => 线性可分）

依照前文中 **help** 部分的分析，记两个凸多面体中最近的两个点连线 L 中点 O ，不难想象过 O 且垂直于 L 的超平面 f 一定能够将两个凸多面体分开（事实上应该能够取得很多个，中点最为特别而已），具体证明如下：

> [!proof] 凸壳不相交 => 线性可分

**假设：** 任意两点之间的距离定义为 $d(x_{1}, x_{2})=||x_{1}-x_{2}||_{2}$，两凸壳之间的距离视为距离最近的一对点（分别属于两个凸壳）之间的距离，即 

$$d(conv(S_{+}), conv(S_{-})) = min||s_{+}-s_{-}|| = ||s_{+m}-s_{-m}||, s_{+m}\in S_{+}, s_{-m}\in S_{-}$$

依照上面的猜想，我们取 $s_{+m}$ 与 $s_{-m}$ 连线 L 的中点 O，过 O 取垂直于 L 的平面 $\alpha$：

$$
\begin{cases} \alpha \perp L\\O \in \alpha \end{cases}
\implies \alpha : (x_{+}-x_{-})^T\left( x - \frac{x_{+}-x_{-}}{2} \right) = 0
\implies \begin{cases}
w = (x_{+}-x_{-})^T \\
b = -\frac12(x_{+}-x_{-})^2
\end{cases}
$$

下证 $\alpha$ 能够分开 $S_{+}, S_{-}$ ：

由于凸壳不相交，又基于 $x_{+m},x_{-m}$ 的定义，我们得到：

$$
\begin{cases}
\forall s_{+} \in S_{+}, d(s_{+}, x_{+m}) < d(s_{+}, x_{-m}) \\
\forall s_{-} \in S_{-}, s(s_{-}, x_{+m}) > d(s_{-}, x_{-m})
\end{cases}
$$

所以：$\forall s_{+} \in S_{+}$，（记 $f(x) = (x_{+}-x_{-})^T\left( x - \frac{x_{+}-x_{-}}{2} \right)$ ）有：

$$
f(s_{+}) = \frac{||x - x_{-}||^2 - ||x-x_{+}||^2}{2} = \frac{d(x, x_{-}) - d(x, x_{+})}{2} > 0
$$

同理可得 $\forall s_{-}\in S_{-}, f(s_{-})<0$ ，因此存在超平面 $\alpha$ 能分离 $S_{+}, S_{-}$ ，充分性得证。

综上所述，样本集线性可分的充分必要条件是正实例点集所构成的凸壳与负实例点集所构成的凸壳互不相交。

