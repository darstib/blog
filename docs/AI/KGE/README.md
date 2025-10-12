---
comments: true
---

# Knowledge Graph Embedding

知识图谱嵌入 (Knowledge Graph Embedding, KGE) 是知识图谱研究的一个子反向，其目标是将知识图谱中的实体和关系嵌入到一个连续的向量空间中，而得到的这些嵌入向量可以被用在很多知识图谱的子任务中，比如知识图谱补全。

基本思路是：

1. 基于观测**事实**（fact，实体-关系-实体三元组，一般使用 $\mathbb{D}^{+}=\{(h, r, t)\}$）表示实体和关系
2. 学习一个**评估函数** $f_{r}(h, t)$ 来衡量事实的**合理性 (Plausibility)**（其实可以认为是损失函数）
3. 最大化合理性来更新实体和关系的表示

KG 嵌入的方式根据评估函数的不同可以分成**平移距离模型(Translation Distance Model)** 和**语义匹配模型(Semantic Matching Model)** 两种形式。

## 平移距离模型(TDM)

TDM 利用基于距离的评估函数，这类模型将“关系”视为连接两个实体嵌入向量的一个向量（的平移），即 $\vec{r} = \vec{t} - \vec{h}$ 。

### TransE

TransE是最早也是最著名的平移距离模型（之后也有很多变体，如 TransH, TransR），它将实体和关系都用 d 维空间中的向量来表示，并且希望学习到的嵌入向量满足 $\vec{r} = \vec{t} - \vec{h}$，而其评估函数可以表示为（p 一般取 1 或 2）：

$$
f_r(h,t)=-||h+r-t||_p
$$

TransE 的缺点在于只适合处理一对一的关系，而当知识图谱中出现一对多，多对一，多对多的关系的时候，使用这种算法学习到的嵌入向量的表示能力并不好。

> [!help]+ 
> 
> 举个例子，一个父亲 h 可能有多个儿子 $t_{i}$，他们的关系 r 是一样的，按照上面简单的逻辑，所有的 $t_{i}$ 学习得到的 t 将会是完全相同的；
> 
> 又比如，A 是 B 的姐姐，B 是 C 的姐姐，A 也是 C 的姐姐，但是 A 和 B 之间的 r 显然无法和 A 与 C 之间的 r 一致。

> [!note] 一部分改进思路认为将关系放入不同的空间中讨论以面对更加复杂的情况
> 	
> - TransH, TransR, TransD, TranSparse

![https://ieeexplore.ieee.org/document/8047276](https://raw.githubusercontent.com/darstib/public_imgs/utool/2510/12_251012-180855.png)

### TransH

为了解决多元关系上 TransE 的局限性，TransH 提出当实体参与不同的关系时，将其投影嵌入到一个新的空间中。具体而言，为每个关系定义一个超平面（法向量为 $w_{r}$），投影公式为（v 代表 h 和 t）：

$$
v_\perp=v-w_r^Tvw_r
$$

### TransR

TransR 则提出为每个关系建立专门的投影空间，使用矩阵 $M_{r} \in \mathbb{R}^{d\times k}$ 进行线性变换（v 代表 h 和 t）：

$$
v_{\perp} = M_{r}v
$$

### TransD

由于 TransR 中 $M_{r}$ 的参数量较大，TransD 通过用三个映射向量 $w_{h}, w_{r}, w_{t}$ 来构建两个投影矩阵，从而减少参数量：

$$
\begin{aligned}
M_r^{1}=w_rw_h^{T}+I,&\quad M_r^{2}=w_rw_t^{T}+I\\
h_{\perp } = M_{r}^{1}h,&\quad t_{\perp } = M_{r}^{2}t
\end{aligned}
$$

### TranSparse

TranSparse 则通过引入稀疏性约束 $\theta_{r}$ 来控制投影投影矩阵的参数量，具体如下（$M_{r}(\theta_{r})$ 相同时为共享版本）；

$$h_{\perp} = M_r^1(\theta_r^1)h, \quad t_{\perp} = M_r^2(\theta_r^2)t$$

> [!note] 一部分改进思路则认为是 $\vec{r} = \vec{t} - \vec{h}$ 约束过紧了，调整违反约束收到的惩罚
> 
> - TransM, TransF, TransA

### TransM

TransM 提出的思路是为每个关系设定一个权重 $\theta_{r}$，为一对多，多对一，多对多关系赋予较小的权重，也即减小这些关系对训练的影响（把简单关系做好）：

$$
f_r(h,t)=-\theta_r\|\mathbf{h}+\mathbf{r}-\mathbf{t}\|_{p}
$$

### TransF

TransF 则认为只要 r 和 t-h 的反向差不多就行，因此有：

$$
f_r(h,t)=(\mathbf{h}+\mathbf{r})^\top\mathbf{t}+(\mathbf{t}-\mathbf{r})^\top\mathbf{h}.
$$

### TransA

TransA 参考马氏距离，引入了一个新的评估函数（$M_{r}$ 为对称矩阵）：

$$
f_r(h,t)=(|h+r-t|)^TM_r(|h+r-t|)
$$

通过学习 $M_{r}$ 来应对复杂的情况。

> [!note] 还有人认为嵌入太固定了导致无法表达复杂的信息，可以将实体和关系表达为分布来显示建模噪声和多样性
> 
> - KG2E, TransG

### KG2E

KG2E 将每个实体和关系都表示为多元高斯 $N\left( \mu, \Sigma \right)$；此时比较的是 $t-h \sim N(\mu_t-\mu_h,\, \Sigma_t+\Sigma_h)$ 与 $r \sim N(\mu_r,\, \Sigma_r)$ 两个分布的相似度。

相似度用两类度量计算：

1. KL 散度（Kullback-Leibler Divergence，越小越好）
2. 概率积内核（Probability Product Kernel，越大越好）

### TransG

TransG 认为一个关系往往是多义的，于是把关系表示为高斯混合 $r = \sum_i p_i\, \mathcal{N}(\mu^{(i)}_r,\, \sigma^2 I)$，实体仍用各自的高斯（常取各向同性方差）。打分是对各语义分量的加权求和，本质是对多种“平移” $h + \mu^{(i)}_r \approx t$ 的指数式相似度求混合；混合分量的数量与权重可用中餐馆过程自适应学习，从数据中自动发现“一个关系的多种语义”。

> 直观上，Gaussian/混合高斯嵌入能更稳健地处理不完备与噪声数据，并刻画关系多义性；代价是参数更多（如协方差、混合分量）与训练计算更复杂。

### 小结

![](https://raw.githubusercontent.com/darstib/public_imgs/PicGo//PicGo_exe/202510122211651.png)

## 语义匹配模型(SMM)

​SMM 通常使用基于相似度的评估函数，通过计算实体和关系在向量空间中的潜在语义匹配度来评估嵌入向量的合理性。

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2510/12_251012-224554.png)

### RESCAL

RESCAL (a.k.a. the bilinear model) 认为实体用向量表示，关系则直接使用矩阵表示，评估函数是一个双线性函数：

$$
f_r(h,t)=\mathbf{h}^\top\mathbf{M}_r\mathbf{t}=\sum_{i=0}^{d-1}\sum_{j=0}^{d-1}\left[\mathbf{M}_r\right]_{ij}\cdot[\mathbf{h}]_i\cdot[\mathbf{t}]_j
$$

- DistMult 将 $M_{r}$ 约束为一个对角矩阵，显然这只能够处理对称的关系
	- $f_r(h,t)=\mathbf{h}^\top\mathrm{diag}(\mathbf{r})\mathbf{t}=\sum_{i=0}^{d-1}[\mathbf{r}]_i\cdot[\mathbf{h}]_i\cdot[\mathbf{t}]_i$
- Hol