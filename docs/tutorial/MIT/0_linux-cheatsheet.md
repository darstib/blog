---
comments: true
tags:
- MIT
date: 2024-03-15
---

> [!SUMMARY]-
> 本文精简介绍了Linux shell基础，包括路径、文件管理、命令连接、权限和根目录结构。

## 前言

### 什么是 shell?

shell 是操作系统为用户提供交互界面的命令行解释器的统称，例如 Windows 中的 cmd 就是一种 shell。bash 是其中最流行的一种，也是多数 linux 自带的 shell 。

Linux 包含多种 Shell ，常见的有：

- Bourne Shell（ATT 的 Bourne 开发，名为 sh）
- Bourne Again Shell（/bin/bash）
- C Shell（Bill Joy 开发，名为 csh）
- K Shell（ATT的David G.koun 开发，名为 ksh）
- Z Shell（Paul Falstad 开发，名为 zsh）

你需要使用一个类 Unix shell 来完成文中所提到的操作。你可以：

- 使用安装了 Linux 的电脑，或者是 macOS 等类 Unix 系统；
- 对于 Windows 用户，你可以：
	- 使用 Linux 虚拟机；
	- 使用 [WSL(Windows Subsystem for Linux)](https://docs.microsoft.com/zh-cn/windows/wsl/) （本人操作环境为 Ubuntu 22.04）。

### bash

```shell
yourUserName@yourComputerName:~$  # 提示符示例
```

- `$USER`: 当前用户名 (`echo $USER`)。
- `~`:  Home目录 (`pwd` 查看当前路径)。
- `$PATH`: 程序搜索路径 (`which` 查找程序位置)。

当我们想要运行一个环境变量中有的程序的时候，直接输入名称即可；例如，Linux 中有一个程序叫做 `date`，直接输入就可以，这个程序将输出当前的时间：

```shell
:~$ date
Fri Mar 15 19:40:29 CST 2024
```

程序可以附加参数，例如：

```shell
:~$ echo hello
hello
```

这里的 `hello`，就是传给程序 `echo` 的参数。`echo` 程序的功能就是输出它的参数。参数和程序名、参数与参数之间都要使用空格隔开。如果参数里包含空格，可以用 `'` 或 `"` 将参数包裹起来，或者在空格前面加上一个反斜杠转义（如 `My\ PC` 会被转义成 `My PC`）

## 命令

### 路径操作

| 命令    | 作用       | 示例             |
| ----- | -------- | -------------- |
| `pwd` | 显示当前绝对路径 | `/home/user`   |
| `cd`  | 改变当前路径   | `cd /`, `cd -` |
| `.`   | 当前目录     | `code .`       |
| `..`  | 父目录      | `cd ..`        |

### 文件/目录管理

| 命令        | 作用                                   |
| ----------- | -------------------------------------- |
| `ls`        | 列出目录内容                           |
| `ls -l`     | 列出详细信息                           |
| `ls -l -h` | 以人类易读格式显示文件大小            |
| `man` |查看命令帮助文档|
| `touch`     | 创建文件/更新时间戳                     |
| `mkdir`     | 创建目录                               |
| `mv`        | 移动/重命名文件/目录                     |
| `cp`        | 复制文件                               |
| `cp -r`     | 递归复制目录                           |
| `rm`        | 删除文件                               |
| `rm -r`     | 递归删除目录                           |
| `rm -rf`    | 强制递归删除 (慎用!)                      |

`ls -l` 输出示例及解释:

```
drwxr-xr-x 5 user group 4096 Mar 15 16:15 dirname
```

| 字段          | 解释                               |
| ------------- | ---------------------------------- |
| `d`           | 文件类型 (目录)                   |
| `rwxr-xr-x`   | 权限 (所有者/组/其他)                |
| `5`           | 硬链接数                         |
| `user`        | 文件所有者                        |
| `group`      | 文件所属组                       |
| `4096`        | 文件大小 (字节)                    |
| `Mar 15 16:15` | 修改时间                        |
| `dirname`     | 文件/目录名                        |

### 符号与连接

| 符号   | 作用                  |
| ---- | ------------------- |
| `<`  | 输入重定向               |
| `>`  | 输出重定向 (覆盖)          |
| `>>` | 输出重定向 (追加)          |
| `    | `                   |
| `&&` | 逻辑与 (前一命令成功才执行后一命令) |
| `    |                     |
| `;`  | 顺序执行命令              |
| `#`  | 注释                  |
| `\`  | 转义特殊字符              |
| `'`  | 单引号内字符串原样输出         |
| `"`  | 双引号内有选择地转义          |

### sudo

- `sudo`: 以超级用户 (root) 权限执行命令。
- 使用场景: 权限不足时 (`Permission denied`)。
- 提示语强调责任。

### chmod (权限修改)

#### 字符串语法

| 符号 | 含义         |
| ---- | ------------ |
| u    | user (所有者) |
| g    | group (组)    |
| o    | others (其他) |
| a    | all (所有人)   |
| +    | 添加权限     |
| -    | 移除权限     |
| =    | 设置权限     |
| r    | read (读)    |
| w    | write (写)   |
| x    | execute (执行)|

#### 八进制语法

| 八进制 | 二进制 | 权限  |
| ----- | ------ | ----- |
| 0     | 000    | ---   |
| 1     | 001    | --x   |
| 2     | 010    | -w-   |
| 3     | 011    | -wx   |
| 4     | 100    | r--   |
| 5     | 101    | r-x   |
| 6     | 110    | rw-   |
| 7     | 111    | rwx   |

- 示例: `chmod 755 file` (rwxr-xr-x), `chmod 644 file` (rw-r--r--)

### APT 命令

| **apt 命令**              | 命令取代的命令 (旧版)         | 命令的功能                   | 备注                                                                             |
| ----------------------- | -------------------- | ----------------------- | ------------------------------------------------------------------------------ |
| **apt install**         | apt-get install      | 安装软件包                   | `apt install <package_name>` 安装单个,  `apt install <package_1> <package_2>` 安装多个 |
| **apt remove**          | apt-get remove       | 移除软件包                   |                                                                                |
| **apt purge**           | apt-get purge        | 移除软件包及配置文件              |                                                                                |
| apt update              | apt-get update       | 刷新存储库索引 (更新可安装的软件列表)    | `apt update <package_name>` 可用于更新指定软件                                          |
| **apt upgrade**         | apt-get upgrade      | 升级所有可升级的软件包             |                                                                                |
| apt full-upgrade        | apt-get dist-upgrade | 升级软件包，自动处理依赖关系 (可能删除旧包) | 升级前先删除需要更新的软件包                                                                 |
| **apt autoremove**      | apt-get autoremove   | 自动删除不需要的依赖和库文件          |                                                                                |
| apt search              | apt-cache search     | 搜索软件包                   |                                                                                |
| apt show                | apt-cache show       | 显示软件包详细信息 (版本、依赖等)      |                                                                                |
| apt list --upgradeable  |                      | 列出可更新的软件包及版本信息          |                                                                                |
| apt list --installed    |                      | 列出所有已安装的软件包             |                                                                                |
| apt list --all-versions |                      | 列出所有已安装的软件包的版本信息        |                                                                                |

## 根目录结构


![](https://raw.gitmirror.com/darstib/public_imgs/utool/2503/14_250314-204022.png)

在一个[学长的笔记](https://www.yuque.com/dogge2333/study/talqwu#525eb713)中将根目录结构讲得比较详细了，其要点整理成表格如下：

|        目录        |                    描述                    |                备注                 |
| :--------------: | :--------------------------------------: | :-------------------------------: |
|      `/bin`      |             核心二进制文件，包含基本命令。              |          链接到 `/usr/bin`           |
|     `/sbin`      |             系统管理员使用的系统管理程序。              | Superuser Binaries，链接到 `/usr/bin` |
|     `/boot`      |         操作系统启动所需文件，包括内核和引导加载程序。          |                                   |
|      `/dev`      |            设备文件，提供访问硬件设备的端口。             |           不是驱动程序，而是访问接口           |
|      `/etc`      |               系统配置文件和子目录。                |                                   |
|   `/etc/rc.d`    |              系统启动和关闭时使用的脚本。              |                                   |
|     `/home`      |            用户主目录，每个用户有自己的目录。             |                                   |
| `/lib`, `/lib64` |             系统及软件所需的动态链接共享库。             | 类似于 Windows 的 DLL，链接到 `/usr/lib`  |
|      `/mnt`      |             临时挂载其他文件系统的挂载点。              |                                   |
|     `/proc`      |          虚拟文件系统，映射系统内存，提供系统信息。           |           进程信息，可直接访问和修改           |
|     `/root`      |           系统管理员（root 用户）的主目录。            |                                   |
|      `/srv`      |             存放服务启动后需要提取的数据。              |                                   |
|      `/sys`      |           内核设备树的反映,sysfs 文件系统。           |        内核对象创建时，对应文件和目录也会创建        |
|      `/tmp`      |                临时文件存放目录。                 |                公共的                |
|      `/usr`      | 用户应用程序和文件，类似于 Windows 的 `Program Files`。 |   包含 `/usr/src`, `/usr/sbin` 等    |
|    `/usr/src`    |                  内核源代码。                  |                                   |
|   `/usr/sbin`    |         超级用户使用的比较高级的管理程序和系统守护程序。         |                                   |
|      `/var`      |             存放经常变化的文件，如日志文件。             |             variable              |
|  `/lost+found`   |              系统非法关机后，存放的文件。              |               通常为空                |
|      `/opt`      |              可选的附加软件包的安装目录。              |               默认为空                |
|     `/media`     |        自动挂载的可移动介质（如 U 盘、光驱）的挂载点。         |                                   |

> [!tip]-
>
> 对于软链接可以通过 `ls -l /` 命令查看。

## 参考资料

-  [MIT The Missing Semester of Your CS Education](https://missing.csail.mit.edu/)
-  [Cyrus' Blog](https://blog.codecyrus.com/posts/linux-shell-basic-usage/)
-  [GNU manual documents](https://www.gnu.org/software/coreutils/manual/html_node/General-output-formatting.html)
