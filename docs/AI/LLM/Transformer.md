> [!quote]
>
> - [x] [从编解码和词嵌入开始，一步一步理解Transformer](https://www.bilibili.com/video/BV1XH4y1T76e)
> - [ ] [Transformer精讲](https://adaning.github.io/posts/6744.html) or [The Illustrated Transformer](https://www.yuque.com/zhangqiang-studyisalifestyle/it-technology/transformer-the-illustrated-transformer) or [The Transformer Blueprint](https://deeprevision.github.io/posts/001-transformer/)
> - [ ] [Hello! · Transformers快速入门](https://transformers.run/)

> [!wiki] [Transformer (deep learning)](https://en.wikipedia.org/wiki/Transformer_(deep_learning))
>
> In [deep learning](https://en.wikipedia.org/wiki/Deep_learning), the **transformer** is an [artificial neural network](https://en.wikipedia.org/wiki/Artificial_neural_network) architecture based on the multi-head [attention](https://en.wikipedia.org/wiki/Attention_(machine_learning)) mechanism, in which text is converted to numerical representations called [tokens](https://en.wikipedia.org/wiki/Large_language_model#Tokenization), and each token is converted into a vector via lookup from a [word embedding](https://en.wikipedia.org/wiki/Word_embedding) table.

![https://deeprevision.github.io/posts/001-transformer/|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773124649411.png)

这篇文章不是针对 [_Attention Is All You Need_](https://arxiv.org/abs/1706.03762) 这篇论文的解读，而是对整个架构的解读；也即，不止会提到论文中使用了什么技术，还会对模块进行分析。

## Embedding and Positional Encoding

> [!info]
>
> - [ ] [Transformer 修炼之道（一）、Input Embedding](https://zhuanlan.zhihu.com/p/372279569)

> 在 NLP 中，常将一类语言经过 **BPE(byte-pair encoding)** 处理后的进行分词得到“子词”(Sub-word)，一般称为 **Token**；Token 将会被根据一张训练得到的映射表被编码为 **Embedding**，以此输入到模型中。在 DL 中普遍用 **Word Embedding** 做词嵌入。

### [todo] Embedding

### Positional Encoding

> [!info]
>
> - [x] [探秘Transformer之（8）--- 位置编码	- 罗西的思考	- 博客园](https://www.cnblogs.com/rossiXYZ/p/18744797#13-%E8%A7%A3%E5%86%B3%E6%80%9D%E8%B7%AF)（非常细致）
> - [x] [Transformer学习笔记一：Positional Encoding（位置编码）](https://zhuanlan.zhihu.com/p/454482273)（相对精简）
> - [ ] [Transformer中的位置编码(Position Encoding)	- 郑之杰的个人网站](https://0809zheng.github.io/2022/07/01/posencode.html)
> - [ ] [让研究人员绞尽脑汁的Transformer位置编码](https://kexue.fm/archives/8130)

在 Transformer 中，Input/Target sequence 在进行词嵌入后，还需要加上一个 positional encoding（即位置编码或者说位置嵌入）。Transformer 为了捕捉长序列上的语义关系和并行化处理，舍弃了顺序处理序列的模式；在后面学习注意力机制的时候，会发现 Attention 过程中，对序列中的每个 token 都是池化操作（即位置无关的，证明过程可见[探秘Transformer之（8）--- 位置编码](https://www.cnblogs.com/rossiXYZ/p/18744797#%E4%BD%8D%E7%BD%AE%E4%B8%8D%E5%8F%98%E6%80%A7)）；所以在训练的过程中丢失了位置信息。

而在 NLP 任务中，语序是非常重要的。~~看来 Attention is not all you need。~~

> [!quote] [探秘Transformer之（8）--- 位置编码	- 罗西的思考	- 博客园](https://www.cnblogs.com/rossiXYZ/p/18744797#13-%E8%A7%A3%E5%86%B3%E6%80%9D%E8%B7%AF)
>
> 既然 Transformer 中的自注意力机制无法捕捉输入元素序列的顺序，因此我们需要对位置关系进行建模，把单词的顺序合并到 Transformer 架构中，从而打破这种置换不变性，于是 Transformer 作者提出了 Position Embedding 的方法，也就是“位置向量”或者说“位置编码”。
>
> 位置编码的作用就是**给每个位置都加上一个唯一的位置编码向量，即将词序信息向量化**。对于输入的每个单词，每个单词都有对应的向量（与位置无关）。为了给每个位置都加上一个唯一的位置编码向量码，需要使用另一个**具有相同维度的向量**，其中每个向量唯一地代表句子中的一个位置。然后通过将词嵌入与其相应的位置嵌入求和来形成 Transformer 层的输入，即输入模型的整个 Embedding 是 Word Embedding 与 Positional Embedding 直接相加之后的结果。模型会将这个结果矩阵作为输入提供给后续层。

> [!info]
>
> - [x] [transformer中使用的position embedding为什么是加法而非concat？](https://www.zhihu.com/question/485476372)

目前而言，位置编码有两大类：

- 绝对位置编码 Absolute Position Encoding (APE)
- 相对位置编码 Relative Position Encoding (RPE)

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/11_1773197037211.png)

在[探秘Transformer之（8）--- 位置编码	- 应具备的性质](https://www.cnblogs.com/rossiXYZ/p/18744797#14-%E5%BA%94%E5%85%B7%E5%A4%87%E7%9A%84%E6%80%A7%E8%B4%A8) 部分结合文献探讨了位置编码的需求和演化，这里进行简要的分析：

### 朴素的想法

- 用整型值作为位置值：第一个 token 标记 1，第二个标记 2……
	 - 优点：简单、计算快
	 - 缺点：如果遇到比训练更长的序列，不利于泛化；长度太大的序列位置值也会很大，对原本的嵌入影响会很大
- 用归一化值作为位置值：第一个 token 标记 0，最后一个标记 1，其余等距划分
	 - 缺点：在长度不同的序列同一位置具备不同的位置编码，相对位置信息不同，混淆了语义信息
- 用二进制作为位置值：考虑位置编码需要与词嵌入结果相加，维度需要为 $D_{in}$
	 - 缺点：位置变化不连续、不一致
	 - 例如 $D_{in}=2$，则位置可以表示为 [0,0]、[0,1]、[1,0]、[1,1]；而 [0, 0] -> [0, 1] 与 [0, 1] -> [1, 0] 在嵌入空间上显然是不同的
- 用三角函数作为位置值：
	 - 回顾上面，我们需要位置编码满足：位置值有界、适应不同长度的序列、位置变化是连续、平滑的，显然将每个分量设置为一个三角函数可以满足
	 - 对于第 $t$ 个 token，可以构造一个由不同频率的 $\sin/\cos$ 分量组成的位置向量
- 在一些文献中对编码提出了额外的要求，进一步将波长拉长、使用 $\sin/\cos$ 交替来表示位置……不过那都是那个领域的研究人员的工作了，下面直接来看 Transformer 中的三角函数式位置编码。

在前面对位置编码的要求逐步提高、逐一候选下，Transformer 的位置编码使用的正是三角函数式位置编码，一般称为 Sinusoidal 位置编码：

记 $t$ 为 token 在序列中的位置，$PE_t \in \mathbb{R}^{D_{in}}$ 表示其位置编码，则第 $i$ 个分量可以表示为：

$$
PE_t^{(i)}=
\begin{cases}
\sin(w_k t), & \text{if } i=2k \\
\cos(w_k t), & \text{if } i=2k+1
\end{cases}
\quad
\text{where } w_k=\frac{1}{10000^{2k/D_{in}}},\ i \in \left\{0, 1, ..., \frac{D_{in}}{2}-1\right\}
$$

这样的编码有一些较好的性质：

- 性质一：两个位置编码的点积(dot product) 仅取决于偏移量 $\Delta t$，也即两个位置编码的点积可以反应出两个位置编码间的相对距离，即 $PE_t^T * PE_{t+\triangle t}=\sum_{i=0}^{\frac{D_{in}}2-1}\cos(w_i\bigtriangleup t)$
 	- 这意味着虽然当前编码的是绝对位置，但是也能从中学习到相对位置信息
- 性质二：位置编码的点积是无向的，即 $PE_t^T * PE_{t+\triangle t}=PE_t^T * PE_{t-\triangle t}$，不难由性质一推出
- 性质三：对于相差较远的两个位置，他们的编码相差也会较大，利于理解和区分词序

## Attention

> [!info]
>
>- [x] [10. 注意力机制 — 动手学深度学习 2.0.0 documentation](https://zh-v2.d2l.ai/chapter_attention-mechanisms/index.html)
>- [x] [神经网络算法	- 一文搞懂Transformer中的三种注意力机制	- 53AI-AI知识库|企业AI知识库|大模型知识库|AIHub](https://www.53ai.com/news/qianyanjishu/1079.html)

### 生物学中的注意力提示

“是否包含自主性提示”将注意力机制与全连接层或汇聚层区别开来。在注意力机制的背景下，自主性提示被称为查询（query）。给定任何查询，注意力机制通过注意力汇聚（attention pooling）将选择引导至感官输入（sensory inputs，例如中间特征表示）。在注意力机制中，这些感官输入被称为值（value）。更通俗的解释，每个值都与一个键（key）配对，这可以想象为感官输入的非自主提示。如图 10.1.3 所示，可以通过设计注意力汇聚的方式，便于给定的查询（自主性提示）与键（非自主性提示）进行匹配，这将引导得出最匹配的值（感官输入）。

![图10.1.3 注意力机制通过注意力汇聚将查询（自主性提示）和键（非自主性提示）结合在一起，实现对值（感官输入）的选择倾向](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773125446445.png)

用数学语言表示，假设有查询 $q \in \mathbb{R}^q$ 和 $m$ 对键和值 $(k_i \in \mathbb R^k, v_i \in \mathbb R^v)$，并使用，则注意力汇聚可以表示为：

$$
f(\mathbf{q},(\mathbf{k}_1,\mathbf{v}_1),\ldots,(\mathbf{k}_m,\mathbf{v}_m))=\sum_{i=1}^m\mathbf{softmax}(a(\mathbf{q},\mathbf{k}_i))\mathbf{v}_i\in\mathbb{R}^v
$$

其中 $a(q, k_i)$ 表示注意力评分，softmax 操作是为了归一化为加权求和。

![图10.3.1 计算注意力汇聚的输出为值的加权和](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773128097593.png)

### Scaled Dot-Product Attention

在 NLP 任务中，往往将输入进行嵌入，再经过 $W_q, W_k, W_v$ 投影得到 $Q, K, V$；在 Transformer 中，使用 **缩放点积注意力机制 (Scaled Dot-Product Attention)** 计算注意力评分：

![https://www.bilibili.com/video/BV1XH4y1T76e|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773127778538.png)

即先计算点积，再进行缩放。除以 $\sqrt{D_{out}}$ 是基于概率分布下，$Q$ 和 $K$ 的点积均值为 0，方差则为 $D_{out}$。

### Self-Attention

对于 $Q, K, V$ 来自同一输入的情况，称为 **self-attention（自注意力）**。

### Cross-Attention

如果 $Q$ 与 $K, V$ 来自于不同的输入，则属于交叉注意力机制。

![https://www.bilibili.com/video/BV1XH4y1T76e|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773131456495.png)

### Causal-Attention

在推理/生成阶段，模型需要完成“预测下一个词元”的任务；但是此时不应该看到“当前要生成的词本身以及后面的词”的信息，因此引入掩码机制，即将不应该看到的词的注意力评分调整为 0。

![https://www.kaggle.com/code/aisuko/causal-self-attention|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773136292995.png)

### Multi-head Attention

多头注意力，简单而言是对于同一组输入有多组 $W_q, W_k, W_v$ 以及后续的注意力操作（称为注意力头；这里可以使用各种注意力机制，如 cross-attention）；每个注意力头得到一个输出 $Z^{(i)}$，拼接后得到 $Z$，最后经过线性变换（全连接层）$W$ 得到最终的输出 $Y$：

![https://www.bilibili.com/video/BV1XH4y1T76e|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_260310-164701.png)

在这个视频中，UP 将注意力机制类比为 CNN，而多头注意力就是多个卷积核，希望能够从不同的“角度”捕捉不同的信息。

![https://lilianweng.github.io/posts/2018-06-24-attention/|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773126382284.png)

所以，让我们区分一下：

- **Scaled Dot-Product Attention** 是一种计算注意力评分（也即注意力权重）的方法
- **Self/Cross/Causal-Attention** 是不同的、应用 Scaled Dot-Product Attention 的组件
- **Multi-head attention** 则在三种组件的基础上进行了改进，捕获多个层次的信息

## Seq2Seq

> [!quote]
>
> - [ ] [从语言模型到Seq2Seq：Transformer如戏，全靠Mask](https://www.kexue.fm/archives/6933)
> - [ ] [Seq2Seq中Exposure Bias现象的浅析与对策](https://www.kexue.fm/archives/7259)
> - [ ] [TeaForN：让Teacher Forcing更有“远见”一些](https://www.kexue.fm/archives/7818/)
> - [ ] [**通俗易懂地理解Gumbel Softmax**](https://zhuanlan.zhihu.com/p/633431594)

Transformer 基于 Seq2Seq 模型，通常而言将会包括 Encoder 和 Decoder 两部分：

![https://jalammar.github.io/illustrated-transformer/|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773125130734.png)

> [!tip]
>
> [9.6. 编码器-解码器架构 — 动手学深度学习 2.0.0 documentation](https://zh.d2l.ai/chapter_recurrent-modern/encoder-decoder.html)
>
> 正如我们在 [9.5节](https://zh.d2l.ai/chapter_recurrent-modern/machine-translation-and-dataset.html#sec-machine-translation) 中所讨论的，机器翻译是序列转换模型的一个核心问题，其输入和输出都是长度可变的序列。为了处理这种类型的输入和输出，我们可以设计一个包含两个主要组件的架构：第一个组件是一个编码器（encoder）：它接受一个长度可变的序列作为输入，并将其转换为具有固定形状的编码状态。第二个组件是解码器（decoder）：它将固定形状的编码状态映射到长度可变的序列。这被称为编码器-解码器（encoder-decoder）架构，如[图9.6.1](https://zh.d2l.ai/chapter_recurrent-modern/encoder-decoder.html#fig-encoder-decoder) 所示。
>
> ![图9.6.1 编码器-解码器架构](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773123859673.png)

而在 Encoder 和 Decoder 中往往会由多层（在论文中使用了 6 层）神经网络构成；Encoder 作用就是用来编码整个输入的序列，Decoder 的作用则是对 Encoder 的序列编码进行解码。

有了前面的基础，我们可以轻松地理解 Transformer 的架构；下面将具体展开对 Encoder 和 Decoder 的分析：

![https://www.53ai.com/news/qianyanjishu/1079.html|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773134129707.png)

## Encoder

> [!info]
>
> - [ ] [Transformer精讲	- Encoder Side | DaNing的博客](https://adaning.github.io/posts/6744.html#toc-heading-9)

先来看 Encoder 部分（即上图的左侧）：

1. 首先针对原始的输入 $I$（例如，一句话），经过 Input Embedding 和 Positional Encoding 得到 $X$
2. 在 Encoder 的每一层神经网络，$X$ 依次经过多头自注意力层、残差连接与层归一化；前馈神经网络、残差连接与归一化，得到 Encoder 的输出 $E$

多头注意力在前面已经分析过，编码器部分使用的是多头自注意力，目的是能够充分利用上下文信息进行编码。

### residual connect

### LayerNorm

> [!info]
>
> - [ ] [Transformer学习笔记三](https://zhuanlan.zhihu.com/p/456863215)

> [!tip]
>
> [Transformers快速入门	- 层归一化](https://transformers.run/c1/attention/#322-%E5%B1%82%E5%BD%92%E4%B8%80%E5%8C%96)
>
> 层归一化（Layer Normalization）负责将一个批次（batch）输入中的每一个都标准化为均值为零且具有单位方差。跳跃连接则是将张量直接传递给模型的下一层而不进行处理，并将其添加到处理后的张量中。
>
> 目前有层后归一化和层前归一化两种常见的向 Transformer 编码器/解码器中添加归一化的方式，如图 3-5 所示：
>
> - **层后归一化（Post layer normalization，Post-Norm）**：Transformer 论文中使用的方式，将层归一化放在跳跃连接之间。但是因为梯度可能会发散，这种做法很难训练，还需要结合学习率预热（learning rate warm-up）等技巧；
> - **层前归一化（Pre layer normalization, Pre-Norm）**：**目前主流的做法**，将层归一化放置于跳跃连接的范围内。这种做法通常训练过程会更加稳定，并且不需要任何学习率预热。
>
> ![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2603/10_1773147936995.png)

### FeedForward

## Decoder

对于 Decoder 部分（即上图的右侧）：

1. 同样是针对原始的输出 $O$（例如，要续写的内容），经过 Output Embedding 和 Positional Encoding 得到 $X$
2. 在 Decoder 的每一层神经网络，$X$ 依次经过多头因果注意力层、残差连接与归一化；多头交叉注意力、残差连接与归一化；前馈神经网络、残差连接与归一化，得到 Decoder 的输出 $D$
3. 最后经过线性变换和 Softmax 得到输出各个词的概率。

### Generation

> [!info]
>
> - [ ] [解码策略高级方法](https://jianzhnie.github.io/llmtech/#/inference/%E8%A7%A3%E7%A0%81%E7%AD%96%E7%95%A5%E9%AB%98%E7%BA%A7%E6%96%B9%E6%B3%95)
> - [ ] [LLM之Generate/Inference（生成/推理）中参数与解码策略原理及其代码实现](https://zhuanlan.zhihu.com/p/653926703)

#### Greedy Search

> **对于词表** $\mathcal{D}$ **，要生成长度为** $l$ **的序列**

**在** [9.7. 序列到序列学习（seq2seq）](https://zh-v2.d2l.ai/chapter_recurrent-modern/seq2seq.html) **中的训练和预测阶段，**循环神经网络编码器-解码器是逐词元地预测输出序列，一般而言是每个时间步选取生成概率最大的词元，也即**贪心搜索**（时间复杂度为 $O(|\mathcal D| l)$）；**但是局部最优不等于全局最优，在时间步 2 选取 C 可能会有更好的序列：**

![在每个时间步，贪心搜索选择具有最高条件概率的词元](https://cdn.nlark.com/yuque/0/2026/svg/38866291/1768618764138-9a539d32-d018-4390-a595-278f16f2aa42.svg)

![对于前一图，说明可能存在更优的序列](https://cdn.nlark.com/yuque/0/2026/svg/38866291/1768619302487-bc7edb73-fd9d-4f36-9cc5-9b2507e7e44b.svg)

**为了找到全局最优，唯有将所有可能的序列找出并进行比较，也即穷举搜索；但是搜索时间/空间复杂度为** $O(|\mathcal{D}|^l)$ **，这对于稍大的词表和稍长的序列显然都是不可接受的。**

#### Beam Search

> [!info]
>
> - [x] [9.8. 束搜索 — 动手学深度学习 2.0.0 documentation](https://zh-v2.d2l.ai/chapter_recurrent-modern/beam-search.html)
>  	- [63 束搜索【动手学深度学习v2】](https://www.bilibili.com/video/BV1B44y1C7m1/)
>  	- [x] [十分钟读懂Beam Search 1：基础](https://zhuanlan.zhihu.com/p/114669778) **（代码讲解）**
>  	- [x] [使用Transformers做限制集束搜索（Constrained Beam Search）的文本生成](https://zhuanlan.zhihu.com/p/537164040)

**束搜索则在贪心搜索和穷举搜索进行了折中，基本模型如下：**

![束搜索过程（束宽：2，输出序列的最大长度：3）](https://cdn.nlark.com/yuque/0/2026/svg/38866291/1768619781844-c620052c-0ba3-490a-ad4a-9f1664cc4df8.svg)

**在每个时间步中，对于词表中的每个词元获得生成概率后进行排序，并只保留概率最大的前 $k$ 个词元对应的路径（$k$ 为超参数，束宽 (beam size)）；不难发现，这类似于同时执行了“贪心算法”“次贪心算法”“次次贪心算法”，所以时间复杂度为** $O(k*|\mathcal D|l)$ **，在正确率和时间复杂度上做出权衡。**

#### Sampling

> [!info]
>
> - [ ] [十分钟读懂Beam Search 2：一些改进](https://zhuanlan.zhihu.com/p/115076102)

**Beam Search** 的问题：针对同一段文字，让当时的 GPT-2（使用 Beam Search 策略）和人类续写同一段文本，分析续写内容的词频分布情况：人类选择的词（橙线）并不是像机器选择的（蓝线）那样总是那些条件概率最大的词。这些概率大的词会发生正反馈，产生循环。

![https://arxiv.org/pdf/1904.09751	- Figure2](https://raw.githubusercontent.com/darstib/public_imgs/utool/2601/20_260120-095715.png)

为此，研究人员设计了多种采样方式，即避免在选择最后的输出序列时只选择概率最大的那条路（往往会涉及到“温度”这一概念）：

- random sampling
- Nucleus sampling
- Top-k sampling

### Teacher forcing

> [!info]
>
> - [https://en.wikipedia.org/wiki/Teacher_forcing](https://en.wikipedia.org/wiki/Teacher_forcing)
> - [x] [https://zhuanlan.zhihu.com/p/644211164](https://zhuanlan.zhihu.com/p/644211164)
> - [x] [https://kexue.fm/archives/7259](https://kexue.fm/archives/7259)

本来是**训练** RNN 时的一种算法；

- 训练时，采用 Autoregressive mode：在每一步模型预测完成后都会使用真实的标签 $\tilde{y}$ 替代模型实际的输出 $y$，附在原输入 $(x)$ 后作为新的输入 $(x, \tilde{y})$；
 	- 如下图 b)，就好比上数学课老师带着我们一步一步推导答案，能够在推到下一步时确保前面都是对的
- 预测时，采用 Teacher Forcing mode：则不会替代模型的实际输出 $y$，也就是将模型的实际输出 $y$ 附在原输入后作为新的输入 $(x, y)$ 生成下一个 token；
 	- 如下图 a)，就好比开始自己写答案，有可能都对，也有可能一步错步步错，或者过程错但是结果对

![](https://cdn.nlark.com/yuque/0/2026/png/38866291/1773063849660-4a4ca9d1-26b4-40f7-b54d-1c4ace6be6af.png)

#### Exposure Bias

> [!info]
>
> - [x] [https://zhuanlan.zhihu.com/p/644211164](https://zhuanlan.zhihu.com/p/644211164)
> - [x] [https://kexue.fm/archives/7259](https://kexue.fm/archives/7259)

在 Teacher Forcing 模式下，模型训练时和测试时的任务不对等、差异称为“曝光误差”；就好比学生只在教师的带领下一步步解题，却从来不自己进行练习和批改，便学不会如何去找到正确的解题过程。

在 2015 年，谷歌提出“计划采样”(scheduled sampling) 的方案，即在 Autoregressive mode 和 Teacher Forcing 进行过渡：也即概率选择 $y$ or $\tilde y$ 放在原输入 $x$ 之后作为下一个 token 生成任务的输入。这个概率随着训练的进行而改变：前期模型能力较差，需要更多的指导；后期模型能力渐强，需要更多的练习。

## [todo] Contrastive Learning

- [ ] [对比学习（Contrastive Learning）综述](https://zhuanlan.zhihu.com/p/346686467)
- [ ] [对比学习（Contrastive Learning）概述](https://zhuanlan.zhihu.com/p/630101991)
- [ ] [对比学习batch size 优化 - GradCache](https://zhuanlan.zhihu.com/p/17807595253)
- [ ] **Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey E. Hinton. 2020. A Simple Framework for Contrastive Learning of Visual Representations. In ICML.**