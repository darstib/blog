---
comments: true
date: 2024-03-16
tags:
- begin
---

***

> [!SUMMARY]-
> 
> Logisim 是一款用于学习计算机系统和数字逻辑电路的软件。
>
> - **电线：** 不同颜色的电线代表不同的含义。
> - **引脚：** 可以添加输入/输出引脚，并改变数据位宽和输入值。
> - **Wiring 工具：** 包括探针、常量、隧道、分线器等，用于信号传输和处理。
> - **MUX（多路选择器）：** 根据选择端信号选择输入端口。
> - **Register（寄存器）：** 用于存储数据。
> - **自定义封装电路：** 可以创建自己的电路模块。

<!-- more -->

对于每一位学习计算机系统或者数字逻辑电路的 zjuer，logisim 是必须使用的，下面将较为详细地介绍其使用方法。

> [!PREREQUISITE]
>
> - 安装 logisim-evolution 并学会启动
> 
> - 清楚基本的概念，如引脚、反相器及对应图标，线路连接原理 

> [!ENV]
>
> - logisim-evolution-3.8.0-all.jar

> [!TIP]
>
> File => Prefence => Language => cn/cn 可以设置中文
> 
> 但是不是很建议。

基本使用可以先看[Logisim 教程](https://soc.ustc.edu.cn/COD/other/logisim/)

## 电线

下面是电线颜色代表含义

![|450](attachments/logisim%20基本使用-1.png)

## 引脚

### 引脚的添加

下面是输入引脚（输出引脚同理）添加步骤：（椭圆表示起始步骤，下同）

![|450](attachments/logisim%20基本使用.png)

### 引脚的使用

我们可以看到，可以改变数据位宽(data bits)，通过“手指”可以点击改变输入 **0/1**

> 引脚内部数字的排列顺序与二进制相同，我们亦可以说图中输入的是 3'b010（即立即数）
> **立即数线路数组**[¶](https://zju-sys.pages.zjusct.io/sys1/sys1-sp24/lab1-1/#_11 "Permanent link")
>
> 立即数数组由三部分组成 : `imm = LEN ' BASE NUM`
> 

- 第一部分 LEN 是立即数的线路长度，LEN=3 表示立即数大小为 3 位线路
- 第二部分 BASE 表示立即数的进制，b、d、h 分别表示二进制、十进制、十六进制
- 第三部分 NUM 是对应立即数的值，必须和 BASE 指示的进制相对应，例如 4'b98 就是非法的

> 将立即数转化为电路的方法如下：
> 
> 将立即数转换为二进制的 01 串，如果 01 串位数少于 LEN 则在前面补 0，如果大于 LEN 则高位截断

2. 立即数的 0 表示该线路的输入是 GND，立即数是 1 表示该线路输入是 VCC

3. 立即数的 01 串从低位到高位依次是 IMM[0], IMM[1], ..., IMM[LEN-1]

```txt
3'b01 // 3'b001 
6'd67 // 6'b1000011 -> 6'b000011 
16'h1234 // 16'b0001001000110100
```

改变输入引脚的输入后，可以发现线路颜色变了，那么就可以尝试遍历不同的输入观察输出了！

> [!tip]+
>
> - 想改变引脚朝向？选中引脚后上下左右方向键即可！
> - 双击引脚可以命名哦，这对于导出电路非常重要（注意字母大小写！）

## Wiring 工具

页面上直接能看见的工具我们不再讲解，来看看 **Wiring** 中的工具：

<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/18_logisim_begin-2.png" alt="" style="width: 30%;">
    <p></p>
</div>

### probe（探针）

获得线路信号

![|425](attachments/logisim%20基本使用-3.png)

不过其实用“手指”点线路就能看到信号，探针适用于需要观察多条线路信号

### Constant（常量 ）

顾名思义，当我们想要一个（局部）唯一的输入时使用，同样可以改变位宽、值

![|475](attachments/logisim%20基本使用-4.png)

注意，值 `Value` 使用 16 进制表示

![|450](attachments/logisim%20基本使用-5.png)

### Tunnel（隧道）

隧道起到一个传输信号的作用，同名隧道代表同一个值

![|475](attachments/logisim%20基本使用-6.png)

### splitter（分线器）

我们常需要将位宽合并，直接相连是不可行的

![|450](attachments/logisim%20基本使用-7.png)

分线器就是用于将信号分路/合并的

![|475](attachments/logisim%20基本使用-8.png)

注意调设位宽等，小数字暗示了输出位置

也可以用于截取信号，左侧面板调节每个口的信号源

![|450](attachments/logisim%20基本使用-9.png)

其他 wiring 工具我们在后面遇到再进行讲解

## MUX（多路选择器）

多路选择器（Multiplexer）在复用器 Plexers 中

![|425](attachments/logisim%20基本使用-10.png)

如图，`select bits` (记为 n) 代表选择端信号的位数，输入端口数即为 $2^{n}$ ；`data bits` 即数据位宽，要求输入端（每一个）、多路选择器、输出端一致；在图中，由上至下依次为 $0,1,2\dots 2^{n}-1$ 接口，选择端的输入即表示选择几号接口的输入

## Register（寄存器）

(To be continue)

## 自定义封装电路

(To be continue)

## 参考文章

- https://blog.csdn.net/RuanFun/article/details/130795720
- https://blog.csdn.net/qq_44838412/article/details/107074857
