---
tags:
  - notes
comments: true
---

> [!quote] 参考《统计学习方法》的第一章和[机器学习方法概论](https://www.huaxiaozhuan.com/%E7%BB%9F%E8%AE%A1%E5%AD%A6%E4%B9%A0/chapters/0_introduction.html)

在《统计学习方法》的第一章第一节第一段中声明：统计学习（statistical learning）是关于计算机基于数据构建概率统计模型并运用模型对数据进行预测与分析的一门学科。统计学习也称为统计机器学习（statistical machine learning）。所以下面我不具体区分统计学习和机器学习了，暂且认为在后续笔记中二者等价。

## 统计机器学习

赫尔伯特•西蒙（Herbert A. Simon）曾对“学习”给出以下定义：“如果一个系统能够通过执行某个过程改进它的性能，这就是学习。” 后续介绍的就是系统学习的**方法**。

在统计机器学习中，研究的对象是**数据**，研究的方法具有三要素：**模型、策略、算法**。

## 模型

学习条件概率分布 $P(Y|X)$ 或决策函数 $f(X)$，它们构成了假设空间。

- 线性模型举例：感知机，k 近邻，k 均值，线性支持向量机
- 非线性模型举例：基于核函数的支持向量机，深度学习

- 参数化模型：假设模型参数的维度固定，模型可以由有限维参数完全刻画。
- 非参数化模型：假设模型参数的维度不固定或者无穷大，随着训练数据量的增加不断增大。

- 在线学习（online learning）
- 批量学习（batch learning）/离线学习（offline learning）

- 生成模型：如贝叶斯学习（Bayesian learning）
- 判别模型：如核方法（Kernel method）

- 监督学习：分类问题、标注问题、回归问题
- 无监督学习；

## 策略

从假设空间中选取最优模型的准则。

- **数据 (Data):** 假设我们有一个训练数据集 $D = \{(x_1, y_1), (x_2, y_2), \dots, (x_N, y_N)\}$，其中每个样本 $(x_i, y_i)$ 都是从一个未知的真实数据联合分布 $P(x, y)$ 中独立同分布 (i.i.d.) 采样得到的。
- **模型 (Model):** 我们的目标是学习一个假设函数 $f(x; \theta)$，它由参数 $\theta$ 决定，用来预测输入 $x$ 对应的输出 $y$。
- **损失函数 (Loss Function):** $L(y, f(x; \theta))$ 是一个非负实值函数，用于量化预测值 $f(x; \theta)$ 与真实值 $y$ 之间的差异。损失越小，代表模型预测得越好。

### 风险最小化框架 (Risk Minimization)

风险最小化框架的目标是找到一个最优的参数 $\theta$，使得模型的损失最小。

#### 期望风险 (Expected Risk)

期望风险是指模型在 **所有可能的数据（真实数据分布）** 上的平均损失。这是我们理论上最想最小化的目标。

$$
R_{exp}(\theta) = E_{(x,y) \sim P(x,y)}[L(y, f(x; \theta))] = \int_{X \times Y} L(y, f(x; \theta)) P(x, y) \,dx\,dy
$$

- **核心问题:** 真实分布 $P(x, y)$ 是未知的，所以期望风险无法直接计算。

#### 经验风险 (Empirical Risk)

由于无法计算期望风险，我们退而求其次，使用已有的 **训练数据** 上的平均损失来近似它。

$$
R_{emp}(\theta) = \frac{1}{N} \sum_{i=1}^{N} L(y_i, f(x_i; \theta))
$$

- **经验风险最小化 (Empirical Risk Minimization, ERM):** 寻找使经验风险最小的参数 $\theta$ 的原则。
    $$
    \hat{\theta}_{ERM} = \arg\min_{\theta} R_{emp}(\theta)
    $$
- **核心问题:** 当模型复杂度过高或数据量不足时，ERM 容易导致 **过拟合 (Overfitting)**。模型在训练集上表现完美，但在未见过的测试集上表现很差。

#### 结构风险 (Structural Risk)

为了解决过拟合问题，在经验风险的基础上增加了一个代表模型复杂度的 **正则化项 (Regularizer)** 或 **惩罚项 (Penalty Term)**，构成了结构风险。

$$
R_{srm}(\theta) = R_{emp}(\theta) + \lambda J(\theta) = \frac{1}{N} \sum_{i=1}^{N} L(y_i, f(x_i; \theta)) + \lambda J(\theta)
$$

- **结构风险最小化 (Structural Risk Minimization, SRM):** 寻找使结构风险最小的参数 $\theta$ 的原则。
    $$
    \hat{\theta}_{SRM} = \arg\min_{\theta} R_{srm}(\theta)
    $$

- $J(\theta)$ 是一个关于模型参数 $\theta$ 的函数，$\theta$ 越复杂，$J(\theta)$ 的值越大。例如，$L_2$ 正则化项 $J(\theta) = ||\theta||_2^2$。
- $\lambda$ 是一个超参数，用于权衡经验风险和模型复杂度。

### 概率估计框架 (Probabilistic Estimation)

概率估计框架将模型学习看作一个参数估计问题，目标是找到最能解释观测数据的参数 $\theta$。

#### 极大似然估计 (Maximum Likelihood Estimation, MLE)

MLE 的目标是寻找参数 $\theta$，使得 **观测到的数据出现的概率最大**。它假设参数 $\theta$ 是一个未知的固定值。

- **似然函数 (Likelihood):** 假设数据点之间独立同分布，给定参数 $\theta$ 时，整个数据集 $D$ 的似然函数是：
    
    $$P(D|\theta) = \prod_{i=1}^{N} P(y_i|x_i; \theta)
    $$
- 为了计算方便，通常最大化对数似然函数 (Log-Likelihood):
    $$
    \mathcal{L}(\theta) = \log P(D|\theta) = \sum_{i=1}^{N} \log P(y_i|x_i; \theta)
    $$
- **MLE 估计量:**
    
    $$\hat{\theta}_{MLE} = \arg\max_{\theta} \mathcal{L}(\theta) = \arg\max_{\theta} \sum_{i=1}^{N} \log P(y_i|x_i; \theta)
    $$

#### 最大后验估计 (Maximum a Posteriori, MAP)

MAP 不仅考虑数据的似然性，还引入了关于参数 $\theta$ 的 **先验知识 (Prior Knowledge)**。它假设参数 $\theta$ 本身也服从一个分布 $g(\theta)$。MAP 的目标是找到在观测到数据后，**后验概率 $P(\theta|D)$ 最大的参数**。

- 根据贝叶斯定理 (Bayes' Theorem):
    $$
    P(\theta|D) = \frac{P(D|\theta)g(\theta)}{P(D)}
    $$
- 其中 $P(D)$ 与 $\theta$ 无关，因此最大化后验概率等价于最大化分子：
    $$
    \hat{\theta}_{MAP} = \arg\max_{\theta} P(\theta|D) = \arg\max_{\theta} P(D|\theta)g(\theta)
    $$
- 同样，我们可以最大化其对数形式：
    $$
    \hat{\theta}_{MAP} = \arg\max_{\theta} (\log P(D|\theta) + \log g(\theta)) = \arg\max_{\theta} \left( \sum_{i=1}^{N} \log P(y_i|x_i; \theta) + \log g(\theta) \right)
    $$

### 建立对应关系与证明

现在我们将风险最小化和概率估计联系起来。核心思想是：**通过选择特定的损失函数 $L$ 和正则化项 $J$，可以使风险最小化等价于概率估计。**

#### 经验风险最小化 (ERM) $\iff$ 极大似然估计 (MLE)

**结论:** 当我们选择 **损失函数为负对数似然函数** 时，经验风险最小化就等价于极大似然估计。

**证明:**

将 MLE 的目标转换为一个最小化问题：

$$
\hat{\theta}_{MLE} = \arg\max_{\theta} \sum_{i=1}^{N} \log P(y_i|x_i; \theta) = \arg\min_{\theta} \left( -\sum_{i=1}^{N} \log P(y_i|x_i; \theta) \right)
$$

现在，我们来看 ERM 的目标：

$$
\hat{\theta}_{ERM} = \arg\min_{\theta} \frac{1}{N} \sum_{i=1}^{N} L(y_i, f(x_i; \theta))
$$

如果我们定义损失函数为负对数似然：

$$
L(y_i, f(x_i; \theta)) := -\log P(y_i|x_i; \theta)
$$

那么 ERM 的目标就变为：

$$
\hat{\theta}_{ERM} = \arg\min_{\theta} \frac{1}{N} \sum_{i=1}^{N} (-\log P(y_i|x_i; \theta)) = \arg\min_{\theta} \left( -\frac{1}{N} \sum_{i=1}^{N} \log P(y_i|x_i; \theta) \right)
$$

由于 $1/N$ 是一个正的常数，最小化上式等价于最小化括号内的求和项，这与 MLE 的最小化形式完全相同。

> [!example]+ **示例:** 在线性回归中，假设噪声服从均值为0、方差为 $\sigma^2$ 的高斯分布，即 $y \sim \mathcal{N}(f(x;\theta), \sigma^2)$。
> 
> $$P(y_i|x_i; \theta) = \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(y_i - f(x_i; \theta))^2}{2\sigma^2}\right)$$
> 
> 其负对数似然损失为：
> 
> $$-\log P(y_i|x_i; \theta) = \frac{(y_i - f(x_i; \theta))^2}{2\sigma^2} + \text{const}$$
> 
> 最小化这个损失，就等价于最小化 **平方误差损失 (Squared Error Loss)**。因此，在线性回归中，最小二乘法（ERM 的一种）等价于高斯噪声假设下的极大似然估计。

#### 结构风险最小化 (SRM) $\iff$ 最大后验估计 (MAP)

**结论:** 当我们选择 **损失函数为负对数似然函数**，并且 **正则化项为负对数先验** 时，结构风险最小化就等价于最大后验估计。

**证明:**

将 MAP 的目标转换为一个最小化问题：

$$
\hat{\theta}_{MAP} = \arg\max_{\theta} \left( \sum_{i=1}^{N} \log P(y_i|x_i; \theta) + \log g(\theta) \right) = \arg\min_{\theta} \left( -\sum_{i=1}^{N} \log P(y_i|x_i; \theta) - \log g(\theta) \right)
$$

现在，我们来看 SRM 的目标：

$$
\hat{\theta}_{SRM} = \arg\min_{\theta} \left( \sum_{i=1}^{N} L(y_i, f(x_i; \theta)) + \tilde{\lambda} J(\theta) \right)
$$

(这里用 $\tilde{\lambda}$ 是为了和前面公式的 $\lambda$ 区分，因为 $\lambda=1/N$)

如果我们定义：

1.  **损失函数:** $L(y_i, f(x_i; \theta)) := -\log P(y_i|x_i; \theta)$
2.  **正则化项:** $J(\theta) := -\log g(\theta)$

那么 SRM 的目标就变为：

$$
\hat{\theta}_{SRM} = \arg\min_{\theta} \left( \sum_{i=1}^{N} (-\log P(y_i|x_i; \theta)) + \tilde{\lambda} (-\log g(\theta)) \right)
$$

当超参数 $\tilde{\lambda}=1$ 时，上式与 MAP 的最小化形式完全相同。因此，MAP 估计可以被看作是正则化的极大似然估计，也等价于一种特殊的结构风险最小化。

> [!example]- 正则化项示例:
> 
> - **L2 正则化 (Ridge Regression):** 如果参数的先验分布 $g(\theta)$ 是一个均值为0的高斯分布 $g(\theta) \sim \mathcal{N}(0, \alpha^2 I)$，那么负对数先验 $-\log g(\theta) = \frac{1}{2\alpha^2}||\theta||_2^2 + \text{const}$。这正好对应了 $L_2$ 正则化项。
> - **L1 正则化 (Lasso):** 如果参数的先验分布 $g(\theta)$ 是一个拉普拉斯分布 (Laplace Distribution)，那么负对数先验 $-\log g(\theta)$ 正好对应了 $L_1$ 正则化项 $||\theta||_1$。

#### 期望风险最小化 (ERM) $\iff$ 后验概率最大化 (Bayesian Estimation)

“后验概率最大化” 通常就是指 **MAP**；然而，一个完整的 **贝叶斯估计 (Bayesian Estimation)** 观点与 MAP 是不同的。贝叶斯方法并不寻求一个单一的点估计 $\hat{\theta}$，而是计算参数的 **完整后验分布** $P(\theta|D)$。在做预测时，它会通过积分（或求和）来考虑所有可能的参数值，并用后验概率加权：

**后验预测分布 (Posterior Predictive Distribution):**

$$
P(y_{new}|x_{new}, D) = \int P(y_{new}|x_{new}, \theta) P(\theta|D) \,d\theta
$$

这种方法通过模型平均，更充分地利用了后验信息，是比 MAP 更彻底的贝叶斯方法，通常能提供更好的不确定性估计和更强的抗过拟合能力。

### 总结与辨析

|        框架         |                        目标函数                        |                       对应关系                       | 核心思想                         |
| :---------------: | :------------------------------------------------: | :----------------------------------------------: | :--------------------------- |
| **经验风险最小化 (ERM)** |      $R_{emp} = \frac{1}{N}\sum L(y_i, f_i)$       |                 **极大似然估计 (MLE)**                 | 最小化训练集上的平均损失                 |
| **结构风险最小化 (SRM)** |      $R_{srm} = R_{emp} + \lambda J(\theta)$       |                 **最大后验估计 (MAP)**                 | 在最小化训练损失的同时，惩罚模型复杂度以防过拟合     |
| **极大似然估计 (MLE)**  |          $\sum \log P(y_i\|x_i; \theta)$           |             **ERM** (当$L = -\log P$)             | 找最能解释观测数据的参数                 |
| **最大后验估计 (MAP)**  | $\sum \log P(y_i \| x_i; \theta) + \log g(\theta)$ | **SRM** (当 $L = -\log P$, $J = -\log g(\theta)$) | 结合数据和先验知识，找到后验概率最大的参数        |
|     **贝叶斯估计**     |               $P(\theta\|D)$ (整个分布)                |                     (无直接对应)                      | 不找单一最优参数，而是计算参数的完整后验分布，并用于预测 |

## 算法

- [数值计算](https://www.huaxiaozhuan.com/%E6%95%B0%E5%AD%A6%E5%9F%BA%E7%A1%80/chapters/3_numerical_computaion.html)
