---
comments: true
tags:
- MIT
- blog
- note
date: 2024-03-16
---
***

> [!SUMMARY]-
>
> 本文介绍了 shell 脚本和一些基本工具的使用方法。
>
> - **shell 脚本：** 使用 `#!` 指定解释器，使用 `echo` 输出文本，可以使用两种方式运行。
> - **shell 变量：** 使用 `=` 定义，使用 `$` 使用，可以使用只读变量。
> - **字符串：** 使用单引号或双引号定义，可以使用拼接和数组。
> - **通配：** 使用 `?` 和 `*` 进行匹配，使用花括号展开命令。
> - **shebang：** 使用 `#!` 声明解释器，可以使用 `env` 提高可移植性。
> - **shell 工具：** 介绍了 `man`、`TLDR pages`、`find`、`fd`、`locate`、`grep`、`rg`、`history`、`fasd` 和 `autojump` 等工具。

<!-- more -->

## I Shell 脚本

Shell 脚本（shell script），是一种为 shell 编写的脚本程序。

业界所说的 shell 通常都是指 shell 脚本，但读者朋友要知道，shell 和 shell script 是两个不同的概念。

由于习惯的原因，简洁起见，本文出现的 "shell 编程" 都是指 shell 脚本编程，不是指开发 shell 自身。

在一般情况下，人们并不区分 Bourne Shell 和 Bourne Again Shell，所以，像 **#!/bin/sh**，它同样也可以改为 **#!/bin/bash**。

`#!` 告诉系统其后路径所指定的程序即是解释此脚本文件的 Shell 程序。

<!-- more -->

### I.1 创建脚本

如果我们想要创建一个 shell 脚本，那么，打开文本编辑器(可以使用 vi/vim 或者 nano 命令（新手推荐）来创建文件)，新建一个文件 first.sh，扩展名为 sh（sh代表shell），扩展名并不影响脚本执行，见名知意就好，如果你用 php 写 shell 脚本，扩展名就用 php 好了。

输入一些代码，第一行一般是这样：

```shell title="first.sh"
$ nano first.sh # 接下来将进入编辑界面
#!/bin/bash
echo 'Hello world!'
```

之后只需要 `ctrl+o` 保存，回车确认文件名，`ctrl+x` 退出即可。

`#!` 是一个约定的标记，它告诉系统这个脚本需要什么解释器来执行，即使用哪一种 Shell；echo 命令用于向窗口输出文本

### I.2 运行 Shell 脚本有两种方法：

**1、作为可执行程序**

将上面的代码保存为 first.sh，并 cd 到相应目录：

```shell
chmod +x ./first.sh  #使脚本具有执行权限
# 或者我们可以用下面的语句
chmod 775 ./first.sh 
./first.sh  #执行脚本
```

看不懂 775 的话回看 [[]]

注意，一定要写成 ./first.sh，而不是 **first.sh**，运行其它二进制的程序也一样，直接写 first.sh，linux 系统会去 PATH 里寻找有没有叫 first.sh 的，而只有 /bin, /sbin, /usr/bin，/usr/sbin 等在 PATH 里，你的当前目录通常不在 PATH 里，所以写成 first.sh 是会找不到命令的，要用 ./first.sh 告诉系统说，就在当前目录找。

**2、作为解释器参数**

这种运行方式是，直接运行解释器，其参数就是 shell 脚本的文件名，如：

`/bin/sh first.sh` 

> 我现在是使用 vscode 远程 ssh 连接 ubuntu 进行的编辑运行，如果单纯使用终端可能需要相关 vim 编辑技能，请自行了解；暂时使用下方方式也无妨，但基于 [EOF 可做多行注释](https://www.w3schools.cn/linux/linux_shell_variable.html#:~:text=%E5%A4%9A%E8%A1%8C%E6%B3%A8%E9%87%8A-,%E5%A4%9A%E8%A1%8C%E6%B3%A8%E9%87%8A%E8%BF%98%E5%8F%AF%E4%BB%A5%E4%BD%BF%E7%94%A8%E4%BB%A5%E4%B8%8B%E6%A0%BC%E5%BC%8F)，比较可能会出问题
> ![[attachments/Pasted image 20240222173832.png]]

理论上我们最好不使用双引号

> `!` 即使被双引号（`"`）包裹也具有特殊的含义。单引号（`'`）则不一样，此处利用这一点解决输入问题。更多信息请参考 [Bash quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html) 手册

## II shell 变量

### II.1 变量定义

定义变量时，变量名不加美元符号（$，PHP 语言中变量需要），例如

```shell
my_name=qssg #请不要在 = 两侧留空格，在shell脚本中使用空格会起到分割参数的作用，有时候可能会造成混淆
```

命名规则想必都烂熟于心，大体就是只有字母、下划线、数字（不打头）

#### II.1.1 只读变量

使用 readonly 命令可以将变量定义为只读变量，只读变量的值不能被改变。

下面的例子尝试更改只读变量，结果报错：

```#!/bin/bash  
myUrl="https://www.google.com"  
readonly myUrl  
myUrl="https://www.w3schools.com"
```

运行脚本，结果如下：

`/bin/sh: NAME: This variable is read only.`

### II.2 变量赋值

```
my_name="tom"  
echo $my_name  
my_name="alibaba"  
echo $my_name  
```

这样写是合法的，但注意，第二次赋值的时候不能写` $my_name="alibaba"`，使用变量的时候才加美元符($）

和其他大多数的编程语言一样，`bash`也支持`if`, `case`, `while` 和 `for` 这些控制流关键字。同样地， `bash` 也支持函数，它可以接受参数并基于参数进行操作。下面这个函数是一个例子，它会创建一个文件夹并使用`cd`进入该文件夹

```shell
mcd () {
    mkdir -p "$1"
    cd "$1"
}
```

关于这个 `$1` ,见[特殊变量表示参数](https://missing-semester-cn.github.io/2020/shell-tools/#:~:text=1%22%0A%20%20%20%20cd%20%22%241%22%0A%7D-,%E8%BF%99%E9%87%8C%20%241%20%E6%98%AF%E8%84%9A%E6%9C%AC%E7%9A%84%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%8F%82%E6%95%B0,-%E3%80%82%E4%B8%8E%E5%85%B6%E4%BB%96%E8%84%9A%E6%9C%AC)

其中较为常用的有：

- `$?` - 前一个命令的返回值
- `!!` - 完整的上一条命令，包括参数
    - 常见应用：当你因为权限不足执行命令失败时，可以使用 `sudo !!` 再尝试一次

### II.3 使用变量

使用变量时，需要在变量名前加上 `$` 

```shell
echo $my_name
echo ${my_name}
```

变量名外面的花括号是可选的，加不加都行，加花括号是为了帮助解释器识别变量的边界，比如下面这种情况：

```shell
for skill in Ada Coffe Action Java; do  
    echo "I am good at ${skill}Script"  
done  
```

如果不给skill变量加花括号，写成`echo "I am good at $skillScript"`，解释器就会把$skillScript当成一个变量（其值为空），代码执行结果就不是我们期望的样子了。

Bash 中的字符串通过 `'` 和 `"` 分隔符来定义，但是它们的含义并不相同。以 `'` 定义的字符串为原义字符串，其中的变量不会被转义，而 `"` 定义的字符串会将变量值进行替换。 ^10e53b

```shell
foo=bar
echo "$foo"
# 打印 bar
echo '$foo'
# 打印 $foo
```

推荐给所有变量加上花括号或者双引号，这是个好的编程习惯

### II.4 删除变量

使用 unset 命令可以删除变量。语法：

`unset variable_name` 

变量被删除后不能再次使用；unset 命令不能删除只读变量

## III 字符串

#### III.1.1 字符串格式

字符串可以由单引号和双引号包裹，这点 [[02-shell 脚本和工具#^10e53b|前面]] 已经讲的较为明白了

#### III.1.2 拼接字符串

无需多说，将前文总结可以运行

```shell
my_name="qssg"
# 使用双引号拼接
greeting="hello, "$my_name" !"
greeting_1="hello, ${my_name} !"
echo $greeting  $greeting_1  
# 使用单引号拼接
greeting_2='hello, '$my_name' !'
greeting_3='hello, ${my_name} !'
echo $greeting_2  $greeting_3
```

运行结果：（根据上边文字颜色其实都能猜到）

![[attachments/Pasted image 20240222194212.png]]

#### III.1.3 字符串数组

可以直接看 [w 3 school](https://www.w3schools.cn/linux/linux_shell_variable.html#:~:text=%E7%9C%8B%E9%94%99%E4%BA%86%E5%93%A6%E3%80%82-,shell%20%E6%95%B0%E7%BB%84,-bash%E6%94%AF%E6%8C%81%E4%B8%80) 上的讲解，不加赘述

### III.2 获取返回值

#### III.2.1 STDOUT & STDERR

命令通常使用 `STDOUT`来返回输出值，使用`STDERR` 来返回错误及错误码，便于脚本以更加友好的方式报告错误。 返回码或退出状态是脚本/命令之间交流执行状态的方式。返回值0表示正常执行，其他所有非0的返回值都表示有错误发生

#### III.2.2 && ||

退出码可以搭配 `&&`（与操作符）和 `||`（或操作符）使用，用来进行条件判断，决定是否执行其他程序。它们都属于[短路运算符](https://en.wikipedia.org/wiki/Short-circuit_evaluation)（short-circuiting） 同一行的多个命令可以用 `;` 分隔。程序 `true` 的返回码永远是 `0`，`false` 的返回码永远是 `1`

#### III.2.3 命令替换（command substitution）

当通过 `$(CMD)` 这样的方式来执行 `CMD` 这个命令时，它的输出结果会替换掉 `$(CMD)` 。

例如，如果执行 `for file in $(ls)` ，shell首先将调用`ls` ，然后遍历得到的这些返回值

[进程替换以及一些例子](https://missing-semester-cn.github.io/2020/shell-tools/#:~:text=%E8%BF%9B%E7%A8%8B%E6%9B%BF%E6%8D%A2(process%20 substitution)看不太懂，有兴趣请自行学习

## IV 通配

当执行脚本时，我们经常需要提供形式类似的参数。bash使我们可以轻松的实现这一操作，它可以基于文件扩展名展开表达式。这一技术被称为shell的 _通配_（_globbing_）

有点像正则表达式

- 通配符 - 当你想要利用通配符进行匹配时，你可以分别使用 `?` 和 `*` 来匹配一个或任意个字符。例如，对于文件`foo`, `foo1`, `foo2`, `foo10` 和 `bar`, `rm foo?`这条命令会删除`foo1` 和 `foo2` ，而`rm foo*` 则会删除除了`bar`之外的所有文件。
- 花括号`{}` - 当你有一系列的指令，其中包含一段公共子串时，可以用花括号来自动展开这些命令。这在批量移动或转换文件时非常方便。

例如：

```shell
convert image.{png,jpg}
# 会展开为
convert image.png image.jpg
cp /path/to/project/{foo,bar,baz}.sh /newpath
# 会展开为
cp /path/to/project/foo.sh /path/to/project/bar.sh /path/to/project/baz.sh /newpath
# 也可以结合通配使用
mv *{.py,.sh} folder
# 会移动所有 *.py 和 *.sh 文件
mkdir foo bar
# 下面命令会创建foo/a, foo/b, ... foo/h, bar/a, bar/b, ... bar/h这些文件
touch {foo,bar}/{a..h}
touch foo/x bar/y
# 比较文件夹 foo 和 bar 中包含文件的不同
diff <(ls foo) <(ls bar)
# 输出
# < x
# ---
# > y
```

编写 `bash` 脚本有时候会很别扭和反直觉。例如 [shellcheck](https://github.com/koalaman/shellcheck) 这样的工具（或者是 vscode 上同名插件）可以帮助你定位 sh/bash 脚本中的错误

## V shebang

通常地，我们称 `#!` 为 `shebang`，wiki 百科上是这样解释的：

![[attachments/Pasted image 20240222194757.png]]

通俗地说，就是用 `shebang` 来声明下面的脚本应该使用什么程序去运行

比如说，这是一段 Python 脚本，作用是将输入的参数倒序输出：

```shell
#!/usr/local/bin/python
import sys
for arg in reversed(sys.argv[1:]):
    print(arg)
```

在 `shebang` 行中使用 [`env`](https://man7.org/linux/man-pages/man1/env.1.html) 命令是一种好的做法，它会利用环境变量中的程序来解析该脚本，这样就提高脚本的可移植性。`env` 会利用 `PATH` 环境变量来进行定位

例如，使用了 `env` 的 shebang 看上去时这样的 `#!/usr/bin/env python`

[shell函数和脚本有一些不同点](https://missing-semester-cn.github.io/2020/shell-tools/#:~:text=bin%2Fenv%20python%E3%80%82-,shell%E5%87%BD%E6%95%B0%E5%92%8C%E8%84%9A%E6%9C%AC%E6%9C%89%E5%A6%82%E4%B8%8B%E4%B8%80%E4%BA%9B%E4%B8%8D%E5%90%8C%E7%82%B9)，请读者自行跳转观看

## VI Shell 工具

### VI.1 man

`man` 命令是 manual（手册）的缩写，属于是网页版 linux 手册

### VI.2 TLDR pages

`man` 命令有时过于详细了，不利于我们学习常用的命令及选项

 [TLDR pages](https://tldr.sh/) 是一个很不错的替代品，它提供了一些案例，可以帮助您快速找到正确的选项（当然，也可以找找其他比较靠谱的 Linux 手册）。
 
### VI.3 文件查找

程序员们面对的最常见的重复任务就是查找文件或目录。所有的类UNIX系统都包含一个名为 [`find`](https://man7.org/linux/man-pages/man1/find.1.html) 的工具，它是 shell 上用于查找文件的绝佳工具。`find`命令会递归地搜索符合条件的文件，例如：

```shell
# 查找所有名称为src的文件夹
find . -name src -type d
# 查找所有文件夹路径中包含test的python文件
find . -path '*/test/*.py' -type f
# 查找前一天修改的所有文件
find . -mtime -1
# 查找所有大小在500k至10M的tar.gz文件
find . -size +500k -size -10M -name '*.tar.gz'
```

除了列出所寻找的文件之外，find 还能对所有查找到的文件进行操作。这能极大地简化一些单调的任务。

```
# 删除全部扩展名为.tmp 的文件
find . -name '*.tmp' -exec rm {} \;
# 查找全部的 PNG 文件并将其转换为 JPG
find . -name '*.png' -exec convert {} {}.jpg \;
```

尽管 `find` 用途广泛，它的语法却比较难以记忆。例如，为了查找满足模式 `PATTERN` 的文件，您需要执行 `find -name '*PATTERN*'` (如果您希望模式匹配时是不区分大小写，可以使用`-iname`选项）

您当然可以使用 alias 设置别名来简化上述操作，但 shell 的哲学之一便是寻找（更好用的）替代方案。 记住，shell 最好的特性就是您只是在调用程序，因此您只要找到合适的替代程序即可（甚至自己编写）。

例如，[`fd`](https://github.com/sharkdp/fd) 就是一个更简单、更快速、更友好的程序，它可以用来作为`find`的替代品。它有很多不错的默认设置，例如输出着色、默认支持正则匹配、支持unicode并且我认为它的语法更符合直觉。以模式`PATTERN` 搜索的语法是 `fd PATTERN`。

大多数人都认为 `find` 和 `fd` 已经很好用了，但是有的人可能想知道，我们是不是可以有更高效的方法，例如不要每次都搜索文件而是通过编译索引或建立数据库的方式来实现更加快速地搜索。

这就要靠 [`locate`](https://man7.org/linux/man-pages/man1/locate.1.html) 了。 `locate` 使用一个由 [`updatedb`](https://man7.org/linux/man-pages/man1/updatedb.1.html) 负责更新的数据库（在大多数系统中 `updatedb` 都会通过 [`cron`](https://man7.org/linux/man-pages/man8/cron.8.html) 每日更新）而在数据库中进行搜索可比在硬盘搜索快多了。这便需要我们在速度和时效性之间作出权衡。而且，`find` 和类似的工具可以通过别的属性比如文件大小、修改时间或是权限来查找文件，`locate` 则只能通过文件名。[更详细的对比](https://unix.stackexchange.com/questions/60205/locate-vs-find-usage-pros-and-cons-of-each-other)

### VI.4 代码查找

很多时候我们需要找到写过的一段代码。为了实现这一点，很多类 UNIX 的系统都提供了 [`grep`](https://man7.org/linux/man-pages/man1/grep.1.html) 命令，它是用于对输入文本进行匹配的通用工具。

`grep` 有很多选项，这也使它成为一个非常全能的工具。其中我经常使用的有 `-C` ：获取查找结果的上下文（Context）；`-v` 将对结果进行反选（Invert），也就是输出不匹配的结果。举例来说， `grep -C 5` 会输出匹配结果前后五行。当需要搜索大量文件的时候，使用 `-R` 会递归地进入子目录并搜索所有的文本文件。

但是，我们有很多办法可以对 `grep -R` 进行改进，例如使其忽略`.git` 文件夹，使用多CPU等等。

因此也出现了很多它的替代品，包括 [ack](https://beyondgrep.com/), [ag](https://github.com/ggreer/the_silver_searcher) 和 [rg](https://github.com/BurntSushi/ripgrep)。它们都特别好用，但是功能也都差不多，我比较常用的是 ripgrep (`rg`) ，因为它速度快，而且用法非常符合直觉。例子如下：

```
# 查找所有使用了 requests 库的文件
rg -t py 'import requests'
# 查找所有没有写 shebang 的文件（包含隐藏文件）
rg -u --files-without-match "^#!"
# 查找所有的foo字符串，并打印其之后的5行
rg foo -A 5
# 打印匹配的统计信息（匹配的行和文件的数量）
rg --stats PATTERN
```

与 `find`/`fd` 一样，重要的是你要知道有些问题使用合适的工具就会迎刃而解，而具体选择哪个工具则不是那么重要

### VI.5 查找 shell 命令

`history` 命令允许您以程序员的方式来访问shell中输入的历史命令。这个命令会在标准输出中打印shell中的里面命令。如果我们要搜索历史记录，则可以利用管道将输出结果传递给 `grep` 进行模式搜索。 `history | grep find` 会打印包含find子串的命令。

对于大多数的shell来说，您可以使用 `Ctrl+R` 对命令历史记录进行回溯搜索。敲 `Ctrl+R` 后您可以输入子串来进行匹配，查找历史命令行。

反复按下就会在所有搜索结果中循环。在 [zsh](https://github.com/zsh-users/zsh-history-substring-search) 中，使用方向键上或下也可以完成这项工作。

`Ctrl+R` 可以配合 [fzf](https://github.com/junegunn/fzf/wiki/Configuring-shell-key-bindings#ctrl-r) 使用。`fzf` 是一个通用对模糊查找工具，它可以和很多命令一起使用。这里我们可以对历史命令进行模糊查找并将结果以赏心悦目的格式输出。

另外一个和历史命令相关的技巧我可以称之为**基于历史的自动补全**。这一特性最初是由 [fish](https://fishshell.com/) shell 创建的，它可以根据您最近使用过的开头相同的命令，动态地对当前对 shell 命令进行补全。这一功能在 [zsh](https://github.com/zsh-users/zsh-autosuggestions) 中也可以使用，它可以极大的提高用户体验。

你可以修改 shell history 的行为，例如，如果在命令的开头加上一个空格，它就不会被加进shell记录中。当你输入包含密码或是其他敏感信息的命令时会用到这一特性。 为此你需要在`.bashrc`中添加`HISTCONTROL=ignorespace`或者向`.zshrc` 添加 `setopt HIST_IGNORE_SPACE`。 如果你不小心忘了在前面加空格，可以通过编辑。`bash_history`或 `.zhistory` 来手动地从历史记录中移除那一项

### VI.6 查找文件夹

（比较深一些，慢慢学）

之前对所有操作我们都默认一个前提，即您已经位于想要执行命令的目录下，但是如何才能高效地在目录 间随意切换呢？有很多简便的方法可以做到，比如设置alias，使用 [ln -s](https://man7.org/linux/man-pages/man1/ln.1.html) 创建符号连接等。而开发者们已经想到了很多更为精妙的解决方案。

由于本课程的目的是尽可能对你的日常习惯进行优化。因此，我们可以使用[`fasd`](https://github.com/clvv/fasd)和 [autojump](https://github.com/wting/autojump) 这两个工具来查找最常用或最近使用的文件和目录。

Fasd 基于 [_frecency_](https://developer.mozilla.org/en-US/docs/Mozilla/Tech/Places/Frecency_algorithm) 对文件和文件排序，也就是说它会同时针对频率（_frequency_）和时效（_recency_）进行排序。默认情况下，`fasd`使用命令 `z` 帮助我们快速切换到最常访问的目录。例如， 如果您经常访问`/home/user/files/cool_project` 目录，那么可以直接使用 `z cool` 跳转到该目录。对于 autojump，则使用`j cool`代替即可。

还有一些更复杂的工具可以用来概览目录结构，例如 [`tree`](https://linux.die.net/man/1/tree), [`broot`](https://github.com/Canop/broot) 或更加完整的文件管理器，例如 [`nnn`](https://github.com/jarun/nnn) 或 [`ranger`](https://github.com/ranger/ranger)

## VII 小结

两篇笔记只是让我们初步窥见 bash 的功能以及可以怎么使用，但真正熟练地使用必然是伴随着大量的使用，以及在实际学习和工作中如何去发挥作用，这才应当是我们要关注的。

此外，missing-semester 本身留了[几个作业](https://missing-semester-cn.github.io/2020/shell-tools/#:~:text=nnn%20%E6%88%96%20ranger%E3%80%82-,%E8%AF%BE%E5%90%8E%E7%BB%83%E4%B9%A0,-%E4%B9%A0%E9%A2%98%E8%A7%A3%E7%AD%94)，现在来看难度不小，不妨下次复习来做？

## 参考文档