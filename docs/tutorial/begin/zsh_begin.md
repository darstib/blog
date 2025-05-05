---
comments: true
date: 2025-05-05
tags:
- begin
---

> [!summary]- [zsh 安装与配置，使用 oh-my-zsh 美化终端](https://www.haoyep.com/posts/zsh-config-oh-my-zsh/)
> 
> 本文 zsh 配置部分主要参考上面的链接，这篇文章主要使用我保留下来的配置文件，用于极速配置我的 zsh （写这篇文章的时候大概是我第 5 次配置了，所以打算记录下来）。

## 配置

zsh 安装美化极速版（使用我的配置）；对于 macOS，前两步以及第三步安装 zsh 可以跳过。

1. [安装 WSL 2](https://docs.eesast.com/docs/tools/wsl#%E5%AE%89%E8%A3%85-wsl-2)
2. 安装发行版：
	- `wsl -l` 列出已安装发行版
	- `wsl -l -o` 列出可用发行版
	- `wsl --install [Distro] [Options...]` 安装指定发行版
	- `wsl -d <Distro>` 运行指定发行版
	- `wsl -s <Distro>` 设置默认发行版
	- `<Distro> config --default-user <user>` 设置发行版默认用户
3. 发行版迁移：
	- `wsl --shutdown` 关闭 wsl 上运行的发行版
	- `wsl --export <Distro> <FileName> [Options...]` 建议将分发版导出到 tar 文件。
	- `wsl --unregister <Distro>` 将原来的卸载
	- `wsl --import-in-place <Distro> <InstallLocation> <FileName>` 导出
4. [安装 zsh & oh-my-posh](https://www.haoyep.com/posts/zsh-config-oh-my-zsh/)：
	- `sudo apt update && sudo apt upgrade -y` => `sudo apt install zsh git curl -y`
	- `chsh -s /bin/zsh` 设置 zsh 为默认终端，最终应该会出现一个 `~/.zshrc` 文件
	- `sh -c "$(curl -fsSL https://install.ohmyz.sh/)"` 安装 oh-my-zsh
	- `git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k` 获取 powerlevel10k 主题
	- `git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions` 获取推荐补全插件
	- `git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting` 获取高亮插件
5. 使用我的[配置文件](https://github.com/darstib/config/tree/main/zsh)
	- 重新打开终端后，应该会进入 p10k 的配置界面让我们判断此时符号显示是否正常以检测当前终端对特殊符号的兼容性；
	- 但是我现在使用的这个配置基本没有符号要求，所以随便选即可，最终应该会出现一个 `~/.p10k.zsh` 文件
	- 将 [zsh 配置文件](https://github.com/darstib/config/tree/main/zsh) 中的 `.zshrc .p10k.zsh` 文件覆盖当前文件内容
		- 或者在当前步骤刚开始时直接将上述文件夹中的 `.zshrc .p10k.zsh` 文件放在 `~/` 下（没有尝试过，可能会有不兼容的地方）
	- 重启终端即可。

## 备注

1. 由于我有多个发行版，所以在文件路径前展示了 OS_ICON，例如下面的 "Deb"：

```sh
Deb ~
$
```

不想要的话可以在 `~/.p10k.zsh` 中下面的 `os_icon` 一行注释后重新加载 `source ~/.p10k.zsh` 即可

```sh
typeset -g POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(
  # =========================[ Line #1 ]=========================
  # per_directory_history   # Oh My Zsh per-directory-history local/global indicator
  context                 # user@host
  os_icon                 # OS icon
  dir                       # current directory
  dir_writable            # current directory writable indicator
  background_jobs           # presence of background jobs
  vim_shell                 # vim shell indicator (:sh)
  toolbox                   # toolbox name (https://github.com/containers/toolbox)
  vcs                       # git status
  command_execution_time    # previous command duration
  # =========================[ Line #2 ]=========================
  newline                   # \n
  prompt_char               # prompt symbol
)
```