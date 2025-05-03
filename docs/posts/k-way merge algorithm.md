---
comments: true
date: 2024-03-23
tags:
- blog
- algo
---

> [!SUMMARY]-
>  
> k-way merge algorithm 是一种外部排序算法，用于对超过内存容量的数据进行排序。
> 
> - **k-way merge with 2*k tapes：** 使用 2*k 个磁带进行 k-way merge，将数据分成 k 个顺串，每次合并 k 个顺串，直到所有数据排序完成。
> - **k-way merge with k+1 tapes：** 使用 k+1 个磁带进行 k-way merge，通过将数据分配到 k 个磁带，并利用一个空磁带进行合并，减少了磁带的使用。
> - **Fibonacci sequence of order K：** 使用 k 阶斐波那契数列分配数据，可以使合并次数最少。
> - **Replacement selection：** 采用替换选择的方式构建顺串，可以减少顺串数量，提高排序效率。

<!-- more -->

如果我们想要对超过内存最大容量的数据进行排序，就需要用到外部排序(External sort)，一个比较有效的方法就是 k-way merge algorithm.

> 实现语言：C
> 
> 知识条件：掌握了合并排序（Merge sort）

我们将以磁带作为文件储存工具来演示 k-way merge algorithm

我们规定：

- 内部一次可以排序的最大数据量为 M
- 总需要排序的数据量为 N (N >> M)
- 每一个磁盘总是足够大的，能够容纳 M 个数据

> [!INFO]
>
> We call each set of sorted records a _run_ .
>
> 我们把每一小段排序好的数据称为 _顺串_ 。

> [!ATTENTION]
>
> 一般而言，文件读写本身花费的时间远长于排序用时，所以我们应该尽量减少读写次数（也叫趟数 (passes)），所以尽量将内存读满，顺串一般数据量为M

## k-way merge with  2\*k tapes

我们将 2\*k 个磁带分为 k 个输入磁带和 k 个输出磁带

1. 我们将总数据 N 依次取 M 个输入内存获得 $\frac{N}{M}$ （向上取整，不满 M 项的顺串按 M 项记）个长为 M 的顺串，将顺串轮流输入 k 个输入磁带上
2. 使用优先队列取 k 个输入磁带最前端项中的最小项进行合并k 个顺串（类似合并排序），获得长为 k\*M 的顺串轮流输入 k 个输出磁带上
3. 角色交换，输入磁带看作输出磁带，输出磁带看作输入磁带，重复步骤 2
4. 当顺串长度变为 N 时结束。 

> [!NOTE]
>
> 不难推断，k-way merge 的时间复杂度为 $O\left( \log_{k}\left( \frac{N}{M} \right) \right)$

下面是一些图解：

### 2-way merge

![](attachments/k-way%20merge%20algorithm.png)

### 3-way merge

![](attachments/k-way%20merge%20algorithm-1.png)

## k-way merge with k+1 tapes

> [!QUESTION]
>
> 使用 2\*k 个磁带固然可行，但是不难发现不少磁带在后面的时候使用很少，我们能否想办法减少不必要的磁带使用？

1. 假想我们将总数据的顺串分给 k 个磁带的时候并不太均匀，总是能找到一个磁带（记为 $T_{1}$）分得顺串量（设为 $k_1$）最少
2. 在进行 $k_1$ 次 Merge_k 输入剩余的一个空磁带（记为 $T_{k+1}$）后，这个磁带一定为空，而 $T_{k+1}$ 上有 $k_{1}$ 个长为 $kM$ 的顺串
3. 我们将 $T_{1}$ 看作空磁带，$T_{k+1}$ 看作包含 $k*k_{1}$ 个长为 M 的顺串，重复步骤 2，直到所有顺串在一个磁带上

下面是一个例子

### 2-way merge

![](attachments/k-way%20merge%20algorithm-2.png)

### Fibonacci sequence of order K

在上面的例子中，我们如果将 34 个顺串 5、29 分给两个磁盘，不难退出如下合并过程

![](attachments/k-way%20merge%20algorithm-3.png)

单看合并次数 pass $7->12$  ，我们几乎可以认为用时翻倍，这是不能容忍的

> [!QUESTION]
>
> 怎样的分配才算合理？

> [!INFO]
>
> _Fibonacci sequence of order K_（K 阶级斐波那契数列）
> 
> 我们认为符合下面公式的数列称为 K 阶级斐波那契数列
>
> $$F^{(k)}(N)=\begin{cases}0\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad0\leq N\leq k-2\\1\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad N=k-1 \\F^{k}(N-1)+\dots+F^{k}(N-k)\quad\quad N\geq k\end{cases}$$

而当我们在进行 k-way merge 时按照 k 阶斐波那契数列分配时合并次数最少。

例如：对于 3 阶斐波那契数列：0, 0, 1, 1, 2, 4, 7, 13, 24, 44...

如果我们要将 3 分到三个磁盘上，我们这样考虑：寻找一段连续的斐波那契数 a,b,c,d ，满足：total = c+(b+c)+(a+b+c) = b+2c+d。对于 31，不难得到应该为 2,4,7,13，故分为 7,11,13 。

## Replacement selection

> [!QUESTION]
>
> 根据上面我们获取顺串的方式，顺串长度不超过 M，也就导致顺串数量不少于
> $\frac{N}{M}+1$ 个；而我们发现趟数 (passes) 与顺串数成正相关，能不能减少顺串数呢？

我们考虑一个更好地构建顺串的办法——替换选择(_Replacement selection_)

1. 将输入磁盘前 M 个数据输入内存（内存中依旧使用优先队列排序）
2. 执行 DeleteMin 操作将最小值 x 输入输出磁盘中
3. 从输入磁盘再读取一个数据 y，如果 y >= x，则 y 放入内存并上滤，重复步骤 2；如果 y < x，则将 y 放入优先队列的死区(dead space)并认为优先队列大小减 1，y 参加下一个顺串的构建
4. 如果优先队列减小为 0 (End of Run) 或者是输入磁盘已经为空 (end of tape) 时，将死区中的所有元素排序后作为一个顺串输出 (Rebuild Heap) ；重复步骤 1

不难推断，这样构建的顺串长度至少为 M，从而达到了减少顺串数量的目的

> [!NOTE]
>
> 当输入磁盘数据足够大且随机时，获得的顺串平均长度约为 2M

下面是 M=3 时的一个图示

![](attachments/k-way%20merge%20algorithm-4.png)

## Huffman Tree in merge

![](attachments/k-way%20merge%20algorithm-5.png)

## 参考文档

- [k-way merge algorithm](https://en.wikipedia.org/wiki/K-way_merge_algorithm#Two-way_merge)
- Data structures and algorithm analysis in C (P 251-254)
    - 数据结构与算法分析 C 语言描述（英文版·第2版） (Mark Allen Weiss)
- ZJU ADS slider 