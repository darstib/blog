---
tags:
  - notes
  - cs188
comments: true
dg-publish: true
---

# The Pac-Man Projects

这里是CS188 sp24 的 project [The Pac-Man Projects](https://inst.eecs.berkeley.edu/~cs188/sp24/projects/) 的解答。

项目实现效果大致如：[pacman_game](https://inst.eecs.berkeley.edu/~cs188/sp24/assets/images/pacman_game.gif)。

> [!ATTENTION]
>
> 以下所有讲解默认读者阅读或者理解了对应 `[!PREREQUISITE]` 部分的所有内容，且**看懂** python 语法没有问题。

- [project-0](project-0.md)
- [project-1](project-1.md)
- [project-2](project-2.md)
- [project-3](project-3.md)
- [project-4](project-4.md)

project5/6 讲解起来十分复杂，可能直接看代码会有更深的感受，并没有实现相关讲解；project6 的 Q7 代码已经完成，但是训练下来效果不佳，问题不知何处寻，遂放弃。在实验中可能遇到 logits 这个术语：

> [!info]+ [logits in NN](https://www.zhihu.com/question/60751553)
> 
> logit 源自 **log**istic un**it** ，原本是 sigmoid 函数 $\sigma(x) = 1 / (1 + e^x)$ 的反函数：
> 
> $$\mathrm{logit}(p)=\log \left( \frac{p}{1-p} \right)$$
> 
> 也即 $\sigma(\mathrm{logit(p)}) = p$，由于在神经网络中对最后一层全连接层的输出往往要经过非线性激活函数并认为输出的是“概率”估计，因而将最后一个全连接层的输出称为 logits 。
> 
> 可以认为 logits 是对所有动作的“打分”，激活函数只是将其转化为概率分布。

> [!ENV]- 本人 project 环境
>
> - project 0-3
> 	- WSL ubuntu 22.04；
> 	- miniconda => python=3.9.19
> - project 4-6
> 	- MacOS 
> 	- miniforge3 => Python=3.10.16
