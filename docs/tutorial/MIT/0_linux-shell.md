---
comments: true
tags:
- MIT
date: 2024-03-15
---
***

> [!SUMMARY]-
> 
> 本文介绍了 Linux shell 的基本使用，包括路径操作、文件管理、命令连接、权限管理等。
>
> - **shell：** 操作系统为用户提供的命令行解释器，如 bash。
> - **路径：** pwd/cd 命令可操作路径，`.` 代表当前目录，`..` 代表父目录。
> - **文件管理：** touch 创建/更新文件，mkdir 创建目录，mv 移动/重命名，cp 复制，rm 删除。
> - **命令连接：** `<`、`>`、`>>`、`|`、`&&`、`||`、`;` 可连接命令。
> - **权限管理：** chmod 可调整文件权限，字符串语法和数字语法均可使用。

<!-- more -->
## I 前言

### I.1 什么是 shell?

shell是操作系统为用户提供交互界面的命令行解释器的统称，例如Windows中的cmd就是一种shell。bash 是其中最流行的一种。bash 是 Bourne Again shell 的简称。

> 本文多学习借鉴自 [Cyrus' Blog](https://cyrus28214.top/post/bb59eff0fad1/?highlight=linux)，再加入自己的部分理解。

你需要使用一个类Unix shell来完成文中所提到的操作。你可以：

- 使用安装了Linux的电脑
- 使用Linux虚拟机
- 使用 [WSL(Windows Subsystem for Linux)](https://docs.microsoft.com/zh-cn/windows/wsl/) （本人操作环境为 Ubuntu 22.04）

### I.2 使用shell

进入shell，可以看到这样的一行提示：

```shell
yourUserName@yourComputerName:~$
```

 - `yourUserName` 代表当前用户的用户名，也可以使用 `echo $USER` 来查看，以后我们省略不写；
 - `~`代表当前所在路径，也可以使用`pwd`来查看；
 - `$`是命令提示符，提示用户现在可以输入命令了。

`~` 是表示用户的**home**目录，非 root 用户的 `~` 代表 `/home/$USER/`，而 root 用户的 `~` 代表 `/root`。

当我们想要运行一个程序的时候，直接输入名称即可

例如，Linux 中有一个程序叫做 `date`，直接输入就可以，这个程序将输出当前的时间：

```shell
:~$ date
Fri Mar 15 19:40:29 CST 2024
```

程序可以附加参数，例如：

```shell
:~$ echo hello
hello
```

这里的`hello`，就是传给程序`echo`的参数。`echo`程序的功能就是输出它的参数。参数和程序名、参数与参数之间都要使用空格隔开。如果参数里包含空格，可以用`'`或`"`将参数包裹起来，或者在空格前面加上一个反斜杠转义（如`My\ Photos`会被转义成`My Photos`）

shell怎么知道这些程序在哪里呢？其实shell会在`$PATH`里面的路径寻找。这里的`$PATH`和上面的`$USER`都是shell中的变量，`$`表示引用变量，提示shell把`$变量名`替换成变量的值。`$PATH`储存了多个路径，用“:”隔开，提示了shell去哪里找这个程序。你也可以使用`which`来查找某一个程序的具体位置。输入程序的完整路径，也可以绕过`$PATH`运行程序。

```shell
:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
:~$ which echo
/bin/echo
:~$ /bin/echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

## II 命令

### II.1 路径: pwd/cd 

在 Linux 和 MacOS 中，路径使用 `/` 分隔，而在 Windows 中是 `\`。在 Linux 和 MacOS 中，路径从 `/` 开始，代表根目录（包含了所有目录）；在 Windows 中，路径从盘符开始，如 `C:\`。

以 `/` 开头的路径叫绝对路径，否则就是相对路径。`pwd`（print working directory 的缩写）可以显示当前所在的绝对路径，`cd`（change directory 的缩写）可以改变当前所在路径。

`.` 代表当前所在目录，`..` 代表父目录。

在 shell 中输入路径时，可以按 Tab 来自动补全文件名。另外，在 shell 中按↑/↓方向键，可以浏览历史命令。

```txt
:~$ pwd
/home/yourusername
:~$ cd /home
:/home$ pwd
/home
:/home$ cd ..
:/$ pwd
/
:/$ cd ./home
:/home$ pwd
/home
```

输入 `cd -` 可以移动到上次所在的目录，相当于 `cd $OLDPWD`，非常方便。

```shell
:/$ cd ~
:~$ pwd
/home/yourusername
:~$ echo $OLDPWD
/
:~$ cd -
/
:/$ pwd
/
```

### II.2 ls

`ls`（list的缩写）可以列出当前目录下有什么：

```shell
:/$ ls
bin
boot
dev
etc
home
...
```

绝大多数程序都可以接受以`-`开头的参数来改变程序的行为。例如，`-h`或`--help`一般会输出程序的帮助文本，如：

```shell
:/$ ls --help
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
...
```

> `[OPTION]` 表示参数是可选的
> 显示 `ls` 的帮助只能使用 `--help` 而不能使用 `-h`，因为 `-h` 已经被其他功能占用了

其中有一行

```shell
  -l                         use a long listing format
```

根据这个内容，我们给`ls`命令附加上`-l`参数，有：

```
:/home$ ls -l
total 12
drwxr-xr-x 5 yourusername yourusername 4096 Mar 15 16:15 code
drwxr-xr-x 6 yourusername yourusername 4096 Mar 14 16:00 webpage
drwxr-xr-x 9 yourusername yourusername 4096 Mar 13 19:13 work
```

`-l`参数非常有用，可以列出详细信息。

第一列的第一个字符是`d`代表这是一个文件夹，下面列出了可能的类型：

| 标识符 | 类型         | 英文                    |
| --- | ---------- | --------------------- |
| –   | 常规文件       | regular file          |
| d   | 文件目录       | directory             |
| c   | 字符设备文件     | character device file |
| b   | 块设备文件      | block device file     |
| s   | 本地socket文件 | local socket file     |
| p   | 命名管道       | named pipe            |
| l   | 符号链接       | symbolic link         |

然后是九个字符描述了使用此文件的权限，三个字符为一组分成三组，分别表示文件持有者、文件持有组、和其他用户的权限。每组的三个字符中，`r`、`w`、`x`分别代表read读、write写、execute执行权限，`-`代表没有权限。

例如`rwxr-xr--`代表文件持有者可以读、写、运行此文件，文件持有组可以读、运行此文件，其他用户只能读此文件。

第二列是有多少“硬链接”指向这个文件。

第三列和第四列，分别是文件持有者和文件持有组的名称

第五列是文件大小，默认以byte为单位，如果想要显示成“8M”,“13K”这种形式，只需要为`ls`命令附加上`-h`参数。

第六列就是文件的修改时间，即[mtime]()。

最后一列就是文件名

### II.3 man

`man`可以显示一个命令的详细帮助文档，输入`man ls`，会显示比`ls --help`更加详细的命令使用帮助。

### II.4 touch、mkdir、mv、cp、rm

`touch 文件名`有两个作用：

- 若文件不存在，创建这个文件
- 若文件存在，将文件的[atime]()和[mtime]()设置为现在的时间。

`mkdir 目录名`（make directory）可以创建新的文件夹，例：

```shell
:~$ mkdir case
:~$ ls -l
total 16
drwxr-xr-x 2 qssg qssg 4096 Mar 15 19:53 case
...
```

`mv 源 目标`（move），可以用来移动文件/文件夹，也可以用来重命名文件/文件夹。

根据“源”和“目标”的不同，`mv`会做出以下不同的行为：

- 移动：如果目标是一个存在的路径，则源会被移动到此目录下，名称不变。
- 重命名：否则，则源文件名会变为此目标文件名，如果存在同名文件，则会覆盖己存在的同名文件。

`cp`（copy）的使用和`mv`很像，会在目标目录下生成一个副本，如果需要复制一个文件夹，需要附加`-r`参数（recursive 递归的缩写），来递归地拷贝文件夹下所有文件。

`rm 目标`（remove）可以删除文件或目录，如果要删除的是一个目录，也需要附加`-r`参数，来执行递归地删除。默认情况下，`rm`命令需要你逐个确认你是否确定删除这个文件，附加`-f`参数可以无需再次确认， **使用`-f`时请保证你真的要删除，没有再次确定的机会了**

## III 符号

### III.1 `<`、`>`、`>>`、`|`、`&&`、`||`、`;`

"< 文件"可以使用文件作为程序的输入，"> 文件"可以将程序的输出保存到文件中（不存在就会被创建）

```shell
:~$ echo hello > hello.txt
:~$ cat hello.txt
hello
:~$ cat < hello.txt
hello
:~$ cat < hello.txt > hello2.txt
:~$ cat hello2.txt
hello
```

上面 `cat` 的作用是将文件的内容展示到命令行输出。

“>”会覆盖原来存在的文件，如果文件不存在，会创建一个新文件并写入。

如果不想原来存在的文件被覆盖，而是想将新的内容加在文件末尾，可以使用“>>”

“|”长得像一个管道，它的作用就是像管道一样连接两个程序的输入与输出，它会把前面的程序的输出作为后面的程序的输入。

```shell
:~$ ls -l / | tail -n1
drwxr-xr-x  13 root root    4096 May  2  2023 var
```

这里的 `tail -n1` 表示将取输入的最后一行并输出。

`&&` 其实是逻辑与运算，也可以用来连接两条命令，当前面的命令执行成功时才执行后面的命令。用 `&&` 连接多个命令，假如中间发生了错误，就不会继续执行，引发一连串的错误。

`||` 相应的，逻辑或运算是当前面的命令执行失败时才执行后面的命令。可以用于设置一个“Plan B”，当前面的命令执行失败，就执行“Plan B”。

`;` 就是单纯的先后执行两条命令，无论成功与否，两条命令都会执行。

### III.2 `#`

`#`表示注释，`#`后的文本会被忽略。

```shell
:~$ echo hello
hello
:~$ echo #hello
:~$ touch hello
:~$ touch #hello
touch: missing file operand
Try 'touch --help' for more information.
```

### III.3 `\`、`'`、`"`

在shell中，有一些字符不能直接作为参数的一部分传递，例如`!`、`$`、` `、`#`、`\`。

使用反斜杠`\`可以转义单个字符，使其正常输出：

```shell
:~$ echo hello$world
hello
:~$ echo hello\$world
hello$world
:~$ echo hello     world
hello world
:~$ echo hello\ \ \ \ \ world
hello     world
:~$ echo hello\world
helloworld
:~$ echo hello\\world
hello\world
```

使用单引号`'`括起来，可以让字符串原样输出，不进行转义和替换

```shell
:~$ echo 'hello\\world'
hello\\world
```

使用双引号`"`括起来的字符串仍然有部分会被转义，参见[Quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html)。

```shell
:~$ echo '$SHELL'
$SHELL
:~$ echo "$SHELL"
/bin/bash
:~$ echo "hello world"
hello world
```

## IV sudo

Linux系统中有一个用户的身份是特殊的，那就是 root 用户，root用户拥有最高的权限，可以做几乎任何事情，直接登录到root用户是很危险的，因为你可能一不小心就利用root权限做出了一些破环性的操作（例如：误删除数据、全局修改了关键系统设置），因此，常常使用`sudo 命令`（意思是 do as superuser），来使用超级用户权限执行命令，这样可以让你能再次确认你的操作无误。

当你输入一个命令，发现命令行输出了“Permission denied”，很可能就是你没有合适的权限执行这个命令，只要在原命令前加上`sudo`就可以解决。

第一次`sudo`时，会输出一段这样的提示：

```shell
We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:
    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.
```

翻译如下：

```shell
我们确信您已经收到了本地系统管理员的例行讲解。
通常可以归结为以下三点：
    #1) 尊重他人隐私。
    #2) 打字前先思考。
    #3) 权力越大，责任越大。
```

“With great power comes great responsibility.”

使用root权限时要时刻提醒自己，谨慎对待每一个命令

下面有一个来自 MIT Missing Semester 的例子，指出了使用`sudo`的一个常见误区：

>例如，您笔记本电脑的屏幕亮度写在 `brightness` 文件中，它位于
>```txt
>/sys/class/backlight
>```
>通过将数值写入该文件，我们可以改变屏幕的亮度。现在，蹦到您脑袋里的第一个想法可能是：
>```txt
>$ sudo find -L /sys/class/backlight -maxdepth 2 -name '*brightness*'
>/sys/class/backlight/thinkpad_screen/brightness
>$ cd /sys/class/backlight/thinkpad_screen
>$ sudo echo 3 > brightness
>An error occurred while redirecting file 'brightness'
>open: Permission denied
>```
>出乎意料的是，我们还是得到了一个错误信息。毕竟，我们已经使用了 `sudo` 命令！关于 shell，有件事我们必须要知道。`|`、`>`、和 `<` 是通过 shell 执行的，而不是被各个程序单独执行。 `echo` 等程序并不知道 `|` 的存在，它们只知道从自己的输入输出流中进行读写。 对于上面这种情况， shell (权限为您的当前用户) 在设置 `sudo echo` 前尝试打开 brightness 文件并写入，但是系统拒绝了 shell 的操作因为此时 shell 不是根用户。
>
>明白这一点后，我们可以这样操作：
>```txt
>$ echo 3 | sudo tee brightness
>```
>因为打开 /sys 文件的是 tee 这个程序，并且该程序以 root 权限在运行，因此操作可以进行。 这样您就可以在 /sys 中愉快地玩耍了，例如修改系统中各种LED的状态（路径可能会有所不同）：
>```txt
>$ echo 1 | sudo tee /sys/class/leds/input6::scrolllock/brightness
>```

## V chmod

前面我们提到了文件的三种权限`rwx`，使用`chmod`可以调整这些权限。

chmod 可以使用两种语法，字符串语法和数字语法。

### V.1 字符串语法

- 用`ugoa`四个字母表示设置哪些人的权限
- 用`+-=`三个字母表示如何改变权限
- 用`rwx`表示什么权限

|符号|含义|
|---|---|
|u|user，文件的拥有者|
|g|group，文件拥有者所在的组的其他人|
|o|others，除了ug的其他人|
|a|all，所有人|
|+|添加权限|
|-|减少权限|
|=|设置权限|
|r|read，读取|
|w|write，写入|
|x|execute，执行|

例如：

`chmod ug+rw file`表示文件拥有者所在的组的所有人添加读取和写入file的权限。

`chmod a-w file`表示所有人都不能写入file。

`chmod ug=rwx,o=x file`表示文件拥有者所在的组的所有人都可以读、写、运行file，其他人只能运行file

### V.2 八进制数字语法

一共有三种权限`rwx`，$2^3=8$，可以使用8个数字来表示某种人的权限，权限又分为针对三种人`ugo`，于是，一个文件的权限可以用三个0-7的数字表示。

`rwx`三种权限从高位到低位可以组成一个三位二进制数，`0`代表没有这种权限，`1`代表有，再将这个二进制数转化成八进制（或者十进制，在这里结果是一样的），就得到了对应的数字，下面列出了0-7对应的权限：

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

例如：

- `chmod 777 file`代表所有人都有file的所有权限
- `chmod 755 file`代表file的权限是`rwxr-xr-x`

755是创建新文件夹的默认权限

- `chmod 644 file`代表file的权限是`rw-r--r--`

644是创建新文件的默认权限

使用数字来设置权限，可以仅仅用三个字符就设置好每一个权限，非常方便快捷。

## VI 其他常用

| apt              | 命令取代的命令              | 命令的功能           |
| ---------------- | -------------------- | --------------- |
| apt install      | **apt-get install**      | 安装软件包           |
| apt remove       | **apt-get remove**       | 移除软件包           |
| apt purge        | apt-get purge        | 移除软件包及配置文件      |
| apt update       | apt-get update       | 刷新存储库索引         |
| apt upgrade      | apt-get upgrade      | 升级所有可升级的软件包     |
| apt autoremove   | apt-get autoremove   | 自动删除不需要的包       |
| apt full-upgrade | apt-get dist-upgrade | 在升级软件包时自动处理依赖关系 |
| apt search       | apt-cache search     | 搜索应用程序          |
| apt show         | apt-cache show       | 显示安装细节          |

## VII 参考资料

-  [Cyrus' Blog](https://cyrus28214.top/post/bb59eff0fad1/?highlight=linux)
-  [MIT The Missing Semester of Your CS Education](https://missing.csail.mit.edu/)
-  [GNU manual documents](https://www.gnu.org/software/coreutils/manual/html_node/General-output-formatting.html)

