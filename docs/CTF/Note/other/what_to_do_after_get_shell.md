---
tags:
- notes
- ctf
comments: true
---

拿到 shell/ 可以任意代码执行了都不知道该干什么？下面是可能的思路以 [moectf2024 moejail_lv1](https://ctf.xidian.edu.cn/games/10/challenges?challenge=95) 为例。

## 暴力搜索文件内容

例如，我们可以使用 `find . -name "*" -exec grep -H "flag{" {} \;` 来递归搜索文件中包含 `flag{` 字段的文件，熟悉命令的话可以知道，`.` 表示由当前路径开始，`*` 所在的引号内表示匹配的文件名，`*` 表示我们想要搜索所有文件。

（这里使用 /tmp/ 是因为我已经知道它在那了，节约时间）

![](attachments/what_to_do_after_get_shell-4.png)

如果发现什么都没搜到，可能需要注意的是[globbing pathnames](https://man7.org/linux/man-pages/man7/glob.7.html)：

> [!quote] 
>
> If a filename starts with a `.`, this character must be matched explicitly.  (Thus, _rm *_ will not remove .profile, and _tar c *_ will not archive all your files; _tar c ._ is better.)

例如

![](attachments/what_to_do_after_get_shell-6.png)

但是

![](attachments/what_to_do_after_get_shell-7.png)

## 查看一些关键信息

### 环境变量

执行 `env` 或者 `set` 可以查看环境变量（有时可能就是 `echo $FLAG` 就可以了）。

### 命令历史

在 `~/.history` `~/.bash_history` `~/.zsh_history` 中可能包含了执行过的历史记录，从命令我们可以推测出题人之前在这干了什么。

例如，我在使用 zsh 之前只是使用 bash 安装了 zsh 而已：

![](attachments/what_to_do_after_get_shell-8.png)

## 从当前文件找线索

### 查看当前路径

可以使用 `pwd` `ls` `ls -a` 等查看当前路径及文件。

![](attachments/what_to_do_after_get_shell.png)

### 就近查看文件寻找有用信息

![](attachments/what_to_do_after_get_shell-1.png)

![](attachments/what_to_do_after_get_shell-2.png)

### 查看对应的文件

![](attachments/what_to_do_after_get_shell-3.png)

## 其他

其他可能存在信息，但是不那么常见的内容，包括当前 shell 所在服务器/系统的信息，运行过的进程等等……

在 Linux 系统中，你可以使用多种命令行工具来查看进程信息。以下是一些常用的命令：

1. **`ps` 命令**：
    - 用于查看当前运行的进程。
    - 示例：`ps aux` 显示所有用户的所有进程。
    - 示例：`ps -ef` 以完整格式显示进程。
2. **`top` 命令**：
    - 实时显示系统中正在运行的进程，并提供 CPU 和内存使用情况。
    - 只需在命令行中输入 `top`，然后按 `q` 退出。
3. **`htop` 命令**：
    - 类似于 `top`，但提供了更友好的用户界面和更多功能（如可视化）。
    - 如果没有安装，可以通过 `sudo apt install htop` 或 `sudo yum install htop` 安装。
4. **`pgrep` 命令**：
    - 根据名称查找进程 ID（PID）。
    - 示例：`pgrep python` 查找所有 Python 进程的 PID。
5. **`pidof` 命令**：  
    - 用于查找特定程序的 PID。
    - 示例：`pidof bash`
6. **`pstree` 命令**：
    - 以树形结构显示进程及其子进程。
    - 示例：`pstree`
7. **`lsof` 命令**：
    - 列出打开的文件及其相关联的进程。
    - 示例：`lsof | grep <filename>` 查找特定文件的相关进程。
8. `/proc/目录结构：`
    - `/proc/<PID>/status`: 查看特定进程的信息。
    - `/proc/<PID>/cmdline`: 查看启动该进程时使用的命令行参数。