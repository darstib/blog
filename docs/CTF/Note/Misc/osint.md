---
tags:
- wp
- ctf
comments: true
---

## GeekGame2023

### 小北问答!!!!!

- [prob18-trivia](https://github.com/PKU-GeekGame/geekgame-3rd/tree/master/official_writeup/prob18-trivia)

#### Q1

根据 GPL 许可证的要求，基于 Linux 二次开发的操作系统内核必须开源。例如小米公司开源了 Redmi K60 Ultra 手机的内核。其内核版本号是？

首先去找找看，发现 [github 仓库](attachments/osint.png)，自然是最好的；进入后搜索 [Redmi K60 Ultra](attachments/osint-1.png)，切换到 corot-s-oss 分支。

先看 README 文件，无；基于 [Linux kernel licensing rules](https://www.kernel.org/doc/html/v4.18/process/license-rules.html#:~:text=with%20an%20explicit%20syscall%20exception%20described%20in%20LICENSES/exceptions/Linux%2Dsyscall%2Dnote%2C%20as%20described%20in%20the%20COPYING%20file.) ，查看 [Linux-syscall-note](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/blob/corot-t-oss/LICENSES/exceptions/Linux-syscall-note) ，也没有版本信息。

[devv_ai 对话记录](https://devv.ai/search?threadId=e0tg4uzc75kw) => [Where do I find the version of a Linux kernel source tree?](https://stackoverflow.com/questions/12151694/where-do-i-find-the-version-of-a-linux-kernel-source-tree)

查看 [MakeFile](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/blob/corot-t-oss/Makefile) ，结合 `^\d+\.\d+\.\d+$` 的答案格式 => `5.15.78`

> [!Extra]
>
> 直接使用网页上端的搜索栏，只能够搜索默认分支，而我们想要搜索特定的分支。
> 
> - git clone ，随后在本地搜索 => 略麻烦，但是可以使用命令行
> - 将 url 中的 `github.com` 改为 `github.dev` （或者按下 `.` ），可以在在线编辑器中打开；但是此时左侧的搜索依旧不能使用（因为只能够搜索 [打开的编辑器](attachments/osint-2.png) 部分）
>     - 使用[高级搜索](attachments/osint-3.png)

#### Q2

每款苹果产品都有一个内部的识别名称（Identifier），例如初代 iPhone 是 iPhone1,1。那么 Apple Watch Series 8（蜂窝版本，41mm 尺寸）是什么？

查询的地点挺多的：

- 我搜的：[everymac](https://everymac.com/systems/apple/index-apple-specs-applespec.html) => [Watch6,16](https://everymac.com/systems/apple/apple-watch/specs/apple-watch-series-8-gps-cellular-41mm-us-canada-a2772.html#:~:text=mm%20%2D%20MNUX3LL/A*%20%2D-,Watch6%2C16,-%2D%20A2772*)
- 官方题解：[appledb](https://appledb.dev/) => [Watch6,16](https://appledb.dev/device/identifier/Watch6,16.html) （甚至在 url 中就用的是 identifier）

#### Q3

本届 PKU GeekGame 的比赛平台会禁止选手昵称中包含某些特殊字符。截止到 2023 年 10 月 1 日，共禁止了多少个字符？（提示：本题答案与 Python 版本有关，以平台实际运行情况为准）

根据在 github 上的账号找到[比赛平台后端](https://github.dev/PKU-GeekGame/gs-backend)，[搜索“nickname” 或者 “昵称”](attachments/osint-4.png) [^1]，查看 `cls.DISALLOWED_CHARS` 。

[^1]: 可以先去平台注册一个新号，故意取些乱七八糟的名字，看看回显

也就是说，我们需要 `len(WHITESPACE)` ，将它复制下来运行好了：

```python title="test.py"
from typing import TYPE_CHECKING, Optional, Set
from unicategories import categories
import sys


def unicode_chars(*cats: str) -> Set[str]:
    ret = set()
    for cat in cats:
        ret |= set(categories[cat].characters())
    return ret


EMOJI_CHARS = (
    {chr(0x200D)}  # zwj
    | {chr(0x200B)}  # zwsp, to break emoji componenets into independent chars
    | {chr(0x20E3)}  # keycap
    | {chr(c) for c in range(0xFE00, 0xFE0F + 1)}  # variation selector
    | {chr(c) for c in range(0xE0020, 0xE007F + 1)}  # tag
    | {chr(c) for c in range(0x1F1E6, 0x1F1FF + 1)}  # regional indicator
)
# https://www.compart.com/en/unicode/category
DISALLOWED_CHARS = (
    unicode_chars(
        "Cc", "Cf", "Cs", "Mc", "Me", "Mn", "Zl", "Zp"
    )  # control and modifier chars
    | {chr(c) for c in range(0x12423, 0x12431 + 1)}  # too long
    | {chr(0x0D78)}  # too long
) - EMOJI_CHARS

print(sys.version)
print(len(DISALLOWED_CHARS))
```

提示与实际 python 版本有关，尝试[寻找信息](attachments/osint-5.png) => `python >= 3.8` ，我们把 3.8/3.9/3.10/3.11/3.12 都试试好了。

> [!NOTE]
>
> 在线运行的网站没找到能够，干脆用 conda 各个版本创建一个[测试环境](attachments/osint-6.png)，结果分别如下：
> 
> - 3.8.20 => `4445`
> - 3.9.20/3.10.15 => `4472`
> - 3.11.10 => `4587`
> - 3.12.7 => `4636`

#### Q4

在 2011 年 1 月，Bilibili 游戏区下共有哪些子分区？（按网站显示顺序，以半角逗号分隔）

这个真找不到，本以为太古老了，不过是确实不知道 [web archive](https://web.archive.org/)；还要知道以前 bilibili 是 https://bilibili.us （哇哦）=> `游戏视频,游戏攻略·解说,Mugen,flash游戏`

