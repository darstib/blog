奇异值分解 (Singular Value Decomposition, SVD) 是线性代数中一种极其重要的矩阵分解方法，在机器学习、数据挖掘、信号处理和统计学等领域有着广泛的应用。它能将一个任意形状的实矩阵分解为三个具有特殊性质的矩阵的乘积。

## 特征分解/谱分解 (page 3-5)

在深入了解奇异值分解之前，我们首先需要回顾一下**特征分解**（也称为**谱分解**），因为 SVD 可以看作是特征分解在任意矩阵上的推广。

### 特征值与特征向量 (page 3)

> [!definition]+ 定义：特征值与特征向量
>
> 对于一个给定的 $N \times N$ 方阵 $A$，如果存在一个标量 $\lambda$ 和一个非零的 $N$ 维向量 $v$，使得以下关系成立：
>
> $$
> Av = \lambda v
> $$
>
> 那么，我们称 $\lambda$ 为矩阵 $A$ 的一个**特征值** (Eigenvalue)，称 $v$ 为对应于特征值 $\lambda$ 的**特征向量** (Eigenvector)。
>
> ---
> **几何意义**：
> 矩阵 $A$ 对其特征向量 $v$ 的线性变换，效果仅仅是对向量 $v$ 进行了一个标量 $\lambda$ 倍的缩放，而没有改变其方向。

为了求解特征值，我们可以将上式改写为 $(A - \lambda I)v = 0$，其中 $I$ 是单位矩阵。由于 $v$ 是非零向量，这要求矩阵 $(A - \lambda I)$ 是奇异的，即它的行列式为 0。

$$
P(\lambda) = \det(A - \lambda I) = 0
$$

这个方程被称为矩阵 $A$ 的**特征多项式** (Characteristic Polynomial)，它的解就是矩阵 $A$ 的所有特征值。

### 特征分解 (page 4)

> [!theorem]+ 定理：特征分解
>
> 如果一个 $N \times N$ 的方阵 $A$ 拥有 $N$ 个线性无关的特征向量 $q_i$ ($i = 1, \dots, N$)，那么矩阵 $A$ 是**可对角化**的，并且可以被分解为：
>
> $$
> A = Q \Lambda Q^{-1}
> $$
>
> 其中：
> - $Q$ 是一个 $N \times N$ 的方阵，其第 $i$ 列是 $A$ 的特征向量 $q_i$。
> - $\Lambda$ 是一个对角矩阵，其对角线上的元素 $\Lambda_{ii} = \lambda_i$ 是与特征向量 $q_i$ 对应的特征值。
>
> ---
> **特殊情况**：
> 如果 $A$ 是一个**实对称矩阵**，那么它的特征向量是相互正交的。此时，矩阵 $Q$ 是一个**正交矩阵**[^1]，满足 $Q^{-1} = Q^T$。分解形式变为：
>
> $$
> A = Q \Lambda Q^T
> $$

> [!attention]+
>
> **只有可对角化的矩阵才能进行特征分解**。一个矩阵可对角化的充分必要条件是它有 $N$ 个线性无关的特征向量。所有对称矩阵都可对角化，但并非所有方阵都可对角化。

#### 示例 (page 5)

- **可对角化矩阵**:
    矩阵 $A = \begin{bmatrix} 1 & 0 \\ 1 & 3 \end{bmatrix}$ 是可对角化的。可以找到一个可逆矩阵（由其特征向量构成）来完成对角化。

- **不可对角化矩阵**:
    矩阵 $\begin{bmatrix} 3 & 1 \\ 0 & 3 \end{bmatrix}$ 是一个典型的不可对角化矩阵。它只有一个特征值 $\lambda=3$，但对应的特征向量空间维度仅为 1，找不到两个线性无关的特征向量。

## 奇异值分解的定义与性质 (page 6-12)

特征分解非常强大，但它有两大局限：

1.  必须作用于方阵。
2.  该方阵必须是可对角化的。

**奇异值分解 (SVD)** 则突破了这些限制，它可以对**任何形状**的矩阵（$m \times n$）进行分解。

### 定义 (page 6-7)

> [!definition]+ 定义 15.1：奇异值分解 (SVD)
>
> 对于任意一个非零的 $m \times n$ 实矩阵 $A \in \mathbb{R}^{m \times n}$，它可以被分解为三个实矩阵的乘积：
>
> $$
> A = U \Sigma V^T \quad (15.1)
> $$
>
> 其中：
> - $U$ 是一个 $m \times m$ 的**正交矩阵** ($U^T U = I_m$)。
> - $V$ 是一个 $n \times n$ 的**正交矩阵** ($V^T V = I_n$)。
> - $\Sigma$ 是一个 $m \times n$ 的**矩形对角矩阵**，其对角线上的元素 $\sigma_i$ 称为**奇异值** (Singular Value)，它们非负且按降序排列：
>
> $$
> \begin{align}
> &\Sigma = \text{diag}(\sigma_1, \sigma_2, \dots, \sigma_p) \\
> &\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_p \ge 0 \\
> &p = \min(m, n)
> \end{align}
> $$
>
> ---
> **核心术语**：
> - $U\Sigma V^T$：矩阵 $A$ 的**奇异值分解**。
> - $\sigma_i$：矩阵 $A$ 的**奇异值**。
> - $U$ 的列向量：**左奇异向量** (Left Singular Vectors)。
> - $V$ 的列向量：**右奇异向量** (Right Singular Vectors)。

> [!note]+ 推广
> SVD 是特征分解对任意矩阵的推广。对于一个正定对称矩阵而言，其 SVD 和特征分解是相同的。对于其他矩阵，SVD 和特征分解则有很大不同。

### 示例 (page 8-11)

给定一个 $5 \times 4$ 矩阵 $A$：

$$
A = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 0 & 4 \\
0 & 3 & 0 & 0 \\
0 & 0 & 0 & 0 \\
2 & 0 & 0 & 0
\end{bmatrix}
$$

它的奇异值分解 $A = U\Sigma V^T$ 由以下矩阵给出：

$$
U = \begin{bmatrix}
0 & 0 & \sqrt{0.2} & 0 & \sqrt{0.8} \\
1 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 \\
0 & 0 & \sqrt{0.8} & 0 & -\sqrt{0.2}
\end{bmatrix}_{5 \times 5}
\quad
\Sigma = \begin{bmatrix}
4 & 0 & 0 & 0 \\
0 & 3 & 0 & 0 \\
0 & 0 & \sqrt{5} & 0 \\
0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0
\end{bmatrix}_{5 \times 4}
\quad
V^T = \begin{bmatrix}
0 & 0 & 0 & 1 \\
0 & 1 & 0 & 0 \\
1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0
\end{bmatrix}_{4 \times 4}
$$

- **矩阵 $\Sigma$** 是一个矩形对角矩阵，对角线元素 (4, 3, $\sqrt{5}$, 0) 是非负且降序排列的奇异值。
- **矩阵 $U$ 和 $V$** 都是正交矩阵，满足 $UU^T = I_5$ 和 $VV^T = I_4$。
- **SVD 的不唯一性**：奇异值 $\sigma_i$ 是唯一的，但左右奇异向量不是。例如，可以同时改变一对左右奇异向量的符号 ($u_i \to -u_i$, $v_i \to -v_i$)，分解依然成立。或者，当有重复的奇异值时，对应的奇异向量可以在它们张成的子空间内任意旋转。

### 奇异值分解基本定理 (page 12)

> [!theorem]+ SVD 基本定理
>
> 若 $A$ 为一 $m \times n$ 实矩阵 ($A \in \mathbb{R}^{m \times n}$)，则 $A$ 的奇异值分解存在：
>
> $$
> A = U\Sigma V^T
> $$
>
> 其中 $U$ 是 $m$ 阶正交矩阵，$V$ 是 $n$ 阶正交矩阵，$\Sigma$ 是 $m \times n$ 矩形对角矩阵，其对角线元素非负，且按降序排列。

## 奇异值分解的计算 (page 13-24 & 41-53)

我们可以通过构造 $U, \Sigma, V$ 的方式来证明 SVD 的存在性，这个过程本身也揭示了如何计算 SVD。

> [!tip]+ SVD 计算算法
>
> **核心思想**：将 SVD 与**对称矩阵的特征分解**联系起来。
>
> 从 $A=U\Sigma V^T$ 出发，我们可以推导出：
>
> $$
> A^T A = (V\Sigma^T U^T)(U\Sigma V^T) = V(\Sigma^T\Sigma)V^T
> $$
>
> $$
> A A^T = (U\Sigma V^T)(V\Sigma^T U^T) = U(\Sigma\Sigma^T)U^T
> $$
>
> 这两个式子是两个标准的**特征分解**！
> - $A^T A$ 是一个 $n \times n$ 的对称矩阵。它的特征向量构成了**右奇异向量矩阵 $V$**。
> - $AA^T$ 是一个 $m \times m$ 的对称矩阵。它的特征向量构成了**左奇异向量矩阵 $U$**。
> - $A^T A$ 和 $AA^T$ 的非零特征值是相同的，它们的平方根就是**奇异值 $\sigma_i$**。
>
> **计算步骤概览 (以 $A^T A$ 为例，假设 $m \geq n$):**
>
> 1.  **构造 $V$ 和 $\Sigma$**:
>     a. 计算 $n \times n$ 对称矩阵 $W = A^T A$。
>     
>     b. 求解 $W$ 的特征值 $\lambda_1, \dots, \lambda_n$ 和对应的特征向量 $v_1, \dots, v_n$。
>     
>     c. 特征值均为非负数[^2]。将它们降序排列：$\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n \ge 0$。
>     
>     d. 将单位化的特征向量 $v_i$ 作为列，构成正交矩阵 $V = [v_1 \ v_2 \ \dots \ v_n]$。
>     
>     e. 计算奇异值 $\sigma_i = \sqrt{\lambda_i}$。用它们构成 $m \times n$ 矩形对角矩阵 $\Sigma$。
> 2.  **构造 $U$**:
>     a. 对于前 $r$ 个正奇异值（其中 $r=\text{rank}(A)$），计算对应的左奇异向量：
>
>        $$
>        u_j = \frac{1}{\sigma_j}Av_j, \quad j=1, 2, \dots, r
>        $$
>
>     b. 这 $r$ 个向量 $u_j$ 构成了 $U$ 的前 $r$ 列 $U_1$。它们是标准正交的。
>     c. 如果 $m > r$，则需要找到另外 $m-r$ 个标准正交向量来扩充 $U_1$，使其成为一个完整的 $m \times m$ 正交矩阵 $U$。这些补充的向量构成了 $A^T$ 的零空间 $N(A^T)$ 的一组标准正交基。
>
> 3.  **得到分解**:
>     最终得到 $A = U\Sigma V^T$。

> [!example]- 计算示例 (page 46-52)

我们来计算矩阵 $A = \begin{bmatrix} 1 & 1 \\ 2 & 2 \\ 0 & 0 \end{bmatrix}$ 的 SVD。

1.  **求 $A^TA$ 的特征值和特征向量**
    $$
    W = A^T A = \begin{bmatrix} 1 & 2 & 0 \\ 1 & 2 & 0 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 2 & 2 \\ 0 & 0 \end{bmatrix} = \begin{bmatrix} 5 & 5 \\ 5 & 5 \end{bmatrix}
    $$
    特征方程为 $\det(W - \lambda I) = (5-\lambda)^2 - 25 = \lambda^2 - 10\lambda = 0$，解得特征值 $\lambda_1=10, \lambda_2=0$。

2.  **求正交矩阵 $V$**
    - 对于 $\lambda_1 = 10$，解 $(W - 10I)x=0$ 得特征向量 $x = \begin{bmatrix} c \\ c \end{bmatrix}$。单位化后取 $v_1 = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix}$。
    - 对于 $\lambda_2 = 0$，解 $(W - 0I)x=0$ 得特征向量 $x = \begin{bmatrix} c \\ -c \end{bmatrix}$。单位化后取 $v_2 = \begin{bmatrix} 1/\sqrt{2} \\ -1/\sqrt{2} \end{bmatrix}$。
    - 因此，$V = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix}$。

3.  **求对角矩阵 $\Sigma$**
    奇异值为 $\sigma_1 = \sqrt{\lambda_1} = \sqrt{10}$，$\sigma_2 = \sqrt{\lambda_2} = 0$。
    矩阵 $A$ 是 $3 \times 2$ 的，所以 $\Sigma$ 也是 $3 \times 2$ 的：
    $$
    \Sigma = \begin{bmatrix} \sqrt{10} & 0 \\ 0 & 0 \\ 0 & 0 \end{bmatrix}
    $$

4.  **求正交矩阵 $U$**
    矩阵的秩 $r=1$ (只有一个正奇异值)。
    - 计算 $u_1$:
        $$
        u_1 = \frac{1}{\sigma_1} A v_1 = \frac{1}{\sqrt{10}} \begin{bmatrix} 1 & 1 \\ 2 & 2 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix} = \frac{1}{\sqrt{20}} \begin{bmatrix} 2 \\ 4 \\ 0 \end{bmatrix} = \begin{bmatrix} 1/\sqrt{5} \\ 2/\sqrt{5} \\ 0 \end{bmatrix}
        $$
    - 我们需要再找两个与 $u_1$ 正交的单位向量 $u_2, u_3$。它们是 $A^T$ 零空间 $N(A^T)$ 的基。
        求解 $A^Tx=0$，即 $\begin{bmatrix} 1 & 2 & 0 \\ 1 & 2 & 0 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = 0$，得到 $x_1+2x_2=0$。
        $N(A^T)$ 的一组基可以是 $\begin{pmatrix}-2 \\ 1 \\ 0\end{pmatrix}$ 和 $\begin{pmatrix}0 \\ 0 \\ 1\end{pmatrix}$。
        使用格拉姆-施密特方法正交化和单位化，得到：
        $u_2 = \begin{bmatrix} -2/\sqrt{5} \\ 1/\sqrt{5} \\ 0 \end{bmatrix}$, $u_3 = \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$。
    - 因此，$U = \begin{bmatrix} 1/\sqrt{5} & -2/\sqrt{5} & 0 \\ 2/\sqrt{5} & 1/\sqrt{5} & 0 \\ 0 & 0 & 1 \end{bmatrix}$。

5.  **最终分解**
    $$
    A = U\Sigma V^T =
    \begin{bmatrix}
    1/\sqrt{5} & -2/\sqrt{5} & 0 \\
    2/\sqrt{5} & 1/\sqrt{5} & 0 \\
    0 & 0 & 1
    \end{bmatrix}
    \begin{bmatrix}
    \sqrt{10} & 0 \\
    0 & 0 \\
    0 & 0
    \end{bmatrix}
    \begin{bmatrix}
    1/\sqrt{2} & 1/\sqrt{2} \\
    1/\sqrt{2} & -1/\sqrt{2}
    \end{bmatrix}
    $$

## 紧奇异值分解与截断奇异值分解 (page 25-30)

上面介绍的 $A=U_{m \times m} \Sigma_{m \times n} V_{n \times n}^T$ 称为**完全奇异值分解 (Full SVD)**。在实际应用中，我们常常使用其更紧凑的形式。

### 紧奇异值分解 (Compact SVD) (page 26)

在 SVD 中，很多奇异值为 0，对应的左右奇异向量其实没有对矩阵 $A$ 的构成做出贡献。我们可以把这些部分去掉，得到**紧奇异值分解**。

> [!definition]+ 定义：紧奇异值分解
>
> 设矩阵 $A$ 的秩为 $\text{rank}(A) = r$ ($r \le \min(m, n)$)，则其紧 SVD 为：
>
> $$
> A = U_r \Sigma_r V_r^T
> $$
>
> 其中：
> - $U_r$ 是一个 $m \times r$ 矩阵，由 $U$ 的前 $r$ 列（对应 $r$ 个正奇异值）构成。
> - $\Sigma_r$ 是一个 $r \times r$ 的对角矩阵，由 $r$ 个正奇异值构成。
> - $V_r$ 是一个 $n \times r$ 矩阵，由 $V$ 的前 $r$ 列构成。

紧 SVD 的分解结果是**精确的**，它移除了所有不必要的信息，其分解矩阵的尺寸更小。

### 截断奇异值分解 (Truncated SVD) (page 28)

在很多应用中，我们不仅想去掉 0 奇异值，还想进一步丢弃那些**非常小**的奇异值，以达到数据压缩或降噪的目的。这就引出了**截断奇异值分解**。

> [!definition]+ 定义：截断奇异值分解 (TSVD)
>
> 在 SVD 中，只保留最大的 $k$ 个奇异值及其对应的左右奇异向量 ($k < r$)，得到矩阵 $A$ 的一个**近似**：
>
> $$
> A \approx A_k = U_k \Sigma_k V_k^T \quad (15.19)
> $$
>
> 其中：
> - $U_k$ 是 $m \times k$ 矩阵（$U$ 的前 $k$ 列）。
> - $\Sigma_k$ 是 $k \times k$ 对角矩阵（前 $k$ 个奇异值）。
> - $V_k$ 是 $n \times k$ 矩阵（$V$ 的前 $k$ 列）。

$A_k$ 是一个秩为 $k$ 的矩阵，它是所有秩不超过 $k$ 的矩阵中，对原矩阵 $A$ 的**最佳近似**（我们将在下一节详细讨论）。这使得 TSVD 成为主成分分析 (PCA)、推荐系统、图像压缩等技术的核心。

## 几何解释 (page 31-36)

SVD 有一个非常直观的几何解释。任何一个矩阵 $A$ 所代表的线性变换 $T: \mathbb{R}^n \to \mathbb{R}^m$ ($x \mapsto Ax$)，都可以被分解为三个基本操作：

> [!extra]+ SVD 的几何变换
>
> 变换 $A = U\Sigma V^T$ 作用于一个向量 $x$ 的过程 ($Ax = U(\Sigma(V^T x))$) 如下：
>
> 1.  **一次旋转或反射 ($V^T$)**:
>     $V$ 是正交矩阵，它的列向量 $\{v_i\}$ 构成了 $\mathbb{R}^n$ 空间的一组新的标准正交基。$V^T$ 的作用是将输入向量 $x$ 从原始坐标系旋转到这个新的基坐标系下。
> 2.  **一次坐标轴缩放 ($\Sigma$)**:
>     $\Sigma$ 是一个矩形对角矩阵。它的作用是在新坐标系的各个轴向上进行缩放，第 $i$ 个轴向被缩放 $\sigma_i$ 倍。如果 $m \ne n$，它还负责维度的改变。
> 3.  **另一次旋转或反射 ($U$)**:
>     $U$ 也是正交矩阵，它的列向量 $\{u_i\}$ 构成了 $\mathbb{R}^m$ 空间的一组标准正交基。它的作用是将经过缩放后的向量，从中间坐标系旋转到最终的目标空间坐标系下。

*上图形象地展示了 SVD 的几何意义：一个单位圆（在 $\mathbb{R}^2$ 中）首先经过 $V^T$ 旋转，然后经过 $\Sigma$ 沿轴拉伸成一个椭圆，最后经过 $U$ 再次旋转。*

## 奇异值分解与矩阵近似 (page 54-69)

### 弗罗贝尼乌斯范数 (Frobenius norm) (page 55)

为了衡量一个矩阵对另一个矩阵的近似程度，我们需要一个度量标准。**弗罗贝尼乌斯范数**是常用的选择。

> [!definition]+ 定义：弗罗贝尼乌斯范数
>
> 对于矩阵 $A = [a_{ij}]_{m \times n}$，其弗罗贝尼乌斯范数定义为：
>
> $$
> ||A||_F = \left( \sum_{i=1}^m \sum_{j=1}^n (a_{ij})^2 \right)^{\frac{1}{2}}
> $$
>
> 这等价于将矩阵所有元素拉成一个长向量后计算其 $L_2$ 范数。在机器学习中，这对应于平方损失函数。

> [!lemma]+ 引理 15.1 (page 56)
>
> 矩阵的弗罗贝尼乌斯范数也可以用其奇异值表示：
>
> $$
> ||A||_F = \left( \sigma_1^2 + \sigma_2^2 + \dots + \sigma_r^2 \right)^{\frac{1}{2}}
> $$
>
> 其中 $r$ 是矩阵的秩。
>
> **证明思路**：弗罗贝尼乌斯范数在正交变换下保持不变，即 $||UA||_F = ||AV||_F = ||A||_F$。因此 $||A||_F = ||U\Sigma V^T||_F = ||\Sigma||_F$。而 $||\Sigma||_F$ 就是其对角线元素（奇异值）的平方和的平方根。

### 矩阵的最优近似 (Eckart-Young-Mirsky 定理) (page 58)

这是 SVD 在应用中最为核心和强大的定理之一。

> [!theorem]+ 定理 15.2 & 15.3 (Eckart-Young-Mirsky)
>
> 设矩阵 $A \in \mathbb{R}^{m \times n}$ 的秩为 $r$，其截断奇异值分解为 $A_k = U_k\Sigma_k V_k^T$ ($k < r$)。在所有秩不超过 $k$ 的 $m \times n$ 矩阵的集合 $\mathcal{M}$ 中，$A_k$ 是在弗罗贝尼乌斯范数意义下对 $A$ 的**最佳近似**。
>
> 即：
>
> $$
> ||A - A_k||_F = \min_{X \in \mathcal{M}, \text{rank}(X)\le k} ||A - X||_F
> $$
>
> 并且，这个最小的近似误差为：
>
> $$
> ||A - A_k||_F = \left( \sigma_{k+1}^2 + \sigma_{k+2}^2 + \dots + \sigma_r^2 \right)^{\frac{1}{2}}
> $$

这个定理告诉我们，**要想用一个低秩矩阵最好地逼近原始矩阵，截断 SVD 是最优的选择**。我们丢弃的奇异值越小，近似的精度就越高。

- **紧 SVD** 是在弗罗贝尼乌斯范数意义下的**无损压缩**。
- **截断 SVD** 是在弗罗贝尼乌斯范数意义下的**有损压缩**，但它是最优的有损压缩。

### 矩阵的外积展开式 (page 67)

SVD 还有另一种非常有用的表示形式，即**外积展开**。

> [!note]+ SVD 外积展开
>
> 矩阵 $A$ 可以表示为一系列秩为 1 的矩阵之和：
>
> $$
> A = \sum_{i=1}^r \sigma_i u_i v_i^T = \sigma_1 u_1 v_1^T + \sigma_2 u_2 v_2^T + \dots + \sigma_r u_r v_r^T
> $$
>
> 其中，$u_i v_i^T$ 是一个 $m \times n$ 的秩一矩阵，由左奇异向量 $u_i$ 和右奇异向量 $v_i$ 的外积得到。
>
> ---
> **与 TSVD 的关系**：
>
> 截断 SVD 得到的最佳低秩近似 $A_k$ 就是这个级数的前 $k$ 项之和：
>
> $$
> A_k = \sum_{i=1}^k \sigma_i u_i v_i^T
> $$
>
> 因为奇异值 $\sigma_i$ 是递减的，所以每一项的“重要性”也在递减。这再次说明了为什么只取前几项就能很好地近似原矩阵。

## 总结 (page 72-75)

1.  **SVD 定义**: 任何 $m \times n$ 矩阵 $A$ 可分解为 $A = U\Sigma V^T$，其中 $U, V$ 是正交矩阵，$\Sigma$ 是对角元素非负递减的矩形对角矩阵。
2.  **存在性与唯一性**: SVD 对任意实矩阵都存在，但 $U, V$ 矩阵不唯一。
3.  **分解类型**: 包括**完全 SVD**、**紧 SVD** (等秩，无损) 和**截断 SVD** (低秩，最优有损近似)。
4.  **几何意义**: SVD 将一个线性变换分解为“旋转-缩放-旋转”三个步骤。
5.  **与特征分解的关系**: $V$ 是 $A^TA$ 的特征向量矩阵，$U$ 是 $AA^T$ 的特征向量矩阵，奇异值是特征值的平方根。这是计算 SVD 的主要方法。
6.  **最优近似**: 截断 SVD $A_k$ 在弗罗贝尼乌斯范数下提供了对 $A$ 的最佳低秩近似，是数据压缩和降维的关键。
7.  **外积形式**: $A = \sum \sigma_i u_i v_i^T$ 提供了一种将矩阵看作多个“重要成分”叠加的视角。

[^1]: **正交矩阵** (Orthogonal Matrix): 一个方阵 $Q$，如果其转置等于其逆 ($Q^T = Q^{-1}$)，则称其为正交矩阵。它的所有列（或行）向量构成一组标准正交基。
[^2]: **半正定矩阵** (Positive Semi-definite Matrix): 对于一个对称矩阵 $M$，如果对任意非零向量 $x$，都有 $x^T M x \ge 0$，则称 $M$ 是半正定的。它的所有特征值都非负。$A^TA$ 就是一个典型的半正定矩阵，因为 $x^T(A^TA)x = (Ax)^T(Ax) = ||Ax||^2 \ge 0$。