## 计算机体系结构课程回顾

### 贯穿设计的八个伟大思想 (page 2-5, 不直接考)

在计算机设计领域，有八个伟大的体系结构思想，它们在过去半个多世纪中一直被应用和发展。在学习计算机体系结构时，我们需要时常思考这些思想是如何在具体技术中发挥作用的。

#### 1. 为摩尔定律而设计 (Design for Moore's law)

> [!wiki]+ 摩尔定律 (Moore's Law)
>
> 摩尔定律指出，集成电路上可容纳的晶体管数量，约每隔 18-24 个月便会增加一倍。
>
> 这意味着计算机硬件的性能会以指数级的速度增长。因此，体系结构设计师在项目启动时就必须预测几年后技术发展的水平，确保设计完成时不会过时。例如，一个为期三年的项目，其设计目标应基于三年后预期的芯片能力，而非项目开始时的技术水平。

#### 2. 使用抽象简化设计 (Use abstraction to simplify design)

> [!definition]+ 抽象 (Abstraction)
>
> 抽象是通过隐藏底层实现的复杂细节，为上层提供一个简化的模型或接口来管理复杂性的方法。
>
> 在计算机系统中，抽象无处不在：
> - **硬件层面**：指令集体系结构（Instruction Set Architecture, ISA）是对处理器硬件的抽象，它定义了软件如何与硬件交互，而无需关心具体的微体系结构（microarchitecture）实现。
> - **软件层面**：操作系统为应用程序提供了诸如文件系统、虚拟内存等抽象，使得程序无需直接和磁盘、物理内存等硬件打交道。

#### 3. 加速常用事件 (Make the common case fast)

这个原则强调应优先优化最常执行的操作或路径。因为优化常用部分带来的性能提升远大于优化不常用部分。

> [!example]+ 举例
>
> 假设一个程序 90%的时间在执行某种计算，10%的时间在执行 I/O 操作。那么将计算部分的性能提升一倍，对总性能的提升效果（整体加速接近 1.8 倍）将远大于将 I/O 性能提升一倍（整体加速约 1.09 倍）。
>
> 这也是 **Amdahl 定律** 的一个核心思想。

#### 4. 通过并行提升性能 (Improve performance via parallelism)

> [!definition]+ 并行 (Parallelism)
>
> 并行是指同时执行多个计算任务的能力。这是提高性能最重要的方法之一。并行可以在不同层次上实现：
> - **指令级并行 (Instruction-Level Parallelism, ILP)**：通过流水线（Pipelining）或超标量（Superscalar）等技术，让多条指令在同一时间的不同阶段或不同执行单元上执行。
> - **数据级并行 (Data-Level Parallelism, DLP)**：通过 SIMD (Single Instruction, Multiple Data) 指令，用一条指令同时处理多个数据。例如，向量处理器（Vector Processor）。
> - **任务级并行 (Task-Level Parallelism, TLP)**：在多核处理器上，将不同的线程或进程分配到不同的核心上并行执行。

#### 5. 通过流水线提升性能 (Improve performance via pipelining)

流水线是一种特殊的指令级并行技术。它将一个任务（例如一条指令的执行）分解为多个独立的阶段（stage），然后让不同的任务在不同的阶段上重叠执行，就像工厂的装配线一样。这大大提高了任务的吞吐率（throughput），但通常不会缩短单个任务的延迟（latency）。

#### 6. 通过预测提升性能 (Improve performance via prediction)

在很多情况下，等待一个操作的结果会造成处理器停顿（stall）。预测（Prediction），也称为推测执行（Speculation），指的是在结果未知时先猜测一个可能的结果，并基于这个猜测继续执行。

> [!example]+ 分支预测 (Branch Prediction)
>
> 当遇到条件分支指令时，处理器不必等待条件判断完成，而是预测分支是否会跳转。如果预测正确，就获得了性能提升；如果预测错误，则需要撤销（squash）错误路径上的指令，并从正确路径重新执行，这会带来一定的性能损失。但只要预测准确率足够高，总体性能就能得到提升。

#### 7. 使用存储器层次结构 (Use a hierarchy of memories)

> [!definition]+ 存储器层次结构 (Memory Hierarchy)
>
> 理想的存储器应该既快、又大、又便宜，但这三者在物理上是矛盾的。存储器层次结构通过构建一个由不同速度、容量和成本的存储设备组成金字塔结构来解决这个问题。
>
> - **顶层**：速度最快、容量最小、每比特成本最高的存储器，如寄存器（Registers）和高速缓存（Cache）。
> - **底层**：速度最慢、容量最大、每比特成本最低的存储器，如主存（Main Memory）和磁盘（Disk）。
>
> 这个结构利用了程序的**局部性原理（Principle of Locality）**，使得处理器大部分时间访问的都是顶层的高速存储器，从而获得接近顶层存储器的访问速度和接近底层存储器的容量。

#### 8. 通过冗余提高可靠性 (Improve dependability via redundancy)

> [!note]+ 可靠性 (Dependability)
>
> 计算机系统可能会因为各种原因（如硬件老化、环境干扰）而出错。通过增加冗余组件，系统可以具备检测甚至纠正错误的能力，从而提高其可靠性。
>
> 例如，服务器通常会使用纠错码存储器（Error-Correcting Code, ECC Memory）来检测和纠正内存中的单位元错误。磁盘阵列（RAID）技术通过冗余磁盘来防止因单个磁盘损坏而导致的数据丢失。

### CPU 性能 (page 6-7)

为了衡量 CPU 性能，我们通常关注程序在 CPU 上的执行时间。

#### CPU 性能公式 (page 6, 量化分析方法)

CPU 执行时间可以通过以下公式计算：

$$
\text{CPU Execution Time} = \text{CPU Clock Cycles} \times \text{Clock Period}
$$

其中：
- **CPU Clock Cycles**：执行一个程序所需的时钟周期总数。
- **Clock Period**：一个时钟周期的时长（例如，1 纳秒）。

由于时钟频率（Clock Rate）是时钟周期的倒数（`Clock Rate = 1 / Clock Period`），公式也可以写成：

$$
\text{CPU Execution Time} = \frac{\text{CPU Clock Cycles}}{\text{Clock Rate}}
$$

从这个公式可以看出，要缩短程序的执行时间（即提高性能），可以从两个方面入手：

1. **减少程序所需的时钟周期数**。
2. **缩短每个时钟周期的长度**（即提高时钟频率）。

#### 指令数和 CPI (page 7)

程序的时钟周期总数又可以进一步分解：

$$
\text{CPU Clock Cycles} = \text{Instruction Count} \times \text{CPI}
$$

- **Instruction Count (IC)**：程序的指令总数。它由程序本身、编译器和指令集体系结构（ISA）共同决定。
- **CPI (Cycles Per Instruction)**：平均每条指令所需的时钟周期数。它主要由 CPU 的硬件设计（微体系结构）决定。不同的指令类型（如整数加法、浮点除法）可能有不同的 CPI，因此总的 CPI 是所有指令类型的加权平均值。

将上述公式结合，我们得到一个更全面的 CPU 性能公式：

$$
\text{CPU Time} = \text{Instruction Count} \times \text{CPI} \times \text{Clock Period}
$$

或者

$$
\text{CPU Time} = \frac{\text{Instruction Count} \times \text{CPI}}{\text{Clock Rate}}
$$

> [!important]+ 性能分析
>
> 这个公式揭示了评估 CPU 性能的三个关键因素：指令数、CPI 和时钟频率。在进行性能优化时，必须综合考虑这三者。例如，某个编译器优化可能会减少指令数，但导致生成的指令需要更多的周期（CPI 增加），最终性能不一定提升。同样，单纯追求高频率也可能导致 CPI 增加，从而无法带来实际的性能提升。

### Amdahl 定律 (page 8, 量化分析方法)

> [!theorem]+ Amdahl's Law (阿姆达尔定律)
>
> 阿姆达尔定律描述了对一个系统中的某个部分进行优化后，整个系统性能提升的上限。这个上限受限于该部分在总执行时间中所占的比例。
>
> 公式如下：
>
> $$
> \text{Speedup}_{\text{overall}} = \frac{\text{Execution time}_{\text{old}}}{\text{Execution time}_{\text{new}}} = \frac{1}{(1 - \text{Fraction}_{\text{enhanced}}) + \frac{\text{Fraction}_{\text{enhanced}}}{\text{Speedup}_{\text{enhanced}}}}
> $$
>
> - $\text{Fraction}_{\text{enhanced}}$: 可被优化的部分在原执行时间中所占的比例。
> - $\text{Speedup}_{\text{enhanced}}$: 该部分本身性能提升的倍数。

这个定律告诉我们，要想获得显著的整体性能提升，必须优化那些占据大部分执行时间的部分。这正是“加速常用事件”思想的数学体现。

### RISC 处理器经典五级流水线 (page 9)

流水线技术是实现指令级并行的核心。一个经典的 RISC 处理器流水线通常分为五个阶段：
1. **IF (Instruction Fetch)**：取指令
2. **ID (Instruction Decode)**：指令译码并读取寄存器
3. **EX (Execute)**：执行或计算地址
4. **MEM (Memory Access)**：访存
5. **WB (Write Back)**：写回结果

然而，流水线并非总能顺利运行，它会遇到各种“冒险”（Hazards），这些冒险是由指令之间的“相关”（Dependences）引起的。

> [!definition]+ 相关 vs. 冒险
>
> - **相关 (Dependence)**: 指令之间在数据、名字或控制流上的依赖关系。这是**程序本身的属性**。
> - **冒险 (Hazard)**: 在流水线中，如果下一条指令无法在预定的时钟周期开始执行，就发生了冒险。这是**流水线组织的属性**。冒险的根源是相关。

#### 流水线冒险的分类 (page 9-10)

流水线冒险主要分为三类：

1. **结构冒险 (Structural Hazards)**：当硬件资源不足，无法同时满足流水线中多条指令的需求时发生。例如，只有一个存储器端口，但 IF 阶段和 MEM 阶段的指令都需要访问存储器。

2. **数据冒险 (Data Hazards)**：当一条指令需要使用前面尚未完成指令的结果时发生。

    - **写后读 (Read After Write, RAW)**：最常见的数据冒险。后一条指令读取的寄存器，是前一条指令将要写入的目标。
        ```assembly
        FADD.D F6, F0, F12  ; F6 is the destination
        FSUB.D F8, F6, F14  ; FSUB.D needs the result in F6
        ```
    - **读后写 (Write After Read, WAR)**：也称反相关。后一条指令写入的目标寄存器，是前一条指令要读取的源。在简单的五级流水线中不常见，但在乱序执行（out-of-order execution）中需要处理。
        ```assembly
        FDIV.D F2, F6, F4   ; FDIV.D reads F6
        FADD.D F6, F0, F12  ; FADD.D writes to F6
        ```
    - **写后写 (Write After Write, WAW)**：也称输出相关。两条指令写入同一个目标寄存器。同样，在简单流水线中不常见，但在乱序执行中很重要。
        ```assembly
        FDIV.D F2, F0, F4   ; FDIV.D writes to F2
        FSUB.D F2, F6, F14  ; FSUB.D also writes to F2
        ```
3. **控制冒险 (Control Hazards)**：由分支指令引起。处理器需要确定下一条要执行的指令地址，但在分支结果出来前，这个地址是不确定的。

### 动态调度：Scoreboard 算法和 Tomasulo 算法 (page 11-14)

为了解决由数据冒险（特别是 RAW）导致的流水线停顿，并更好地发掘指令级并行，现代处理器普遍采用**动态调度（Dynamic Scheduling）** 技术，其中最著名的是 **Tomasulo 算法**。

#### 核心思想 (page 11)

动态调度的核心思想是**乱序执行 (Out-of-Order Execution, OoOE)**。它允许指令在满足其数据相关性后立即执行，而不必严格按照程序原本的顺序。

> [!tip]+ Tomasulo 算法的关键组件 (page 12)
>
> 1. **保留站 (Reservation Stations, RS)**: 每个功能单元（如加法器、乘法器）前都有一组保留站。指令被发射（issue）后，会进入保留站等待其操作数。
> 2. **公共数据总线 (Common Data Bus, CDB)**: 当一个功能单元计算出结果后，它会通过 CDB 将结果广播给所有等待该结果的保留站和寄存器堆。这使得结果可以被立即转发，避免了经过寄存器堆的延迟。
> 3. **寄存器重命名 (Register Renaming)**: Tomasulo 算法通过保留站隐式地实现了寄存器重命名，从而消除了 WAR 和 WAW 这两种伪相关（name dependences）。

#### 支持精确异常 (page 13-14)

原始的 Tomasulo 算法不支持精确异常[^1]。为了解决这个问题，现代处理器引入了**重排序缓冲区 (Reorder Buffer, ROB)**。

[^1]: **精确异常 (Precise Exception)** 是指当一条指令发生异常时，处理器状态看起来就像是该指令之前的所有指令都已经完成，而该指令及其之后的所有指令都尚未执行。这对于操作系统处理异常至关重要。

> [!definition]+ 重排序缓冲区 (Reorder Buffer, ROB)
>
> ROB 是一个先进先出（FIFO）的队列，用于暂存乱序执行完成的指令结果。指令按照**顺序提交 (In-order Commit)** 的方式离开 ROB。
>
> 结合 ROB 后，指令的执行流程变为：
> 1. **顺序发射 (In-order Issue)**：指令按程序顺序发射到 ROB 和保留站。
> 2. **乱序执行 (Out-of-Order Execution)**：指令在保留站中等待操作数，一旦就绪就乱序执行。
> 3. **乱序写回 (Out-of-Order Writeback)**：结果通过 CDB 广播到 ROB 和保留站。
> 4. **顺序提交 (In-order Commit)**：只有当一条指令到达 ROB 的队首，并且没有产生异常时，其结果才会被真正写入寄存器或内存，并从 ROB 中移除。
>
> 通过顺序提交，如果一条指令（例如 `I_j`）发生异常，那么所有在它之后的指令（即使已经执行完毕）都不会提交它们的结果，从而保证了精确异常。
>
> **硬件推测 (Hardware-Based Speculation)** (page 14) 正是基于这种带有 ROB 的 Tomasulo 结构实现的。当进行分支预测时，后续指令可以推测性地执行，其结果保存在 ROB 中。如果预测正确，结果被提交；如果预测错误，只需清空 ROB 中推测路径上的所有条目即可。

### 存储器层次结构 (page 15-21)

如前所述，存储器层次结构是为了解决速度、容量和成本之间的矛盾而设计的。它利用了程序的**局部性原理**。

> [!wiki]+ 局部性原理 (Principle of Locality)
>
> 程序在访问存储器时倾向于表现出两种局部性：
> - **时间局部性 (Temporal Locality)**: 如果一个数据项被访问，那么它在不久的将来很可能再次被访问。
> - **空间局部性 (Spatial Locality)**: 如果一个数据项被访问，那么与它地址相邻的数据项也很可能在不久的将来被访问。

#### 什么是 Cache (page 16)

**高速缓存 (Cache)** 是存储器层次结构中的核心概念。它是一个小而快的存储器，用于存放主存中部分数据的副本。当 CPU 需要数据时，它首先检查 Cache：
- **命中 (Hit)**：如果在 Cache 中找到了数据，CPU 可以直接快速获取。
- **缺失 (Miss)**：如果在 Cache 中未找到数据，CPU 必须从下一级较慢的存储器（如主存）中获取数据，并将其加载到 Cache 中，以备将来访问。

> [!note]+ Cache 无处不在 (page 16)
> 在计算机体系结构中，几乎所有为了弥合速度差异而设置的缓冲区都可以看作是一种 Cache。
> * **寄存器** 是变量的 Cache（由软件管理）。
> * **L1 Cache** 是 L2 Cache 的 Cache。
> * **主存 (DRAM)** 可以看作是磁盘上**虚拟内存 (Virtual Memory)** 的 Cache。
> * **TLB (Translation Lookaside Buffer)** 是页表（Page Table）的 Cache。

#### 现代计算机的存储层次 (page 15, 17)

现代计算机通常有多级 Cache（L1, L2, L3），它们的容量和速度逐级变化。
- **个人移动设备 (Personal Mobile Device)**: 通常有两级 Cache。
- **笔记本/台式机 (Laptop/Desktop)**: 通常有三级 Cache。
- **服务器 (Server)**: 通常也有三级 Cache，但容量更大，速度更快。

#### Cache 设计的四个基本问题 (page 18)

设计一个 Cache 时，必须回答以下四个关键问题：

1. **块放置 (Block Placement)**: 一个从主存取出的块（Block）可以放在 Cache 的哪个位置？
    - **直接映射 (Direct Mapped)**: 每个主存块只能映射到 Cache 中的一个固定位置。
    - **全相联 (Fully Associative)**: 每个主存块可以映射到 Cache 中的任何位置。
    - **组相联 (Set Associative)**: Cache 被分成若干组（Set），每个主存块只能映射到固定的组，但在组内可以放在任何位置。这是前两者的折中，也是现代处理器最常用的方案。

2. **块识别 (Block Identification)**: 如何在 Cache 中找到一个块？
    - 通过比较地址中的**标记 (Tag)** 部分来识别。每个 Cache 行（line）除了存储数据块外，还存有标记位和有效位（valid bit）。

3. **块替换 (Block Replacement)**: 当发生 Cache 缺失且没有空闲位置时，应该替换哪个旧的块？
    - **随机 (Random)**: 随机选择一个块替换。
    - **最近最少使用 (Least Recently Used, LRU)**: 替换最长时间未被访问的块。
    - **先进先出 (First-In, First-Out, FIFO)**: 替换最早进入的块。

4. **写策略 (Write Strategy)**: 当发生写操作时，如何处理？
    - **写命中 (Write Hit)**:
        - **写直通 (Write-Through)**: 同时更新 Cache 和主存。通常配合**写缓冲 (Write Buffer)** 来隐藏写主存的延迟。
        - **写回 (Write-Back)**: 只更新 Cache，并设置一个**脏位 (Dirty Bit)**。该块只有在被替换时，如果脏位为 1，才会被写回主存。
    - **写缺失 (Write Miss)**:
        - **写分配 (Write Allocate)**: 先将块读入 Cache，再进行写操作（类似于写命中）。
        - **非写分配 (No-Write Allocate)**: 直接写入主存，不将块调入 Cache。

#### Cache 性能优化 (page 19-20)

Cache 的性能由**平均访存时间 (Average Memory Access Time, AMAT)** 来衡量：

$$
\text{AMAT} = \text{Hit Time} + \text{Miss Rate} \times \text{Miss Penalty}
$$

- **Hit Time**: 命中时间，访问 Cache 所需的时间。
- **Miss Rate**: 缺失率，访问 Cache 未命中的比例。
- **Miss Penalty**: 缺失代价，处理一次 Cache 缺失所需的额外时间。

因此，所有 Cache 优化技术都可以归结为对这三个参数的优化：

1. **降低缺失代价 (Reduce Miss Penalty)**: 多级缓存、关键宇优先（critical word first）。
2. **降低缺失率 (Reduce Miss Rate)**: 增大 Cache 容量、增大块大小、提高相联度、编译器优化。
3. **通过并行降低缺失代价和缺失率 (Reduce via parallelism)**: 非阻塞缓存（non-blocking caches）、硬件/软件预取（prefetching）。
4. **降低命中时间 (Reduce Hit Time)**: 使用更小、更简单的 Cache、流水化 Cache 访问。

最终，CPU 的整体性能也和 AMAT 息息相关，其公式可以表示为：

$$
\text{CPUtime} = \text{IC} \times \left(
(\text{CPI}_{\text{AluOps}} + \frac{\text{MemAccess}}{\text{Inst}} \times \text{AMAT} ) \times \text{CycleTime}
\right)
$$
这表明，内存访问的性能直接影响了总的 CPI。

### 指令级并行（ILP）的开发 (page 22)

除了前面提到的流水线，还有其他技术可以进一步发掘指令级并行。

- **超标量 (Superscalar)**: 在每个时钟周期内，可以发射和执行多条指令。这需要多个并行的功能单元。
- **超流水线 (Super-pipelining)**: 将流水线阶段划分得更细，从而可以提高时钟频率。
- **超长指令字 (Very Long Instruction Word, VLIW)**: 由编译器在编译时将多条可以并行执行的独立操作捆绑成一条很长的指令。硬件设计相对简单，但非常依赖编译器的能力。

### 并行体系结构分类 (page 23-35)

根据指令流（Instruction Stream）和数据流（Data Stream）的数量，Flynn 提出了经典的计算机体系结构分类法，即**Flynn 分类法 (Flynn's Taxonomy)**。

#### Flynn 分类法 (page 23-24)

1. **SISD (Single Instruction, Single Data)**: 单指令流，单数据流。传统的串行冯·诺依曼体系结构计算机。
2. **SIMD (Single Instruction, Multiple Data)**: 单指令流，多数据流。一条指令可以同时对多个数据执行相同操作。
3. **MISD (Multiple Instruction, Single Data)**: 多指令流，单数据流。多个处理器对同一个数据流执行不同操作，较为罕见。
4. **MIMD (Multiple Instruction, Multiple Data)**: 多指令流，多数据流。包含多个独立处理器，每个处理器执行自己的指令序列，处理自己的数据。这是当前并行计算机最主流的形式。

#### SIMD 体系结构 (page 25-27)

SIMD 利用了**数据级并行 (Data-Level Parallelism)**。

- [x] **向量处理器 (Vector Processor)**: 拥有专门的向量指令和向量寄存器，可以高效处理数组等数据结构。
- [x] **阵列处理器 (Array Processor)**: 包含大量处理单元，在控制器统一指挥下对数据的不同部分执行相同操作。
- **单级互连网络 (Single-stage interconnection network, 可能有小题)**: 用于 SIMD 架构中各处理单元之间或处理单元与存储体之间的数据交换。

#### MIMD 体系结构 (page 28-30)

MIMD 利用了**任务级并行 (Task-Level Parallelism)**。根据处理器共享内存的方式，MIMD 可以分为两大类：

1. **UMA (Uniform Memory Access)**: 统一内存访问模型，也称为**对称多处理器 (Symmetric Multiprocessors, SMP)**。所有处理器访问任何内存位置的延迟都是相同的。物理内存是集中式的，被所有处理器共享。

2. **NUMA (Non-Uniform Memory Access)**: 非统一内存访问模型，也称为**分布式共享内存 (Distributed Shared-Memory, DSM)**。物理内存分布在各个处理器节点上，处理器访问本地内存速度快，访问远程内存速度慢。

#### 内存一致性与缓存一致性 (page 31-35)

在 MIMD 系统中，由于多个处理器拥有各自的 Cache，必须解决数据一致性的问题。

> [!definition]+ 一致性 vs. 一贯性
>
> - **缓存一致性 (Cache Coherence)**: 定义了对**同一个内存地址**的读写行为。它确保任何处理器读取一个地址时，都能得到**最新**的写入值，无论这个值是由哪个处理器写入的。
> - **内存一致性 (Memory Consistency)**: 定义了对**不同内存地址**的读写操作的顺序。它规定了当一个处理器观察到其他处理器对不同地址的写操作时，这些写操作发生的顺序。

##### 缓存一致性协议 (Cache Coherence Protocols) (page 32)

主要有两种实现方法：

1. （考试重点）**监听协议 (Snooping Protocol)**: 用于基于总线的 SMP (UMA) 系统。每个 Cache 控制器都会“监听”总线上的所有事务。当一个 Cache 需要修改其数据时，它会通过总线广播一个消息，其他 Cache 接收到消息后会更新或无效化自己的副本。
2. **目录协议 (Directory-based Protocol)**: 用于大规模的 DSM (NUMA) 系统。系统中有一个集中的“目录”，记录了每个内存块的状态以及哪些处理器缓存了该块。当需要进行读写时，不再通过广播，而是向目录发送请求，由目录来协调各个 Cache 的更新。

##### 监听协议示例：MSI 与 MESI (page 33-35)

监听协议通常使用一个有限状态机来维护每个 Cache 块的状态。

> [!tip]+ MSI 协议 (page 33-34，重点)
>
> MSI 是基础的三态协议：
> - **M (Modified)**: 已修改。该 Cache 块是内存块的唯一副本，并且内容已被修改（与主存不一致）。
> - **S (Shared)**: 共享。该 Cache 块是内存块的干净副本（与主存一致），可能存在于多个处理器的 Cache 中。
> - **I (Invalid)**: 无效。该 Cache 块中的数据是无效的。

> [!tip]+ MESI 协议 (page 35)
>
> MESI 协议是 MSI 的一个扩展，增加了一个**独占 (Exclusive)** 状态，以优化“读-修改-写”序列。
> - **M (Modified)**: 同 MSI。
> - **E (Exclusive)**: 独占。该 Cache 块是内存块的唯一副本，但内容是干净的（与主存一致）。当处理器要写这个块时，可以直接进入 M 状态，无需通知其他 Cache，从而减少了总线流量。
> - **S (Shared)**: 同 MSI。
> - **I (Invalid)**: 同 MSI。