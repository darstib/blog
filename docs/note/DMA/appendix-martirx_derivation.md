---
title: "矩阵求导术（上/下）"
source: "https://zhuanlan.zhihu.com/p/24709748"
author:
  - "[[长躯鬼侠数学爱好者]]"
published:
created: 2025-12-29
description: "矩阵求导的技术，在统计学、控制论、机器学习等领域有广泛的应用。鉴于我看过的一些资料或言之不详、或繁乱无绪，本文来做个科普，分作两篇，上篇讲标量对矩阵的求导术，下篇讲矩阵对矩阵的求导术。"
---

> [!attention] 本文为搬运
> 
> 本文为[矩阵求导术（上）](https://zhuanlan.zhihu.com/p/24709748)及其下篇的搬运，主要是对其存档并对其中的数学公式进行了重排版。
> 如有侵权请[联系我](https://kg.darstib.cn/connect_me/) 删除。

在[线性代数 - 矩阵运算](https://www.huaxiaozhuan.com/%E6%95%B0%E5%AD%A6%E5%9F%BA%E7%A1%80/chapters/1_algebra.html)部分给出了矩阵运算的常用结论，但是如何理解的？如何推导？

[矩阵求导](https://zhida.zhihu.com/search?content_id=2070530&content_type=Article&match_order=1&q=%E7%9F%A9%E9%98%B5%E6%B1%82%E5%AF%BC&zhida_source=entity) 的技术，在统计学、控制论、机器学习等领域有广泛的应用。鉴于我看过的一些资料或言之不详、或繁乱无绪，本文来做个科普，分作两篇，上篇讲标量对矩阵的求导术，下篇讲矩阵对矩阵的求导术。**本文使用小写字母 $x$ 表示标量，粗体小写字母 $\boldsymbol{x}$ 表示（列）向量，大写字母 $X$ 表示矩阵。**

## 标量对矩阵的求导

首先来琢磨一下定义，标量 $f$ 对矩阵 $X$ 的导数，定义为：
$$
\frac{\partial f}{\partial X} = \left[\frac{\partial f }{\partial X_{ij}}\right]
$$
即 $f$ 对 $X$ 逐元素求导排成与 $X$ 尺寸相同的矩阵。然而，这个定义在计算中并不好用，实用上的原因是对函数较复杂的情形难以逐元素求导；哲理上的原因是逐元素求导破坏了 **整体性** 。试想，为何要将 $f$ 看做矩阵 $X$ 而不是各元素 $X_{ij}$ 的函数呢？答案是用矩阵运算更整洁。所以在求导时不宜拆开矩阵，而是要找一个从整体出发的算法。

为此，我们来回顾，一元微积分中的导数（标量对标量的导数）与微分有联系：$df = f'(x)dx$ ；多元微积分中的[梯度](https://zhida.zhihu.com/search?content_id=2070530&content_type=Article&match_order=1&q=%E6%A2%AF%E5%BA%A6&zhida_source=entity) （标量对向量的导数）也与微分有联系：
$$
df = \sum_{i=1}^n \frac{\partial f}{\partial x_i}dx_i = \frac{\partial f}{\partial \boldsymbol{x}}^T d\boldsymbol{x}
$$
这里第一个等号是[全微分公式](https://zhida.zhihu.com/search?content_id=2070530&content_type=Article&match_order=1&q=%E5%85%A8%E5%BE%AE%E5%88%86%E5%85%AC%E5%BC%8F&zhida_source=entity) ，第二个等号表达了梯度与微分的联系：全微分 $df$ 是梯度向量 $\frac{\partial f}{\partial \boldsymbol{x}}$ ($n\times 1$) 与微分向量 $d\boldsymbol{x}$ ($n\times 1$) 的内积；受此启发，我们将矩阵导数与微分建立联系：
$$
df = \sum_{i=1}^m \sum_{j=1}^n \frac{\partial f}{\partial X_{ij}}dX_{ij} = \text{tr}\left(\frac{\partial f}{\partial X}^T dX\right)
$$
其中 $\text{tr}$ 代表[迹](https://zhida.zhihu.com/search?content_id=2070530&content_type=Article&match_order=1&q=%E8%BF%B9&zhida_source=entity) (trace)，是方阵对角线元素之和，满足性质：**对尺寸相同的矩阵 $A,B$， $\text{tr}(A^TB) = \sum_{i,j}A_{ij}B_{ij}$，即 $\text{tr}(A^TB)$ 是矩阵 $A,B$ 的内积** 。与梯度相似，这里第一个等号是全微分公式，第二个等号表达了矩阵导数与微分的联系：全微分 $df$ 是导数 $\frac{\partial f}{\partial X}$ ($m\times n$) 与微分矩阵 $dX$ ($m\times n$) 的内积。

然后来建立运算法则。回想遇到较复杂的一元函数如 $f = \log(2+\sin x)e^{\sqrt{x}}$，我们是如何求导的呢？通常不是从定义开始求极限，而是先建立了初等函数求导和四则运算、复合等法则，再来运用这些法则。故而，我们来创立常用的矩阵微分的运算法则：

1. **加减法**：$d(X\pm Y) = dX \pm dY$；**矩阵乘法**：$d(XY) = (dX)Y + X dY$；**转置**：$d(X^T) = (dX)^T$；**迹**：$d\text{tr}(X) = \text{tr}(dX)$。
2. **逆**：$dX^{-1} = -X^{-1}dX X^{-1}$。此式可在 $XX^{-1}=I$ 两侧求微分来证明。
3. **行列式**：$d|X| = \text{tr}(X^{\#}dX)$，其中 $X^{\#}$ 表示 $X$ 的[伴随矩阵](https://zhida.zhihu.com/search?content_id=2070530&content_type=Article&match_order=1&q=%E4%BC%B4%E9%9A%8F%E7%9F%A9%E9%98%B5&zhida_source=entity)，在 $X$ 可逆时又可以写作 $d|X|= |X|\text{tr}(X^{-1}dX)$。此式可用 Laplace 展开来证明，详见张贤达《矩阵分析与应用》第 279 页。
4. **逐元素乘法**：$d(X\odot Y) = dX\odot Y + X\odot dY$，$\odot$ 表示Hadamard product，尺寸相同的矩阵 $X,Y$ 逐元素相乘
5. **逐元素函数**：$d\sigma(X) = \sigma'(X)\odot dX$，$\sigma(X) = \left[\sigma(X_{ij})\right]$ 是逐元素标量函数运算，$\sigma'(X)=[\sigma'(X_{ij})]$ 是逐元素求导数。例如：
    $$
    X=\left[\begin{matrix}X_{11} & X_{12} \\ X_{21} & X_{22}\end{matrix}\right], \quad d \sin(X) = \left[\begin{matrix}\cos X_{11} dX_{11} & \cos X_{12} d X_{12}\\ \cos X_{21} d X_{21}& \cos X_{22} dX_{22}\end{matrix}\right] = \cos(X)\odot dX
    $$

我们试图利用矩阵导数与微分的联系 $df = \text{tr}\left(\frac{\partial f}{\partial X}^T dX\right)$，在求出左侧的微分 $df$ 后，该如何写成右侧的形式并得到导数呢？这需要一些迹技巧 (trace trick)：

1. **标量套上迹**：$a = \text{tr}(a)$。
2. **转置**：$\text{tr}(A^T) = \text{tr}(A)$。
3. **线性**：$\text{tr}(A\pm B) = \text{tr}(A)\pm \text{tr}(B)$。
4. **矩阵乘法交换**：$\text{tr}(AB) = \text{tr}(BA)$，其中 $A$ 与 $B^T$ 尺寸相同。两侧都等于 $\sum_{i,j}A_{ij}B_{ji}$。
5. **矩阵乘法/逐元素乘法交换**：$\text{tr}(A^T(B\odot C)) = \text{tr}((A\odot B)^TC)$，其中 $A, B, C$ 尺寸相同。两侧都等于 $\sum_{i,j}A_{ij}B_{ij}C_{ij}$。

观察一下可以断言，**若标量函数 $f$ 是矩阵 $X$ 经加减乘法、逆、行列式、逐元素函数等运算构成，则使用相应的运算法则对 $f$ 求微分，再使用迹技巧给 $df$ 套上迹并将其它项交换至 $dX$ 左侧，对照导数与微分的联系 $df = \text{tr}\left(\frac{\partial f}{\partial X}^T dX\right)$，即能得到导数。**

**特别地，若矩阵退化为向量，对照导数与微分的联系 $df = \frac{\partial f}{\partial \boldsymbol{x}}^T d\boldsymbol{x}$，即能得到导数。**

在建立法则的最后，来谈一谈复合：假设已求得 $\frac{\partial f}{\partial Y}$，而 $Y$ 是 $X$ 的函数，如何求 $\frac{\partial f}{\partial X}$ 呢？在微积分中有标量求导的链式法则 $\frac{\partial f}{\partial x} = \frac{\partial f}{\partial y} \frac{\partial y}{\partial x}$，但这里我们 **不能随意沿用标量的链式法则**，因为[矩阵对矩阵的导数](https://zhida.zhihu.com/search?content_id=2070530&content_type=Article&match_order=1&q=%E7%9F%A9%E9%98%B5%E5%AF%B9%E7%9F%A9%E9%98%B5%E7%9A%84%E5%AF%BC%E6%95%B0&zhida_source=entity) $\frac{\partial Y}{\partial X}$ 截至目前仍是未定义的。于是我们继续追本溯源，链式法则是从何而来？源头仍然是微分。我们直接从微分入手建立复合法则：先写出 $df = \text{tr}\left(\frac{\partial f}{\partial Y}^T dY\right)$，再将 $dY$ 用 $dX$ 表示出来代入，并使用迹技巧将其他项交换至 $dX$ 左侧，即可得到 $\frac{\partial f}{\partial X}$。

最常见的情形是 $Y = AXB$，此时：
$$
df = \text{tr}\left(\frac{\partial f}{\partial Y}^T dY\right) = \text{tr}\left(\frac{\partial f}{\partial Y}^T AdXB\right) =  \text{tr}\left(B\frac{\partial f}{\partial Y}^T AdX\right) = \text{tr}\left((A^T\frac{\partial f}{\partial Y}B^T)^T dX\right)
$$
可得到 $\frac{\partial f}{\partial X}=A^T\frac{\partial f}{\partial Y}B^T$。注意这里 $dY = AdXB$，由于 $A,B$ 是常量，$dA=0,dB=0$，以及我们使用矩阵乘法交换的迹技巧交换了 $\frac{\partial f}{\partial Y}^T AdX$ 与 $B$。

接下来演示一些算例。特别提醒要依据已经建立的运算法则来计算，不能随意套用微积分中标量导数的结论，比如认为 $AX$ 对 $X$ 的导数为 $A$，这是没有根据、意义不明的。

### 例 1

> [!question]
> 
> $f = \boldsymbol{a}^T X\boldsymbol{b}$，求 $\frac{\partial f}{\partial X}$。其中 $\boldsymbol{a}$ 是 $m\times 1$ 列向量，$X$ 是 $m\times n$ 矩阵，$\boldsymbol{b}$ 是 $n\times 1$ 列向量，$f$ 是标量。

**解**：先使用矩阵乘法法则求微分，
$$
df = d\boldsymbol{a}^TX\boldsymbol{b}+\boldsymbol{a}^TdX\boldsymbol{b}+\boldsymbol{a}^TXd\boldsymbol{b} = \boldsymbol{a}^TdX\boldsymbol{b}
$$
注意这里的 $\boldsymbol{a}, \boldsymbol{b}$ 是常量，$d\boldsymbol{a} = \boldsymbol{0}, d\boldsymbol{b} = \boldsymbol{0}$。由于 $df$ 是标量，它的迹等于自身，$df = \text{tr}(df)$，套上迹并做矩阵乘法交换：
$$
df = \text{tr}(\boldsymbol{a}^TdX\boldsymbol{b}) = \text{tr}(\boldsymbol{b}\boldsymbol{a}^TdX)= \text{tr}((\boldsymbol{a}\boldsymbol{b}^T)^TdX)
$$
注意这里我们根据 $\text{tr}(AB) = \text{tr}(BA)$ 交换了 $\boldsymbol{a}^TdX$ 与 $\boldsymbol{b}$。对照导数与微分的联系 $df = \text{tr}\left(\frac{\partial f}{\partial X}^T dX\right)$，得到：
$$
\frac{\partial f}{\partial X} = \frac{\partial (\boldsymbol{a}^T X\boldsymbol{b})}{\partial X} = \boldsymbol{a}\boldsymbol{b}^T
$$

> [!attention] 
> 
> 注意：这里不能用 $\frac{\partial f}{\partial X} =\boldsymbol{a}^T \frac{\partial X}{\partial X}\boldsymbol{b}=?$ ，导数与矩阵乘法的交换是不合法则的运算（而微分是合法的）。有些资料在计算矩阵导数时，会略过求微分这一步，这是逻辑上解释不通的。

### 例 2

> [!question] 
> 
> $f = \boldsymbol{a}^T \exp(X\boldsymbol{b})$，求 $\frac{\partial f}{\partial X}$。其中 $\boldsymbol{a}$ 是 $m\times 1$ 列向量，$X$ 是 $m\times n$ 矩阵，$\boldsymbol{b}$ 是 $n\times 1$ 列向量，$\exp$ 表示逐元素求指数，$f$ 是标量。

**解**：先使用矩阵乘法、逐元素函数法则求微分：
$$
df = \boldsymbol{a}^T(\exp(X\boldsymbol{b})\odot (dX\boldsymbol{b}))
$$
再套上迹并做交换：
$$
\begin{aligned}
df &= \text{tr}( \boldsymbol{a}^T(\exp(X\boldsymbol{b})\odot (dX\boldsymbol{b}))) \\
&= \text{tr}((\boldsymbol{a}\odot \exp(X\boldsymbol{b}))^TdX \boldsymbol{b}) \\
&= \text{tr}(\boldsymbol{b}(\boldsymbol{a}\odot \exp(X\boldsymbol{b}))^TdX) \\
&= \text{tr}(((\boldsymbol{a}\odot \exp(X\boldsymbol{b}))\boldsymbol{b}^T)^TdX)
\end{aligned}
$$
注意这里我们先根据 $\text{tr}(A^T(B\odot C)) = \text{tr}((A\odot B)^TC)$ 交换了 $\boldsymbol{a}$、$\exp(X\boldsymbol{b})$ 与 $dX\boldsymbol{b}$，再根据 $\text{tr}(AB) = \text{tr}(BA)$ 交换了 $(\boldsymbol{a}\odot \exp(X\boldsymbol{b}))^TdX$ 与 $\boldsymbol{b}$。对照导数与微分的联系，得到：
$$
\frac{\partial f}{\partial X} = (\boldsymbol{a}\odot \exp(X\boldsymbol{b}))\boldsymbol{b}^T
$$

### 例 3

> [!question] 
> 
> $f = \text{tr}(Y^T M Y), Y = \sigma(WX)$，求 $\frac{\partial f}{\partial X}$。其中 $W$ 是 $l\times m$ 矩阵，$X$ 是 $m\times n$ 矩阵，$Y$ 是 $l\times n$ 矩阵，$M$ 是 $l\times l$ 对称矩阵，$\sigma$ 是逐元素函数，$f$ 是标量。

**解**：先求 $\frac{\partial f}{\partial Y}$。求微分，使用矩阵乘法、转置法则：
$$
df = \text{tr}((dY)^TMY) + \text{tr}(Y^TMdY) = \text{tr}(Y^TM^TdY) + \text{tr}(Y^TMdY) = \text{tr}(Y^T(M+M^T)dY)
$$
对照导数与微分的联系，得到 $\frac{\partial f}{\partial Y}=(M+M^T)Y = 2MY$，注意这里 $M$ 是对称矩阵。为求 $\frac{\partial f}{\partial X}$，写出 $df = \text{tr}\left(\frac{\partial f}{\partial Y}^T dY\right)$，再将 $dY$ 用 $dX$ 表示出来代入，并使用矩阵乘法/逐元素乘法交换：
$$
df = \text{tr}\left(\frac{\partial f}{\partial Y}^T (\sigma'(WX)\odot (WdX))\right) = \text{tr}\left(\left(\frac{\partial f}{\partial Y} \odot \sigma'(WX)\right)^T W dX\right)
$$
对照导数与微分的联系，得到：
$$
\frac{\partial f}{\partial X}=W^T \left(\frac{\partial f}{\partial Y}\odot \sigma'(WX)\right)=W^T((2M\sigma(WX))\odot\sigma'(WX))
$$

### 例 4【线性回归】

> [!question] 
> 
> $l = \|X\boldsymbol{w}- \boldsymbol{y}\|^2$，求 $\boldsymbol{w}$ 的最小二乘估计，即求 $\frac{\partial l}{\partial \boldsymbol{w}}$ 的零点。其中 $\boldsymbol{y}$ 是 $m\times 1$ 列向量，$X$ 是 $m\times n$ 矩阵，$\boldsymbol{w}$ 是 $n\times 1$ 列向量，$l$ 是标量。

**解**：这是标量对向量的导数，不过可以把向量看做矩阵的特例。先将向量模平方改写成向量与自身的内积：
$$
l = (X\boldsymbol{w}- \boldsymbol{y})^T(X\boldsymbol{w}- \boldsymbol{y})
$$
求微分，使用矩阵乘法、转置等法则：
$$
dl = (Xd\boldsymbol{w})^T(X\boldsymbol{w}-\boldsymbol{y})+(X\boldsymbol{w}-\boldsymbol{y})^T(Xd\boldsymbol{w}) = 2(X\boldsymbol{w}-\boldsymbol{y})^TXd\boldsymbol{w}
$$
注意这里 $Xd\boldsymbol{w}$ 和 $X\boldsymbol{w}-\boldsymbol{y}$ 是向量，两个向量的内积满足 $\boldsymbol{u}^T\boldsymbol{v} = \boldsymbol{v}^T \boldsymbol{u}$。对照导数与微分的联系 $dl = \frac{\partial l}{\partial \boldsymbol{w}}^Td\boldsymbol{w}$，得到：
$$
\frac{\partial l}{\partial \boldsymbol{w}} = 2X^T(X\boldsymbol{w}-\boldsymbol{y})
$$
令 $\frac{\partial l}{\partial \boldsymbol{w}}=\boldsymbol{0}$ 即 $X^TX\boldsymbol{w} = X^T\boldsymbol{y}$，得到 $\boldsymbol{w}$ 的最小二乘估计为 $\boldsymbol{w} = (X^TX)^{-1}X^T\boldsymbol{y}$。

### 例 5【方差的最大似然估计】

> [!question] 
> 
> 样本 $\boldsymbol{x}_1,\dots, \boldsymbol{x}_N \sim \mathcal{N}(\boldsymbol{\mu}, \Sigma)$，求方差 $\Sigma$ 的最大似然估计。写成数学式是：
> 
> $$
> l = \log|\Sigma|+\frac{1}{N}\sum_{i=1}^N(\boldsymbol{x}_i-\boldsymbol{\bar{x}})^T\Sigma^{-1}(\boldsymbol{x}_i-\boldsymbol{\bar{x}})
> $$
> 
> 求 $\frac{\partial l }{\partial \Sigma}$ 的零点。其中 $\boldsymbol{x}_i$ 是 $m\times 1$ 列向量，$\bar{\boldsymbol{x}}=\frac{1}{N}\sum_{i=1}^N \boldsymbol{x}_i$ 是样本均值，$\Sigma$ 是 $m\times m$ 对称正定矩阵，$l$ 是标量，$\log$ 表示自然对数。

**解**：首先求微分，使用矩阵乘法、行列式、逆等运算法则，第一项是：
$$
d\log|\Sigma| = |\Sigma|^{-1}d|\Sigma| = \text{tr}(\Sigma^{-1}d\Sigma)
$$
第二项是：
$$
\frac{1}{N}\sum_{i=1}^N(\boldsymbol{x}_i-\boldsymbol{\bar{x}})^Td\Sigma^{-1}(\boldsymbol{x}_i-\boldsymbol{\bar{x}}) = -\frac{1}{N}\sum_{i=1}^N(\boldsymbol{x}_i-\boldsymbol{\bar{x}})^T\Sigma^{-1}d\Sigma\Sigma^{-1}(\boldsymbol{x}_i-\boldsymbol{\bar{x}})
$$
再给第二项套上迹做交换：
$$
\begin{aligned}
& \text{tr}\left(-\frac{1}{N}\sum_{i=1}^N(\boldsymbol{x}_i-\boldsymbol{\bar{x}})^T\Sigma^{-1}d\Sigma\Sigma^{-1}(\boldsymbol{x}_i-\boldsymbol{\bar{x}})\right) \\
&= -\frac{1}{N} \sum_{i=1}^N \text{tr}((\boldsymbol{x}_i-\boldsymbol{\bar{x}})^T\Sigma^{-1} d\Sigma \Sigma^{-1}(\boldsymbol{x}_i-\boldsymbol{\bar{x}})) \\
&= -\frac{1}{N}\sum_{i=1}^N\text{tr}\left(\Sigma^{-1}(\boldsymbol{x}_i-\boldsymbol{\bar{x}})(\boldsymbol{x}_i-\boldsymbol{\bar{x}})^T\Sigma^{-1}d\Sigma\right) \\
&= -\text{tr}(\Sigma^{-1}S\Sigma^{-1}d\Sigma)
\end{aligned}
$$
其中先交换迹与求和，然后将 $\Sigma^{-1} (\boldsymbol{x}_i-\boldsymbol{\bar{x}})$ 交换到左边，最后再交换迹与求和，并定义 $S = \frac{1}{N}\sum_{i=1}^N(\boldsymbol{x}_i-\boldsymbol{\bar{x}})(\boldsymbol{x}_i-\boldsymbol{\bar{x}})^T$ 为样本方差矩阵。得到：
$$
dl = \text{tr}\left(\left(\Sigma^{-1}-\Sigma^{-1}S\Sigma^{-1}\right)d\Sigma\right)
$$
对照导数与微分的联系，有：
$$
\frac{\partial l }{\partial \Sigma}=(\Sigma^{-1}-\Sigma^{-1}S\Sigma^{-1})^T
$$
其零点即 $\Sigma$ 的最大似然估计为 $\Sigma = S$。

### 例 6【多元 logistic 回归】

> [!question] 
> 
> $l = -\boldsymbol{y}^T\log\text{softmax}(W\boldsymbol{x})$，求 $\frac{\partial l}{\partial W}$。其中 $\boldsymbol{y}$ 是除一个元素为 1 外其它元素为 0 的 $m\times 1$ 列向量，$W$ 是 $m\times n$ 矩阵，$\boldsymbol{x}$ 是 $n\times 1$ 列向量，$l$ 是标量；$\log$ 表示自然对数，$\text{softmax}(\boldsymbol{a}) = \frac{\exp(\boldsymbol{a})}{\boldsymbol{1}^T\exp(\boldsymbol{a})}$，其中 $\exp(\boldsymbol{a})$ 表示逐元素求指数，$\boldsymbol{1}$ 代表全 1 向量。

**解 1**：首先将 softmax 函数代入并写成：
$$
l = -\boldsymbol{y}^T \left(\log (\exp(W\boldsymbol{x}))-\boldsymbol{1}\log(\boldsymbol{1}^T\exp(W\boldsymbol{x}))\right) = -\boldsymbol{y}^TW\boldsymbol{x} + \log(\boldsymbol{1}^T\exp(W\boldsymbol{x}))
$$
这里要注意逐元素 $\log$ 满足等式 $\log(\boldsymbol{u}/c) = \log(\boldsymbol{u}) - \boldsymbol{1}\log(c)$，以及 $\boldsymbol{y}$ 满足 $\boldsymbol{y}^T \boldsymbol{1} = 1$（因为 y 表示的是标签，即 `[0, 1, 0, 0, ...]`）。求微分，使用矩阵乘法、逐元素函数等法则：

$$
dl =- \boldsymbol{y}^TdW\boldsymbol{x}+\frac{\boldsymbol{1}^T\left(\exp(W\boldsymbol{x})\odot(dW\boldsymbol{x})\right)}{\boldsymbol{1}^T\exp(W\boldsymbol{x})}
$$

再套上迹并做交换，注意可化简 $\boldsymbol{1}^T\left(\exp(W\boldsymbol{x})\odot(dW\boldsymbol{x})\right) = \exp(W\boldsymbol{x})^TdW\boldsymbol{x}$，这是根据等式 $\boldsymbol{1}^T (\boldsymbol{u}\odot \boldsymbol{v}) = \boldsymbol{u}^T \boldsymbol{v}$，故：
$$
\begin{aligned}
dl &= \text{tr}\left(-\boldsymbol{y}^TdW\boldsymbol{x}+\frac{\exp(W\boldsymbol{x})^TdW\boldsymbol{x}}{\boldsymbol{1}^T\exp(W\boldsymbol{x})}\right) \\
&=\text{tr}(-\boldsymbol{y}^TdW\boldsymbol{x}+\text{softmax}(W\boldsymbol{x})^TdW\boldsymbol{x}) \\
&= \text{tr}(\boldsymbol{x}(\text{softmax}(W\boldsymbol{x})-\boldsymbol{y})^TdW)
\end{aligned}
$$
对照导数与微分的联系，得到：
$$
\frac{\partial l}{\partial W}= (\text{softmax}(W\boldsymbol{x})-\boldsymbol{y})\boldsymbol{x}^T
$$

**解2**：定义 $\boldsymbol{a} = W\boldsymbol{x}$，则 $l = -\boldsymbol{y}^T\log\text{softmax}(\boldsymbol{a})$，先同上求出 $\frac{\partial l}{\partial \boldsymbol{a}} = \text{softmax}(\boldsymbol{a})-\boldsymbol{y}$，再利用复合法则：
$$
dl = \text{tr}\left(\frac{\partial l}{\partial \boldsymbol{a}}^Td\boldsymbol{a}\right) = \text{tr}\left(\frac{\partial l}{\partial \boldsymbol{a}}^TdW \boldsymbol{x}\right) = \text{tr}\left(\boldsymbol{x}\frac{\partial l}{\partial \boldsymbol{a}}^TdW\right)
$$
得到 $\frac{\partial l}{\partial W}= \frac{\partial l}{\partial\boldsymbol{a}}\boldsymbol{x}^T$。

最后一例留给经典的神经网络。神经网络的求导术是学术史上的重要成果，还有个专门的名字叫做 BP 算法，我相信如今很多人在初次推导 BP 算法时也会颇费一番脑筋，事实上使用矩阵求导术来推导并不复杂。为简化起见，我们推导二层神经网络的 BP 算法。

### 例 7【二层神经网络】

> [!question] 
> 
> $l = -\boldsymbol{y}^T\log\text{softmax}(W_2\sigma(W_1\boldsymbol{x}))$，求 $\frac{\partial l}{\partial W_1}$ 和 $\frac{\partial l}{\partial W_2}$。其中 $\boldsymbol{y}$ 是除一个元素为 1 外其它元素为 0 的 $m\times 1$ 列向量，$W_2$ 是 $m\times p$ 矩阵，$W_1$ 是 $p \times n$ 矩阵，$\boldsymbol{x}$ 是 $n\times 1$ 列向量，$l$ 是标量；$\log$ 表示自然对数，$\text{softmax}(\boldsymbol{a})$ 同上，$\sigma$ 是逐元素 sigmoid 函数 $\sigma(a) = \frac{1}{1+\exp(-a)}$。

**解**：定义 $\boldsymbol{a}_1=W_1\boldsymbol{x}$，$\boldsymbol{h}_1 = \sigma(\boldsymbol{a}_1)$，$\boldsymbol{a}_2 = W_2 \boldsymbol{h}_1$，则 $l =-\boldsymbol{y}^T\log\text{softmax}(\boldsymbol{a}_2)$。在前例中已求出 $\frac{\partial l}{\partial \boldsymbol{a}_2} = \text{softmax}(\boldsymbol{a}_2)-\boldsymbol{y}$。使用复合法则：
$$
dl = \text{tr}\left(\frac{\partial l}{\partial \boldsymbol{a}_2}^Td\boldsymbol{a}_2\right) = \text{tr}\left(\frac{\partial l}{\partial \boldsymbol{a}_2}^TdW_2 \boldsymbol{h}_1\right) + \underbrace{ \text{tr}\left(\frac{\partial l}{\partial \boldsymbol{a}_2}^TW_2 d\boldsymbol{h}_1\right)}_{dl_2}
$$
使用矩阵乘法交换的迹技巧从第一项得到 $\frac{\partial l}{\partial W_2}= \frac{\partial l}{\partial\boldsymbol{a}_2}\boldsymbol{h}_1^T$，从第二项得到 $\frac{\partial l}{\partial \boldsymbol{h}_1}= W_2^T\frac{\partial l}{\partial\boldsymbol{a}_2}$。

接下来对第二项继续使用复合法则来求 $\frac{\partial l}{\partial \boldsymbol{a}_1}$，并利用矩阵乘法和逐元素乘法交换的迹技巧：
$$
dl_2 = \text{tr}\left(\frac{\partial l}{\partial\boldsymbol{h}_1}^Td\boldsymbol{h}_1\right) = \text{tr}\left(\frac{\partial l}{\partial\boldsymbol{h}_1}^T(\sigma'(\boldsymbol{a}_1)\odot d\boldsymbol{a}_1)\right) = \text{tr}\left(\left(\frac{\partial l}{\partial\boldsymbol{h}_1}\odot \sigma'(\boldsymbol{a}_1)\right)^Td\boldsymbol{a}_1\right)
$$
得到 $\frac{\partial l}{\partial \boldsymbol{a}_1}= \frac{\partial l}{\partial\boldsymbol{h}_1}\odot\sigma'(\boldsymbol{a}_1)$。为求 $\frac{\partial l}{\partial W_1}$，再用一次复合法则：
$$
dl_2 = \text{tr}\left(\frac{\partial l}{\partial\boldsymbol{a}_1}^Td\boldsymbol{a}_1\right) = \text{tr}\left(\frac{\partial l}{\partial\boldsymbol{a}_1}^TdW_1\boldsymbol{x}\right) = \text{tr}\left(\boldsymbol{x}\frac{\partial l}{\partial\boldsymbol{a}_1}^TdW_1\right)
$$
得到 $\frac{\partial l}{\partial W_1}= \frac{\partial l}{\partial\boldsymbol{a}_1}\boldsymbol{x}^T$。

> [!note]+ 
> 
> **推广**：样本 $(\boldsymbol{x}_1, y_1), \dots, (\boldsymbol{x}_N,y_N)$，
> 
> $$
> l = -\sum_{i=1}^N \boldsymbol{y}_i^T\log\text{softmax}(W_2\sigma(W_1\boldsymbol{x}_i + \boldsymbol{b}_1) + \boldsymbol{b}_2)
> $$
> 
> 其中 $\boldsymbol{b}_1$ 是 $p \times 1$ 列向量，$\boldsymbol{b}_2$ 是 $m\times 1$ 列向量，其余定义同上。

**解1**：定义 $\boldsymbol{a}_{1,i} = W_1 \boldsymbol{x}_i + \boldsymbol{b}_1$，$\boldsymbol{h}_{1,i} = \sigma(\boldsymbol{a}_{1,i})$，$\boldsymbol{a}_{2,i} = W_2\boldsymbol{h}_{1,i} + \boldsymbol{b}_2$，则 $l = -\sum_{i=1}^N \boldsymbol{y}_i^T \log \text{softmax}(\boldsymbol{a}_{2,i})$。先同上可求出 $\frac{\partial l}{\partial \boldsymbol{a}_{2,i}} = \text{softmax}(\boldsymbol{a}_{2,i})-\boldsymbol{y}_i$。使用复合法则，
$$
\begin{aligned}
dl &= \text{tr}\left(\sum_{i=1}^N\frac{\partial l}{\partial \boldsymbol{a}_{2,i}}^T d \boldsymbol{a}_{2,i}\right) \\
&= \text{tr}\left( \sum_{i=1}^N \frac{\partial l}{\partial \boldsymbol{a}_{2,i}}^T dW_2 \boldsymbol{h}_{1,i}\right) + \underbrace{\text{tr}\left( \sum_{i=1}^N \frac{\partial l}{\partial \boldsymbol{a}_{2,i}}^T W_2 d\boldsymbol{h}_{1,i}\right)}_{dl_2} + \text{tr}\left( \sum_{i=1}^N \frac{\partial l}{\partial \boldsymbol{a}_{2,i}}^T d \boldsymbol{b}_2\right)
\end{aligned}
$$
从第一项得到得到 $\frac{\partial l}{\partial W_2}= \sum_{i=1}^N \frac{\partial l}{\partial\boldsymbol{a}_{2,i}}\boldsymbol{h}_{1,i}^T$，从第二项得到 $\frac{\partial l}{\partial \boldsymbol{h}_{1,i}}= W_2^T\frac{\partial l}{\partial\boldsymbol{a}_{2,i}}$，从第三项得到到 $\frac{\partial l}{\partial \boldsymbol{b}_2}= \sum_{i=1}^N \frac{\partial l}{\partial\boldsymbol{a}_{2,i}}$。

接下来对第二项继续使用复合法则，得到 $\frac{\partial l}{\partial \boldsymbol{a}_{1,i}}= \frac{\partial l}{\partial\boldsymbol{h}_{1,i}}\odot\sigma'(\boldsymbol{a}_{1,i})$。为求 $\frac{\partial l}{\partial W_1}, \frac{\partial l}{\partial \boldsymbol{b}_1}$，再用一次复合法则：
$$
dl_2 = \text{tr}\left(\sum_{i=1}^N \frac{\partial l}{\partial\boldsymbol{a}_{1,i}}^Td\boldsymbol{a}_{1,i}\right) = \text{tr}\left(\sum_{i=1}^N \frac{\partial l}{\partial\boldsymbol{a}_{1,i}}^TdW_1\boldsymbol{x}_i\right) + \text{tr}\left(\sum_{i=1}^N \frac{\partial l}{\partial\boldsymbol{a}_{1,i}}^Td\boldsymbol{b}_1\right)
$$
得到 $\frac{\partial l}{\partial W_1}= \sum_{i=1}^N \frac{\partial l}{\partial\boldsymbol{a}_{1,i}}\boldsymbol{x}_i^T$，$\frac{\partial l}{\partial \boldsymbol{b}_1}= \sum_{i=1}^N \frac{\partial l}{\partial\boldsymbol{a}_{1,i}}$。

**解2**：可以用矩阵来表示 $N$ 个样本，以简化形式。定义 $X = [\boldsymbol{x}_1, \cdots, \boldsymbol{x}_N]$，$A_1 = [\boldsymbol{a}_{1,1},\cdots,\boldsymbol{a}_{1,N}] =W_1 X + \boldsymbol{b}_1 \boldsymbol{1}^T$，$H_1 = [\boldsymbol{h}_{1,1}, \cdots, \boldsymbol{h}_{1,N}] = \sigma(A_1)$，$A_2 = [\boldsymbol{a}_{2,1},\cdots,\boldsymbol{a}_{2,N}] = W_2 H_1 + \boldsymbol{b}_2 \boldsymbol{1}^T$，注意这里使用全 1 向量来扩展维度。先同上求出 $\frac{\partial l}{\partial A_2} = [\text{softmax}(\boldsymbol{a}_{2,1})-\boldsymbol{y}_1, \cdots, \text{softmax}(\boldsymbol{a}_{2,N})-\boldsymbol{y}_N]$。使用复合法则，

$$
dl = \text{tr}\left(\frac{\partial l}{\partial A_2}^T d A_2\right) = \text{tr}\left( \frac{\partial l}{\partial A_2}^T dW_2 H_1 \right) + \underbrace{\text{tr}\left(\frac{\partial l}{\partial A_2}^T W_2 d H_1\right)}_{dl_2} + \text{tr}\left(\frac{\partial l}{\partial A_2}^T d \boldsymbol{b}_2 \boldsymbol{1}^T\right)
$$
从第一项得到 $\frac{\partial l}{\partial W_2}= \frac{\partial l}{\partial A_2}H_1^T$，从第二项得到 $\frac{\partial l}{\partial H_1}= W_2^T\frac{\partial l}{\partial A_{2}}$，从第三项得到到 $\frac{\partial l}{\partial \boldsymbol{b}_2}= \frac{\partial l}{\partial A_2}\boldsymbol{1}$。

接下来对第二项继续使用复合法则，得到 $\frac{\partial l}{\partial A_1}= \frac{\partial l}{\partial H_1}\odot\sigma'(A_1)$。为求 $\frac{\partial l}{\partial W_1}, \frac{\partial l}{\partial \boldsymbol{b}_1}$，再用一次复合法则：
$$
dl_2 = \text{tr}\left(\frac{\partial l}{\partial A_1}^TdA_1\right) = \text{tr}\left(\frac{\partial l}{\partial A_1}^TdW_1X\right) + \text{tr}\left( \frac{\partial l}{\partial A_1}^Td\boldsymbol{b}_1 \boldsymbol{1}^T\right)
$$
得到 $\frac{\partial l}{\partial W_1}=  \frac{\partial l}{\partial A_1}X^T$，$\frac{\partial l}{\partial \boldsymbol{b}_1}= \frac{\partial l}{\partial A_1}\boldsymbol{1}$。

## 矩阵对矩阵的求导

本文承接上篇[矩阵求导术（上）](https://zhuanlan.zhihu.com/p/24709748)，来讲矩阵对矩阵的求导术。使用小写字母 $x$ 表示标量，粗体小写字母 $\boldsymbol{x}$ 表示列向量，大写字母 $X$ 表示矩阵。矩阵对矩阵的求导采用了向量化的思路，常应用于二阶方法中 [Hessian 矩阵](https://zhida.zhihu.com/search?content_id=2132061&content_type=Article&match_order=1&q=Hessian%E7%9F%A9%E9%98%B5&zhida_source=entity) 的分析。

首先来琢磨一下定义。矩阵对矩阵的导数，需要什么样的定义？

1. 矩阵 $F(p\times q)$ 对矩阵 $X(m\times n)$ 的导数应包含所有 $mnpq$ 个偏导数 $\frac{\partial F_{kl}}{\partial X_{ij}}$，从而不损失信息；
2. 导数与微分有简明的联系，因为在计算导数和应用中需要这个联系；
3. 导数有简明的从整体出发的算法。

我们先定义向量 $\boldsymbol{f}(p\times 1)$ 对向量 $\boldsymbol{x}(m\times 1)$ 的导数（梯度矩阵，分母布局）：
$$
\frac{\partial \boldsymbol{f}}{\partial \boldsymbol{x}} = \begin{bmatrix} \frac{\partial f_1}{\partial x_1} & \frac{\partial f_2}{\partial x_1} & \cdots & \frac{\partial f_p}{\partial x_1}\\ \frac{\partial f_1}{\partial x_2} & \frac{\partial f_2}{\partial x_2} & \cdots & \frac{\partial f_p}{\partial x_2}\\ \vdots & \vdots & \ddots & \vdots\\ \frac{\partial f_1}{\partial x_m} & \frac{\partial f_2}{\partial x_m} & \cdots & \frac{\partial f_p}{\partial x_m}\\ \end{bmatrix} \quad (m\times p)
$$
有 $d\boldsymbol{f} = \frac{\partial \boldsymbol{f} }{\partial \boldsymbol{x} }^T d\boldsymbol{x}$。再定义矩阵的（按列优先）向量化：
$$
\mathrm{vec}(X) = [X_{11}, \ldots, X_{m1}, X_{12}, \ldots, X_{m2}, \ldots, X_{1n}, \ldots, X_{mn}]^T \quad (mn\times 1)
$$
并定义矩阵 $F$ 对矩阵 $X$ 的导数：
$$
\frac{\partial F}{\partial X} = \frac{\partial \mathrm{vec}(F)}{\partial \mathrm{vec}(X)} \quad (mn\times pq)
$$
导数与微分有联系：
$$
\mathrm{vec}(dF) = \frac{\partial F}{\partial X}^T \mathrm{vec}(dX)
$$

几点说明如下：

1. 按此定义，标量 $f$ 对矩阵 $X(m\times n)$ 的导数 $\frac{\partial f}{\partial X}$ 是 $mn\times 1$ 向量，与上篇的定义不兼容，不过二者容易相互转换。为避免混淆，用记号 $\nabla_X f$ 表示上篇定义的 $m\times n$ 矩阵，则有 $\frac{\partial f}{\partial X}=\mathrm{vec}(\nabla_X f)$。虽然本篇的技术可以用于标量对矩阵求导这种特殊情况，但使用上篇中的技术更方便。读者可以通过上篇中的算例试验两种方法的等价转换。
2. 标量对矩阵的二阶导数，又称 Hessian 矩阵，定义为：
    $$
    \nabla^2_X f = \frac{\partial^2 f}{\partial X^2} = \frac{\partial \nabla_X f}{\partial X} \quad (mn\times mn)
    $$
    是对称矩阵。对向量 $\frac{\partial f}{\partial X}$ 或矩阵 $\nabla_X f$ 求导都可以得到 Hessian 矩阵，但从矩阵 $\nabla_X f$ 出发更方便。
3. $\frac{\partial F}{\partial X} = \frac{\partial\mathrm{vec} (F)}{\partial X} = \frac{\partial F}{\partial \mathrm{vec}(X)} = \frac{\partial\mathrm{vec}(F)}{\partial \mathrm{vec}(X)}$，求导时矩阵被向量化，弊端是这在一定程度破坏了矩阵的结构，会导致结果变得形式复杂；好处是多元微积分中关于梯度、Hessian 矩阵的结论可以沿用过来，只需将矩阵向量化。例如优化问题中，牛顿法的更新 $\Delta X$，满足：
    $$
    \mathrm{vec}(\Delta X) = -(\nabla^2_X f)^{-1}\mathrm{vec}(\nabla_X f)
    $$
4. 在资料中，矩阵对矩阵的导数还有其它定义，比如 $\frac{\partial F}{\partial X} = \left[\frac{\partial F_{kl}}{\partial X}\right]$ ($mp\times nq$)，或是 $\frac{\partial F}{\partial X} = \left[\frac{\partial F}{\partial X_{ij}}\right]$ ($mp\times nq$)，它能兼容上篇中的标量对矩阵导数的定义，但微分与导数的联系（$dF$ 等于 $\frac{\partial F}{\partial X}$ 中逐个 $m\times n$ 子块分别与 $dX$ 做内积）不够简明，不便于计算和应用。资料[5]综述了以上定义，并批判它们是坏的定义，能配合微分运算的才是好的定义。
5. 在资料中，有分子布局和分母布局两种定义，其中向量对向量的导数的排布有所不同。本文使用的是**分母布局**，机器学习和优化中的梯度矩阵采用此定义。而控制论等领域中的 Jacobian 矩阵采用**分子布局**，向量 $\boldsymbol{f}$ 对向量 $\boldsymbol{x}$ 的导数定义是：
    $$
    \frac{\partial \boldsymbol{f}}{\partial \boldsymbol{x}} = \begin{bmatrix} \frac{\partial f_1}{\partial x_1} & \frac{\partial f_1}{\partial x_2} & \cdots & \frac{\partial f_1}{\partial x_m}\\ \frac{\partial f_2}{\partial x_1} & \frac{\partial f_2}{\partial x_2} & \cdots & \frac{\partial f_2}{\partial x_m}\\ \vdots & \vdots & \ddots & \vdots\\ \frac{\partial f_p}{\partial x_1} & \frac{\partial f_p}{\partial x_2} & \cdots & \frac{\partial f_p}{\partial x_m}\\ \end{bmatrix}
    $$
    对应地导数与微分的联系是 $d\boldsymbol{f} = \frac{\partial \boldsymbol{f} }{\partial \boldsymbol{x}}  d\boldsymbol{x}$；同样通过向量化定义矩阵 $F$ 对矩阵 $X$ 的导数 $\frac{\partial F}{\partial X} = \frac{\partial \mathrm{vec}(F)}{\partial \mathrm{vec}(X)}$，有 $\mathrm{vec}(dF) = \frac{\partial F}{\partial X} \mathrm{vec}(dX)$。两种布局下的导数互为转置，二者求微分的步骤是相同的，仅在对照导数与微分的联系时有一个转置的区别，读者可根据所在领域的习惯选定一种布局。

然后来建立运算法则。仍然要利用导数与微分的联系 $\mathrm{vec}(dF) = \frac{\partial F}{\partial X}^T \mathrm{vec}(dX)$，求微分的方法与上篇相同，而从微分得到导数需要一些向量化的技巧：

1. **线性**：$\mathrm{vec}(A+B) = \mathrm{vec}(A) + \mathrm{vec}(B)$。
2. **矩阵乘法**：$\mathrm{vec}(AXB) = (B^T \otimes A) \mathrm{vec}(X)$，其中 $\otimes$ 表示 [Kronecker 积](https://zhida.zhihu.com/search?content_id=2132061&content_type=Article&match_order=1&q=Kronecker%E7%A7%AF&zhida_source=entity)，$A(m\times n)$ 与 $B(p\times q)$ 的 Kronecker 积是 $A\otimes B = [A_{ij}B]$ ($mp\times nq$)。此式证明见张贤达《矩阵分析与应用》第 107-108 页。
3. **转置**：$\mathrm{vec}(A^T) = K_{mn}\mathrm{vec}(A)$，$A$ 是 $m\times n$ 矩阵，其中 $K_{mn}$ ($mn\times mn$) 是[交换矩阵](https://zhida.zhihu.com/search?content_id=2132061&content_type=Article&match_order=1&q=%E4%BA%A4%E6%8D%A2%E7%9F%A9%E9%98%B5&zhida_source=entity) (commutation matrix)，将按列优先的向量化变为按行优先的向量化。例如：
    $$
    K_{22} = \begin{bmatrix}1 & 0 & 0& 0 \\ 0& 0& 1& 0 \\ 0& 1& 0& 0 \\ 0& 0 &0 & 1\end{bmatrix}, \quad \mathrm{vec}(A^T)= \begin{bmatrix} A_{11} \\ A_{12} \\ A_{21} \\ A_{22}\end{bmatrix}, \quad \mathrm{vec}(A)=\begin{bmatrix} A_{11} \\ A_{21} \\ A_{12} \\ A_{22}\end{bmatrix}
    $$
4. **逐元素乘法**：$\mathrm{vec}(A\odot X) = \mathrm{diag}(A)\mathrm{vec}(X)$，其中 $\mathrm{diag}(A)$ ($mn\times mn$) 是用 $A$ 的元素（按列优先）排成的对角阵。

观察一下可以断言，**若矩阵函数 $F$ 是矩阵 $X$ 经加减乘法、逆、行列式、逐元素函数等运算构成，则使用相应的运算法则对 $F$ 求微分，再做向量化并使用技巧将其它项交换至 $\mathrm{vec}(dX)$ 左侧，对照导数与微分的联系 $\mathrm{vec}(dF) = \frac{\partial F}{\partial X}^T \mathrm{vec}(dX)$，即能得到导数。**

**特别地，若矩阵退化为向量，对照导数与微分的联系 $d\boldsymbol{f} = \frac{\partial \boldsymbol{f} }{\partial \boldsymbol{x} }^T d\boldsymbol{x}$，即能得到导数。**

再谈一谈复合：假设已求得 $\frac{\partial F}{\partial Y}$，而 $Y$ 是 $X$ 的函数，如何求 $\frac{\partial F}{\partial X}$ 呢？从导数与微分的联系入手，$\mathrm{vec}(dF) = \frac{\partial F}{\partial Y}^T\mathrm{vec}(dY) = \frac{\partial F}{\partial Y}^T\frac{\partial Y}{\partial X}^T\mathrm{vec}(dX)$，可以推出链式法则：
$$
\frac{\partial F}{\partial X} = \frac{\partial Y}{\partial X}\frac{\partial F}{\partial Y}
$$

和标量对矩阵的导数相比，矩阵对矩阵的导数形式更加复杂，从不同角度出发常会得到形式不同的结果。有一些 Kronecker 积和交换矩阵相关的恒等式，可用来做等价变形：

1. $(A\otimes B)^T = A^T \otimes B^T$。
2. $\mathrm{vec}(\boldsymbol{ab}^T) = \boldsymbol{b}\otimes\boldsymbol{a}$。
3. $(A\otimes B)(C\otimes D) = (AC)\otimes (BD)$。可以对 $F = D^TB^TXAC$ 求导来证明，一方面，直接求导得到 $\frac{\partial F}{\partial X} = (AC) \otimes (BD)$；另一方面，引入 $Y = B^T X A$，有 $\frac{\partial F}{\partial Y} = C \otimes D, \frac{\partial Y}{\partial X} = A \otimes B$，用链式法则得到 $\frac{\partial F}{\partial X} = (A\otimes B)(C \otimes D)$。
4. $K_{mn} = K_{nm}^T, K_{mn}K_{nm} = I$。
5. $K_{pm}(A\otimes B) K_{nq} = B\otimes A$，$A$ 是 $m\times n$ 矩阵，$B$ 是 $p\times q$ 矩阵。可以对 $AXB^T$ 做向量化来证明，一方面，$\mathrm{vec}(AXB^T) = (B\otimes A)\mathrm{vec}(X)$；另一方面，$\mathrm{vec}(AXB^T) = K_{pm}\mathrm{vec}(BX^TA^T) = K_{pm}(A\otimes B)\mathrm{vec}(X^T) = K_{pm}(A\otimes B) K_{nq}\mathrm{vec}(X)$。

接下来演示一些算例。

### 例 1

> [!question] 
> 
> $F = AX$， $X$ 是 $m\times n$ 矩阵，求 $\frac{\partial F}{\partial X}$。

**解**：先求微分：$dF=AdX$，再做向量化，使用矩阵乘法的技巧，注意在 $dX$ 右侧添加单位阵：
$$
\mathrm{vec}(dF) = \mathrm{vec}(AdX) = (I_n\otimes A)\mathrm{vec}(dX)
$$
对照导数与微分的联系得到 $\frac{\partial F}{\partial X} = I_n\otimes A^T$。

*特例*：如果 $X$ 退化为向量，即 $\boldsymbol{f} = A \boldsymbol{x}$，则根据向量的导数与微分的关系 $d\boldsymbol{f} = \frac{\partial \boldsymbol{f}}{\partial \boldsymbol{x}}^T d\boldsymbol{x}$，得到 $\frac{\partial \boldsymbol{f}}{\partial \boldsymbol{x}} = A^T$。

### 例 2

> [!question]
> 
> $f = \log |X|$，$X$ 是 $n\times n$ 矩阵，求 $\nabla_X f$ 和 $\nabla^2_X f$。

**解**：使用上篇中的技术可求得 $\nabla_X f = X^{-1T}$。为求 $\nabla^2_X f$，先求微分：
$$
d\nabla_X f = -(X^{-1}dXX^{-1})^T
$$
再做向量化，使用转置和矩阵乘法的技巧：
$$
\mathrm{vec}(d\nabla_X f)= -K_{nn}\mathrm{vec}(X^{-1}dX X^{-1}) = -K_{nn}(X^{-1T}\otimes X^{-1})\mathrm{vec}(dX)
$$
对照导数与微分的联系，得到 $\nabla^2_X f = -K_{nn}(X^{-1T}\otimes X^{-1})$，注意它是对称矩阵。在 $X$ 是对称矩阵时，可简化为 $\nabla^2_X f = -X^{-1}\otimes X^{-1}$。

### 例 3

> [!question] 
> 
> $F = A\exp(XB)$，$A$ 是 $l\times m$ 矩阵，$X$ 是 $m\times n$ 矩阵，$B$ 是 $n\times p$ 矩阵，exp 为逐元素函数，求 $\frac{\partial F}{\partial X}$。

**解**：先求微分：
$$
dF = A(\exp(XB)\odot (dXB))
$$
再做向量化，使用矩阵乘法的技巧：
$$
\mathrm{vec}(dF) = (I_p\otimes A)\mathrm{vec}(\exp(XB)\odot (dXB))
$$
再用逐元素乘法的技巧：
$$
\mathrm{vec}(dF) = (I_p \otimes A) \mathrm{diag}(\exp(XB))\mathrm{vec}(dXB)
$$
再用矩阵乘法的技巧：
$$
\mathrm{vec}(dF) = (I_p\otimes A)\mathrm{diag}(\exp(XB))(B^T\otimes I_m)\mathrm{vec}(dX)
$$
对照导数与微分的联系得到 $\frac{\partial F}{\partial X} = (B\otimes I_m)\mathrm{diag}(\exp(XB))(I_p\otimes A^T)$。

### 例 4【一元 logistic 回归】

> [!question] 
> 
> $l = -y \boldsymbol{x}^T \boldsymbol{w} + \log(1 + \exp(\boldsymbol{x}^T\boldsymbol{w}))$，求 $\nabla_\boldsymbol{w} l$ 和 $\nabla^2_\boldsymbol{w} l$。其中 $y$ 是取值 0 或 1 的标量，$\boldsymbol{x},\boldsymbol{w}$ 是 $n\times 1$ 列向量。

**解**：使用上篇中的技术可求得 $\nabla_\boldsymbol{w} l = \boldsymbol{x}(\sigma(\boldsymbol{x}^T\boldsymbol{w}) - y)$，其中 $\sigma(a) = \frac{\exp(a)}{1+\exp(a)}$ 为 [sigmoid 函数](https://zhida.zhihu.com/search?content_id=2132061&content_type=Article&match_order=1&q=sigmoid%E5%87%BD%E6%95%B0&zhida_source=entity)。为求 $\nabla^2_\boldsymbol{w} l$，先求微分：
$$
d\nabla_\boldsymbol{w} l = \boldsymbol{x} \sigma'(\boldsymbol{x}^T\boldsymbol{w})\boldsymbol{x}^T d\boldsymbol{w}
$$
其中 $\sigma'(a) = \frac{\exp(a)}{(1+\exp(a))^2}$ 为 sigmoid 函数的导数，对照导数与微分的联系，得到 $\nabla_w^2 l = \boldsymbol{x}\sigma'(\boldsymbol{x}^T\boldsymbol{w})\boldsymbol{x}^T$。

**推广**：样本 $(\boldsymbol{x}_1, y_1), \dots, (\boldsymbol{x}_N,y_N)$，
$$
l = \sum_{i=1}^N \left(-y_i \boldsymbol{x}_i^T\boldsymbol{w} + \log(1+\exp(\boldsymbol{x_i}^T\boldsymbol{w}))\right)
$$
求 $\nabla_w l$ 和 $\nabla^2_w l$。有两种方法，解 1：先对每个样本求导，然后相加；解 2：定义矩阵 $X = \begin{bmatrix}\boldsymbol{x}_1^T \\ \vdots \\ \boldsymbol{x}_N^T \end{bmatrix}$，向量 $\boldsymbol{y} = \begin{bmatrix}y_1 \\ \vdots \\ y_N\end{bmatrix}$，将 $l$ 写成矩阵形式：
$$
l = -\boldsymbol{y}^T X\boldsymbol{w} + \boldsymbol{1}^T\log(\boldsymbol{1} + \exp(X\boldsymbol{w}))
$$
进而可以使用上篇中的技术求得 $\nabla_\boldsymbol{w} l = X^T(\sigma(X\boldsymbol{w}) - \boldsymbol{y})$。为求 $\nabla^2_\boldsymbol{w} l$，先求微分，再用逐元素乘法的技巧：
$$
d\nabla_\boldsymbol{w} l = X^T (\sigma'(X\boldsymbol{w})\odot (X d\boldsymbol{w})) = X^T \text{diag}(\sigma'(X\boldsymbol{w}))Xd\boldsymbol{w}
$$
对照导数与微分的联系，得到 $\nabla_w^2 l = X^T\text{diag}(\sigma'(X\boldsymbol{w}))X$。

### 例 5【多元 logistic 回归】

> [!question] 
> 
> $l = -\boldsymbol{y}^T\log \text{softmax}(W\boldsymbol{x}) = -\boldsymbol{y}^TW\boldsymbol{x} + \log(\boldsymbol{1}^T\exp(W\boldsymbol{x}))$，求 $\nabla_W l$ 和 $\nabla^2_W l$。其中 $\boldsymbol{y}$ 是除一个元素为 1 外其它元素为 0 的 $m\times 1$ 列向量，$W$ 是 $m\times n$ 矩阵，$\boldsymbol{x}$ 是 $n\times 1$ 列向量，$l$ 是标量。

**解**：上篇中已求得 $\nabla_W l = (\text{softmax}(W\boldsymbol{x})-\boldsymbol{y})\boldsymbol{x}^T$。为求 $\nabla^2_W l$，先求微分：定义 $\boldsymbol{a} = W\boldsymbol{x}$，
$$
\begin{aligned}
d\nabla_W l &= \left(\frac{\exp(\boldsymbol{a})\odot d\boldsymbol{a}}{\boldsymbol{1}^T\exp(\boldsymbol{a})} - \frac{\exp(\boldsymbol{a}) (\boldsymbol{1}^T(\exp(\boldsymbol{a})\odot d\boldsymbol{a}))}{(\boldsymbol{1}^T\exp(\boldsymbol{a}))^2}\right) \boldsymbol{x}^T \\
&= \left( \frac{\text{diag}(\exp(\boldsymbol{a}))}{\boldsymbol{1}^T\exp(\boldsymbol{a})} - \frac{\exp(\boldsymbol{a})\exp(\boldsymbol{a})^T}{(\boldsymbol{1}^T\exp(\boldsymbol{a}))^2} \right)d\boldsymbol{a} \boldsymbol{x}^T \\
&=\left(\text{diag}(\text{softmax}(\boldsymbol{a})) - \text{softmax}(\boldsymbol{a})\text{softmax}(\boldsymbol{a})^T\right)d\boldsymbol{a} \boldsymbol{x}^T
\end{aligned}
$$
注意这里化简去掉逐元素乘法，第一项中 $\exp(\boldsymbol{a})\odot d\boldsymbol{a} = \text{diag}(\exp(\boldsymbol{a})) d\boldsymbol{a}$，第二项中 $\boldsymbol{1}^T(\exp(\boldsymbol{a})\odot d\boldsymbol{a}) = \exp(\boldsymbol{a})^Td\boldsymbol{a}$。定义矩阵 $D(\boldsymbol{a}) = \text{diag}(\text{softmax}(\boldsymbol{a})) - \text{softmax}(\boldsymbol{a})\text{softmax}(\boldsymbol{a})^T$，
$$
d\nabla_W l =D(\boldsymbol{a})d\boldsymbol{a}\boldsymbol{x}^T = D(W\boldsymbol{x})dW \boldsymbol{x}\boldsymbol{x}^T
$$
做向量化并使用矩阵乘法的技巧，得到 $\nabla^2_W l = (\boldsymbol{x}\boldsymbol{x}^T) \otimes D(W\boldsymbol{x})$。

## 总结

**最后做个总结**。我们发展了从 **整体** 出发的矩阵求导的技术，**导数与微分的联系是计算的枢纽**：

- 标量对矩阵的导数与微分的联系是 $df = \mathrm{tr}(\nabla_X^T f dX)$，先对 $f$ 求微分，再使用迹技巧可求得导数。
    - 特别地，标量对向量的导数与微分的联系是 $df = \nabla^T_{\boldsymbol{x}}f d\boldsymbol{x}$。
- 矩阵对矩阵的导数与微分的联系是 $\mathrm{vec}(dF) = \frac{\partial F}{\partial X}^T \mathrm{vec}(dX)$，先对 $F$ 求微分，再使用向量化的技巧可求得导数。
    - 特别地，向量对向量的导数与微分的联系是 $d\boldsymbol{f} = \frac{\partial \boldsymbol{f}}{\partial \boldsymbol{x}}^Td\boldsymbol{x}$。

**参考资料**：
1. 张贤达. *矩阵分析与应用*. 清华大学出版社有限公司, 2004.
2. Fackler, Paul L. "Notes on matrix calculus." *North Carolina State University* (2005).
3. Petersen, Kaare Brandt, and Michael Syskind Pedersen. "The matrix cookbook." *Technical University of Denmark* 7 (2008): 15.
4. HU, Pili. "Matrix Calculus: Derivation and Simple Application." (2012).
5. Magnus, Jan R., and Heinz Neudecker. "Matrix Differential Calculus with Applications in Statistics and Econometrics." Wiley, 2019.