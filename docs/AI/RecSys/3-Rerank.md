# 重排

粗排和精排后都可以有对应的后处理提高推荐内容效果（其中精排后的后处理一般被称为重排）。

![re-rank](https://raw.githubusercontent.com/darstib/public_imgs/utool/2509/02_250902-214412.png)

后处理时不仅是选取综合得分最高的物品，还期望保有一定的多样性以提高用户体验。在每一个阶段都有对应的技巧保留物品的多样性，具体可见 [Improvement_04](https://github.com/wangshusen/RecommenderSystem/blob/main/Slides/08_Improvement_04.pdf)。

## Maximal Marginal Relevance (MMR)

精排给 𝑛 个候选物品打分，融合之后的分数为 $[r_{1}, r_{2}, \dots, r_{n}]$。

参考于其他聚类相关算法，我们将已经选中的物品记为 S，未选中物品记为 R；初始化时将融合分数最高的物品放入 S ，其它物品保留在 R 中。

对于 R 中的每一个物品计算 Marginal Relevance 分数（$\theta$ 为超参数）

$$\mathrm{MR}_i=\theta\cdot\mathrm{r}_i-(1-\theta)\cdot\max_{j\in\mathcal{S}}\mathrm{~sim}(i,j)$$

即将与已选物品的相似程度作为罚项；取其最大者 $\underset{i\in\mathbb{R}}{\operatorname*{argmax}}\mathrm{MR}_i$ 加入 S，直到 S 中物品数量足够。

## Determinantal Point Process (DPP)

> [!info]- 超平行体
> 
> 在以 $[v_{1}, v_{2}, \dots, v_{n}], v_{i} \in \mathbb{R}^{d}$ 为基的欧氏空间中，超平行体是 $u = \alpha_{1}v_{1} + \alpha_{2}v_{2}+ \dots + \alpha_{n}v_{n}, \alpha_{i} \in [0, 1]$ 所构成的区域（显然需要 $k \leq d$）：
> 
> $$
> \mathcal{P}(\boldsymbol{v}_1,\cdots,\boldsymbol{v}_k)=\{\alpha_1\boldsymbol{v}_1+\cdots+\alpha_k\boldsymbol{v}_k\mid0\leq\alpha_1,\cdots,\alpha_k\leq1\}
> $$
> 
> 在二维空间中，超平行体是一个平行四边形。

假设我们现在将 k 个物品表征为 d 维的单位向量，计算构成的超平面体的**体积** $vol(\mathcal{P}(\boldsymbol{v}_1,\cdots,\boldsymbol{v}_k))$；当物品向量两两正交时体积最大，当物品向量线性相关时体积为 0，即物品相似度较高。基于数学推导可以得到（基于 $k\leq d$）：

$$
\det(V^TV)=\mathrm{~vol}(\mathcal{P}(v_1,\cdotp\cdotp\cdotp,v_k))^2
$$

也即可以得到：一组物品向量组成的矩阵 $V$ ，那么 $V^{T}V$ 的行列式大小反映了这组物品向量内部的相似关系；使用 $V_{\mathcal{S}}$ 表示由 $\mathcal{S}$ 中物品的向量构成的矩阵，那么有：

$$
\underset{\mathcal{S}:|\mathcal{S}|=k}{\operatorname*{argmax}}\quad\theta\cdot\left(\sum_{j\in\mathcal{S}}\text{r}_j\right)+(1-\theta)\cdot\log\det(\boldsymbol{V}_S^T\boldsymbol{V}_S)
$$

这是一个组合优化算法，属于 NP-Hard 算法，业界使用贪心算法（可以发现和 MMR 的迭代过程一致，只是改了相似度罚项）；使用 $A_{S} := V^{T}_{S}V_{S}$：

$$
\operatorname*{argmax}_{i\in\mathcal{R}}
\Bigl( \theta \cdot \operatorname{r}_i
+ (1-\theta)\cdot\log\det(A_{\delta\cup\{i\}}) \Bigr)
$$

> [!extra]- DPP 求解
>
> 上述公式中最大的难点在于大矩阵的行列式求解困难。暴力求解 $\det(A_{S \cup \{i\}})$ 需要 $O(|S|^{3})$ 复杂度，从 n 个物品中选取 k 个物品的时间复杂度将达到 $O(nk^{4})$；加上计算 A 本身需要 $O(n^{2}d)$，总时间复杂度为 $O(n^{2}d + nk^{4})$ 。
>
> Hulu 设计了一种数值算法，基于 Cholesky 分解，每一轮分解能够利用上一轮分解结果，最终将整体时间复杂度加快到了 $O(n^{2}d + nk^{2})$。
> 
> 基于 Gram-

## 业务规则约束和滑动窗口

在实际业务中可能依据经验需要遵循一些其他的规则。在重排时，规则优先于 MMR/DPP 算法；即每一轮先使用规则将部分 R 中物品剔除得到 R'，再寻找 MR 最大的未选物品。

- 最多连续出现 k 项同一类型的物品
	- 避免物品类型过于单一
- 每 k 项至多出现 1 项某类物品
	- 例如因运营等导致某类物品的推荐系数提高
	- 这类物品不应该出现过多，因为实际会影响用户体验
- 前 t 项至多出现 k 项某类物品
	- 在推送时前 t 项往往是用户一眼能看到的物品
	- 不适合出现过多运营推广内容

当 S 较大而没达到数量要求时，可能所有未选物品与已选物品之一的相似度都非常高，几乎所有物品 i 的 $\max sim(i, j)$ 都接近 1，MMR 算法失效。

解决方案是做出妥协，在计算 $\max sim(i, j)$ 时 j 不再是 S 中的所有物品，而是一个窗口 W 中的物品（一般取最近加入 S 的若干物品），即认为可以与较早加入的物品有较高的相似度。
