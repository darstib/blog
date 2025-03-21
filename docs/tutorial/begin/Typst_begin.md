---
comments: true
date: 2024-05-18
tags:
- begin
---
***

> [!SUMMARY]-
> 
> Typst 是一款轻量级的标记语言排版系统，可以用来替代 LaTeX 或 Word 等工具。
>
> - **基本使用：** Typst 提供了在线编辑器和本地编辑器，支持实时渲染和模板使用。
> - **环境配置：** 在 VScode + Ubuntu 环境下，完成安装 Typst 插件和 typst-cli 工具，并进行模板导入。
> - **参考文档：** 文章提供了 Typst 官方文档、教程和相关资源的链接。

本文将分为 **使用学习** 与 **本地环境配置** 两个部分。 

<!-- more -->

## 使用学习

### 基本介绍

> [!INTRODUCTION]
>
> Typst 是为科学写作而诞生的基于标记的排版系统。它被设计之初就是作为一种替代品，用于替代像 LaTeX 这样的高级工具，又或者是像 Word 和 Google Docs 这样的简单工具。我们对 Typst 的目标是构建一个功能强大的排版工具，并且让用户可以愉快地使用它。

相比于 LaTeX，typst 最大的特点就是轻量和[增量编译](https://en.wikipedia.org/wiki/Incremental_compiler)，这也导致了 typst 支持较为频繁地实时渲染。

### 在线环境

在最开始，我们可以在 typst 的[官方网站](https://typst.app/)直接使用它，也就是人们常说的 **开箱即用**。

注册登入，看到下面的界面：

![](attachments/Make%20pdf%20with%20typst.png)

点击 `Empty document` ，设置一个名字（这里使用 **test** 作为测试名），创建后到达下面的界面：

![](attachments/Make%20pdf%20with%20typst-1.png)

在左侧简单输入几个字符作为测试，待加载完成（√ 处可以看见加载的动图）后右侧就出现了文字：很简单，左侧编辑，右侧看效果。

![](attachments/Make%20pdf%20with%20typst-2.png)

当然，这只是写文本，我们需要在样式上优化，这需要读者自行阅读[教程](https://typst-doc-cn.github.io/docs/tutorial/)，不是我三言两语讲的完的。

完成后，点击右上角的下载图标即可下载 pdf。

### 引入模板

很多时候我们并不想要所有的样式都自己写，这个时候 **模板** 就很重要了，我们可以在 [主页面](https://typst.app/)左下角的星球图标 [typst universe](https://typst.app/universe) 的 [templates](https://typst.app/universe/search/?kind=templates) 看到许多模板。点进一个作为示例：

![](attachments/Make%20pdf%20with%20typst-3.png)

点击图片我们可以预览样式，右侧的 `create project in app` 可以将模板导入到我们的主页面中：（下面在右侧自命名后创建即可）

![](attachments/Make%20pdf%20with%20typst-4.png)

![](attachments/Make%20pdf%20with%20typst-6.png)

点击右侧需要修改的部分就会自动定位到左侧对应的编辑部分，然后修改即可；左侧图标第一个是文件夹。注意，对于图片等考虑 **路径** 的编辑还请仔细阅读文档相关部分，了解 **路径** 这一概念。

### 开始使用

学习一个东西最好的办法就是阅读他的[官方文档](https://typst.app/docs/tutorial/)。对于教程，如果您不喜英文，可以看看非官方维护的[中文教程](https://typst-doc-cn.github.io/docs/tutorial/)。当然，有时候官方文档会较为晦涩；又或者过于详细，而我们不需要知道那么多。

一个语法简单的介绍使用可见我使用 touyin 做的 [typst_cheatsheet](../../static/typst_cheatsheet.zip) 笔记，使用 [touyin](https://touying-typ.github.io/zh/) 模板；[Typst Examples Book](https://sitandr.github.io/typst-examples-book/book/) 也是一个很好的入门和进阶教程。

## 本地环境配置

相比于在线，我更加喜欢在本地环境编辑。下面是在 VScode + 类 unix 环境上编辑 typst 的配置说明。

> [!env]-
> 
> 注：我使用了 wsl:ubuntu 22.04；关于 vscode 安装不多说明，网上一大堆。
> 
> 对于 macOS，使用 `brew install typst` 应该就能够安装好。

### vscode 配置

安装下面的插件（后续可能有变动，按需）：

- Typst LSP
- ~~Typst Preview~~
- Typst Companion

> 这些插件我自己自定义过快捷键，就不讲解如何使用了，一搜一大堆。

### typst-cli 安装

安装 typst-cli 是为了让我们能够像 `git clone` 一样能够拉取编辑材料至本地使用。注意我们上方 `模板使用`  部分的截图中有这么一行 `typst init @preview/bloated-neurips:0.2.1` ，这就是在 typst-cli 中使用的。

```sh
# 如果没有安装过curl和cargo这两个工具，请自行搜索
# 由于 typst 由 rust 编写，需要安装 rust 编译器
# 安装 Rust 环境并激活，之前安装过则不需要执行下面这两行
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs/ | sh -s -- -y
source $HOME/.cargo/env
# 安装 Typst CLI
cargo install --git https://github.com/typst/typst.git typst-cli
# 键入检查是否安装成功
typst
# or
typst --version
```

过程中出现问题 `failed to run custom build command for openssl-sys v0.9.60` 可以尝试以下几个命令，来自 [StackOverflow](https://stackoverflow.com/questions/65553557/why-rust-is-failing-to-build-command-for-openssl-sys-v0-9-60-even-after-local-in)；您可以逐一尝试，我也不记得我是在尝试哪一个过后成功的了。🥲

```bash
sudo apt install pkg-config
sudo apt-get install libudev-dev
sudo apt install libssl-dev
sudo apt install librust-openssl-sys-dev
sudo apt install pkg-config
sudo dnf install perl
sudo apt-get install build-essential
```

![](attachments/Make%20pdf%20with%20typst-7.png)

### 模板导入

在命令行(CLI)中进入到合适位置，键入

```bash
[~/work/typst/template]$ typst init @preview/bloated-neurips:0.2.1
```

![](attachments/Make%20pdf%20with%20typst-8.png)

可以看到左侧已经可以出现了文件夹了，可以直接使用了，先预览看看（插件使用自查）

![](attachments/Make%20pdf%20with%20typst-9.png)

如果出现红色报错等情况，对于模板而言很可能就是 **路径** 问题，时而需要自己修改；对于我们自己写路径，相对路径是最好的，因为不知道什么时候我们可能就将文件夹修改了位置。

## 推荐宏包

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

- 参考：[Typst Examples Book - package](https://sitandr.github.io/typst-examples-book/book/packages/index.html)

## 参考资料

- https://typst.app/
- https://forum.typst.app/
- https://typst.app/docs/tutorial/
- https://typst-doc-cn.github.io/docs/tutorial/
- https://typst.app/universe/package/bloated-neurips
- https://github.com/howardlau1999/sysu-thesis-typst
- https://stackoverflow.com/questions/65553557/why-rust-is-failing-to-build-command-for-openssl-sys-v0-9-60-even-after-local-in

