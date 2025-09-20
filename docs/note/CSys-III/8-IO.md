---
tags:
  - notes
comments: true
---

# I/O 系统

本文档综合讲解了计算机系统中的 I/O（输入/输出）系统，涵盖了从硬件交互到软件接口、性能优化以及内核子系统的各个方面。

## I/O 系统概述 (page 2-37)

> [!extra]- 磁盘系统回顾 (page 2-4)
>
> 在深入 I/O 系统之前，快速回顾了磁盘相关概念：
>
> - **磁盘组成**: 盘片（platter）、磁道（track）、扇区（sector）、柱面（cylinder）。
> - **定位时间**: 寻道时间（seek time）+ 旋转延迟（rotational latency）。
> - **磁盘结构与连接**: 主机直连（host-）、网络（network-）、存储区域网络（storage area network, SAN）。
> - **磁盘调度算法**: 先来先服务（FCFS）、最短寻道时间优先（SSTF）、扫描算法（SCAN）、循环扫描算法（C-SCAN）、LOOK、C-LOOK。
> - **磁盘管理**: 物理格式化（physical formatting）、分区（partition disk）、逻辑格式化（logical formatting）。
> - **RAID (Redundant Array of Inexpensive Disks)**:
>     - **RAID 0**: 条带化（split），无冗余，提升性能。
>     - **RAID 1**: 镜像（mirror），提供数据冗余。
>     - **RAID 4/5/6**: 带奇偶校验的块级条带化（block with parity），提供数据冗余和性能平衡。

I/O 管理是操作系统设计和运行中的一个重要组成部分。I/O 设备是计算机与用户和其他系统进行交互的方式，其类型和控制方法多种多样，性能也差异巨大。设备驱动程序（Device Driver）封装了设备细节，并提供统一的接口。新型设备层出不穷，使得 I/O 管理成为一个持续演进的领域。

### I/O 硬件 (page 6-7)

I/O 硬件种类繁多，包括存储设备（如磁盘）、通信设备（如网卡）和人机交互设备（如键盘、鼠标）。尽管种类繁多，但它们与计算机接口的信号有一些共同概念。

- **总线 (Bus)**: 连接计算机各组件（包括 CPU）的互连线路。
- **端口 (Port)**: 设备的连接点。
- **控制器 (Controller)**: 控制设备的组件。控制器可以集成在设备内部，也可以是单独的电路板。它们通常包含处理器、微代码（microcode）、私有内存（private memory）和总线控制器等。

计算机访问 I/O 设备的方式主要有两种：**轮询（polling）** 和 **中断（interrupt）**。

![PC Bus Structure|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2506/13_250613-141832.png)

### I/O 硬件与 CPU 交互 (page 8)

不同的 CPU 架构对 I/O 硬件的访问方式有所不同：

- **专用 I/O 指令 (Dedicated I/O Instructions)**: 某些 CPU 架构（如 x86 的 `in`, `out`, `ins`, `outs` 指令）提供专门的 I/O 指令来访问设备。这些指令主要用于访问设备控制器中用于数据和控制的寄存器。
    - 设备通常提供用于数据输入/输出（`data-in/data-out`）、状态（`status`）和控制/命令（`control/command`）的寄存器。
    - 设备驱动程序（device driver）会将命令或数据指针写入这些寄存器。
    - 这些寄存器通常只有 1-4 字节大小，或者作为 FIFO（先入先出）缓冲区。
- **内存映射 I/O (Memory-mapped I/O)**: 许多设备将它们的寄存器或板载内存映射到 CPU 的内存地址空间中。这意味着 CPU 可以像访问普通内存一样，通过加载/存储指令来访问这些设备寄存器或内存。
    - 这种方式常用于访问大容量的板载内存，如图形卡的显存。

> [!example]+ PC 上的 I/O 端口地址范围 (page 9)
>
> 在 PC 架构中，部分 I/O 端口的十六进制地址范围与对应设备示例如下：
>
> | I/O 地址范围 (十六进制) | 设备                |
> | :---------------------- | :------------------ |
> | 000-00F                 | DMA 控制器          |
> | 020-021                 | 中断控制器          |
> | 040-043                 | 定时器              |
> | 200-20F                 | 游戏控制器          |
> | 2F8-2FF                 | 串口 (secondary)    |
> | 320-32F                 | 硬盘控制器          |
> | 378-37F                 | 并口                |
> | 3D0-3DF                 | 显卡控制器          |
> | 3F0-3F7                 | 软盘驱动器控制器    |
> | 3F8-3FF                 | 串口 (primary)      |

### 轮询 (Polling) (page 10)

轮询是一种 I/O 访问机制，CPU 会周期性地检查设备的状态寄存器，以确定设备是否准备好进行 I/O 操作或操作是否完成。

- **操作流程**:
    1. 如果设备正忙（通过检查状态寄存器），CPU 会进行忙等待（busy-wait）。
    2. 一旦设备空闲，设备驱动程序将命令发送到设备控制器（写入命令寄存器）。
    3. CPU 持续读取状态寄存器，直到它指示命令已执行完成。
    4. 读取执行状态，并可能重置设备状态。
- **优缺点**:
    - **优点**: 简单易实现。
    - **缺点**: 需要忙等待，会浪费 CPU 资源。如果设备速度慢，效率会非常低下。仅当设备非常快时，轮询才比较合理。

### 中断 (Interrupts) (page 11-17)

中断是另一种 I/O 访问机制，旨在避免 CPU 的忙等待，提高 CPU 资源利用率。

- **基本原理**:
    - 设备驱动程序（作为操作系统的一部分）向控制器（或设备）发送命令后立即返回，CPU 可以调度其他任务。
    - 当命令执行完成或发生特定事件时，设备会向处理器发出中断信号。
    - 操作系统通过中断处理程序（interrupt handler）来检索结果。
- **上下文切换 (Context Switch)**: 基于中断的 I/O 操作在开始和结束时都需要进行上下文切换。
    - 当中断频率极高时，频繁的上下文切换会消耗大量 CPU 时间。
    - **解决方案**: 在高中断频率下，有时会选择使用轮询。例如，Linux 的 **NAPI（New API）** 在高网络负载下会启用轮询，以减少中断和上下文切换的开销。

> [!note]+ 中断驱动 I/O 周期 (page 12)
>
> 一个典型的中断驱动 I/O 周期流程如下：
>
> 1. **设备驱动程序发起 I/O**: CPU 上的设备驱动程序发起一个 I/O 操作。
> 2. **I/O 控制器启动 I/O**: I/O 控制器接收到命令，并启动 I/O 操作。
> 3. **设备产生中断信号**: 当 I/O 完成（输入数据准备好、输出完成或发生错误）时，设备生成中断信号。
> 4. **CPU 接收中断并转移控制**: CPU 在执行指令间隙检查中断。接收到中断后，CPU 将控制权转移到中断处理程序。
> 5. **中断处理程序处理数据**: 中断处理程序处理数据。如果是输入操作，将数据存储到设备驱动程序缓冲区。
> 6. **中断处理程序返回**: 中断处理程序处理完毕后返回。
> 7. **CPU 恢复被中断任务**: CPU 恢复执行被中断的任务。

#### 中断在 CPU 架构中的实现 (page 13-15)

操作系统会维护一个中断向量表（Interrupt Vector Table），其中包含了不同类型中断对应的处理程序入口地址。

- **Intel Pentium 中断向量表 (page 13)**:
    - 0-18: 预定义异常，如除法错误（0）、调试异常（1）、断点（3）、页错误（14）等。
    - 19-31: Intel 保留。
    - 32-255: 可屏蔽中断（maskable interrupts），通常用于外部设备中断。
- **Linux 在 ARM64 上的中断向量表 (page 14)**:
    - 展示了 ARM64 架构下 Linux 内核的异常向量表定义（`ENTRY(vectors)`），包括同步异常（`sync`）、中断请求（`irq`）、快速中断请求（`fiq`）和错误（`error`）等，针对不同的异常级别（EL0, EL1h, EL1t）有不同的入口。
    - 代码片段显示了如何设置向量基地址寄存器 `vbar_el1`。
- **Linux 在 RISC-V64 上的中断向量表 (page 15)**:
    - 展示了 RISC-V64 架构下 Linux 内核的异常向量表定义（`SYM_CODE_START(excp_vect_table)`），包含了各种陷阱（trap）或异常的处理入口，如指令错位（`insn_misaligned`）、指令非法（`insn_illegal`）、断点（`break`）、页错误（`page_fault`）等。
    - `setup_trap_vector` 函数通过 `csrw CSR_TVEC, a0` 将异常处理函数的地址写入 `CSR_TVEC` 控制状态寄存器。

#### 中断与异常 (page 16)

中断不仅用于 I/O 操作，也用于处理各种异常事件：

- **保护错误 (Protection Error)**: 访问违规，如访问不允许的内存区域。
- **页错误 (Page Fault)**: 内存访问错误，如访问未映射或不在物理内存中的页面。
- **系统调用 (System Calls)**: 软件中断，应用程序通过系统调用请求操作系统服务。

#### 多 CPU 系统中的中断 (page 16-17)

在多核 CPU 系统（Multi-CPU systems）中，中断可以并行处理。

- **CPU 亲和性 (CPU Affinity)**:
    - 有时一个 CPU 可以专门用于处理中断，以优化中断处理性能。
    - 中断也可以被分配到特定的 CPU 上处理，这被称为 **SMP IRQ Affinity**。
    - 从 Linux 2.4 内核开始，系统管理员可以为特定的中断请求（IRQ）分配到特定的处理器或处理器组。
    - **目的**: 允许系统更高效地处理各种硬件事件，平衡工作负载。
    - **应用示例**:
        - 在多处理器机器中，将不同的网卡（NIC）绑定到不同的 CPU，可以更好地处理网络流量。
        - 数据库服务器或具有大量磁盘存储的服务器，可以专门分配一个 CPU 处理磁盘控制器，另一个 CPU 处理网卡，从而提高响应时间。

### 直接内存访问 (Direct Memory Access, DMA) (page 18-19)

DMA 是一种允许 I/O 设备和内存之间直接传输数据，而无需 CPU 干预的技术。

> [!definition]+ DMA (page 18)
>
> **DMA** 允许 I/O 设备和内存之间直接传输数据，绕过 CPU。这意味着 CPU 只需要发出命令，而数据传输本身由 DMA 控制器（DMA Controller）完成，从而减轻 CPU 的负担。

- **优势**:
    - 数据传输绕过 CPU，CPU 可以执行其他任务。
    - 无需通过编程 I/O（逐字节传输），数据可以以大块（large blocks）的形式传输，效率更高。
- **组件**: 需要设备或系统中存在 DMA 控制器。
- **操作流程**:
    1. 操作系统向 DMA 控制器发出命令，命令中包含操作类型、数据在内存中的地址、要传输的字节数等信息。
    2. 这些命令通常是指向命令的指针，写入 DMA 控制器的命令寄存器。
    3. DMA 控制器根据命令直接在 I/O 设备和内存之间传输数据。
    4. 传输完成后，DMA 设备会向 CPU 发出中断信号，通知 CPU 传输完成。

> [!example]- DMA 传输步骤 (page 19)
>
> 假设设备驱动程序要将 `drive2` 中的数据传输到内存地址 `x` 处的缓冲区：
>
> 1. **设备驱动程序请求传输**: 设备驱动程序被告知将 `drive2` 的数据传输到内存地址 `x` 的缓冲区。
> 2. **驱动程序指示控制器**: 设备驱动程序告诉驱动器控制器将 `c` 字节数据传输到地址 `x` 的缓冲区。
> 3. **驱动器控制器启动 DMA**: 驱动器控制器（SAS 驱动器控制器）发起 DMA 传输。
> 4. **DMA 控制器传输数据**: DMA 控制器直接将数据传输到内存中的缓冲区 `x`，同时内存地址递增，计数器 `c` 递减，直到 `c` 变为 0。
> 5. **DMA 完成中断 CPU**: 当 `c` 变为 0 时，DMA 控制器中断 CPU，以信号通知传输完成。

### 应用程序 I/O 接口 (page 20-22)

应用程序通过 I/O 接口与 I/O 设备进行交互。操作系统通过系统调用（system calls）封装设备行为，提供通用接口。

- **设备作为文件**: 在 Linux 中，设备可以像文件一样被访问，这大大简化了编程模型。
- **`ioctl`**: 对于低层级的设备访问和控制，Linux 提供 `ioctl` 系统调用。

> [!example]+ Linux `/dev` 目录列表 (page 21，但下面的内容是我自己电脑上的)
>
> ```shell
> $ ls -l
> total 0
> crw-r--r-- 1 root root     10, 235 Jun 13 14:38 autofs
> drwxr-xr-x 2 root root         560 Jun 13 14:38 block
> drwxr-xr-x 2 root root          80 Jun 13 14:38 bsg
> crw-rw---- 1 root disk     10, 234 Jun 13 14:38 btrfs-control
> drwxr-xr-x 3 root root          60 Jun 13 14:38 bus
> drwxr-xr-x 2 root root        2.7K Jun 13 14:38 char
> crw------- 1 root root      5,   1 Jun 13  2025 console
> lrwxrwxrwx 1 root root          11 Jun 13 14:38 core -> /proc/kcore
> crw------- 1 root root     10, 125 Jun 13 14:38 cpu_dma_latency
> crw------- 1 root root     10, 203 Jun 13 14:38 cuse
> drwxr-xr-x 6 root root         120 Jun 13 14:38 disk
> drwxr-xr-x 3 root root         100 Jun 13 14:38 dri
> crw-rw-rw- 1 root root     10, 127 Jun 13 14:38 dxg
> lrwxrwxrwx 1 root root          13 Jun 13 14:38 fd -> /proc/self/fd
> crw-rw-rw- 1 root root      1,   7 Jun 13 14:38 full
> crw-rw-rw- 1 root root     10, 229 Jun 13 14:38 fuse
> drwxr-xr-x 2 root root           0 Jun 13 14:38 hugepages
> crw------- 1 root root    229,   0 Jun 13 14:38 hvc0
> crw--w---- 1 root tty     229,   1 Jun 13 14:38 hvc1
> ...
> ```
>
> 输出中的每一行代表一个设备文件或目录，显示了其权限、所有者、组、大小、时间戳以及设备类型（例如 `c` 代表字符设备，`d` 代表目录，`b` 代表块设备，`l` 代表符号链接）。`disk` 和 `tty` 是常见的设备文件，可以像普通文件一样进行读写操作。

- **设备驱动层**: 设备驱动层（device-driver layer）隐藏了不同 I/O 控制器之间的差异，为内核提供统一的接口。
    - 每个操作系统都有自己的 I/O 子系统和设备驱动框架。
    - 新设备如果遵循已实现的协议，则无需额外的开发工作。

> [!note]+ I/O 结构 (page 22)
>
> 典型的 I/O 结构分为硬件层和软件层，并进一步细分：
>
> - **软件层 (Software)**:
>     - **内核 (Kernel)**: 操作系统的核心部分。
>     - **内核 I/O 子系统 (Kernel I/O subsystem)**: 处理 I/O 请求的核心逻辑。
>     - **设备驱动程序 (Device Driver)**: 针对特定设备（如 SCSI、键盘、鼠标、PCI 总线设备、软盘、ATAPI 设备）提供接口。
> - **硬件层 (Hardware)**:
>     - **设备控制器 (Device Controller)**: 控制实际硬件设备，例如 SCSI 设备控制器、键盘控制器、鼠标控制器、PCI 总线设备控制器、软盘控制器、ATAPI 设备控制器。
>     - **设备 (Devices)**: 实际的物理 I/O 设备，如 SCSI 设备、键盘、鼠标、PCI 总线、软盘驱动器、ATAPI 设备（包括磁盘、磁带、驱动器）。
>
> 这种分层结构使得操作系统能够通过设备驱动程序与各种底层硬件进行交互，同时为应用程序提供统一的 I/O 接口。

### I/O 设备的特点 (page 23-28)

I/O 设备在多个维度上存在显著差异，这影响了它们的管理方式和性能。

#### 设备的分类维度 (page 23)

- **数据传输模式**:
    - **字符流 (character-stream)**: 以字符为单位传输数据，如键盘、串口。
    - **块 (block)**: 以固定大小的块为单位传输数据，如磁盘。
- **访问方法**:
    - **顺序访问 (sequential-access)**: 数据只能按顺序访问，如磁带。
    - **随机访问 (random-access)**: 数据可以随机访问，如磁盘、内存。
- **同步性**:
    - **同步 (synchronous)**: I/O 操作完成后才返回，进程等待。
    - **异步 (asynchronous)**: I/O 操作在后台进行，进程不等待，通过信号或回调通知完成。
    - 或两者兼有。
- **共享性**:
    - **可共享 (sharable)**: 多个进程可以同时访问，如文件系统。
    - **专用 (dedicated)**: 每次只能被一个进程独占访问，如打印机。
- **操作速度**: 设备速度差异巨大，从毫秒级到微秒级，甚至纳秒级。
- **读写能力**:
    - **读写 (read-write)**: 可读可写，如磁盘。
    - **只读 (read only)**: 只能读取，如 CD-ROM。
    - **只写 (write only)**: 只能写入，如打印机。

> [!note]+ I/O 设备特性表 (page 24)
>
> | 特性 (aspect)    | 变化 (variation)             | 示例 (example)         |
> | :--------------- | :--------------------------- | :--------------------- |
> | 数据传输模式     | 字符 (character), 块 (block) | 终端 (terminal), 磁盘 (disk) |
> | 访问方法         | 顺序 (sequential), 随机 (random) | 调制解调器 (modem), CD-ROM |
> | 传输调度         | 同步 (synchronous), 异步 (asynchronous) | 磁带 (tape), 键盘 (keyboard) |
> | 共享             | 专用 (dedicated), 可共享 (sharable) | 磁带 (tape), 键盘 (keyboard) |
> | 设备速度         | 延迟 (latency), 寻道时间 (seek time), 传输速率 (transfer rate), 操作间延迟 (delay between operations) | -                      |
> | I/O 方向         | 只读 (read only), 只写 (write only), 读写 (read-write) | CD-ROM, 显卡控制器 (graphics controller), 磁盘 (disk) |

#### 操作系统对设备的分类 (page 25)

操作系统通常将 I/O 设备大致分为以下几类：

- **块 I/O (Block I/O)**:
    - 数据以固定大小的块（block）进行访问。
    - 命令通常包括 `read`、`write`、`seek`。
    - 可以是原始 I/O（raw I/O）、直接 I/O（direct I/O），或通过文件系统访问。
    - 支持内存映射文件访问（memory-mapped file access）。
    - 通常使用 DMA 传输。
    - 示例：磁盘驱动器。
- **字符 I/O (Character I/O)**:
    - 数据以字符流（stream）的形式访问。
    - 设备类型非常多样。
    - 示例：键盘、鼠标、串口。
- **内存映射文件访问 (Memory-mapped File Access)**: 将文件或设备映射到进程的内存空间，通过内存访问指令来读写文件或设备。
- **网络套接字 (Network Sockets)**: 用于网络通信的抽象接口。

操作系统通常会提供一个“后门”或“逃生口”机制，允许应用程序直接向设备发送特定的 I/O 命令。在 Linux 中，这通常是通过 `ioctl` 系统调用完成的。

#### 网络设备 (Network Devices) (page 27)

网络设备由于其数据传输的特殊性，通常拥有自己的接口，与块设备和字符设备有所不同。

- 网络设备接口通常与管道（pipe）和邮箱（mailbox）等机制不同。
- **套接字接口 (Socket Interface)** 是网络访问的流行接口。
    - 它将网络协议的细节与底层的网络操作分离开来。
    - 有趣的是，一些非网络操作也被实现为套接字，例如 Unix 域套接字（Unix socket），用于同一主机上进程间的通信。

#### 时钟与定时器 (Clocks and Timers) (page 28)

时钟和定时器在操作系统中也常被视为一种字符设备。

- 它们提供当前时间、经过时间（elapsed time）和定时器功能，是系统中的关键设备。
- 通常分辨率约为 1/60 秒，但有些操作系统也提供更高分辨率的时钟。

#### 同步/异步 I/O (Synchronous/Asynchronous I/O) (page 29-30)

I/O 操作可以分为同步（Synchronous）和异步（Asynchronous）两大类。

- **同步 I/O (Synchronous I/O)**: 应用程序在 I/O 操作完成之前会被阻塞。
    - **阻塞 I/O (Blocking I/O)**: 进程被暂停，直到 I/O 完成。
        - 易于使用和理解。
        - 但效率可能较低，因为进程必须等待。
        - 不适用于所有需求（例如，需要同时处理多个 I/O 或不希望进程长时间阻塞的场景）。
    - **非阻塞 I/O (Non-blocking I/O)**: I/O 调用会立即返回，返回尽可能多的可用数据。
        - 进程不会被阻塞，会立即返回。
        - 通常需要使用 `select` 或 `poll` 等机制来检查数据是否准备好，然后才能进行读写传输。
- **异步 I/O (Asynchronous I/O)**: 进程在 I/O 操作执行时继续运行，I/O 子系统通过信号（signal）或回调（callback）机制通知进程 I/O 完成。
    - **优点**: 进程可以并发执行，效率非常高，CPU 利用率高。
    - **缺点**: 使用起来相对复杂，需要更复杂的编程模型来处理完成通知。

> [!example]+ 两种 I/O 方法对比 (page 30)
>
> 幻灯片 30 展示了两种 I/O 方法的时间线图：
>
> - **(a) 阻塞 I/O**:
>     - 用户态进程发起 I/O 请求。
>     - 陷入内核（`trap to kernel`），执行系统调用（`system call`）。
>     - 设备驱动程序发起 I/O，此时请求进程进入等待状态（`---waiting---`），无法执行其他任务。
>     - 硬件进行数据传输。
>     - 中断处理程序接收中断，处理数据，并返回。
>     - 系统调用返回到用户态，请求进程恢复执行。
> - **(b) 非阻塞/异步 I/O**:
>     - 用户态进程发起 I/O 请求。
>     - 陷入内核，执行系统调用。
>     - 设备驱动程序发起 I/O，但系统调用立即返回到用户态（`return to calling thread`）。请求进程可以继续执行其他任务，不必等待 I/O 完成。
>     - 硬件进行数据传输。
>     - 中断处理程序接收中断，处理数据，并可能通过信号或其他机制通知请求进程 I/O 完成。
>
> 阻塞 I/O 的优点是流程直观，易于理解和编程，但会占用 CPU 等待 I/O。非阻塞/异步 I/O 则能让 CPU 在 I/O 进行的同时处理其他任务，从而提高系统吞吐量，但程序设计复杂度增加。

### 内核 I/O 子系统 (Kernel I/O Subsystem) (page 31-32)

内核 I/O 子系统是操作系统中管理 I/O 的核心部分，它提供了一系列服务来优化和保护 I/O 操作。

- **I/O 调度 (I/O Scheduling)**:
    - 通过为每个设备维护一个 I/O 请求队列，对 I/O 请求进行排队。
    - 对 I/O 进行调度，以确保公平性（fairness）和提供服务质量（quality of service, QoS）。常见的磁盘调度算法（如 FCFS, SSTF, SCAN 等）就属于 I/O 调度。
- **缓冲 (Buffering)**:
    - 在设备之间传输数据时，将数据存储在内存中。
    - **解决设备速度不匹配**: 例如，从网络接收数据并写入 SSD 时，网络传输速度可能远快于 SSD 写入速度，需要缓冲区进行平滑。双缓冲（double buffering）是常见的实现方式。
    - **解决设备传输大小不匹配**: 例如，网络数据包可能需要重新组装成完整的消息。
    - **维护“复制语义” (copy semantics)**: 例如，`write()` 系统调用通常会先将用户数据复制到内核缓冲区，然后再写入设备，即使在 `write()` 调用返回后用户修改了原始数据，写入设备的数据也不会受到影响。
- **缓存 (Caching)**:
    - 将数据的副本保存在内存中，以便快速访问。
    - 对性能至关重要。
    - 有时与缓冲结合使用。
    - 内存中的缓冲区也常被用作文件操作的缓存。
- **假脱机 (Spooling)**:
    - 假脱机（spool）是一个缓冲区，用于保存设备的输出（或设备的输入），特别是当设备一次只能服务一个请求时。
    - 最常见的例子是打印：多个打印任务会先被发送到打印假脱机，然后由打印机按照顺序逐一处理。
- **设备预留 (Device Reservation)**:
    - 为进程提供对设备的独占访问。
    - 通过系统调用进行设备的分配（allocation）和解除分配（de-allocation）。
    - 在使用设备预留时需要注意避免死锁（deadlock）问题。

### 错误处理 (Error Handling) (page 33)

操作系统在处理 I/O 错误时通常有两种策略：

- **尝试从错误中恢复**:
    - 例如，设备暂时不可用、短暂的写入失败。
    - 有时通过重试读写操作来恢复。
    - 更高级的错误处理系统会跟踪错误频率，如果设备频繁出现错误，可能会停止使用该设备。
- **返回错误码或错误号**:
    - 当 I/O 请求失败时，一些操作系统会直接返回一个错误号或错误码给调用者。
    - 系统错误日志（system error logs）会记录这些问题报告，供系统管理员或开发人员分析。

### I/O 保护 (I/O Protection) (page 34-37)

操作系统需要保护 I/O 设备，防止恶意或未经授权的访问。

- **保护必要性**:
    - 例如，键盘输入可能会被按键记录器（keylogger）窃取，如果键盘未受保护。
    - 必须始终假定用户可能试图非法获取 I/O 访问权限。
- **保护措施**:
    - **特权 I/O 指令**: 将所有 I/O 指令定义为特权指令（privileged instructions），只有在内核模式下才能执行。
    - **通过系统调用执行 I/O**: I/O 操作必须通过系统调用（system calls）来完成。当用户态进程需要执行 I/O 时，它会发起一个系统调用，从而陷入内核模式，由内核执行 I/O 操作。
    - **保护内存映射 I/O 和 I/O 端口**: 内存映射 I/O 区域和 I/O 端口也必须受到保护，通常通过内存管理单元（MMU）或地址映射权限来实现。

> [!example]- 使用系统调用执行 I/O (page 35)
>
> 该图展示了用户态进程如何通过系统调用执行 I/O 操作：
>
> 1. **陷阱到内核 (trap to kernel)**: 用户态的请求进程发起一个系统调用（`system call n`），这会触发一个陷阱（trap）或中断，使 CPU 从用户模式切换到内核模式。
> 2. **执行 I/O (perform I/O)**: 内核接收到系统调用请求后，会调度到对应的系统调用处理函数（`system call dispatch to n`），然后由内核执行实际的 I/O 操作（例如 `read` 操作）。
> 3. **返回到调用线程 (return to calling thread)**: I/O 操作完成后，内核将控制权返回给用户态的调用线程。

- **内核数据结构 (Kernel Data Structures)**:
    - 内核会维护 I/O 组件的状态信息，例如：
        - 打开文件表（open file tables）。
        - 网络连接（network connections）。
        - 字符设备状态。
    - 许多数据结构用于跟踪缓冲区、内存分配和“脏”块（dirty blocks），这些结构有时非常复杂。
    - 某些操作系统（如 Windows）使用消息传递（message passing）来实现 I/O。I/O 信息以消息的形式从用户模式传递到内核，并在流经设备驱动程序并返回到进程时被修改。

> [!example]+ UNIX I/O 内核结构 (page 37)
>
> UNIX 系统的 I/O 内核结构图展示了从用户进程到实际 I/O 设备的层级关系以及相关数据结构：
>
> - **用户进程内存 (user-process memory)**: 包含每个进程的**文件描述符（file descriptor）**。
> - **每进程打开文件表 (per-process open-file table)**: 每个文件描述符对应一个条目，指向系统范围的打开文件表中的记录。
> - **系统范围打开文件表 (system-wide open-file table)**:
>     - 包含**文件系统记录 (file-system record)**: 包括 `inode` 指针，以及指向读写、选择（`select`）、`ioctl` 和关闭（`close`）等功能的函数指针。
>     - 包含**网络（套接字）记录 (networking (socket) record)**: 包括网络信息指针，以及指向读写、选择、`ioctl` 和关闭等功能的函数指针。
> - **活跃 inode 表 (active-inode table)**: 记录当前正在使用的 inode。
> - **网络信息表 (network-information table)**: 记录网络相关信息。
> - **内核内存 (kernel memory)**: 存储这些内核数据结构。
>
> 这种结构允许不同的用户进程通过文件描述符共享文件系统记录或网络记录，实现了 I/O 的统一管理和资源共享。

## I/O 请求到硬件操作的转换 (page 38-39)

系统资源的访问需要映射到具体的硬件操作。

- **读取文件为例**:
    1. **确定设备**: 确定哪个设备（例如磁盘）持有该文件。
    2. **名称转换**: 将文件名转换为设备表示形式（例如在 FAT 和 UNIX 中，通常是主设备号/次设备号，`major/minor`）。
    3. **物理读取**: 从磁盘物理读取数据到缓冲区。
    4. **数据可用**: 将数据提供给请求进程。
    5. **控制返回**: 将控制权返回给请求进程。

> [!example]+ I/O 请求的生命周期 (page 39)
>
> ![Life cycle of I/O request|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2506/13_250613-150923.png)
> 
> 该图详细展示了一个 I/O 请求从用户态到硬件的完整生命周期：
>
> 1. **用户态请求 I/O**: 用户进程发起 I/O 请求。
> 2. **系统调用**: 请求通过系统调用进入内核。
> 3. **内核 I/O 子系统检查**:
>     - 如果内核 I/O 子系统已经能够满足请求（例如数据已在缓存中），则直接将数据放置在返回值或进程空间中，并返回给用户态。
>     - 如果不能满足，则继续下一步。
> 4. **发送请求到设备驱动**: 内核将请求发送到设备驱动程序，如果需要则阻塞请求进程。
> 5. **设备驱动处理**: 设备驱动程序处理请求，向控制器发出命令，并配置控制器使其阻塞直到中断。
> 6. **设备控制器执行命令**: 设备控制器执行命令并监控设备状态。
> 7. **I/O 完成，生成中断**: I/O 完成后，设备控制器生成中断信号。
> 8. **中断处理程序**:
>     - 接收中断，如果是输入操作，将数据存储在设备驱动程序的缓冲区中。
>     - 发送信号以解除阻塞设备驱动程序。
> 9. **设备驱动程序更新状态**: 设备驱动程序确定哪个 I/O 已完成，并指示 I/O 子系统状态已更改。
> 10. **内核 I/O 子系统放置数据**: 内核 I/O 子系统将数据放置在返回值或进程空间中。
> 11. **系统调用返回**: 系统调用返回，I/O 操作完成，输入数据可用或输出完成。

## 性能 (Performance) (page 40-42)

I/O 是影响系统性能的一个主要因素。

- **影响性能的因素**:
    - **CPU 开销**: CPU 需要执行设备驱动程序和内核 I/O 代码。
    - **上下文切换**: 中断导致的频繁上下文切换。
    - **数据缓冲和复制**: 数据在用户空间、内核空间、设备缓冲区之间进行复制，增加开销。
    - **网络流量**: 处理网络流量尤其带来压力，因为它通常涉及大量小包和高中断频率。

> [!example]+ 网络通信：高上下文切换 (page 41)
>
> 该图展示了远程登录时每个字符传输导致的频繁上下文切换：
>
> **发送系统 (Sending System)**:
>
> 1. 用户在键盘上键入字符。
> 2. 键盘生成中断。
> 3. CPU 保存状态，进入内核，接收中断。
> 4. 中断处理程序执行。
> 5. 设备驱动程序处理数据。
> 6. **上下文切换**: 从内核模式切换回用户模式（如果中断处理完毕）。
> 7. 字符被发送，用户进程向网络适配器发送字符，并通过系统调用返回。
> 8. 网络适配器发送数据包。
>
> **接收系统 (Receiving System)**:
>
> 9. 网络适配器接收数据包。
> 10. 网络适配器生成中断。
> 11. CPU 保存状态，进入内核，接收中断。
> 12. 中断处理程序执行。
> 13. 设备驱动程序处理数据。
> 14. **上下文切换**: 从内核模式切换回用户模式。
> 15. 网络守护进程（network daemon）或用户进程接收数据包。
>
> 每一个字符的传输都可能导致发送和接收系统上发生多次上下文切换，从而显著降低性能。

### 提高性能的策略 (page 42)

- **减少上下文切换次数**: 避免频繁的内核/用户模式切换。
- **减少数据复制**: 优化数据路径，避免不必要的数据在内存中的复制。
- **通过大传输、智能控制器和轮询来减少中断**:
    - 使用更大的传输块，减少中断频率。
    - 使用具备更强处理能力的智能控制器，自主完成更多任务。
    - 在特定场景下（如高负载），使用轮询来代替中断。
- **使用 DMA (Direct Memory Access)**: 允许数据直接在设备和内存之间传输，减轻 CPU 负担。
- **使用更智能的硬件设备**: 采用具有更高性能和更强功能的新型 I/O 设备。
- **平衡 CPU、内存、总线和 I/O 性能**: 确保系统各组件之间的性能平衡，以实现最高吞吐量。
- **将用户模式进程/守护进程移到内核线程**: 对于某些关键任务，将其在内核线程中运行可以减少上下文切换的开销，提高效率，但这会增加内核的复杂性和潜在的风险。

## 示例：Linux `tty` 设备 (page 43-46)

以 Linux 的 `tty`（Teletypewriter，终端设备）为例，展示 I/O 设备的初始化和写操作流程。

### 设备初始化 (`/dev/tty`) (page 43)

- `tty_init` 函数负责 `tty` 设备的初始化。
- 该函数会创建 `/dev/tty` 文件，使其可以通过文件系统接口访问。

> [!example]+ `tty_init` 代码片段 (page 43)
>
> ```c
> int _init tty_init(void)
> {
>     // 注册 sysctl 接口，用于管理 dev/tty 相关的参数
>     register_sysctl_init("dev/tty", tty_table);
>     // 初始化字符设备结构
>     cdev_init(&tty_cdev, &tty_fops);
>     // 添加字符设备到系统并注册设备号区域
>     if (cdev_add(&tty_cdev, MKDEV(TTYAUX_MAJOR, 0), 1) ||
>         register_chrdev_region(MKDEV(TTYAUX_MAJOR, 0), 1, "/dev/tty") < 0)
>         panic("Couldn't register /dev/tty driver\n");
>     // 创建/dev/tty 设备文件
>     device_create(&tty_class, NULL, MKDEV(TTYAUX_MAJOR, 0), NULL, "tty");
> }
> ```
>
> 这段代码展示了 `tty` 驱动在 Linux 内核中的初始化过程，包括注册系统控制接口、初始化字符设备结构、添加设备到系统并创建设备文件。

### 设备写入 (`write` 系统调用) (page 44)

当应用程序向 `/dev/tty` 写入数据（例如 `echo` 命令）时，数据会经过一系列函数调用最终到达 `tty_write` 函数。

> [!example]+ `vfs_write` 到 `tty_write` 的调用链 (page 44)
>
> 当一个 `write` 系统调用发生时，数据流经以下路径：
>
> 1. `ssize_t vfs_write(struct file *file, const char __user *buf, size_t count, ...)`: 这是文件系统层面的通用写入函数。它会检查文件权限和可写性。
> 2. `if (file->f_op->write)`: `vfs_write` 会通过文件对象的 `f_op`（文件操作结构体）中的 `write` 或 `write_iter` 函数指针进行间接调用。
> 3. `tty_fops` 结构体：
>     ```c
>     static const struct file_operations tty_fops = {
>         .llseek = no_llseek,
>         .read_iter = tty_read,
>         .write_iter = tty_write, // <-- 这里被调用
>         .splice_read = copy_splice_read,
>         .splice_write = iter_file_splice_write,
>         .poll = tty_poll,
>         .unlocked_ioctl = tty_ioctl, // <-- ioctl 系统调用会到这里
>         .compat_ioctl = tty_compat_ioctl,
>         .open = tty_open,
>         .release = tty_release,
>         .fasync = tty_fasync,
>         .show_fdinfo = tty_show_fdinfo,
>     };
>     ```
>     从 `tty_fops` 定义可以看出，`write_iter` 成员指向 `tty_write` 函数。因此，`vfs_write` 最终会调用 `tty_write` 来处理 `tty` 设备的写入操作。

### Linux `ioctl` 系统调用 (page 45-46)

`ioctl` (Input/Output Control) 系统调用是一个通用的设备控制接口，用于操纵底层设备的参数。

> [!definition]+ `ioctl` (page 45)
>
> `ioctl()` 系统调用用于操作特殊文件的底层设备参数。它允许应用程序发送设备特定的命令，以控制设备的各种特性，例如终端设备的行规程、波特率等。参数 `fd` 必须是一个打开的文件描述符。

- **函数原型**: `int ioctl(int fd, unsigned long request, ...);`
    - `fd`: 打开的文件描述符。
    - `request`: 特定于设备的命令码。
    - `...`: 可变参数，通常是指向数据结构的指针，用于传递命令所需的参数或返回结果。
- **实现**: `ioctl` 系统调用最终会通过文件操作结构体（`file_operations`）中的 `unlocked_ioctl` 函数指针进行间接调用，对于 `tty` 设备而言，就是调用 `tty_ioctl`。

> [!example]+ `ioctl` 系统调用实现 (page 46)
>
> `ioctl` 系统调用在 Linux 内核中的处理路径是：
>
> `ioctl syscall` -> `vfs_ioctl` -> 间接调用 `filp->f_op->unlocked_ioctl` -> `tty_ioctl`
>
> `vfs_ioctl` 是内核中处理 `ioctl` 系统调用的通用函数：
>
> ```c
> long vfs_ioctl(struct file *filp, unsigned int cmd, unsigned long arg)
> {
>     int error = -ENOTTY;
>     // 检查文件操作结构中是否存在 unlocked_ioctl 函数指针
>     if (!filp->f_op->unlocked_ioctl)
>         goto out;
>     // 通过函数指针进行间接调用
>     error = filp->f_op->unlocked_ioctl(filp, cmd, arg);
>     // 处理可能的错误码
>     if (error == -ENOIOCTLCMD)
>         error = -ENOTTY;
> out:
>     return error;
> }
> EXPORT_SYMBOL(vfs_ioctl);
> ```
>
> 这里的 `filp->f_op->unlocked_ioctl` 对于 `tty` 设备而言，就是指向 `tty_fops` 结构体中的 `.unlocked_ioctl = tty_ioctl`。
>
> `ioctl` 提供了强大的设备控制能力，但也因为其底层和灵活性，历史上曾导致许多安全问题，因为它允许用户态程序直接操纵设备参数，如果使用不当，可能被利用进行权限提升或其他恶意行为。

## 总结 (Takeaway) (page 47)

本系列讲解的核心要点：

- **I/O 硬件**: 了解 I/O 设备的基本组成（总线、端口、控制器）和与 CPU 的交互方式（专用 I/O 指令、内存映射 I/O）。
- **I/O 访问**: 掌握轮询和中断两种 I/O 访问机制的原理、优缺点及其在多 CPU 系统中的应用（如 SMP IRQ affinity）。理解 DMA 如何提高 I/O 效率。
- **设备类型**: 区分 I/O 设备的多种特性，如数据传输模式、访问方法、同步性、共享性、速度和读写能力。理解操作系统如何将设备分类为块设备、字符设备、网络设备等。
- **应用程序 I/O 接口**: 了解应用程序如何通过系统调用（如 `read`, `write`, `ioctl`）与 I/O 设备交互，以及设备在 Linux 中如何被抽象为文件。
- **内核 I/O 子系统**: 认识内核 I/O 子系统在管理 I/O 中的作用，包括 I/O 调度、缓冲、缓存、假脱机和设备预留。理解 I/O 请求的生命周期和性能优化策略。
