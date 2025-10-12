---
tags:
  - notes
  - sysI
comments: true
---

## I Verilog HDL

### I.1 Introduction

#### I.1.1 Lexical Conventions（词汇约定）

![|500](attachments/03-Combinational-Logic-Design.png)

![|500](attachments/03-Combinational-Logic-Design-1.png)

> [立即数](https://zju-sys.pages.zjusct.io/sys1/sys1-sp24/lab1-1/#_11)

![|500](attachments/03-Combinational-Logic-Design-2.png)

![|500](attachments/03-Combinational-Logic-Design-3.png)

![|500](attachments/03-Combinational-Logic-Design-4.png) ![|500](attachments/03-Combinational-Logic-Design-5.png)

#### I.1.2 Basic Syntax: Module, Port and Instantiate

![](attachments/03-Combinational-Logic-Design-6.png)

> [!ATTENTION]
>
> 当实例化的模块含参数时，参数列表应该写在 instance-identifier 前面

#### I.1.3 Basic Syntax: Data Type

![|500](attachments/03-Combinational-Logic-Design-7.png)

![|500](attachments/03-Combinational-Logic-Design-8.png)

### I.2 Modeling methods

#### I.2.1 Structured modeling

• Module-level

根据逐层调用自己构建的模块来完成复杂的工程，就像我们在 C 语言中使用函数一样

• Gate-level

通过调用门级电路来完成

• Switch-level

通过调用硬件内部的晶体管

#### I.2.2 Dataflow modeling

• Suitable for modeling **combinational logic circuits**

• Use continuous assignment statements: `assign`

#### I.2.3 Behavioral modeling

`always @(event signal list) procedure statement`

### I.3 testbench

lab 里面经常会用的，作为仿真的测试输入。

## II Combinational Logic Circuit

![|500](attachments/03-Combinational-Logic-Design-9.png)

### II.1 2-level vs. multi-level

|       | speed | cost |
| ----- | ----- | ---- |
| two   | fast  | high |
| multi | low   | low  |

### II.2 design

![|500](attachments/03-Combinational-Logic-Design-10.png)

### II.3 special value

![|500](attachments/03-Combinational-Logic-Design-11.png)

## III Some Classic/Basic Designs

> 下面大多在 lab 中会实现

### III.1 Decoder

实验指导中的一/独热码 [one-hot code](https://zju-sys.pages.zjusct.io/sys1/sys1-sp24/lab1-2/#_4:~:text=%E6%80%A7%E6%9B%B4%E5%B7%AE%E3%80%82-,%E5%A4%8D%E5%90%88%E5%A4%9A%E8%B7%AF%E9%80%89%E6%8B%A9%E5%99%A8%E5%AE%9E%E7%8E%B0%E8%AF%91%E7%A0%81%E5%99%A8,-%E5%AF%B9%E4%BA%8E-N-%E4%BD%8D)，实现如下

![|500](attachments/03-Combinational-Logic-Design-12.png)

可以用于实现组合逻辑电路

![|500](attachments/03-Combinational-Logic-Design-13.png)

### III.2 Seven-Segment Display Decoder

![|500](attachments/03-Combinational-Logic-Design-14.png)

### III.3 Encoder

![|500](attachments/03-Combinational-Logic-Design-15.png)

考虑到一些不正常的输入（比如全为 0 或者多个 1），引入了 **Priority Encoder**

![|500](attachments/03-Combinational-Logic-Design-16.png)

### III.4 Multiplexer

![|500](attachments/03-Combinational-Logic-Design-17.png)

#### III.4.1 example

![|500](attachments/03-Combinational-Logic-Design-18.png)

### III.5 Demultiplexer

![|500](attachments/03-Combinational-Logic-Design-19.png)

### III.6 Half-Adder

![|500](attachments/03-Combinational-Logic-Design-20.png)

实现最基本的加法，输出结果和进位

### III.7 Full adder

#### III.7.1 simple full adder

![](attachments/03-Combinational-Logic-Design-22.png)

用两个半加器将三者加起来

#### III.7.2 ripple-carry adder（行波进位加法器）

![|500](attachments/03-Combinational-Logic-Design-21.png)

将低位的进位 Cout 输入给高位一起加，这和我们手动加法是一致的

#### III.7.3 carry-lookahead adder（超前进位加法器）

## IV Timing Analysis

![|500](attachments/03-Combinational-Logic-Design-23.png)

![|500](attachments/03-Combinational-Logic-Design-24.png)

> 有向无环赋权图 [Activity On Vertex Network (AOV 网)](../../DMPT/notes/05-Graph-Theory.md #Activity -On-Vertex-Network-(AOV-网))

![|500](attachments/03-Combinational-Logic-Design-25.png)

> 一个可能都应对方法：在没有非门的路上加延迟电路以便二者信号同时进入与门

