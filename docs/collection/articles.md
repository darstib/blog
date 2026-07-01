---
comments: true
tags:
- collection
---

> [!quote] 
> 
> - [Computing Life](https://yage.ai/)
> 	- “这个博客叫Computing Life，从 2012 年开始写作，现在有 370 多篇文章，中英双语（[English](https://yage.ai/tag/english.html) / [中文](https://yage.ai/tag/chinese.html)）。主要写 AI 方法论和工程实践，偶尔写天文摄影。贯穿始终的主题是：怎么对技术做清晰的思考，怎么构建真正能用的系统。”

## 知识类

### 传统计算机科学

- [Why you should use `python -m pip`](https://snarky.ca/why-you-should-use-python-m-pip/)
- [huffman-tree](https://oi-wiki.org/ds/huffman-tree/) & [Visual Information Theory](https://colah.github.io/posts/2015-09-Visual-Information/)
    - 哈夫曼树/编码 & 信息论/交叉熵
- [一文读懂Python async/await异步编程](https://zhuanlan.zhihu.com/p/698683843)
	- [FastAPI - 并发 async/await](https://fastapi.tiangolo.com/zh/async/)

### 机器/深度学习

- [神经网络中的偏置（bias）究竟有什么用？](https://www.zhihu.com/question/305340182)
	- 推荐先看[霍普菲尔德网络如何通过能量景观帮助大脑完成记忆回忆？](https://www.bilibili.com/video/BV1d6zSYTEFp)
- [反馈神经网络——Hopfield网络](https://zhuanlan.zhihu.com/p/457810569)
- [凸优化 - 拉格朗日对偶](https://www.lesswrong.com/)
- [混合专家模型 (MoE) 详解](https://huggingface.co/blog/zh/moe)
- [Understanding Reasoning LLMs](https://magazine.sebastianraschka.com/p/understanding-reasoning-llms)
- [DeepSeek-R1技术剖析：没有强化学习基础也能看懂的PPO & GRPO](https://mp.weixin.qq.com/s/OIiNOMcuXERGVOghwNZ5Uw) and [A vision researcher’s guide to some RL stuff: PPO & GRPO](https://yugeten.github.io/posts/2025/01/ppogrpo/)
- [RLHF 技术详解](https://huggingface.co/blog/zh/rlhf)

## 方法教程类

### 终端

#### 美化部分

- [zsh_begin](../tutorial/begin/zsh_begin.md) 记录了我的配置使用；
- [oh my zsh](https://ohmyz.sh/)
	- [zsh + oh-my-zsh 配置](https://www.haoyep.com/posts/zsh-config-oh-my-zsh/)
	- [iTerm2 安装配置](https://guoxudong.io/post/iterm2/#iterm2)
	- [zsh技巧——devv的回答](https://devv.ai/search?threadId=dri8mmonqh34)
	- [zsh卸载](https://gist.github.com/breithbarbot/254e58bd87009963b3f58405d75cbe6c)
- [oh my posh](https://ohmyposh.dev/)
	- [Windows Terminal 内核优化，主题配置](https://www.codestar.top/2024/09/11/Windows/Windows-Terminal%E5%86%85%E6%A0%B8%E3%80%81%E9%85%8D%E7%BD%AE%E5%8F%8A%E4%B8%BB%E9%A2%98%E4%BC%98%E5%8C%96%E5%85%A8%E6%B5%81%E7%A8%8B/)
	- [windows中使用Oh My Posh美化你的终端PowerShell或CMD](https://www.iyouhun.com/post-266.html)
	- [oh my posh setup on windows](https://ohmyposh.dev/docs/installation/windows)
		- [change your prompt](https://ohmyposh.dev/docs/installation/prompt)
- [NerdFont 在WSL2 上安装](https://blog.csdn.net/qq_36835255/article/details/125020375#:~:text=1-,nerd%20fonts%20%E5%AE%89%E8%A3%85,-powerlevel10k%20%E4%BD%BF%E7%94%A8%E7%9A%84)

- [Claude Code完全指南](https://blog.axiaoxin.com/post/claude-code-full-guide/)

#### 工具部分

- [实验室服务器使用指南](https://zhuanlan.zhihu.com/p/668805702)
- [tldr 命令](https://lanlan2017.github.io/blog/42d91331/)
	- [tldr 设置中文](https://www.bilibili.com/video/BV1rm4y137Z9/)
- [advcpmv](https://github.com/jarun/advcpmv)
- [volatility 配置](https://www.cnblogs.com/Jinx8823/p/16642215.html)
- [conda介绍](https://dev.to/bowmanjd/python-tools-for-managing-virtual-environments-3bko#conda)
	- [miniconda 安装](https://docs.anaconda.com/miniconda/#quick-command-line-install)
	- [miniforge](https://github.com/conda-forge/miniforge)
		- [miniforge 安装 sagemath](https://doc.sagemath.org/html/en/installation/conda.html)
	- [conda rename](https://docs.conda.io/projects/conda/en/stable/commands/rename.html)
		```shell title="set auto_activate"
		# 设置默认不启动 base 环境
		conda config --set auto_activate_base false # true
		conda config --add channels conda-forge # add channel
		```
- 其他 python 虚拟环境管理工具可见[虚拟环境](https://pyloong.github.io/pythonic-project-guidelines/introduction/virtualenv/)


### 论文

- [论文四色原理](https://cbhua.github.io/blog/posts/20221010-papermark/) 个人稍作调整
	- 红色：高相关度支撑性信息，可以作为被引用内容；
	- 橙色：论文观点、结论、贡献；
	- 蓝色：批注信息，(reason) $\rightarrow$ **method** $\rightarrow$ result；
	- 紫色：好奇内容，没看懂/希望能够较为深入进行了解，了解后转蓝；
	- 灰色：其他有效信息；
	- 一般采用下划线，高亮进行特别突出。

## 杂文

- [【干货】《统计因果推理入门》读书笔记](https://zhuanlan.zhihu.com/p/380711267)
- [【干货、万字长文】远不止B=MAP：《福格行为模型》到底讲了什么？](https://zhuanlan.zhihu.com/p/462990256)
- [为什么几个朋友自从被字节腾讯阿里裁员以后再也不说话了？](https://www.zhihu.com/question/659273262/answer/1979202605000455789)

## AI work

> [!help]
> 
> 即下面的内容对应于 AI 生成的教程页面/问答过程中我觉得较为实用的内容；
> 
> 部分可能因为权限打不开（希望我没有忘记打开权限）。

- fellou
	- [Python 代码规范](https://0rkd5buozm.fellou.io/python-code-specification-guide-modern-version-vDsqj1Gl)
		- [在Python类型标注中放飞自我](https://zhuanlan.zhihu.com/p/636582050)
		- [谷歌 python 风格规范](https://google.github.io/styleguide/pyguide.html)
- [devv](https://devv.ai/search)
	- [如何获得一篇论文的 bib 信息](https://devv.ai/search?threadId=eh3zbw3osoow)
	- [编程范式](https://devv.ai/search?threadId=edi2mlfxs740)
- [知乎直答](https://zhida.zhihu.com)
	- [vscode 远程服务器网络代理配置](https://zhida.zhihu.com/share/7602573837732502940)