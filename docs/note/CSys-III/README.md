---
comments: true
tags:
  - notes
---

# Computer system III

## note

> [!attention]
>
> 需要声明的是，复习笔记为将 slids 上传给 gemini-2.5 处理后，我自己边学边修改的结果。
>
> 主要是有时候自己想加点东西，而全自己做笔记发现更多的时候还是在复制粘贴截图，故借助 LLM 整理，望悉知。

## scoring

- Final examination (30%)
	- 题型
		- 15 choices (30 pt)
		- 4 answer questions (2 hard / 2 soft)
	- 重点
		- 量化分析方法（Amdahl 定律，CPU 性能公式，Cache 性能优化）
		- Cache 设计的四个基本问题
		- 动态调度（tomasulo 为主）
		- MSI 状态机
		- 内存（页表，和 lab3 有关）
		- 文件系统（I-node，Unix 的组合方案，磁盘块分配）
- Process assessment (70%)
    - homework (4%)
    - class attendance (6%)
    - Labs
        - [x] (8%) lab1 - BHT BTB
        - [x] (8%) lab2 - Cache design
        - [x] (8%) lab3 - Virtual Memory
        - [x] (8%) lab4 - User mode
        - [x] (10%)lab5 - Page fault and fork system call
        - [x] (10%)lab6 - Hard ware support page fault and MMU
        - [x] (8%) project - X part (8%)
 
[实验安排](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/14_250314-220727.png)：

```mermaid
gantt
    title Labs Schedule
    dateFormat  YYYY-MM-DD
    % Anchor: 春二 (W2) starts 2025-02-17. Each subsequent column is 7 days later.
    axisFormat %m/%d

    section Hardware
    % Lab 1: 春二 (W2, 3 weeks)
    Lab 1：分支预测           :l1, 2025-02-26, 21d
    % Lab 2: 春五 (W5, 3 weeks)
    Lab 2：Cache            :l2, 2025-03-19, 21d

    section Soft ware
    % Lab 3: 春八 (W8, 2 weeks)
    Lab 3：虚拟内存             :l3, 2025-04-09, 14d
    % Lab 4: 夏一 (W9, 2 weeks)
    Lab 4：用户模式        :l4, 2025-04-16, 14d
    % Lab 5: 夏二 (W10, 2 weeks)
    Lab 5：缺页+fork    :l5, 2025-04-23, 14d

    section Hard ware
    % 劳动节 marker points between 夏三 (W11) and 夏四 (W12). Milestone at start of W12.
    % 劳动节 (Labor Day approx.) : milestone, m1, 2025-05-01, 0d
    % Lab 6: 夏四 (W12, 4 weeks)
    Lab 6：硬件 缺页+MMU       :l6, 2025-04-30, 28d
    % Project Xpart: 夏五 (W13, 4 weeks)
    Project： Xpart             :px, 2025-05-14, 28d
```

## source url

- linux kernel v5.2.21
	- [下载版](https://git.codelinaro.org/bryan.odonoghue/kernel/-/tree/v5.2.21)
	- [阅读版](https://elixir.bootlin.com/linux/v5.2.21/source)
- [riscv ISA](https://note.tonycrane.cc/cs/pl/riscv/)
	- [非特权级 ISA](https://note.tonycrane.cc/cs/pl/riscv/unprivileged/)
	- [特权级 ISA](https://note.tonycrane.cc/cs/pl/riscv/privileged/)
	- [页表相关](https://note.tonycrane.cc/cs/pl/riscv/paging/)
- some tutorial in sys II
	- [内联汇编](https://zju-sys.pages.zjusct.io/sys2/sys2-fa24/lab4/#_4)
	- [S-mode trap 相关 CSR](https://zju-sys.pages.zjusct.io/sys2/sys2-fa24/lab5/#_5)
	- [软硬件实验 clock_set_next_event 调整](https://zju-sys.pages.zjusct.io/sys2/sys2-fa24/lab7/#_6)
	- [bootloader 介绍](https://zju-sys.pages.zjusct.io/sys2/sys2-fa24/lab7/#bootloader)
	- [硬件调试](https://zju-sys.pages.zjusct.io/sys2/sys2-fa24/lab7/#_22)


