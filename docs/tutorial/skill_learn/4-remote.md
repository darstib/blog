---
comments: true
tags:
- notes
---

在现代软件开发环境中，远程服务器和分布式系统已成为常态。开发人员经常需要在本地机器与远程服务器之间传输文件、同步代码，或者直接在远程环境中工作。下面将介绍四种主要工具：`ssh`、`scp`、`sftp` 和 `rsync`。

## 远程连接与传输工具基础

### SSH：安全连接的基础

> [!wiki]+ [SSH](https://en.wikipedia.org/wiki/Secure_Shell)
>
> The Secure Shell Protocol (SSH Protocol) is a cryptographic network protocol for operating network services securely over an unsecured network. Its most notable applications are remote login and command-line execution.
>
> SSH was designed for [Unix-like] operating systems as a replacement for Telnet and unsecured remote Unix shell protocols, such as the Berkeley Remote Shell (rsh) and the related rlogin and rexec protocols, which all use insecure, plaintext methods of authentication, like passwords.
>
> 安全外壳协议（SSH 协议）是一种用于在不安全的网络上安全地操作网络服务的加密网络协议。它最显著的应用是**远程登录和命令行执行**,是为 [类 Unix] 操作系统设计的，作为 Telnet 和未加密的远程 Unix 外壳协议（如伯克利远程外壳（rsh）以及相关的 rlogin 和 rexec 协议）的替代品，这些协议都使用**不安全的明文认证方法，如密码**。

#### 安装与启动

- windows: [适用于 Windows 的 OpenSSH 入门](https://learn.microsoft.com/zh-cn/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell&pivots=windows-server-2025#enable-openssh-for-windows-server-2025)
- Linux: `sudo apt install openssh-client openssh-server`
- MacOS: （没记错终端中自带了）

查看 ssh 套件是否安装成功：`ssh -V`
查看服务是否运行：`ssh localhost` 即自己连接自己进行尝试。

[^1]: 有些教程给的是 `systemctl status sshd` `service status sshd` ，但是有些不支持 systemd，或者没有启动 systemd 而已，不能准确反映 ssh 服务开启与否。

> [!help]- 自连接练习使用 ssh
>
> 可能对于大多数人来说暂时并没有一个服务器可供连接，此时依旧可以依靠多个（子）系统去使得一个作为服务端，一个作为客户端：
>
> 选取一个类 Unix 系统运行类似于 `sudo systemctl start ssh` 开启 ssh 服务（windows 上可以运行 `netsh interface portproxy show all` 查看当前开放的端口，其他系统自查，此时我们就有了一个 "IP 为 127.0.0.1" 或者说叫 localhost 的主机，在另一个（子）系统中尝试即可。
>
> 参考：[SSH 访问 Windows 的 WSL2 Ubuntu](https://zhi.moe/post/access-into-wsl2-ubuntu-from-macos/)

#### 基本连接

这是最常用的命令，用于登录到远程服务器。

```bash
ssh [username@]remote_host # [表示可以省略]
```

- `username` 是在远程主机上的用户名。**如果省略** `username@`，SSH 会默认使用**当前登录客户端**的用户名尝试接。
- `remote_host` 是远程主机的 IP 地址或域名。

#### 指定端口

默认 SSH 协议使用 22 端口。如果远程服务器的 SSH 服务运行在其他端口（例如 2222），需要使用 `-p` 选项指定。

```bash
ssh username@remote_host -p 2222
```

#### 远程执行命令

可以在不登录交互式 Shell 的情况下，直接在远程主机上执行单个命令。

```bash
ssh username@remote_host command command_arguments
```

- 例如: `ssh user@myserver ls /home/user` 会列出远程服务器上 `/home/user` 目录的内容。
- 如果需要与远程命令进行交互（例如，运行一个需要输入的程序），可以使用 `-t` 选项强制分配一个伪终端 (tty)。

> [!attention]+
>
> ```sh
> $ ssh icsr ls ~
> ```
>
> 对于此处的 `~`，有时会以远程服务器中的 `~` 运行，有时以本地 `~` 代表的地址替换后运行，后者可能会出错因为与远程可能不一致；此时我们也可以用 `ssh icsr "ls ~"` 的方法解决。

#### 免密登录 (Passwordless Login via Keys)

为了安全和便捷，推荐使用 SSH 密钥对进行认证，避免每次连接都输入密码，同时也建议避免不安全的明文认证方法；这里简单探讨生成与 github 配对的 ssh 密钥

- **生成密钥对**:

密钥对的生成和管理使用 `ssh-keygen` 命令，详细用法可以见 `tldr ssh-keygen`，我们此处只解释生成：

```bash
# -t 选项指定使用的密钥算法，建议使用更现代的 ed25519 算法，如果不支持，rsa 也可以
ssh-keygen -t ed25519
# 或者使用 RSA
# ssh-keygen -t rsa -b 4096
```

这个命令会在的本地 `~/.ssh/` 目录下（如果不存在则创建，也可以使用 `-f` 选项指定生成的文件路径）生成两个文件：

- `id_ed25519` (或 `id_rsa`): 这是的**私钥 (Private Key)，极其重要，不能泄露**；
- `id_ed25519.pub` (或 `id_rsa.pub`): 这是的**公钥 (Public Key)**。可以自由安全地分享需要访问的服务上。

- **部署公钥**

最简单的方法是使用 `ssh-copy-id` 命令，它会自动将的公钥 (`~/.ssh/id_ed25519.pub` 或 `id_rsa.pub`) 追加到程主的 `~/.ssh/authorized_keys` 文件中。这个 `authorized_keys` 文件包含了所有**允许**使用对应私钥登录到该户账户的公列表。

```bash
ssh-copy-id username@remote_host
```

- `-i` 选项使用指定密钥文件: 如果的**公钥文件**[^2]不在默认位置或有特定名称（例如 ` my_special_key.pub`）或者我们现在有多对密钥，可以使用 ` -i ` 选项指定。

[^2]: 注意我们向服务器提交的是公钥。 (原文此处有误，已修正)

> [!help]- 为 github 配置 SSH 密钥
>
> 对于为 github 配置 SSH 密钥，需要登录账户后来到 [SSH keys](https://github.com/settings/keys)，点击右上角的 `New SSH key`：
>
> - Title: 起个名字以便你能认识它，一般建议写为来自哪里的/对应的私钥放在那里；
> - Key type: Authentication key 即可；
> - Key：将公钥内容[^3]复制进入即可，例如：
>
> [^3]: 可以看到由 “密钥类型” “B64 编码数据” “注释” 三部分组成。
>
> ```sh
> $ cat ~/.ssh/id_ed25519_github.pub
> ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ8NZClVJvicA06kElyaYhgdjjnFlB9b98pUPzcFLcwC qssgatcn@gmail.com
> ```

之后，当再次使用 `ssh username@remote_host` 连接时，远程主机会要求的客户端使用私钥进行身份验证，如果验证过，无需密码即可登录。同样的，如果私钥名字特殊或者有多个，也需要指定对应的 **私钥文件**。

```bash
ssh -i ~/.ssh/my_special_key username@remote_host
```

#### 配置文件 (~/.ssh/config)

对于经常链接的服务，我们经常使用的选项是基本相同的；如此我们可以在 `~/.ssh/config` 中以如下形式填写（注意，配置文件中的内容缩进不是必要的，但是推荐用于提高可读性）：

```config title="~/.ssh/config"
# darstib@ssh.github.com
Host github                                 # 定义一个配置块的“主机别名”
    User git                                # 默认用户名
    Hostname ssh.github.com                 # 服务器的实际地址
    PreferredAuthentications publickey      # 优先使用公钥验证
    IdentityFile ~/.ssh/id_ed25519_github   # 指定私钥文件地址
    Port 443                                # 指定端口

Host myserver                             # 另一个别名示例
    HostName 192.168.1.100
    User myuser
    Port 2222
    IdentityFile ~/.ssh/id_rsa_myserver
```

之后我们就可以直接使用 `ssh github` 或 `ssh myserver` 来替代一系列的选项了；使用 `ssh -T github` 检查：

```sh
$ ssh -T github
The authenticity of host '[ssh.github.com]:443 ([20.205.243.160]:443)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wxxxxxxxxxisF/zLDA0zPMxxxxxxCOqU.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[ssh.github.com]:443' (ED25519) to the list of known hosts.
Hi darstib! You've successfully authenticated, but GitHub does not provide shell access.
```

当然，如果在命令行中重新指定选项，命令行选项会覆盖配置文件中的设置。

> [!summary]- tldr ssh
>
> ```sh title="tldr ssh"
> $ tldr ssh
> ssh
>
> Secure Shell is a protocol used to securely log onto remote systems.
> It can be used for logging or executing commands on a remote server.
> More information: https://man.openbsd.org/ssh.
>
>  - Connect to a remote server:
>    ssh username@remote_host
>
>  - Connect to a remote server with a specific identity (private key):
>    ssh -i path/to/key_file username@remote_host
>
>  - Connect to a remote server using a specific [p]ort:
>    ssh username@remote_host -p 2222
>
>  - Run a command on a remote server with a [t]ty allocation allowing interaction with the remote command:
>    ssh username@remote_host -t command command_arguments
>
>  - SSH tunneling: [D]ynamic port forwarding (SOCKS proxy on localhost:1080):
>    ssh -D 1080 username@remote_host
>
>  - SSH tunneling: Forward a specific port (localhost:9999 to example.org:80) along with disabling pseudo-[T]ty allocation and executio[N] of remote commands:
>    ssh -L 9999:example.org:80 -N -T username@remote_host
>
>  - SSH [J]umping: Connect through a jumphost to a remote server (Multiple jump hops may be specified separated by comma characters):
>    ssh -J username@jump_host username@remote_host
> ```

一个可能用到但是上面没有展示出来的情况是：如果我们在使用公共的服务器，而需要访问诸如 Github 等网络不稳定的服务时，我们希望能够连接使用流量使用我们本地主机的代理服务，此时可以使用 `-R` 选项，具体而言：

```sh
$ ssh username@remote_host -R <remote_port>:localhost:<local_port>
# 这等价于在 ~/.ssh/config 中使用 `LocalForward <remote_prot> localhost:<local_port>`

# 之后在服务器上设置 http_proxy 即可
# export http_proxy=http://localhost:7890 export https_proxy=http://localhost:7890
```

> [!extra]- 记录一个便于在服务器上设置别名
> 
> ```sh title="~/.bashrc"
> # 建立反向 ssh 隧道
> # ssh 连接 host，并将服务器的 22 端口映射到 host 的 port
> function open_reverse_ssh() {
>    local port=${1:-host-port}
>    local user=${2:-host-username}
>    local host=${3:-host-ip}
>    ssh -R ${port}:localhost:22 ${user}@${host}
> }
> ```

### SCP：安全的文件复制

> [!info]+ SCP (Secure Copy Protocol)
> 
> SCP 是一种基于 SSH 协议在网络上的两台计算机之间传输计算机文件的协议。它提供与 `cp` (本地复制) 命令类似的功能，但增加了安全性和远程传输能力；他的使用方式和 `cp` 也是类似的。

#### 从本地上传文件到远程主机

将本地文件 `local_file.txt` 复制到远程主机的指定路径。

```bash
$ scp /path/to/local_file.txt username@remote_host:/path/to/remote_directory/
# 或者指定远程文件名
$ # scp /path/to/local_file.txt username@remote_host:/path/to/remote_file.txt
```

#### 从远程主机下载文件到本地

将远程主机上的文件 `remote_file.txt` 复制到本地当前目录或指定路径。

```bash
scp username@remote_host:/path/to/remote_file.txt /path/to/local_directory/
# 或者指定本地文件名
# scp username@remote_host:/path/to/remote_file.txt /path/to/local_file.txt
```

#### 传输目录 (使用 `-r` 选项)

递归地复制整个目录。

```bash
# 上传本地目录到远程
scp -r /path/to/local_directory username@remote_host:/path/to/remote_parent_directory/
# 下载远程目录到本地
scp -r username@remote_host:/path/to/remote_directory /path/to/local_parent_directory/
```

#### 指定端口 (使用 `-P` 选项)

如果远程 SSH 服务运行在非默认端口 (如 2222)。

```bash
scp -P 2222 /path/to/local_file.txt username@remote_host:/path/to/remote_directory/
```

#### 在两个远程服务器之间传输（`-3`）

```sh
scp -3 host1:path/to/remote_file host2:path/to/remote_directory
```

#### 其他常用选项

- `-p`: 保留原始文件的修改时间、访问时间和权限模式。
- `-C`: 启用压缩，可能在慢速网络上加快传输速度。
- `-l limit`: 限制使用的带宽，以 Kbit/s 为单位。

> [!summary]- tldr scp
>
> ```sh title="tldr scp"
> $ tldr scp
> scp
>
> Securely copy files between hosts.
> Uses SSH for data transfer, providing the same authentication and security.
> More information: https://man.openbsd.org/scp.
>
> - Copy a local file to a remote host:
>   scp path/to/local_file remote_host:path/to/remote_file
>
> - Copy a file from a remote host to a local directory:
>   scp remote_host:path/to/remote_file path/to/local_directory
>
> - [r]ecursively copy the contents of a directory from a remote host to a local directory:
>   scp -r remote_host:path/to/remote_directory path/to/local_directory
>
> - Copy a file between two remote hosts:
>   scp user1@remote_host1 :path/to/remote_file user2@remote_host2 :path/to/remote_directory
>
> - Copy a file using a specific port:
>   scp -P port path/to/local_file remote_host:path/to/remote_file
>
> - Copy a file using a specific private key for authentication:
>   scp -i ~/.ssh/private_key path/to/local_file remote_host:path/to/remote_file
>
> - Copy a file with [p]reserved modification and access times, and modes from the original file:
>   scp -p path/to/local_file remote_host:path/to/remote_file
> ```

### SFTP：安全的文件传输协议

> [!info]+ SFTP (SSH File Transfer Protocol)
> SFTP 是 SSH 协议的一个子系统，提供安全的文件访问、传输和管理功能。与 SCP 不同，它提供了一个交互式的命令行界面，允许用户浏览远程文件系统、执行文件操作（如重命名、删除、更改权限）等，类似于传统的 FTP，但全程通过 SSH 加密通道进行。

#### 连接到远程主机

启动 SFTP 会话。

```bash
sftp username@remote_host
# 如果需要指定端口
# sftp -P 2222 username@remote_host
```

连接成功后，提示符会变为 `sftp>`。

#### 在 SFTP 交互模式中使用命令

以下是一些常用命令 (在 `sftp>` 提示符下输入):

- **浏览与导航:**
    - `ls [path]`: 列出远程目录内容 (类似 `ls`)。
    - `pwd`: 显示远程当前工作目录。
    - `cd path`: 更改远程工作目录。
    - `lpwd`: 显示本地当前工作目录。
    - `lcd path`: 更改本地工作目录。
    - `lls [path]`: 列出本地目录内容。
- **文件传输:**
    - `get remote_file [local_file]`: 从远程下载文件。
    - `put local_file [remote_file]`: 上传本地文件到远程。
    - `get -r remote_directory [local_directory]`: 递归下载整个远程目录。
    - `put -r local_directory [remote_directory]`: 递归上传整个本地目录。
- **文件管理:**
    - `mkdir directory_name`: 在远程创建目录。
    - `rm file_name`: 删除远程文件。
    - `rmdir directory_name`: 删除远程空目录。
    - `rename old_name new_name`: 重命名远程文件或目录。
    - `chmod mode path`: 更改远程文件权限 (类似 `chmod`)。
    - `chown uid path`: 更改远程文件所有者 (类似 `chown`)。
    - `chgrp gid path`: 更改远程文件所属组 (类似 `chgrp`)。
- **其他:**
    - `help` 或 `?`: 显示帮助信息。
    - `!` : 退出到本地 shell 执行命令 (执行完后返回 SFTP)。
    - `!command`: 在本地 shell 执行指定命令。
    - `exit` 或 `quit` 或 `bye`: 关闭 SFTP 连接。

> [!summary]- tldr sftp
>
> ```sh title="tldr sftp"
> $ tldr sftp
> sftp
>
> Secure File Transfer Program.
> Interactive file transfer program, similar to `ftp`, which performs all operations over an encrypted `ssh` transport.
> See also `scp`.
> More information: https://man.openbsd.org/sftp.
>
> - Connect to a remote server:
>   sftp remote_host
>
> - Connect to a remote server specifying a user:
>   sftp user@remote_host
>
> - Connect to a remote server specifying a port:
>   sftp -P port remote_host
>
> - Connect using a specific private key for authentication:
>   sftp -i path/to/identity_file remote_host
>
> - Transfer remote file to the local machine:
>   get /path/to/remote_file
>
> - Transfer local file to the remote machine:
>   put /path/to/local_file
>
> - Transfer remote directory to the local machine recursively (use `-a` to preserve permissions and access times):
>   get -ar /path/to/remote_directory
>
> - Transfer local directory to the remote machine recursively (use `-a` to preserve permissions and access times):
>   put -ar /path/to/local_directory
> ```

简单来看 sftp 与 ssh + scp 差不多；现在许多客户端相关应用都支持 sftp 图形化交互更加便捷。

### Rsync：高效的文件同步

> [!info]+ Rsync (Remote Sync)
> Rsync 是一个强大的文件同步工具，以其高效的**增量传输算法**（delta algorithm）而闻名。它只传输源文件和目标文件中实际发生变化的部分，因此在同步大量数据、大文件或通过慢速网络连接时非常高效。常用于备份、镜像和文件分发。

#### 本地同步

rsync 可以在本地将 `source_directory` 的**内容**同步到 `destination_directory`。

```bash
rsync [options] source_directory/ destination_directory/
```

> [!attention]+ 注意尾部斜杠
>
> 路径末尾的斜杠 `/` 非常关键：
> 
> - `source_directory/` (有斜杠): 表示同步该目录下的**内容**到目标目录。
> - `source_directory` (无斜杠): 表示将 `source_directory` 这个**目录本身**（及其内容）复制到目标目录下，结果通常是 `destination_directory/source_directory/`。
>  
> 根据需要选择是否添加斜杠。

#### 通过 SSH 同步到远程主机

将本地目录同步到远程主机。

```sh
$ rsync [options] /path/to/local_source/ 
username@remote_host:/path/to/remote_destination/
```

#### 从远程主机同步到本地

将远程目录同步到本地。

```sh
$ rsync [options] username@remote_host:/path/to/remote_source/ /path/to/local_destination/
```

#### 常用选项

- `-a` (archive): 归档模式，**强烈推荐**。等同于 `-rlptgoD`，递归同步并保留大部分文件属性（符号链接、权限、时间戳、属组、属主、设备文件、特殊文件）。
- `-v` (verbose): 显示详细输出，了解正在发生什么。
- `-z` (compress): 在传输过程中压缩文件数据，节省带宽，但消耗 CPU。
- `-P`: 等同于 `--partial --progress`。显示传输进度 (`--progress`)，并允许断点续传 (`--partial`)。
- `-h` (human-readable): 以易读的格式（如 KB, MB）显示文件大小。
- `--delete`: **危险但常用**。使目标目录与源目录**严格**保持一致。如果源目录中没有的文件存在于目标目录，它会被从目标目录**删除**。
- `--exclude=PATTERN`: 排除符合模式的文件或目录；例如 `--exclude='*.log'`
- `--exclude-from=FILE`: 从指定文件中读取排除模式列表
- `-n` 或 `--dry-run`: 模拟执行，显示会进行哪些操作，但**不实际**执行任何文件传输或删除。在执行可能具有破坏性的命令（如带 `--delete`）之前建议使用
- `-e ssh_command`: 指定用于建立连接的 SSH 命令，常用于指定非标准端口或特定 SSH 选项

> [!help]- 使用 `--dry-run` 进行安全检查
>
> 在执行任何可能修改或删除文件的 `rsync` 命令（尤其是带 `--delete` 选项）之前，建议先添加 `-n` 或 `--dry-run` 选项运行一次，仔细检查输出，确保其行为符合预期。
>
> ```bash
> rsync -avznP --delete /local/source/ user@remote :/remote/dest/
> # 确认无误后，去掉 -n 执行实际同步
> rsync -avzP --delete /local/source/ user@remote :/remote/dest/
> ```

> [!summary]- tldr rsync
>
> ```sh title="tldr rsync"
> $ tldr rsync
> rsync
>
> Transfer files either to or from a remote host (but not between two remote hosts).
> Faster than `scp` because it uses a remote-update protocol which transfers only the differences between files.
> More information: https://download.samba.org/pub/rsync/rsync.1.
>
> - Transfer files from local to remote host in [a]rchive mode ([r]ecursive, saves [p]ermissions, symbolic [l]inks, file [t]imes, [g]roups, [o]wner):
>   rsync -a path/to/source_directory username@remote_host :path/to/destination_directory
>
> - Transfer files from remote host to local in [a]rchive mode:
>   rsync -a username@remote_host :path/to/source_directory path/to/destination_directory
>
> - Transfer files in [a]rchive mode showing [P]rogress and using [z] compression:
>   rsync -azP path/to/source_directory username@remote_host :path/to/destination_directory
>
> - Transfer directory contents, but not the directory itself, using archive mode and [v]erbose output:
>   rsync -av path/to/source_directory/ username@remote_host :path/to/destination_directory
>
> - Transfer files using a specific port for ssh connection:
>   rsync -a -e 'ssh -p port' path/to/source_directory username@remote_host :path/to/destination_directory
>
> - Transfer files in archive mode, but don't copy files which are newer on the destination:
>   rsync -au path/to/source_directory username@remote_host :path/to/destination_directory
>
> - Transfer files in archive mode, but delete files on the destination that don't exist on the source:
>   rsync -a --delete path/to/source_directory username@remote_host :path/to/destination_directory
>
> - Transfer files, excluding specific files or directories found in the specified file:
>   rsync -a --exclude-from 'path/to/exclude.txt' path/to/source_directory username@remote_host :path/to/destination_directory
> ```

## 工具比较与选择

选择合适的工具取决于具体的需求：

| 工具      | 主要功能      | 适用场景           | 特点                         |
| :------ | :-------- | :------------- | :------------------------- |
| `ssh`   | 远程登录与命令执行 | 需要远程管理服务器、执行命令 | 安全、基础、提供交互式 Shell、可隧道传输    |
| `scp`   | 安全文件复制    | 简单、一次性的文件或目录传输 | 类似 `cp` 命令，易于使用，功能相对基础     |
| `sftp`  | 安全文件传输协议  | 需要交互式管理远程文件系统  | 类似 FTP，可浏览、管理文件，安全         |
| `rsync` | 高效文件同步    | 备份、镜像、同步大量或大文件 | 增量传输、高效、选项丰富、可保持属性、可删除多余文件 |

## 在 VSCode 中使用远程连接与传输工具

### Remote-SSH 扩展

> [!quote]+ [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
>
> The **Remote - SSH** extension lets you use any remote machine with a SSH server as your development environment. This can greatly simplify development and troubleshooting in a wide variety of situations.  
> 
> Remote - SSH 扩展允许您使用任何具有 SSH 服务器的远程机器作为您的开发环境。这可以在各种情况下极大地简化开发和故障排除。
> 
> 具体使用见[使用 SSH 进行远程开发](https://vscode.js.cn/docs/remote/ssh)。

#### 安装与配置

- 在 VSCode 扩展市场 (侧边栏图标或 `Ctrl+Shift+X`) 搜索并安装 "Remote - SSH"
	- 如果是 windows 还可以安装 “WSL” 扩展；
- 安装后，点击 VSCode 左下角的绿色 `><` 图标，或按 `F1` (或 `Ctrl+Shift+P`) 打开命令面板，输入并选择 "Remote-SSH: Connect to Host..."：
    - 选择已在 `~/.ssh/config` 文件中配置的主机别名。
    - 选择 "+ Add New SSH Host..." 并按提示输入 `ssh username@remote_host [-p port]` 命令，VSCode 会自动帮你添加到 `~/.ssh/config` 文件。
    - 直接输入 `ssh username@remote_host [-p port]` 连接。

#### 远程开发体验

- 连接成功后，VSCode 窗口会重新加载并连接到远程环境。
- **文件资源管理器**: 点击侧边栏的文件图标，选择 "Open Folder..."，输入或浏览远程服务器上的路径。之后你可以像编辑本地文件一样编辑远程文件，保存即同步。
- **扩展兼容**: 大多数 VSCode 扩展 (GitLens, Docker, linters, debuggers 等) 都可以在远程环境无缝工作。
- **端口转发**: 可以通过命令面板 ("Remote-SSH: Forward Port from Active Host...") 轻松设置端口转发，方便访问远程服务。

> [!extra]- 端口转发
> 
> 关于端口转发详见
> 
> - [SSH服务原理和使用技巧](https://www.escapelife.site/posts/e2e78d82.html)
> - [SSH Tunneling: Examples, Command, Server Config](https://www.ssh.com/academy/ssh/tunneling-example)
> - [端口转发](https://wangdoc.com/ssh/port-forwarding)
> 
> 一个可能遇到的需求是在组内共用服务器上需要访问 github 等资源时需要代理，具体可以参考[再探 ssh 和 VScode（（双重）远程转发和本地转发）](https://www.cnblogs.com/coldchair/p/18526990)。

### SFTP 扩展

> [!info]+ SFTP 扩展
>
> 在 Remote-SSH 扩展出现之前，这类 SFTP 扩展很流行，用于直接在 VSCode 中与远程服务器同步文件。现在 Remote-SSH 通常提供了更无缝的体验，但 SFTP 扩展在某些特定场景下（如仅需文件同步而非完整远程开发环境）仍有其用武之地。

#### 安装与配置

- 在扩展市场搜索并安装所需的 SFTP 扩展（如 "SFTP by Natizyskunk"）。
- 打开命令面板 (`Ctrl+Shift+P`)，运行 "SFTP: Config" 命令。这会在当前工作区的 `.vscode` 目录下创建一个 `sftp.json` 配置文件。
- 编辑 `sftp.json`，填写必要的连接信息：

```json title=".vscode/sftp.json"
{
    "name": "My Remote Server", // 连接名称
    "host": "your_remote_host",  // 服务器地址
    "protocol": "sftp",         // 协议
    "port": 22,                 // SSH/SFTP 端口
    "username": "your_username", // 用户名
    // "password": "your_password", // 不推荐！优先使用 privateKey
    "privateKeyPath": "/path/to/your/private/key", // 私钥文件路径 (推荐)
    "passphrase": "your_key_passphrase", // 如果私钥有密码
    "remotePath": "/path/to/remote/project/root", // 远程项目根目录
    "uploadOnSave": true,       // 保存本地文件时自动上传
    "downloadOnOpen": false,     // 打开本地文件时自动从远程下载 (谨慎使用)
    "ignore": [                 // 忽略同步的文件/目录
        ".vscode",
        ".git",
        "node_modules"
    ]
    // ... 更多选项
}
```

#### 文件同步操作

- **自动同步**: 如果 `uploadOnSave` 设置为 `true`，保存本地文件会自动上传到 `remotePath` 下对应的位置。
- **手动同步**: 在文件资源管理器中右键点击文件或目录，选择 SFTP 相关的上传/下载/同步选项。也可以通过命令面板执行 SFTP 命令。

## 进阶技巧与便捷工具

### reync+cron 自动化同步

使用 rsync 

```sh
$ rsync -av --delete/source/dir/ /target/dir/
```

- `-a`：归档模式，保留属性
- `-v`：详细输出
- `--delete`：目标删除源无的文件，实现镜像同步

使用 `cron` 定时任务在后台自动执行：

```sh
$ crontab -e

0 2 * * * /usr/bin/rsync -av --delete /source/dir/ /target/dir/ >> /var/log/rsync_cron.log 2>&1
```

> [!question]+ 能否实现实时同步？
> 
> cron 表达式 `* * * * *` 是 `分钟 小时 日 月 星期几`，即粒度最小也为分钟；可以参考 [通过 rsync 和 cron 实现日志文件的准实时同步](https://alphahinex.github.io/2020/08/09/rsync-and-cron/ "通过 rsync 和 cron 实现日志文件的准实时同步")。

> [!attention]+ Cron 与 SSH
> 
> 在 Cron 任务中使用 SSH/SCP 时，需要确保 SSH 连接可以**非交互式**地建立（即不需要输入密码或私钥密码）。通常这意味着使用无密码的 SSH 密钥，或者配置好 `ssh-agent` (但这在 cron 环境中较复杂)。

### SSH 代理 (`ssh-agent`)

`ssh-agent` 是一个在后台运行的程序，它可以缓存解密后的私钥，这样你只需要在添加密钥到 agent 时输入一次密码，之后在该 agent 运行期间，所有 SSH 连接都可以自动使用缓存的密钥，无需再次输入密码。

```bash
# 启动 ssh-agent (通常在登录时自动启动，或按需启动)
eval $(ssh-agent -s)
# > Agent pid 12345

# 添加私钥到 agent (会提示输入私钥密码，如果设置了)
ssh-add ~/.ssh/id_xxx

# 查看已添加的密钥
ssh-add -l

# 删除所有密钥
# ssh-add -D
```

### 便捷工具与替代方案

#### 图形化工具

- [24款好用的SSH客户端工具推荐，快速连接服务器的工具](https://www.wangdu.site/software/bianchengkaifa/1263.html)
- 我了解的有（其他供大家自己据上面的文章探索）：
	- [termius](https://termius.com/)（跨平台）
		- 界面美观，支持配置文件导入，拖拽式 SFTP；
		- 但是是收费，且同步数据理论上存在一定的风险（因为存储了 ssh 密钥）
		- [入门教程](https://guopengzhen.com/%E7%BF%BB%E8%AF%91/14555/)
	- [MobaXterm](https://mobaxterm.mobatek.net/) (Windows)
		- 一款适用于 Windows 的增强型远程连接工具，集 **SSH 客户端、SFTP 文件传输、X11 图形转发、Unix 命令工具** 于一体，支持多协议（RDP/VNC/FTP/串口等）
		- 点击左上角 session，随后选择协议填写连接即可
			<div style="text-align: center;"><img src="https://raw.githubusercontent.com/darstib/public_imgs/utool/2505/05_250505-115401.png" alt="" style="width: 60%;"><p></p></div>
		- [详细使用教程](https://zhuanlan.zhihu.com/p/61013117)

#### 替代方案 (特定场景)

- [Syncthing](https://syncthing.net/): 开源的点对点 (P2P) 文件同步工具，无需中心服务器，在多台设备间自动同步文件。
- [Rclone](https://rclone.org/): "云存储的瑞士军刀"。支持在数十种云存储服务（S3, Google Drive, Dropbox 等）和本地文件系统之间同步、复制文件，也支持 SFTP。命令行工具，功能极其强大。
- [duplicati](https://duplicati.com/): 基于 rsync / GPG 的加密增量备份工具，适合创建安全的异地备份。

### SSHFS 挂载:

- 项目地址 [sshfs](https://github.com/libfuse/sshfs)
- 在本地系统安装 `sshfs`；
- 使用命令将远程目录挂载到本地：

```bash
# 先创建本地挂载点（或者可以统一挂载在 /mnt/ 下）
$ mkdir ~/remote_mountpoint
# 挂载远程目录
$ sshfs username@remote_host:/path/to/remote/directory ~/remote_mountpoint
```

> [!attention]+
> 
> - SSHFS 的性能可能不如原生远程编辑 (Remote-SSH) 或专门的文件传输工具，尤其是在网络延迟较高或文件数量巨大的情况下。
> 
> - 使用完毕后记得卸载：具体命令因系统而异。

### fastfetch 掌握信息

请看 VCR：[给你的 SSH 登录加上 fastfetch](https://heap.45gfg9.net/t/7a305569871e/)

## 小结

> [!tip]+ 简单选择指南
> 
> - 只想登录操作服务器？ -> `ssh`
> - 快速传几个文件/小目录？ -> `scp`
> - 想在服务器上像用文件管理器一样操作？ -> `sftp` (命令行) 或图形化工具 (如 FileZilla, WinSCP, VSCode Remote-SSH)
> - 需要同步、备份、或者传输大文件/大量文件，追求效率？ -> `rsync`
> - 要在远程服务器上写代码/开发？ -> VSCode + Remote-SSH 插件

扩展阅读：[实验室服务器普通用户使用指南](https://zhuanlan.zhihu.com/p/668805702)

## 参考资料

- [SSH 教程 - 网道 (WangDoc)](https://wangdoc.com/ssh/)
- [在 HTTPS 端口使用 SSH - GitHub Docs](https://docs.github.com/zh/authentication/troubleshooting-ssh/using-ssh-over-the-https-port)
- [OpenSSH Manual Pages (官方文档)](https://man.openbsd.org/sshd_config.5)
- [Visual Studio Code - SFTP Extension Using SSH Authentication](https://stackoverflow.com/questions/46852476/visual-studio-code-sftp-extension-using-ssh-authentication)
