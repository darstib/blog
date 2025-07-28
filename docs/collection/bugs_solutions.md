---
tags:
- collection
comments: true
---

> [!help] 即自己遇到的问题以及相应的解决方法。

## Unix

### ssh to WSL 

- [从 macOS 到 Windows WSL](https://blog.csdn.net/Narutolxy/article/details/144226085)
	- ubuntu: `sudo systemctl start ssh`
- [SSH 访问 Windows 的 WSL2 Ubuntu](https://zhi.moe/post/access-into-wsl2-ubuntu-from-macos/)
	- kali-linux: `sudo /usr/sbin/service ssh start`
- windows 上执行 `netsh interface portproxy show all` 查看开放端口

### Wsl default user
#### 法 1（终端中能运行对应发行版程序）

```windows title="cmd/powershell"
<Distro> config --default-user <user>
```

#### 法 2（通用）

```linux title="/etc/wsl.conf"
[user]
default=darstib
```

### Wsl change disk

> [!attention] 20250714 更：（来自 https://linux.do/t/topic/785798 ）
> 
> ```sh
> wsl --list -v # 获取发行版名称，此处以Ubuntu-24.04为例
> $targetPath = "D:\Ubuntu-24"
> if (!(Test-Path $targetPath)) { New-Item -Path $targetPath -ItemType Directory | Out-Null }
> wsl --shutdown
> wsl --manage Ubuntu-24.04 --move "$targetPath"
> ```

Wsl 越用越大，默认在 C 盘，如何移动到 D 盘自己指定的位置呢？

```shell title="in cmd or powershell"
wsl --shutdown # 关闭 wsl 上运行的发行版
wsl --export <Distro> <FileName> [选项] # 建议将分发版导出到 tar 文件。
wsl --unregister <Distro> # 将原来的卸载
wsl --import-in-place <Distro> <InstallLocation> <FileName>
```

> [!tip]- 显然迁移是需要打包、迁移、解包的，那么当然是发行版越小的时候迁移越方便。

### wsl 磁盘压缩

wsl 不主动释放使用过的空间，可以使用 [WSL2 虚拟磁盘文件(.vhdx)占用过大处理办法](https://www.cnblogs.com/T6uE13s/p/18704140) 解决。

### 忘记了 wsl root 权限密码

- https://learn.microsoft.com/zh-cn/windows/wsl/setup/environment#set-up-your-linux-username-and-password

### 忘记 Vmware-machine 密码

- [bilibili - 忘记虚拟机密码登录不了（虚拟机开启报错）与虚拟机修改密码](https://www.bilibili.com/video/BV1Ha4y1X76Y/?spm_id_from=333.337.search-card.all.click&vd_source=0a037c4dd2becee04d2b1ccafdc1862e)

### change version of JAVA in linux

`sudo update-alternatives --config java`

### change version of GCC in linux

- https://blog.csdn.net/qq_39779233/article/details/105124478
- https://lindevs.com/install-gcc-on-ubuntu/

### Kali linux install

-  [2023 Kali安装教程](https://blog.csdn.net/fingue/article/details/127559353)
- [Kali Linux(VMware)中解决界面太小等问题](https://blog.csdn.net/qq_34668863/article/details/134009574)

## windows

### oh-my-posh 显示 python 虚拟环境

> [!bug]- PowerShell 显示 Module 相关问题
> 
> ```powershell title="Import-Module, Install-Module 无法识别"
> # 检查是否含有 PowerShellGet 模块
> ```
> 
> ```powershell title="模块不存在"
> $Env:PSModulePath -split ';' # 检查 Module 路径，确认确实存在相关模块；否则去下载
> ```

- [python 环境显示：记录一下windows配置oh my posh遇到的坑](http://zhuanlan.zhihu.com/p/677709658)

注意 json 文件中实际不能够有注释：

```json
{
  "type": "python",
  "foreground": "#ffffff",
  "style": "plain",
  "properties": {
    "home_enabled": true,
    "fetch_version": true,
    "fetch_virtual_env": true,
    "display_mode": "context",
    "display_virtual_env": true,
    "dispplay_default": true,
    "display_version": false
  },
  "template": "(\uE235 {{ if .Error }}{{ .Error }}{{ else }}{{ if .Venv }}{{ .Venv }}{{ else }}{{ .Full }}{{ end }}{{ end }})"
},
```

### windows 文件资源管理器中的 “网盘图标” 移除

注册表中：

```
计算机\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\
也有些可能在 HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\MyComputer\NameSpace\
```

### 电脑不使用后两分钟锁屏自动锁屏

- https://www.zhihu.com/question/55617612

### 在 Windows11 上隐藏任务栏中的 copilot

最近在 windows 11 更新后，任务栏中出现了一个 **copilot** ，基于仍然是试用期，而且大陆不能直接访问，懒得用了，放那也碍眼：

- [系统极客-3 招教你在 Windows 11 中轻松关闭或移除 Copilot 功能](https://www.sysgeek.cn/windows-11-disable-copilot/)

### windows 多任务处理 edge 浏览器标签页显示过多

> [!tip]+ 温知识
> 
> 在 windows 上按住 `Alt` 同时按 `Tab` 键会进入“多任务处理”，展示当前打开的软件界面，点按 `Tab` 可以进行切换，松开 `Alt` 则聚焦对应界面。

我对多个浏览器都有使用，发现 Edge 浏览器在“多任务处理”界面中会展示多个标签页，对于我想要切换至其他软件非常不友好（需要多按几下 `Tab`）；原来在系统设置中：

1. 进入 “设置>系统>多任务处理”
2. 调整“对齐或按 AIt+Tab 时显示应用中的标签页”为“不显示选项卡”

此时虽然说“不显示”，但还是会保留基本的 edge 的页面的。

## Network

### macOS clash 系统代理打开无效

- [打开隐私与安全中的高级设置，关闭访问系统范围的设置需要输入管理员密码](https://github.com/clash-verge-rev/clash-verge-rev/issues/1118#issuecomment-2144418510)

### missing cap_net_raw+p capability or setuid

```shell
$ ping github.com
ping: socktype: SOCK_RAW
ping: socket: Operation not permitted
ping: => missing cap_net_raw+p capability or setuid?
$ curl https://baidu.com
curl: (35) GnuTLS, handshake failed: The TLS connection was non-properly terminated.
```

`ping` 权限不够，`sudo setcap cap_net_raw+ep /usr/bin/ping` 提供权限。

### From xxxx icmp_seq=n Destination Host Unreachable

WSL `ping <domain>/<ip>` 时出现无法找到的问题，但是宿主机是可以正常访问的，**unreachable** 似乎将问题指向了 DNS，最后通过修改 `/etc/resolv.conf` 中的 nameserver 后的 DNS 服务器 ip 解决（修改至与宿主机一致即可）。

### 连接需要登录的 wifi 时重定向界面错误

在登入企业/学校 wifi 时，需要账号登入；但是发现只是跳转到 http://www.msftconnecttest.com/redirect 之后显示失败了，在[这里](https://answers.microsoft.com/zh-hans/windows/forum/all/windows%E8%BF%9E%E6%8E%A5%E5%85%AC%E5%85%B1/9cee5962-a379-4335-893f-984f0cd0f151#:~:text=%E7%9A%84%E7%BD%91%E7%BB%9C%E9%97%AE%E9%A2%98-,%E9%A6%96%E5%85%88%E5%85%B3%E9%97%AD%E7%94%B5%E8%84%91%E4%B8%8A%E6%89%80%E6%9C%89%E7%9A%84%E4%BB%A3%E7%90%86%E4%B8%8EVPN%E8%BD%AF%E4%BB%B6,-%E6%8C%89%E4%B8%8B%E3%80%90windows%20%2B%20x) 找到了答案。

简而言之，先把 VPN 什么的关了，否则影响上述链接重定向。

### vscode 中使用 copilot 登录失败

> 在更换学生认证包后，vscode 上的 copilot 突然间登入不上，体现在点击登陆后自动跳转到认证界面，确定后 vscode 这边却没反应。

搜索后有人指向了 setting.json，打开搜索，确实发现了：

```json
"github.copilot.chat.localeOverride": "zh-CN",
"github.copilot.preferredAccount": "...",  // 此处省略我的 GitHub 邮箱地址
"github.copilot.enable": {
  "*": true,
  "plaintext": false,
  "markdown": false,
  "scminput": false
},
```

尝试删除后重试，问题解决；建议 Ctrl x 剪切，万一问题不在这，也能复原。

## Other

#### 如何获取 Google 安全码？

-  [热夏的博客](https://www.lifeee.top/posts/13004.html)
	- 有些手机没有 google 官方给出的获取安全码的方式，我们可以在 google play 中下载 "google" 这个应用。

#### Tab Foucs in Vscode

- **Q:** 在 VSCode 中，Tab 键变成了在各选项间跳跃（即焦点切换），而不是接受 AI 插件给出的建议。
- **A:** 使用 `Ctrl M` 快捷键切换了这一模式。

#### obsidian 文件保存失败？

- [Fail to save files](https://forum.obsidian.md/t/failed-to-save-a-file-eperm-operation-not-permitted/33760/4)

#### Obsidian 调整 mermaid 宽度

- [let-the-user-decide-the-size-and-alignment-of-mermaid-diagrams](https://forum.obsidian.md/t/let-the-user-decide-the-size-and-alignment-of-mermaid-diagrams/7019/1)

#### Syncthing 跨设备同步工具

- [Syncthing - P2P文件同步工具](https://zhuanlan.zhihu.com/p/69267020)

#### Deskflow

- **Q**: `NOTE: cursor is locked to screen, check scroll lock key` 
- (windows) 键盘上的 `ScrLk` 按键。

- **Q:** MacOS 上 Deskflow 反复索要 accessibility，哪怕已经给到
- (MacOS) 参考 [#8028](https://github.com/deskflow/deskflow/issues/8028#issuecomment-2741208978)，之前卸载过 deskflow，导致重新安装后 accessibility 出了问题，只要将选项移除后重新启动 deskflow 并赋权即可。
