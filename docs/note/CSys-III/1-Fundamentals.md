---
tags:
  - notes
comments: true
---

# 计算机系统基础

## I 引言 (page 40-54)

### I.1 冯·诺依曼结构 (Von Neumann Structure) (page 40-41)

> [!definition]+ 冯·诺依曼结构
>
> 现代计算机的基础架构，其核心思想是：
> 1. **存储程序 (Stored Program)**: 指令和数据都以二进制形式存储在同一内存中，没有物理区分。
> 2. **五大部件**: 计算机由运算器、控制器、存储器、输入设备和输出设备组成。其中运算器和控制器通常集成在一起，称为中央处理器 (CPU)。
> 3. **数据流**: CPU 从内存中获取指令和数据进行运算，并将结果写回内存。
>
> 附件的图示清晰地展示了**数据通路 (Data Path)**（蓝色箭头，表示数据流动）和**控制通路 (Control Path)**（红色箭头，表示控制信号流动）。

### I.2 计算机革命 (The Computer Revolution) (page 42)

计算机技术的飞速发展，其背后深刻的驱动力是**摩尔定律 (Moore's Law)**。这使得许多创新的应用成为可能，例如汽车电子、智能手机、人类基因组计划、万维网、搜索引擎以及当前的大语言模型 (Large Language Model)，计算机已经渗透到我们生活的方方面面。

### I.3 计算机领域的巨匠们 (Big Men) (page 44-54)

本课程的学习是“站在巨人的肩膀上”。附件列举了多位对计算机体系结构做出奠基性贡献的科学家，他们的思想和成果是本课程的重要理论基础。

> [!wiki]+ 体系结构领域的先驱
>
> - **John Hennessy & David Patterson**: 2017 年图灵奖得主。他们开创了**精简指令集计算机 (RISC)** 的思想，并提出了对计算机体系结构进行**系统性、定量化**分析的方法。他们合著的《计算机体系结构：一种量化研究方法》是该领域的圣经。
> - **Frederick P. Brooks**: 1999 年图灵奖得主。他在计算机体系结构（定义了 IBM 360 体系结构）、操作系统和软件工程领域都有里程碑式的贡献。其著作《人月神话》是软件工程领域的经典。
> - **Robert Tomasulo**: 他发明的 **Tomasulo 算法**是实现处理器**乱序执行 (Out-of-Order Execution)** 的关键技术，极大地提升了处理器的指令级并行能力。
> - **Seymour Cray**: “超级计算机之父”。他在高性能计算和超级计算机设计领域做出了卓越贡献，并对 RISC 高端微处理器的发展产生了重要影响。
> - **Gene Amdahl**: 提出了著名的**阿姆达尔定律 (Amdahl's Law)**，对计算机体系结构中的流水线、指令预取和 Cache 存储器等有杰出贡献。
> - **Mateo Valero, Yale Patt, Michael J. Flynn**: 他们在指令级并行、超标量处理器设计、处理器组织与分类（弗林分类法）、计算机算术和性能评估等方面做出了重要贡献。

## II 计算机的分类 (page 55-58)

### II.1 弗林分类法 (Flynn's Taxonomy) (page 55)

> [!definition]+ 弗林分类法
>
> 这是基于**指令流 (Instruction Stream)** 和**数据流 (Data Stream)** 的数量对计算机体系结构进行的分类。
>
> - **SISD (Single Instruction, Single Data)**: 单指令流，单数据流。传统的串行计算机，如早期的单核 CPU。
> - **SIMD (Single Instruction, Multiple Data)**: 单指令流，多数据流。执行一条指令可以同时处理多个数据，非常适合多媒体处理和科学计算。现代 CPU 中的 SSE/AVX 指令集就是 SIMD 的例子。
> - **MISD (Multiple Instruction, Single Data)**: 多指令流，单数据流。多个处理器对同一个数据流执行不同的指令。这种结构比较少见，有时用于容错系统。
> - **MIMD (Multiple Instruction, Multiple Data)**: 多指令流，多数据流。多个处理器可以独立地执行不同的指令处理不同的数据。现代的多核处理器、分布式系统都属于 MIMD 结构。

### II.2 按用途和规模分类 (page 56-57)

- **桌面计算机 (Desktop Computers / PC)**: 通用，软件丰富，强调单个用户的良好性能和相对较低的成本。
- **服务器 (Server Computers)**: 强调处理少量复杂应用的高性能，或同时为大量用户提供服务的可靠性。计算、存储和网络能力通常强于个人电脑。
- **嵌入式计算机 (Embedded Computers)**: 数量最大、种类最多的一类。通常作为大系统的一个组件隐藏其中，对功耗、性能、成本有严格的限制。
- **个人移动设备 (Personal Mobile Devices)**: 如智能手机、平板电脑，其设计需求与 PC 类似，但对功耗和尺寸有更苛刻的要求。
- **超级计算机 (Supercomputer)**: 通常是计算机集群，拥有极高的计算能力、性能和可靠性，规模可达整个建筑大小。

## III 性能 (Performance) (page 59-64)

### III.1 定义与衡量性能 (page 59, 61-62)

性能的定义取决于衡量指标。附件中的飞机例子说明：如果看重载客量，波音 747 最好；如果看重巡航速度，协和式飞机最好。

> [!definition]+ 性能指标
>
> - **响应时间 (Response Time) / 延迟 (Latency)**: 完成一个任务所花费的时间。对于单个用户来说，更关心响应时间。
> - **吞吐率 (Throughput)**: 单位时间内完成的任务总量。对于数据中心或服务器管理者来说，更关心吞吐率。
>
> **CPU 时间 (CPU Time)** 是衡量性能的核心指标，它指 CPU 用于处理一个任务的实际时间，不包括 I/O 等待或处理其他任务的时间。它分为：
> - **用户 CPU 时间 (User CPU time)**: 执行程序本身代码所花费的时间。
> - **系统 CPU 时间 (System CPU time)**: 操作系统为该程序执行任务（如系统调用）所花费的时间。

### III.2 性能比较 (page 63-64)

性能与执行时间成反比。

$$
\text{Performance} = \frac{1}{\text{Execution Time}}
$$

因此，比较两台机器 X 和 Y 的性能，只需比较它们的执行时间。
如果“X 比 Y 快 n 倍”，则意味着：

$$
\frac{\text{Performance}_X}{\text{Performance}_Y} = \frac{\text{Execution Time}_Y}{\text{Execution Time}_X} = n
$$

## IV 定量方法 (Quantitative approaches) (page 65-85)

### IV.1 CPU 性能与时钟 (page 67-70)

数字硬件的操作由一个恒定频率的时钟驱动。
- **时钟周期 (Clock Period)**: 一个时钟周期的时长，如 250ps。
- **时钟频率 (Clock Rate)**: 每秒的时钟周期数，如 4.0GHz。

两者互为倒数。

CPU 执行时间可以用以下公式表示：

$$
\text{CPU Execution Time} = \text{CPU Clock Cycles} \times \text{Clock Period} = \frac{\text{CPU Clock Cycles}}{\text{Clock Rate}}
$$

这意味着，要提升性能（减少执行时间），可以**减少所需的时钟周期数**，或者**提高时钟频率**（缩短时钟周期）。但两者往往是相互制约的，例如更复杂的流水线设计可以减少周期数，但可能会限制时钟频率的提高。

### IV.2 指令数与 CPI (page 71-76)

为了更深入地分析，我们将时钟周期数分解：

$$
\text{CPU Clock Cycles} = \text{Instruction Count (IC)} \times \text{Cycles Per Instruction (CPI)}
$$

- **IC (Instruction Count)**: 执行一个程序所需的指令总数。它由算法、编程语言和编译器决定。
- **CPI (Cycles Per Instruction)**: 执行一条指令平均所需的时钟周期数。它主要由 CPU 的微架构设计决定。

> [!math]+ CPU 性能的“The BIG Picture”公式
>
> 将以上公式结合，我们得到最终的 CPU 性能公式：
>
> $$
> \begin{aligned}
> \text{CPU Time} &= \text{Instruction Count} \times \text{CPI} \times \text{Clock Period} \\
> &= \frac{\text{Instruction Count} \times \text{CPI}}{\text{Clock Rate}}
> \end{aligned}
> $$
>
> 这个公式揭示了影响 CPU 性能的三个关键因素：**指令数、CPI 和时钟频率**。任何对系统的优化都必须从这三者入手。算法和编译器主要影响 IC 和 CPI，而 ISA 会影响三者，硬件设计则主要影响 CPI 和时钟频率。

如果程序包含多种不同 CPI 的指令，总的 CPI 是一个加权平均值：

$$
\text{CPI} = \sum_{i=1}^{n} (\text{CPI}_i \times \frac{\text{Instruction Count}_i}{\text{Total Instruction Count}})
$$

其中，`Instruction Count_i / Total Instruction Count` 是第 i 类指令的执行频率。

### IV.3 阿姆达尔定律 (Amdahl's Law) (page 78-85)

> [!theorem]+ 阿姆达尔定律
>
> 对一个计算机系统的某一部分进行优化后，整个系统性能的提升幅度，受限于该部分执行时间占总执行时间的比例。
>
> 这个定律也被称为“**加速大概率事件 (Make the common case fast)**”原则的理论基础。

设 `Fraction_enhanced` 为可被优化的部分所占的执行时间比例，`Speedup_enhanced` 为该部分的性能提升倍数。那么，优化后的总执行时间为：

$$
\text{Execution time}_{\text{new}} = \text{Execution time}_{\text{old}} \times \left( (1 - \text{Fraction}_{\text{enhanced}}) + \frac{\text{Fraction}_{\text{enhanced}}}{\text{Speedup}_{\text{enhanced}}} \right)
$$

总的加速比 (Speedup_overall) 为：

$$
\text{Speedup}_{\text{overall}} = \frac{\text{Execution time}_{\text{old}}}{\text{Execution time}_{\text{new}}} = \frac{1}{(1 - \text{Fraction}_{\text{enhanced}}) + \frac{\text{Fraction}_{\text{enhanced}}}{\text{Speedup}_{\text{enhanced}}}}
$$

> [!example]+ Amdahl's Law 示例 (page 83)
>
> **问题**: 某功能占总运行时间的 40%，现将其速度提升 20 倍，整个系统性能能提升多少？
>
> **解答**:
> `Fraction_enhanced` = 0.4
> `Speedup_enhanced` = 20
>
> $$
> \text{Speedup}_{\text{overall}} = \frac{1}{(1 - 0.4) + \frac{0.4}{20}} = \frac{1}{0.6 + 0.02} = \frac{1}{0.62} \approx 1.613
> $$
>
> 即使一个部分有 20 倍的巨大提升，但由于它只占 40% 的时间，整个系统性能也只提升了约 1.6 倍。

一个重要的推论是，总加速比的上限受限于不可优化部分的比例：

$$
\text{Speedup}_{\text{overall}} < \frac{1}{1 - \text{Fraction}_{\text{enhanced}}}
$$

## V 伟大的体系结构思想 (Great Architecture Ideas) (page 86-91)

这部分总结了半个多世纪以来计算机设计中反复出现的八个伟大思想。

1. **为摩尔定律而设计 (Design for Moore's Law)**: 考虑到芯片上的晶体管数量每 18-24 个月翻一番，架构师必须有前瞻性，设计出在未来技术节点下依然有竞争力的系统。
2. **使用抽象简化设计 (Use abstraction to simplify design)**: 通过分层来隐藏底层细节，使设计者可以专注于当前层次的问题。
3. **加速大概率事件 (Make the common case fast)**: 如阿姆达尔定律所示，集中资源优化最常执行的部分，能获得最大的性能收益。
4. **通过并行提升性能 (Improve performance via parallelism)**: 同时执行多个操作，存在指令级、数据级、线程级等多个层次的并行。
5. **通过流水线提升性能 (Improve performance via pipelining)**: 将一个任务分解为多个阶段，让多个任务的不同阶段重叠执行，从而提高指令吞吐率。
6. **通过预测提升性能 (Improve performance via prediction)**: 在结果未知时进行猜测（如分支预测），如果猜对则节省了等待时间。这是一种**推测执行 (Speculation)**。
7. **使用存储器层次结构 (Use a hierarchy of memories)**: 结合不同速度、容量和成本的存储设备（如 Cache-内存-磁盘），使得程序能以接近最高速存储器的速度，访问到大容量存储器中的数据。
8. **通过冗余提高可靠性 (Improve dependability via redundancy)**: 添加额外的组件来检测甚至纠正错误，如 RAID 磁盘阵列、ECC 内存。

### V.1 总结 (page 91)

- 计算机的**性价比**在底层技术驱动下不断提升。
- **分层抽象**是贯穿软硬件设计的核心思想。
- **ISA** 是关键的软硬件接口。
- **执行时间**是衡量性能的最佳指标。
- 八大体系结构思想是设计现代计算机的基石。