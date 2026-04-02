---
date: 2025-03-10
tags:
- blog
- tool
comments: true
slug: windows-macOS-workflow
---

# Windows MacOS 协同工作流

mac 和 windows 两种系统各有千秋，我全都要！但二者之间的协同工作和开发利用成了难题，搞了很久，留个备忘录方便自己和其他人，包括 **串流** **副屏** **文件同步** 等操作实现；看完全文，不必完全按照我的设计，你应该很容易发现自己也能够设计各式各样的方案出来。

在文章刚写的那段时间内，我还是刚上手 mac，所以主要以 windows 为主；后来打算好好利用一下 mac 用于开发，也研究了一些以 mac 为主的方案。

<!-- more -->

## 串流

|  比较   | sun+moon |   parsec   |         uu remote         |
| :---: | :------: | :--------: | :-----------------------: |
| 跨 LAN |    ❌     |     ✔️     |            ✔️             |
| 稳定安全  |    ✔️    |     ❌      |             ❌             |
| 键盘映射  |   ✔️✔️   |   ✔️✔️✔️   |            ✔️             |
| 配置复杂度 |  ✔️✔️✔️  |    ✔️✔️    |            ✔️             |
|  备注   |          | 剪贴板同步 <br> | 串流时防窥屏+结束后锁屏+文件传输功能，剪贴板同步 |

> [!extra]+
>
> - **跨 LAN**: 可以直接在公网串流，当然通过一些手段使得原本仅 LAN 中使用的方法**看起来** 可以跨局域网使用，这里不予考虑；
> - **稳定安全**：取决于是否需要外部服务器，服务器跑路了就用不了，同时屏幕录像都经过了他人服务器，可能泄露隐私（和上一条应当是始终相反的，除非自己部署服务器）；
> - **键盘映射**：sun+moon 将 `ctrl` 与 `control` 相映射，但是实际 mac 中功能上 `command` 更加贴近；parsec 比较好地做到了这一点，与 uu remote 的比较见下文；
> - **配置复杂度**：看后文实际操作便知道了；
> - 来源于我的主观感受，仅供参考。

综合上述考虑，我在~~局域网内（如校园网、企业网）远程控制时主要使用 sun+moon，公网使用 parsec；uu remote 传输文件以及以备不时之需~~（；而 sunshine + moonlight 后续将会主要用于副屏，切换较为复杂）串流时以 uu remote 为主，希望这个应用能够坚持下去吧（不过从网易的尿性可能也就现在还在开发中所以比较推荐）。

### Parsec & UU remote

二者原理、功能类似，配置简单，分别可以在 [parsec](https://parsec.app/) 和[网页 UU 远程](https://uuyc.163.com/) 中下载，创建账户后，多设备登入同一账户即可，借助其服务器实现公网串流，具体使用不多介绍了，自行探索成本很低，可以参考下面的文章：

- [Parsec介绍及快速配置](https://makise.xlog.app/parsec) or [人人走向云游戏——Parsec详解](https://foxi.buduanwang.vip/virtualization/1736.html/)
- [网易 UU 远程 - 使用帮助](https://uuyc.163.com/help/)

串流最重要的是希望沉浸式体验，但是 uu remote 的快捷键映射并不太好，很多时候会优先使用本机（例如我这里是 mac 控制 windows，mac 如果有全局快捷键和 windows 快捷键冲突，使用的是 mac 自己的，我觉得这是不合理的），parsec 这一点做的比较好；但是 parsec 在安卓端（ios 端未尝试）支持有很大问题（且后续发现使用 parsec 时不能够关闭弹窗，感觉虽然传输画面能够看到发生的所有事，但是实际操作画面只是再更低的一些层面，非常不爽），现在还是以 uu remote 为主。

### Sunshine+Moonlight

> [!quote]-
>
> Sunshine 和 Moonlight 是一对用于游戏流式传输的开源软件，旨在为用户提供高质量、低延迟的游戏体验。它们的工作原理是将游戏从一台主机传输到另一台设备上，能在局域网或互联网中进行游戏流式播放。
> 
> 实际上也有一些 Fork 改进版本，如[基地版](https://docs.qq.com/aio/DSGdQc3htbFJjSFdO?p=DXpTjzl2kZwBjN7jlRMkRJ)，可自行选择。

简而言之，sunshine 作为服务端应用，moonlight 作为客户端应用，能够实现在 **局域网** 内高质量串流[^1] 。

[^1]: 当然，具体效果如何很大程度取决于局域网质量、设备硬件。

#### 安装

分别下载[^2] [sunshine](https://github.com/LizardByte/Sunshine/releases) + [moonlight](https://github.com/moonlight-stream/moonlight-qt/releases)，各自安装打开（sunshine 的打开需要在开始菜单栏，不过有时使用管理员身份打开也是可以的）。

[^2]: 点进链接了还不知道哪个装哪个或者下哪个的建议上网搜索。

接下来我们主要需要操作 sunshine 即服务端（打开文档的那个不用管，相信你也没心思看），在 windows 右下角菜单栏或者托盘中右键图标，`open sunshine` ，看到下面的界面：

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/10_250311-120000.png)

设置用户密码，一般就本地回环链接，简单点就好，之后改起来也麻烦。

#### 配对

在 moonlight 中按照介绍是自动寻找局域网内的设备，但至少我是没有成功找到过，所以点击“手动添加计算机”，输入主机 ip 即可发起配对（注意需要在**局域网**内），且获得一个 PIN 码；此时 windows 端应该有弹窗，或者自己点进 sunshine web UI 中的 "Pin" 部分的 "PIN Pairing" 部分进行配对 (这里是已经配对成功的视图)。

![右上角红色框内手动添加计算机](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/10_250311-141713.png)

## 副屏

我的副屏实现原理与串流相似，只不过将针对性串流屏幕从 windows 实际屏幕转变为创建的虚拟屏；对于虚拟屏，我使用了一款开源软件 [parsec-vdd](https://github.com/nomi-san/parsec-vdd)（其驱动由 parsec 提供）：免费、质量高、稳定（最大的遗憾可能是仅 windows）。

安装、启动 parsec-vdd，按照你的需求 `ADD DISPLAY` ，右键对应屏幕可以调整一些参数，建议在分辨率上与主屏幕契合（就是长对长或者宽对宽），在拼接处更加丝滑；点击下面左图中红色框，或者按照自己的电脑寻找“多屏幕”管理之类的设置，拖动调整：

<div style="display:flex; text-align: center; justify-content: space-between;">
    <div style="display: inline-block; width: 46%; margin: 0.5%;">
        <img src="https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/10_250311-111241.png" alt="img1" style="width: 100%;">
        <p>parsec-vdd</p>
    </div>
    <div style="display: inline-block; width: 50%; margin: 0.5%;">
        <img src="https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/10_250311-105155.png" alt="img2" style="width: 100%;">
        <p>系统多屏幕管理</p>
    </div>
</div>

抉择串流方式：基于副屏大多在局域网内使用，且使用频率更高，已经为了前面提到的稳定安全，我最终使用 **sun+moon** （也完全可以自己选择，parse/uu remote 的操作方式非常简单，就是上面各个设备修改多屏幕控制相关设置即可，操作简单）。

### 单副屏

![sunshine UI > Configuration](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/10_250311-125219.png)

回到 sunshine 的 "configuration > Audio/Video" 部分，找到 Display Device ID，部分，这里展示的是当前 sunshine 对应的 display device id：

![Configuration > Audio/Vedio](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/10_1741582946105.png)

> [!extra]-
>
> 在我刚开始用 sunshine 时标识（虚拟）显示屏还是使用 `display_name` 部分，这在 parsec-vdd 上是非常好获取的，这也是起初我使用 parsec-vdd 的原因之一。

如果为空则默认使用主屏幕，也就是我们前面的串流形式；这里也就是需要修改这里的 ID；但是这个 ID 获取确实是一个头痛的方法[^4]，因为实际上打开 sunshine.exe 后终端很快就没了（如果还有的话就能看到开头有类似[这样的输出](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/10_250311-132043.png)，前提是已经创建了虚拟屏）；比较丑陋的方法是直接点击，让他输出错误信息，然后快速通过截图保留 ID ~~比较考验手速~~ ，配对方式同串流。

> [!help] 【20250705 更】打开 sunshine 后在 `config/sunshine.log` 中可以找到 ID 信息，就是之前终端中的输出？

[^4]: 搜索/尝试过一些命令行获取方式，与这里需要的 ID 并不相同。

### 多副屏

后来发现一个神奇的 [issue](https://github.com/loki-47-6F-64/sunshine/issues/59#issuecomment-1709018824) 回复，也就是把软件文件拷贝一份（重命名，例如 sunshine2），就相当于两个 sunshine 了；通过这个方式，我们当然也可以实现任意多副屏的创建，我的平板也就能派上用武之地了。

需要注意的是需要修改 "Configuration" 中的 "Network" 的端口部分，否则不方便修改 device id （从源文件修改当然也行）；Port 尽量与原 Port 不要太近，因为 sunshine 需要的不是一个端口，而是一个“邻域”，我使用的是间隔 100。

![Configuration > Network|600](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/10_250311-133208.png)

喜忧参半的是，打开 sunshine2 中的 sunshine.exe 时，终端不会消失，而是一直运行在后台：好处是能够完整看到 Device ID 了；坏处是终端关闭了进程也被关闭了，有点碍事。

又一次喜忧参半的是：可以用 [RBtray](https://github.com/benbuck/rbtray) 这个软件缩小终端至托盘；坏处是吞了我一个快捷键 `ctrl + alt + down` [^5] ，自己选择吧。

[^5]: RBtray 使用这个快捷键缩小窗口，但是 vscode 中需要这个快捷键快速创建多光标。

串流时需注意，moonlight 添加设备时需要 `ip:port` ，即需要指定端口了，其余操作相同。

## 同步

我的笔记有时在 windows 编辑，有时在 macOS 编辑，咋办呢？使用 **语雀、飞书** 等在线笔记自然是一个不错的解决方法，但是我对 obsidian 这类本地笔记依赖性比较强，所以还是找到了 [syncthing](https://syncthing.net/) 这一同步工具，具体使用同样无需多言，可参考：

- [多平台文件同步/传输神器——Syncthing使用教程](https://blog.jimmyho.net/archives/1229/)

## 共享键鼠

其实不少工具都已经能够做到这一点了，我使用的是 [deskflow](https://github.com/deskflow/deskflow/)，使用方法也很简单，网上教程也很多；这里提一点键盘映射：我使用 windows 作为 server，Mac 上对应修饰键映射如下：（在 configure Sever 中，双击**信号接收方**即可打开对应的设置页面）

![250615-110728.png](https://raw.githubusercontent.com/darstib/public_imgs/utool/2506/15_250615-110728.png)

> 大概来说，super 对应了 mac 上的 `command` 和 windows 上的 `win` 键。

---

后来尝试了一下，[share mouse](https://www.sharemouse.com/) 比 deskflow 还是要舒服一点？而且 share mouse 是真的 share，没有主次关系，即键鼠本身连着谁都可以操控另一边。更有甚者，可以同步剪贴板，甚至直接拖拽（包括文字，甚至是图片）！

> [!tip]- 推荐 v6.0.59 之后的版本~~也可找下 enterprise 版本更好~~
> 
> 可以看[更新](https://www.sharemouse.com/download/changelog/)：“The Standard Edition now supports two computers and a total of four displays, up from the previous limit of two displays. ” ，即两台设备共四个屏幕；老版本可能会出现每个屏幕都被识别为一个设备的情况，~~不过后续使用似乎遇到这种情况，要么每过一段时间重启，要么找 enterprise~~。

由于平时还是会带着 mac 出门，为了减少重连接（以及暂时还是更加适应 windows 的键盘），还是把键盘连接着 windows（其实也尝试过连在 mac 上，但是此时鼠标在 windows 上时键盘的输出依旧作用在 mac 上，不知道是不是 bug），同时在 mac 的 shareMouse 中调整修饰键映射：

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2511/30_1764472670116.png)

但是还是会遇到一个问题：在 mac 上中英文切换是个问题（我之前都是使用 CapsLk 切换输入法），找解决方法的时候刚好也解决了一个我挺久之前的疑惑：“mac 切换输入法中间总会有个延迟，打起字来非常不爽”，[解决方法](在 windows11 上，如何设置 win+space 切换输入法)就是改用 “control + space” 来切换输入法，这样 shareMouse 就可以为我处理这一点了。

- [一套键鼠无缝切换多台电脑](https://zhuanlan.zhihu.com/p/1823127149)
- [MacOS 与 Win11 ……](https://blog.kl.do/posts/630993824.html)

## 其他参考资料

- [deskflow - wiki](https://github.com/deskflow/deskflow/wiki)
- https://blog.csdn.net/weixin_46065314/article/details/136428076
- https://github.com/moonlight-stream/moonlight-docs/wiki/Setup-Guide

[^6]: Bug: windows 需要授权（不知道咋称呼，就那个把背景一黑弹窗问是否咋咋咋的）时会串流中断，导致失联
