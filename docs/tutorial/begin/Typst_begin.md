---
comments: true
date: 2024-05-18
tags:
- begin
---

> [!SUMMARY]-
> 
> Typst 是一款轻量级的标记语言排版系统，可以用来替代 LaTeX 或 Word 等工具。
>
> - **基本使用：** Typst 提供了在线编辑器和本地编辑器，支持实时渲染和模板使用。
> - **环境配置：** 在 VScode + Ubuntu 环境下，完成安装 Typst 插件和 typst-cli 工具，并进行模板导入。
> - **参考文档：** 文章提供了 Typst 官方文档、教程和相关资源的链接。

<!-- more -->

## 使用学习

### 基本介绍

> [!INTRODUCTION] [概述](https://typst.app/docs)
> 
> Typst is a new markup-based typesetting system for the sciences. It is designed to be an alternative both to advanced tools like LaTeX and simpler tools like Word and Google Docs. Our goal with Typst is to build a typesetting tool that is highly capable and a pleasure to use.
> 
> Typst 是为科学写作而诞生的基于标记的排版系统。它被设计之初就是作为一种替代品，用于替代像 LaTeX 这样的高级工具，又或者是像 Word 和 Google Docs 这样的简单工具。我们对 Typst 的目标是构建一个功能强大的排版工具，并且让用户可以愉快地使用它。
> 
> > [!quote]+ [Typst - Brand](https://typst.app/legal/brand/)
> >
> > If you use the Typst name in prose, always capitalize it as Typst. Pronounce Typst as /taɪpst/, i.e. 'Ty' like in **Ty**pesetting and 'pst' like in Hi**pst**er.
> 
> 
> > [!question]- 即生 LaTeX，何生 Typst?
> >
> > 关于 Typst 的优势等详细了解，有兴趣可以查看 [A Wikipedia article about Typst](https://forum.typst.app/t/a-wikipedia-article-about-typst/444) 处的链接

相比于 LaTeX，typst 最大的特点就是**轻量和增量编译**，这也导致了 typst 支持较为频繁地实时渲染。

> [!wiki]- [Incremental compiler  增量编译器](https://en.wikipedia.org/wiki/Incremental_compiler)
>
> An **incremental compiler** is a kind of [incremental computation](https://en.wikipedia.org/wiki/Incremental_computation "Incremental computation") applied to the field of [compilation](https://en.wikipedia.org/wiki/Compiler "Compiler"). Quite naturally, whereas ordinary compilers make a so-called **clean build**, that is, (re)build all program modules, an incremental compiler recompiles only modified portions of a program.  
> 
> 增量编译器是一种应用于编译领域的增量计算。很自然地，普通编译器进行所谓的干净构建，即（重新）构建所有程序模块，而增量编译器仅重新编译程序中已修改的部分。

## 在线环境

在最开始，我们可以在 typst 的[官方网站](https://typst.app/)直接使用它，和 [overleaf](https://overleaf.com) 是类似的；注册登入，看到下面的界面：

![](attachments/Make%20pdf%20with%20typst.png)

点击 `Empty document` ，设置一个名字，创建后到达下面的界面：

![](attachments/Make%20pdf%20with%20typst-1.png)

在左侧简单输入几个字符作为测试，待加载完成（√ 处可以看见加载的动图）后右侧就出现了文字：很简单，左侧编辑，右侧看效果。

![](attachments/Make%20pdf%20with%20typst-2.png)

当然，这只是写文本，我们需要在样式上优化，这需要读者自行阅读[教程](https://typst-doc-cn.github.io/docs/tutorial/)，不是我三言两语讲的完的。完成后，点击右上角的下载图标即可导出 pdf 或者是其他格式。

### 引入模板

很多时候我们并不想要所有的样式都自己写，这个时候 **模板** 就很重要了，我们可以在 [主页面](https://typst.app/)左下角的星球图标 [typst universe](https://typst.app/universe) 的 [templates](https://typst.app/universe/search/?kind=templates) 看到许多模板。点进一个作为示例：

![](attachments/Make%20pdf%20with%20typst-3.png)

点击图片我们可以预览样式，右侧的 `create project in app` 可以将模板导入到我们的主页面中：（下面在右侧自命名后创建即可）

![](attachments/Make%20pdf%20with%20typst-4.png)

![](attachments/Make%20pdf%20with%20typst-6.png)

点击右侧需要修改的部分就会自动定位到左侧对应的编辑部分，然后修改即可；左侧图标第一个是文件夹。注意，对于图片等考虑 **路径** 的编辑还请仔细阅读文档相关部分，了解 **路径** 这一概念。

## 本地环境配置

如果你在意文件之间代码/图片的复用性，希望自己设计/调节模板/在本地编译运行，下面是在 VScode + 类 unix 环境上编辑 typst 的配置说明；现在 typst 也[开放了可执行程序下载](https://github.com/typst/typst/releases)，但是我没使用过，留给读者探索。

### vscode 配置

安装下面的插件（第一个比较重要，其余按需；使用可以自行搜索）：

- Tinymist Typst
- Typst Sync
- ~~Typst LSP~~
- ~~Typst Preview~~

### typst-cli 安装

> [!attention]+
>
> 安装 typst-cli 是为了让我们能够像 `git clone` 一样能够拉取编辑材料至本地使用。注意我们上方 `模板使用`  部分的截图中有这么一行 `typst init @preview/bloated-neurips:0.2.1` ，这就是在 typst-cli 中使用的；当然，上面给出的那些插件本身会帮助我们将文件获取到 `~/.cache` 中，所以可以自己决定，并非必要内容。

> [!env]+ 安装环境
> 
> 演示使用了 wsl:ubuntu 22.04/kali-linux；对于 macOS，使用 `brew install typst` 应该就能够安装好。

```sh
# 如果没有安装过curl和cargo这两个工具，请自行搜索
# 由于 typst 由 rust 编写，需要安装 rust 编译器
# 安装 Rust 环境并激活，之前安装过则不需要执行下面这两行
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs/ | sh -s -- -y
source $HOME/.cargo/env
```

```sh
# 安装 Typst CLI
cargo install --git https://github.com/typst/typst.git typst-cli
# 键入检查是否安装成功
typst
# or
typst --version
```

过程中出现问题 `failed to run custom build command for openssl-sys v0.9.60` 可以尝试以下几个命令，来自 [StackOverflow](https://stackoverflow.com/questions/65553557/why-rust-is-failing-to-build-command-for-openssl-sys-v0-9-60-even-after-local-in)；您可以逐一尝试，我也不记得我是在尝试哪一个过后成功的了🥲。

```bash
sudo apt install pkg-config
sudo apt install libudev-dev
sudo apt install libssl-dev
sudo apt install librust-openssl-sys-dev
sudo dnf install perl
sudo apt install build-essential
```

![](attachments/Make%20pdf%20with%20typst-7.png)

### 模板导入

在命令行(CLI)中进入到合适位置，例如：

```sh
$ typst init @preview/bloated-neurips:0.2.1
```

![](attachments/Make%20pdf%20with%20typst-8.png)

可以看到左侧已经可以出现了文件夹了，可以直接使用了，先预览看看：

![](attachments/Make%20pdf%20with%20typst-9.png)

如果出现红色报错等情况，对于模板而言很可能就是 **路径** 问题，时而需要自己修改，当然有可能是模板是在某一个大版本之前的内容，其中一些用法被抛弃了[^1]；对于我们自己写路径，相对路径是最好的，因为不知道什么时候我们可能就将文件夹修改了位置；随后我们移动时最好是整个移动，类似于在线环境

[^1]: 其实这种做法非常难绷，导致之前的模板很可能无法直接使用，此时还是选择 [typst app](https://typst.app/) 吧，可以修改编译器版本。

## 开始使用

学习一个东西最好的办法就是阅读他的[官方文档](https://typst.app/docs/tutorial/)。对于教程，如果您不喜英文，可以看看非官方维护的[中文教程](https://typst-doc-cn.github.io/docs/tutorial/)。当然，有时候官方文档会较为晦涩；又或者过于详细，而我们不需要知道那么多。

- 一个语法简单的介绍使用可见我使用 touyin 做的 [typst_cheatsheet](../../static/typst_cheatsheet.pdf)【[源码](../../static/typst_cheatsheet.zip) 】 笔记，使用 [touyin](https://touying-typ.github.io/zh/) 模板；
- [Typst Examples Book](https://sitandr.github.io/typst-examples-book/book/) 
	- 也是一个很好的入门和进阶教程；
- [不太简短的 typst 教程](http://ai-assets.404.net.cn/pdf/typst/typst-zh_CN-20230409.pdf)
	- 教程面向使用是很好的，但是如果没有一点基础可能看不太懂；
- [tex2typst](https://qwinsi.github.io/tex2typst-webapp/) 一个在线转换工具，当然 [pandoc](https://pandoc.org/try/) 等也开始支持 Typst 的相关转换。

### [语法模式](https://typst.app/docs/reference/syntax/)

Typst 有三种语法模式：标记、数学和代码。标记模式是 Typst 文档的默认模式，数学模式允许编写数学公式，代码模式允许使用 Typst 的脚本功能。

| New mode |            Syntax             |            Example            |
| :------: | :---------------------------: | :---------------------------: |
|  Markup  |  Surround markup with `[..]`  |    `let name = [*Typst!*]`    |
|   Code   |   Prefix the code with `#`    |       `Number: #(1 + 2)       |
|   Math   | Surround equation with `$..$` | `$-x$ is the opposite of $x$` |

- 在默认情况下，我们出于 Markup 模式，这也是我们主要填充内容的部分。
- 由于 Typst 的脚本语言与许多现代变成语言非常像（尤其 python），所以只要你学习过一两门编程语言，应该都能大概看懂每一行是在干什么（结合编译结果）；
	- 一旦使用 `#` 进入代码模式，除非在中间切换回标记或数学模式，否则不需要使用更多的井号；
	- 值得注意的是，代码模式下的 “函数” 往往有一个参数的类型为 content，大多数情况下这个参数都可以放在函数调用后，形如 `#func()[content]`；而其他参数可设置默认值，如果不需要修改，那么 `()` 也可以省略，即 `#func[content]` 即可使用，这也是大多数 Markup 的调用形式；反过来想，strong 等也是可以自己调整的，[查看介绍](https://typst.app/docs/reference/model/strong/)；
	- 在 `[]` 包裹的内容也是 Markup 模式，所以我们在可以嵌套进入其他模式。
- Typst 的数学模式中的符号标记与 LaTeX 并不一致；为了摆脱无穷无尽的 `\`，Typst 的想法是：
	- `$$` 包裹的内容中，如果左右两侧是紧靠着的，那么视为行内公式；如果两侧均有空格，那么视为行间公式；
	- 对于其中的字符，使用空格进行分隔，抛弃 `\`，如 `pi` 而非 `\pi` ；而对于诸如 `abandon` 等词，首先将其视为变量去寻找；如果没有定义过这个变量，则会报错。
		- 那么我们该如何获得类似于 $area = \pi * radius^{2}$ 的公式呢？
		- 使用双引号包裹 **两个字母以上的变量名** `$"area" = pi * "radius"^(2)$`。

> [!quote]- [Note on function purity](https://typst.app/docs/reference/foundations/function/#note-on-function-purity)
>
> In Typst, all functions are _pure._ This means that for the same arguments, they always return the same result. They cannot "remember" things to produce another value when they are called a second time.  
> 
> 在 Typst 中，所有函数都是纯函数。这意味着对于相同的参数，它们总是返回相同的结果。它们不能“记住”任何事情，在第二次调用时产生另一个值。
> 
> The only exception are built-in methods like [`array.push(value)`](https://typst.app/docs/reference/foundations/array/#definitions-push). These can modify the values they are called on.  
> 
> 唯一的例外是内置方法，如 `array.push(value)` 。这些方法可以修改它们被调用的值。




## 推荐资料

- [Typst 中文社区导航](https://typst-doc-cn.github.io/guide/)
- [图片识别](https://typress-web.vercel.app/)

- [mitex](https://typst.app/universe/package/mitex/)
    - 支持渲染 latex 语法
- [cmaker](https://typst.app/universe/package/cmarker)
	- 支持渲染 markdown 语法
- [touyin](https://typst.app/universe/package/touying/)
	- 使用 tpyst 制作简单的 ppt
- [cetz](https://typst.app/universe/package/cetz) [docs](https://cetz-package.github.io/)
	- a library for drawing
- [badgery](https://typst.app/universe/package/badgery)
	- 行内小色块
- [gentle-clues](https://typst.app/universe/package/gentle-clues)
	- mdbook-like callouts
- [colorful-boxes](https://typst.app/universe/package/colorful-boxes)
	- 包裹式注释块
- [tablex](https://typst.app/universe/package/tablex/) or [tablem](https://typst.app/universe/package/tablem)
	- 花式表格
- [alog](https://typst.app/universe/package/algo)
	- 带行号代码块、伪代码块

- 部分参考：[Typst Examples Book - package](https://sitandr.github.io/typst-examples-book/book/packages/index.html)

## 参考资料

- https://typst.app/
	- https://forum.typst.app/
	- https://typst.app/docs/tutorial/
	- https://typst.app/universe/package/bloated-neurips
- https://typst-doc-cn.github.io/guide/
- https://github.com/howardlau1999/sysu-thesis-typst
- https://stackoverflow.com/questions/65553557/why-rust-is-failing-to-build-command-for-openssl-sys-v0-9-60-even-after-local-in
- https://sitandr.github.io/typst-examples-book/book/
- http://ai-assets.404.net.cn/pdf/typst/typst-zh_CN-20230409.pdf
