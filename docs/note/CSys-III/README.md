---
comments: true
---

# Computer system III

## scoring

- Final examination (30%)
- Process assessment (70%)
    - homework (4%)
    - class attendance (6%)
    - Labs
        - [ ] (8%) lab1 - BHT BTB
        - [ ] (8%) lab2 - Cache design
        - [ ] (8%) lab3 - Virtual Memory
        - [ ] (8%) lab4 - User mode
        - [ ] (10%)lab5 - Page fault and fork system call
        - [ ] (10%)lab6 - Hard ware support page fault and MMU
        - [ ] (8%) project - X part (8%)
 
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