---
tags:
- notes
- ctf
comments: true
---

## LitCTF 2023

### 导弹迷踪

打开环境[^1]，就是一个游戏。

1. 如果通关到 level6 确实是可以获取 flag 的；
2. 该游戏全部放在前端，通关结果也在前端，查看到 src/game.js 中有结果。

[^1]: 第一次打开是一个黑屏，我以为是特意设计的；试了试 robots.txt，意外的打开了……

直接搜索 CTF、flag 等关键词是没有的，因为作者用了 `F|L|A|G` 分割。 

> [!FLAG]
>
> `NSSCTF{y0u_w1n_th1s_!!!}`


