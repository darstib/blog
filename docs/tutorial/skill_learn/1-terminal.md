---
comments: true
tags:
- notes
---

> [!prerequisite]+ 你需要使用一个类 Unix shell 来完成文中所提到的操作，你可以
>
> - 使用安装了 Linux 的电脑，或者是 macOS 等类 Unix 系统；
> - 对于 Windows 用户，你可以：
>     - 使用 [WSL(Windows Subsystem for Linux)](https://docs.microsoft.com/zh-cn/windows/wsl/)；
>     - 使用 Linux 虚拟机。
> 
>> [!extra]-
>> 
>> 对于命令行、终端、壳等概念我们不做明确区分，有兴趣的同学可以看[命令行界面 (CLI)、终端 (Terminal)、Shell、TTY，傻傻分不清楚？](https://zhuanlan.zhihu.com/p/516408816) 或者 [What is the exact difference between a 'terminal', a 'shell', a 'tty' and a 'console'?](https://unix.stackexchange.com/questions/4126/what-is-the-exact-difference-between-a-terminal-a-shell-a-tty-and-a-con) 中的讲解。

## Linux

### 基本介绍

> [!note]- shell
>
> shell 是操作系统为用户提供交互界面的**命令行解释器**的统称，例如 Windows 中的 cmd 就是一种 shell；bash 是其中最流行的一种，也是多数 linux 自带的 shell 。
> 
> Linux 包含多种 Shell ，常见的有：
> 
> - Bourne Shell（ATT 的 Bourne 开发，名为 sh）
> - **Bourne Again Shell（/bin/bash）**
> - C Shell（Bill Joy 开发，名为 csh）
> - K Shell（ATT的David G.koun 开发，名为 ksh）
> - Z Shell（Paul Falstad 开发，名为 zsh）
> 
> | 特性     | Bash                                   | Zsh                            |
> |:------:|:--------------------------------------:|:------------------------------:|
> | 性能     | 整体性能良好，在大多数任务中表现稳定                     | 通常在处理复杂补全和交互式功能时表现更好           |
> | 配置文件   | `.bashrc`, `.bash_profile`, `.profile` | `.zshrc`, `.zprofile`          |
> | 自动补全   | 基本的命令和文件名补全                            | 高级补全，支持更复杂的命令                  |
> | 历史记录   | `history` (在 `~/.bash_history`)        | `history` （在 `~/.zsh_history`） |
> | 可定制化程度 | 支持基础的自定义，通过 `.bashrc` 修改               | 高度可定制，提供丰富的主题和插件支持             |
> | 稳定性    | 更广泛用于脚本和系统管理                           | 有一些用户偏好和社区支持                   |

> 关于 [linux 发行版](https://101.lug.ustc.edu.cn/Appendix/distribution/) 。

### bash 初印象

```shell title="cli"
yourUserName@yourComputerName:~$ 
```

|         组成         |                        解释                        |
| :----------------: | :----------------------------------------------: |
|   `yourUserName`   |           当前**登录用户**的用户名，用于标识命令执行的用户。            |
|        `@`         |                分隔符，用于区分用户名和计算机名。                 |
| `yourComputerName` |            当前计算机的名称或主机名，用于标识命令执行的设备。             |
|        `:`         |               分隔符，用于分隔主机名和当前工作目录。                |
|        `~`         |      当前用户的主目录的简写，一般代表 `/home/yourUserName`。      |
|        `$`         | 命令提示符，普通用户通常是 `$`，超级用户（root）则为 `#`，借助工具也可以自定义设计。 |

> UserName 和 ComputerName 不建议包含中文字符，在使用 vivado 等工具时容易出现难以察觉的错误。例如上次有个人仿真通过了，但是生成比特流没有明显错误但是最后没有结果；原因在于用户名为中文，vivado 将其忽视导致文件未能找到。

大部分情况下，命令行由 “命令/参数/选项”组成；命令本身往往是一个可执行程序；当我们想要运行一个**环境变量**(`echo $PATH | tr ':' '\n'`)中有的程序的时候，直接输入名称即可；例如，Linux 中有一个程序叫做 `date`，直接输入就可以，这个程序将输出当前的时间：

```shell
:$ date
Wed Mar 19 09:09:08 PM CST 2025
```

> [!example]
>
> - **命令 (Command)**：就像我们要做什么事情，比如“做饭”、“写作业”、“打扫卫生”。在 Linux 里，命令就是告诉计算机要做什么，比如 ls (列出文件)、cp (复制文件)、mv (移动文件)。
>                          
> - **参数 (Argument)**： 告诉命令操作的对象或目标。就像“做**东坡肉**”，“写**数学**作业”，“打扫**卧室**”。参数就是具体针对什么东西来做这件事。
>    
> - **选项 (Option)**： 就像我们做事情的方式或风格，比如“做饭**用小火**”、“写作业一定要用**用笔**”、“打扫卫生**用吸尘器**”。选项通常用来修改命令的默认行为。
>    
> 让我们用一个具体的例子来解释一下：
>
> ```
> ls -l /home/user/documents
> ```
>
> - **ls**：这是命令，意思是“列出文件和目录”。（做什么）
>    
> - **-l**：这是选项，通常以-或--开头。-l 选项表示“以长格式（long format）列出”，会显示文件的详细信息，如权限、所有者、大小、修改时间等。（怎么做）
>    
> - **/home/user/documents**：这是参数，表示命令 ls 要操作的目标，这里是 /home/user/documents 这个目录。（对谁做）
> 
> 所以这条命令的意思就是：以长格式列出 /home/user/documents 目录下的文件和子目录的详细信息。

参数和程序名、参数与参数之间都要使用空格隔开。如果参数里包含空格，可以用 `'` 或 `"` 将参数包裹起来，或者在空格前面加上一个反斜杠转义（如 `My\ repo` 会被转义成 `My repo`，但是还是更加推荐前者，对于程序员来说具有更好地可读性）。

> [!info]+ 变量
>
>           
> |  变量  |                          WSL                          |               Windows                |
> | :--: | :---------------------------------------------------: | :----------------------------------: |
> |  定义  |       命名的存储位置，存储字符串或数值 `export VAR_NAME=value`        | 存储在系统中的路径、配置信息等 `set VAR_NAME=value` |
> |  访问  |                      `$VAR_NAME`                      |             `%VAR_NAME%`             |
> | 环境变量 |               通过 `env` 或 `set` 查看                |   通过 `env` 查看    |
> | 命名规则 |                  大小写敏感，通常使用大写字母和下划线                   | 同前 |
> | PATH | WSL 的 PATH 包括 <u>Windows 文件系统路径</u> ，一定程度上允许直接调用 Windows 应用程序 | Windows 的 PATH 是系统的可执行文件路径，用于查找可执行文件 |
> 
>> 通俗地说，`PATH` 环境变量代表的是**可执行文件的搜索路径** ；出于习惯，大家把可执行程序放在 `bin` 文件夹中，所以 `PAHT` 中很多以 bin 结尾。

> [!wiki]+ [Path](https://en.wikipedia.org/wiki/Path_(computing))
>
> 路径（或文件路径、路径名等）是一串字符，用于**唯一标识目录结构中的位置**。它通过遵循目录树层次结构中的组件组成，这些组件由分隔符分隔，代表每个目录。分隔符最常见的是斜杠（“/”）、反斜杠字符（“\”）或冒号（“:”），尽管某些操作系统可能使用不同的分隔符。
> 
> 特殊：
>  

在介绍一些非常常见的命令之前，我们先了解 `-h/--help` `man` 以及一个扩展工具 `tldr` ：

```sh
$ sudo apt install tldr
...
$ mkdir -p ~/.local/share/tldr # 这是在 ubuntu 上的操作，不同系统可能不一致
$ tldr --update # 更新
$ tldr <cmd>
```

|            工具            |        优点        |            适用场景            |
| :----------------------: | :--------------: | :------------------------: |
| [tldr](https://tldr.sh/) |  简洁明了，易于理解，社区维护  |     需要快速了解命令的基本用法，是初学者     |
|       -h / --help        | 简单直接，快速查看，一般程序自带 |      需要快速查看命令的全部用法和选项      |
|           man            |  内容详尽，官方文档，系统自带  | 需要深入了解命令的所有细节和选项，需要查看权威的文档 |

### 路径操作

|  命令   | 作用       | 示例              |
| :---: | -------- | --------------- |
| `pwd` | 显示当前绝对路径 | `/home/user`    |
| `cd`  | 改变当前路径   | `cd /`, `cd -`  |
|  "z"  | 根据历史推断跳转 | `z fds-project` |

### 文件/目录管理

#### 基本工具

| 命令                        | 作用                       |
| ------------------------- | ------------------------ |
| `ls`                      | 列出目录内容                   |
| `ls -l`                   | 列出详细信息                   |
| `ls -lh`[^1]              | 以人类易读格式显示文件大小            |
| `cat/more/less/head/tail` | 输出文件内容 (con**cat**enate) |
| `touch`                   | 创建文件/更新时间戳               |
| `mkdir`                   | 创建目录                     |
| `mv`                      | 移动/重命名文件/目录              |
| `cp`                      | 复制文件                     |
| `cp -r`                   | 递归复制目录                   |
| `rm`                      | 删除文件                     |
| `rm -r`                   | 递归删除目录                   |
| `rm -rf`                  | 强制递归删除 (慎用!)             |

[^1]: 一般情况下，对于单字符且不带参数的选项可以简写，顺序 <u>通常</u> 不影响结果。

#### bat(cat)  

`cat` 工具的升级版吧，为输入增加更多高亮内容；在 Ubuntu 上使用 apt 安装可能有个[小 bug](https://github.com/sharkdp/bat?tab=readme-ov-file#on-ubuntu-using-apt)，具体就是实际上使用的是 `batcat` ，如果为了习惯可以使用软链接：

```sh
$ mkdir -p ~/.local/bin
$ ln -s /usr/bin/batcat ~/.local/bin/bat
```

#### 编辑器

在一部分情况下：对文件进行很小的修改/文件修改需要高权限/希望减少鼠标依赖并极大提高自己编辑效率/装逼，我们可能会使用到终端上的文本编辑器，下面是常见的三种编辑器：

|                            编辑器                             |                                        优点                                         |         缺点          |                            适用场景                             |
| :--------------------------------------------------------: | :-------------------------------------------------------------------------------: | :-----------------: | :---------------------------------------------------------: |
|            [nano](https://www.nano-editor.org/)            |  [简单易学](https://help.aliyun.com/zh/cloud-shell/nano-editor-tutorial-1)，资源占用少，预装   |     功能有限，可定制性差      |               需要快速编辑文本文件，是初学者，在资源有限的机器上进行文本编辑               |
| [vim](https://www.vim.org/) / [neovim](https://neovim.io/) | 高效编辑，功能强大，可定制性强，[广泛支持](https://help.aliyun.com/zh/cloud-shell/use-the-vim-editor) |   学习曲线相对陡峭，配置比较复杂   |             需要高效地进行文本编辑，需要使用高级编辑功能，需要对编辑器进行深度定制             |
|        [emacs](https://www.gnu.org/software/emacs/)        |     [高度可定制，功能丰富](https://www.wenhui.space/docs/02-emacs/emacs_useguide/)，社区强大     | 学习曲线非常陡峭，资源占用高，配置复杂 | 需要对编辑器进行高度定制，愿意 <u>花费大量时间学习和配置编辑器</u> ，需要使用 `emacs` 的各种扩展功能 |

由于我本身不是忠实的终端编辑器用户（~~我 60%的时间应该都在浏览器上~~），仅在对文件进行很小的修改/文件修改需要高权限情况下使用，所以这里不会讲解太多，也不做具体推荐大家使用哪个，萝卜青菜各有所爱，大家可以点击表格中的链接看看一些基本思想，这里仅演示最为常见的 nano 和 vim 的 “少量基本操作”。

1. nano

> [!help]- nano hot key
>
> |快捷键|含义|使用介绍|
> |---|---|---|
> | `^G` |Help|显示帮助菜单，包含所有可用命令和快捷键列表。|
> | `^O` |Write Out|保存当前文件，相当于“另存为”功能，输入文件名。|
> | `^W` |Where Is|在当前文档中搜索特定文本，输入要搜索的内容。|
> | `^K` |Cut|剪切当前行，剪切的内容存储在剪贴板中。|
> | `^T` |Execute|执行命令或脚本，通常用于执行拼写检查。|
> | `^C` |Location|显示光标在文件中的位置，包括行号和字符位置。|
> | `M-U` |Undo|撤销最近的操作，允许恢复改动。|
> | `M-A` |Set Mark|设置文本选择的开始位置，此后可以使用 `Ctrl+K` 剪切所选文本。|
> | `^X` |Exit|退出 Nano 编辑器，若有未保存的更改，会询问是否保存。|
> | `^R` |Read File|插入另一个文件的内容到当前文件中。|
> | `^\` |Replace|查找并替换文本，输入要查找的内容和替换后字符。|
> | `^U` |Paste|粘贴剪切板中的内容。|
> | `^J` |Justify|调整文本格式，使其对齐。|
> | `^/` |Go To Line|跳转到指定行，需输入行号。|
> | `M-E` |Redo|重做上次撤销的操作。|
> | `M-6` |Copy|复制当前行到剪贴板，通常在选择文本后使用。|
> 
>  至于 M 代表了 `Meta` 这一[修饰键](https://en.wikipedia.org/wiki/Modifier_key)，出于一些历史原因，可以查看这篇[问答](https://unix.stackexchange.com/questions/28993/what-is-bashs-meta-key)；在 windows 上映射为 `Alt` 。

2. vim

<div style="display: flex;">
    <div style="width: 70%; padding-left: 20px;">
        <p>vim 相比于 nano 的特点在于模式切换以使用有限的按键完成需求。</p>
        <p>一般情况下，我们打开 vim 出于 normal 模式，这一模式下我们只能够移动光标（为了减少手的移动，熟练者习惯于使用 hjkl 进行移动，数字可以使后续操作翻倍）和简单操作；从右边的图我们可以看到，使用 `:/?` 等进入 cmd-line 模式，使用 `v/V` 进入 visual 模式，`iao` 等进入 insert mode。</p>
    </div>
    <div style="width: 5%;"></div>
    <div style="width: 20%;">
        <img src="https://raw.githubusercontent.com/darstib/public_imgs/utool/tuchuang/17425275420641742527541177.png" alt="vim mode" style="width: 100%; height: auto;">
        <p>(from wikipedia)</p>
    </div>
    <div style="width: 5%;"></div>
</div>

|          模式          |              操作说明              | 常用操作示例                                                       |
| :------------------: | :----------------------------: | ------------------------------------------------------------ |
|    正常模式 (Normal)     |      用于浏览和操作文本，可以进行简单修改。       | `h`, `j`, `k`, `l`（移动）<br>`u` （撤销某一操作）                       |
|    插入模式 (Insert)     |       输入文本，像使用普通文本编辑器一样。       | `i`（在光标前插入）<br>`a`（在光标后插入）<br>`o`（在下方新建一行并插入）                |
|    可视模式 (Visual)     | 用于选中文本区域，可以对选中文本进行操作，例如复制、删除等。 | `v`（字符选择）<br>`V`（行选择）<br>`Ctrl` + `v`（块选择）                   |
| 命令行模式 (Command-line) |        输入命令进行文件操作、搜索替换等        | `:w`（保存文件）<br>`:q`（退出 Vim）<br>`:%s/foo/bar/g`（'foo' ->'bar'） |

> [!extra]- neovim 入门指南
>
> - [从零开始配置 Neovim(Nvim)](https://martinlwx.github.io/zh-cn/config-neovim-from-scratch/)
> - [VSCode Neovim](https://blog.yusong.me/terminal/vim/vscode-neovim)
> - [给编辑器之神配上GUI（VSCode+Neovim）](https://zhuanlan.zhihu.com/p/679729768)
> - [neovim/doc/usr](https://neovim.io/doc/user/)

3. emacs

我本人并没有使用过 emacs，所以不作演示；下面是使用者 [Akane](https://github.com/Akane-6730) 推荐入门资料，仅供参考。

> [!extra]- emacs 入门指南
>
> - https://pavinberg.github.io/emacs-book/zh
> - https://mint.westdri.ca/emacs/top_intro
> - https://book.emacs-china.org
> - https://remacs.fun

如果真心希望学习使用融入其中之一，足够的耐心、时间、实践都是不可少的，积极寻找相关社区是解决问题的主要方式；在初期，为了较少配置难度，推荐先直接使用其他人的配置，例如：

- neovim: https://github.com/MartinLwx/dotfiles/tree/main/nvim
- emacs: https://github.com/seagle0128/.emacs.d

又或者，在不配置的情况下大家可以在自己喜欢的 IDE （之后我们会以 vsc 为例进行介绍，大家可以自己先搜索安装使用，或者使用其他“热门” IDE）中安装对应的插件以简单体验，当然相当于是阉割版的。

#### 查找工具

|                                  工具                                  |             优点             |             缺点             |                    使用示例                     |                       适用场景                       |
| :------------------------------------------------------------------: | :------------------------: | :------------------------: | :-----------------------------------------: | :----------------------------------------------: |
|              find / [fd](https://github.com/sharkdp/fd)              |     功能强大，灵活，可执行操作，精确搜索     |          速度慢，语法复杂          | `find "." -n ".DS_Store" -exec rm -i {} \;` | 需要根据多种属性条件查找文件，需要在找到文件后**立即执行某些操作**，需要进行精确的文件名匹配 |
|          grep / [rg](https://github.com/BurntSushi/ripgrep)          |                            |                            |                                             |                                                  |
| [the silver searcher](https://github.com/ggreer/the_silver_searcher) |       速度快，智能忽略，易于使用        | 主要用于代码/文件内容搜索，不如 `find` 灵活 |               `ag rust_learn`               |    需要在大型代码库中快速查找字符串或正则表达式，需要忽略版本控制系统忽略的文件和目录     |
|               [fzf](https://github.com/junegunn/fzf/)                | 实时展示结果（交互式查找），模糊搜索，可结合其他命令 |     初始化需要实践，可能大型仓库可能较慢     |   `find path/to/directory -type f \| fzf`   |                 文件名模糊，实时查找、过滤、选择                 |
|                                locate                                |            速度快             |         实时性差，不够精确          |               `ag rust_learn`               |         需要快速查找文件，对实时性要求不高，只需要按文件名进行简单查找          |
|                                which                                 |          简单易用，速度快          |        功能有限，搜索范围有限         |               `which python3`               |                需要查找命令或可执行文件的完整路径                 |
|                               whereis                                |        查找范围较广，简单易用         |       依赖数据库，结果可能不准确        |              `whereis python3`              |            需要查找命令的二进制文件、源代码和 man 手册页             |

一个配合 fzf 的好用组合：

```sh
$ fzf --preview 'batcat --color=always --style=numbers --line-range=:50 {}'
```

#### 文件管理

|                     工具                     |             优点              |        缺点         |                      适用场景                       |
| :----------------------------------------: | :-------------------------: | :---------------: | :---------------------------------------------: |
| [ranger](https://github.com/ranger/ranger) | Vim-like 界面，多列显示，可定制性强，预览功能 |  学习成本，依赖 Python   |    是 Vim 用户，需要多列显示目录结构，需要预览文件内容，需要对文件管理器进行定制    |
|  [broot](https://github.com/Canop/broot)   |    交互式浏览，模糊搜索，可执行操作，速度快     |     需要安装，学习成本     | 需要交互式地浏览目录结构，需要在大型目录中快速定位文件和目录，需要在浏览目录的同时执行文件操作 |
|                    tree                    |       简单易用，输出清晰，广泛可用        | 功能有限，不适合大型目录，交互性差 |          需要快速查看目录结构，目录结构不太复杂，不需要进行文件操作          |

> `nnn` 也是一个类似的工具，但是使用个人感觉体验较差，就没放在这里了；[yazi](https://yazi-rs.github.io/) 也是，但是 ubuntu 上配置比较麻烦，自行了解。

### 符号

> 作用描述从简，不够严谨。

|  符号  | 作用          | 示例                                                                  |
| :--: | ----------- | ------------------------------------------------------------------- |
| `<`  | 输入重定向       | `cat < input.txt`：将 `input.txt` 的内容作为 `cat` 命令的输入。                  |
| `>`  | 输出重定向 (覆盖)  | `echo 'demo string' > demo.txt`：将 `'demo string'` 覆盖 `demo.txt` 。   |
| `>>` | 输出重定向 (追加)  | `echo 'new line' >> demo.txt`：将 `'new line'` 追加到 `demo.txt` 文件末。    |
| `&&` | 逻辑与 (短路)    | `mkdir mydir && cd mydir`：如果成功创建 `mydir` 目录，则进入该目录。                 |
| `;`  | 顺序执行命令      | `date; ls -l`：先执行 `date` 命令，再执行 `ls -l` 命令。                         |
| `#`  | 注释          | `# This is a comment`：这一行是注释，不会被执行。                                 |
| `\`  | 转义特殊字符      | `echo "This is a \$PATH"`：输出 `This is a $PATH`，`$` 符号被转义，不会被当作变量引用。 |
| `'`  | 单引号内字符串原样输出 | `echo 'This is a $PATH'`：输出 `This is a $PATH`，`$PATH` 不会被当作变量引用。    |
| `"`  | 双引号内选择转义    | `echo "The value of PATH is $PATH`                                  |
| `丨`  | 接收前一命令的输出   | `echo $PATH 丨 tr ':' '\n'` （包含中文字符，仅作观看）                            |

### 网络相关

|     命令     | 简介                                                  |
| :--------: | :-------------------------------------------------- |
|    wget    | 一个用于从网络下载文件的命令行工具，支持 HTTP、HTTPS 和 FTP 下载及镜像网站等。     |
|    curl    | 一个用于发送请求与获取响应的命令行工具，支持多种协议，包括 HTTP、HTTPS、FTP、SCP 等。 |
|    dig     | 一种 DNS 查询工具，用于查询 DNS 记录和进行域名解析，可以用于调试和分析 DNS 问题。    |
|    ping    | 一个测试网络连通性的工具，通过发送 ICMP 数据包到目标主机，测量延迟与丢包率。           |
| traceroute | 一个显示数据包从源主机到目标主机经过的路由路径的工具，帮助分析网络连接及延迟。             |
|  nslookup  | 一个用于查询 DNS 记录的命令行工具，可以帮助检查域名解析和 DNS 配置。             |

### APT 命令

对于拥有图形化界面的虚拟机/类 unix 系统用户，在应用商店或者从浏览器下载后安装应用和 windows 没有太大的差别；对于只有一个简单终端的 WSL 用户（当然也可以安装对应图形化界面，尝试过感觉效果一般，没有其必要性），使用包管理器或者获取安装脚本是常见的方式。

> [!wiki]+ [package manager](https://en.wikipedia.org/wiki/Package_manager)
>
> 包管理器/包管理系统是一系列软件工具，自动化了安装、升级、配置和移除计算机程序的过程，使其在计算机上以一致的方式进行。

出于普遍性，我们仅讲解演示 ubuntu 上的包管理，其他发行版可以参考[使用包管理系统安装](https://101.lug.ustc.edu.cn/Ch03/#use-package-management-system)。

> [!extra]- dpkg
>
> **dpkg** 是 Debian 包管理系统的基础工具，用于安装、卸载和管理 `.deb` 软件包；基于 dpkg 构建了 apt，简化了软件的安装、升级以及卸载过程。
> 
> dpkg 是一个底层的工具，用于处理 `.deb` 软件包，而 apt 是一个高级的工具，构建在 dpkg 之上，提供了更强大的功能和更友好的使用方式。

**APT**（Advanced Package Tool）是 Debian 及其衍生发行版（如 Ubuntu）中常使用的包管理系统，常见命令如下，加粗部分为常使用（大多）：

|         apt 命令          |          命令的功能          |     命令取代的命令 (旧版)     |
| :---------------------: | :---------------------: | :------------------: |
|     **apt update**      |  刷新存储库索引 (更新可安装的软件列表)   |    apt-get update    |
|     **apt install**     |          安装软件包          |   apt-get install    |
|     **apt remove**      |          移除软件包          |    apt-get remove    |
|      **apt purge**      |       移除软件包及配置文件        |    apt-get purge     |
|   **apt autoremove**    |     自动删除不需要的依赖和库文件      |  apt-get autoremove  |
|       apt upgrade       |       升级所有可升级的软件包       |   apt-get upgrade    |
|    apt full-upgrade     | 升级软件包，自动处理依赖关系 (可能删除旧包) | apt-get dist-upgrade |
| apt search \<package\>  |          搜索软件包          |   apt-cache search   |
|  apt show \<package\>   |   显示软件包详细信息 (版本、依赖等)    |    apt-cache show    |
| apt list --upgradeable  |     列出可更新的软件包及版本信息      |                      |
|  apt list --installed   |       列出所有已安装的软件包       |                      |
| apt list --all-versions |    列出所有已安装的软件包的版本信息     |                      |

即然是软件管理，那么软件从哪来是一个比较重要的事情；官方软件来源通常在 `/etc/apt/sources.list` 以及 `/etc/apt/sources.list.d/` 下的文件中为我们写好，我们可以先用 `cat` 进行查看

```sh
$ cat /etc/apt/sources.list
$ cat /etc/apt/sources.list | grep -v '#'
```

> [!extra]- source.list format
>
> 对于其中 source 的格式不进行介绍，有兴趣的同学可以在 [source.list format](https://wiki.debian.org/SourcesList#sources.list_format) 中查看。

如果想要安装一些不在上述来源的软件，或者由于种种问题想要切换为国内镜像源，可以按照一定的格式自行添加；也许大家听过 docker 的镜像源比较多，原理是类似的。

对于部分命令，直接运行可能会出现权限不足（Permission denied）的情况，这也是我们后面要讲解的权限相关内容。

```sh
$ apt update
Reading package lists... Done
E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)
E: Unable to lock directory /var/lib/apt/lists/
W: Problem unlinking the file /var/cache/apt/pkgcache.bin - RemoveCaches (13: Permission denied)
W: Problem unlinking the file /var/cache/apt/srcpkgcache.bin - RemoveCaches (13: Permission denied)
$ apt install tldr
Error: Could not open lock file /var/lib/dpkg/lock-frontend - open (13: Permission denied)
Error: Unable to acquire the dpkg frontend lock (/var/lib/dpkg/lock-frontend), are you root?
$ sudo !!
```

### 系统结构介绍

> [!extra]- 用户与用户组、文件系统结构详细介绍
>
> 在这里[用户与用户组、文件系统结构](https://101.lug.ustc.edu.cn/Ch05/)介绍地非常详细。

`ls -l` 输出示例及解释:

```sh
# drwxr-xr-x 5 user group 4096 Mar 19 19 16:18 dirname
drwxr-xr-x  3 darstib darstib 4096 Mar 19 16:18 demo
```

| 字段                | 解释             |
| ----------------- | -------------- |
| `d`               | 文件类型 (目录)      |
| `rwxr-xr-x`       | 权限 (所有者/组/其他)  |
| `3`               | 硬链接数           |
| `user`            | 文件所有者          |
| `group`           | 文件所属组          |
| `4096`            | 文件大小 (字节)，`-h` |
| `Mar 19 19 16:18` | 修改时间           |
| `dirname`         | 文件/目录名         |

#### sudo

- `sudo`: 以超级用户 (root) 权限执行命令；
- 使用场景: 权限不足时 (`Permission denied`)；
- `sudo su` 切换到超级用户身份；
- `passwd` 更改密码。

#### chmod

##### 字符串语法

|符号|含义|
|---|---|
|u|user (所有者)|
|g|group (组)|
|o|others (其他)|
|a|all (所有人)|
|+|添加权限|
|-|移除权限|
|=|设置权限|
|r|read (读)|
|w|write (写)|
|x|execute (执行)|

##### 八进制语法

|八进制|二进制|权限|
|---|---|---|
|0|000|---|
|1|001|--x|
|2|010|-w-|
|3|011|-wx|
|4|100|r--|
|5|101|r-x|
|6|110|rw-|
|7|111|rwx|

> [!example]-
>   
> | 命令               | 说明                 | 权限表示      |
> | ---------------- | ------------------ | --------- |
> | `chmod -x file` | 给自己添加执行权限 | rwxr-xr-x |
> | `chmod 644 file` | 设置所有者 rw，组和其他 r    | rw-r--r-- |
> | `chmod u+x file` | 给所有者添加执行权限         | rwxr--r-- |
> | `chmod g-w file` | 移除组的写权限            | rwxr-xr-- |
> | `chmod a=r file` | 设置所有人只有读权限         | r--r--r-- |

#### 根目录结构

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/14_250314-204022.png)

在一个[学长的笔记](https://www.yuque.com/dogge2333/study/talqwu#525eb713)中将根目录结构讲得比较详细了，其要点整理成表格如下：

|        目录        |                    描述                    |                备注                 |
| :--------------: | :--------------------------------------: | :-------------------------------: |
|     **/bin**     |             核心二进制文件，包含基本命令。              |          链接到 `/usr/bin`           |
|     `/sbin`      |             系统管理员使用的系统管理程序。              | Superuser Binaries，链接到 `/usr/bin` |
|     `/boot`      |         操作系统启动所需文件，包括内核和引导加载程序。          |                                   |
|      `/dev`      |            设备文件，提供访问硬件设备的端口。             |           不是驱动程序，而是访问接口           |
|     **/etc**     |               系统配置文件和子目录。                |                                   |
|   `/etc/rc.d`    |              系统启动和关闭时使用的脚本。              |                                   |
|    **/home**     |            用户主目录，每个用户有自己的目录。             |                                   |
| `/lib`, `/lib64` |             系统及软件所需的动态链接共享库。             | 类似于 Windows 的 DLL，链接到 `/usr/lib`  |
|     **/mnt**     |             临时挂载其他文件系统的挂载点。              |                                   |
|    **/proc**     |          虚拟文件系统，映射系统内存，提供系统信息。           |           进程信息，可直接访问和修改           |
|    **/root**     |           系统管理员（root 用户）的主目录。            |                                   |
|      `/srv`      |             存放服务启动后需要提取的数据。              |                                   |
|      `/sys`      |           内核设备树的反映,sysfs 文件系统。           |        内核对象创建时，对应文件和目录也会创建        |
|      `/tmp`      |                临时文件存放目录。                 |            公共的，所有用户可用             |
|     **/usr**     | 用户应用程序和文件，类似于 Windows 的 `Program Files`。 |   包含 `/usr/src`, `/usr/sbin` 等    |
|    `/usr/src`    |                  内核源代码。                  |                                   |
|   `/usr/sbin`    |         超级用户使用的比较高级的管理程序和系统守护程序。         |                                   |
|      `/var`      |             存放经常变化的文件，如日志文件。             |             variable              |
|  `/lost+found`   |              系统非法关机后，存放的文件。              |               通常为空                |
|      `/opt`      |              可选的附加软件包的安装目录。              |               默认为空                |
|     `/media`     |        自动挂载的可移动介质（如 U 盘、光驱）的挂载点。         |                                   |

> [!wiki]- [软链接](https://zh.wikipedia.org/wiki/%E7%AC%A6%E5%8F%B7%E9%93%BE%E6%8E%A5)
> 
> **符号链接**（英语：Symbolic link），又称**软链接**，是一类特殊的[文件](https://zh.wikipedia.org/wiki/%E8%AE%A1%E7%AE%97%E6%9C%BA%E6%96%87%E4%BB%B6 "计算机文件")， 其包含有一条以绝对[路径](https://zh.wikipedia.org/wiki/%E8%B7%AF%E5%BE%84_\(%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6\) "路径 (计算机科学)")或者相对路径的形式指向其它文件或者目录的引用。
> 
> 对于软链接可以通过 `ls -l /` 命令查看。

## Windows Terminal

### 安装

参考[安装并开始设置 Windows 终端](https://learn.microsoft.com/zh-cn/windows/terminal/install)；建议下载 [everything](https://www.voidtools.com/zh-cn/)。

### 环境变量

将 `git/usr/bin` 加入环境变量以实现命令可执行。

### 讲解

![windows terminal 设置](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/21_250321-153058.png)

## 美化参考

- [zsh + oh-my-zsh 配置](https://www.haoyep.com/posts/zsh-config-oh-my-zsh/)
- windows
	- [Windows Terminal 内核优化，主题配置](https://www.codestar.top/2024/09/11/Windows/Windows-Terminal%E5%86%85%E6%A0%B8%E3%80%81%E9%85%8D%E7%BD%AE%E5%8F%8A%E4%B8%BB%E9%A2%98%E4%BC%98%E5%8C%96%E5%85%A8%E6%B5%81%E7%A8%8B/)
	- [windows中使用Oh My Posh美化你的终端PowerShell或CMD](https://www.iyouhun.com/post-266.html)
	- [oh my posh setup on windows](https://ohmyposh.dev/docs/installation/windows)
		- [change your prompt](https://ohmyposh.dev/docs/installation/prompt)
	- [告别 Windows 终端的难看难用，从改造 PowerShell 的外观开始](https://zhuanlan.zhihu.com/p/56808199)
- mac
	- [iTerm2 安装配置](https://guoxudong.io/post/iterm2/#iterm2)

## 参考资料

-  [Cyrus' Blog](https://blog.codecyrus.com/posts/linux-shell-basic-usage/)
- [《linux 101》](https://101.lug.ustc.edu.cn/)
-  [MIT The Missing Semester of Your CS Education](https://missing.csail.mit.edu/)
- [一些推荐的命令行工具](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-spring-cs/lec1/#/5/1)
- [20 款优秀的终端工具推荐](https://www.peterjxl.com/Terminal/Recommend/)
