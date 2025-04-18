---
comments: true
---

# Skill_learn

## 本期课程介绍

这里是浙江大学 2024-2025 春夏学期计算机学院朋辈辅学**技能拾遗**课程主页，后续内容将在上课前更新。

### 课程安排

考虑到夏学期尤其是接近期中/末时，大家（包括我自己）都非常忙，~~大家也忙着补专业课的朋辈辅学[^4]~~，所以我计划时间安排如下（均在周五 18:30 开始，预计时长 90-120 mins）：

[^4]: 根据往期数据，期末复习的观看量是前瞻的 3-4 倍🤔。

|         上课时间          |    主题     |                                                     内容                                                     |
| :-------------------: | :-------: | :--------------------------------------------------------------------------------------------------------: |
| [3.21](1-terminal.md) |   终端指南    |                                     **Linux shell** + Windows Terminal                                     |
|   [3.28](2-git.md)    | 版本控制与简单开发 |                                   Git + **Github** + Action[ + License]                                    |
|       4.18[^1]        |  文本排版工具   |                                         **Markdown** + [  + Word]                                          |
|     4.25/5.2[^1]      | + 集成开发环境  | [LaTeX](https://cn.overleaf.com/project/)+[Typst](https://typst.app/project/)[ + Visual Studio Code (vsc)] |
|         5.16          |  远程连接与传输  |                                        **ssh** + scp + sftp + rsync                                        |
|         5.30          |  奇怪知识串讲   |                                             妙妙小工具 / 小网站 / 其他？                                              |

[^1]: 作为动态调整部分。

显然 <u>每一周的内容都很多</u> ，但是其中注意到我们的 4 月命途多舛（前有清明节，中有期中周，后有劳动节），我们在前面如果没能够讲完/讲清的部分，会在 4 月进行动态调整。

> [!quote]+ 下面是往期技能拾遗课程中推荐学习但本期未提及/细讲的内容
>
> - [24-春夏技能拾遗课程](https://raw.gitmirror.com/darstib/public_imgs/utool/2503/18_jnsy-sp24.png) （均在内部钉钉群）
> 	- [Docker基础入门](https://n.dingtalk.com/dingding/live-room/index.html?roomId=CUL5K7UaWcKkWNLv&liveUuid=f2742c60-9a9e-4468-b151-d0523d90da73) by [@Foggy-whale](https://github.com/Foggy-whale)
> 	- [makefile](https://n.dingtalk.com/dingding/live-room/index.html?roomId=Ssm0CtL4q7lW1y5U&liveUuid=1465a654-47ba-48af-91ba-d1b3d32e14ba) by [@Foggy-whale](https://github.com/Foggy-whale) or [Makefile 光速入门](https://siyuanblog.cn/archives/makefile)
> 	- [正则表达式](https://n.dingtalk.com/dingding/live-room/index.html?roomId=iJaprRX0kVlR8bi6&liveUuid=00fc196f-b10f-402d-a5a4-7c96549effb8) by [@Foggy-whale](https://github.com/Foggy-whale)
> 	- [shell script](https://n.dingtalk.com/dingding/live-room/index.html?roomId=DNzTTQFbGdVos1LD&liveUuid=3b20f813-eb26-4f2f-9699-207d8bd17257) by [@Foggy-whale](https://github.com/Foggy-whale)
> - [23-秋冬技能拾遗课程](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-fall-ckc/#/)
> 	- [lec6：网络 / 网站基础知识概述](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-fall-ckc/lec6/) by [@45gfg9](https://github.com/45gfg9)
> - [23-春夏技能拾遗课程](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-spring-cs/#/)
> 	- [lec2：Git/GitHub 基础介绍](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-spring-cs/lec2/) | [BV1og4y1u7XU](https://www.bilibili.com/video/BV1og4y1u7XU/)
> 	- [lec4：LaTeX 排版简要介绍](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-spring-cs/lec4/) | [BV12k4y1s7Y3](https://www.bilibili.com/video/BV12k4y1s7Y3/)
> - [《Linux101》](https://101.lug.ustc.edu.cn/)
> 	- （乱入）中国科学技术大学 Linux 用户协会出品

### 课程声明

出于个人风格并考虑**大家的需求**（有需求请大胆提出，评论区与钉钉均可），请容许我简单浪费大家几分钟提出几点建议和声明：

> [!info]- 本期课程原则
>
>> [!quote]- 君子生非异也，善假于物也
>>
>> 精通一些工具不仅可以帮助大家更快的使用工具完成任务，并且可以帮助解决在之前看来似乎无比复杂的问题；但是我本人其实主张根据需求找合适的工具，而本期技能拾遗的目的是指导那些大家都应该掌握的工具的基本使用，同时简单介绍大家以后很可能会使用到的工具以及相关的作用。
>
>> [!quote]- 精工巧具之大观也，前人之述备矣
>> 
>> 这门课叫 “技能拾遗”，但前人似乎已经帮大家捡的差不多了，我该帮大家捡点什么呢？我不认为我能够讲得比前人更好，所以对于 pbfx 前面几期课程已经讲解得非常详细的内容，我打算以 cheatsheet+demo 的形式讲解，**以本科阶段够用为主**，**不会深入**，并尽量留下我认为的“前人之述”；同时横向比较多个工具，由同学们自己选择最后使用什么、掌握什么。
>
>> [!quote]- 常用者求专精，备预者取通广
>>
>> 根据需求寻找效果类似的工具时，我主张：
>> 
>> - 常用的工具找最喜欢的
>> - 不常用工具找最泛用的
> 
>> [!quote]- [转录异常，难免故障](https://scp-wiki-cn.wikidot.com/transcription-malfunctioned-hub)
>> 
>> 意思是我不过将知识技能整理、搬运，没有多少自己的产出，且知识转移转移过程中难免小问题，请多担待。
> 
>> [!wiki]- [知识诅咒](https://en.wikipedia.org/wiki/Curse_of_knowledge)
>> 
>> The curse of knowledge, also called the curse of expertise or expert's curse, is a cognitive bias that occurs when a person who has specialized knowledge assumes that others share in that knowledge.
>> 
>> 意思是当一个人拥有专门知识时，会假设他人也共享这种知识；很有可能我在讲解时假设大家掌握了一些知识，或者有了一些思维（例如如果对 html+css 较为了解，其他文本标记语言上手也是非常快的），我会尽量使用 `prerequisite` 进行声明，并尽快更新在对应内容前方。
>>  
>>> [!prerequisite]

总之，我不希望重复造轮子；或者说我希望能够覆盖到更浅但更多的内容供同学们学习，希望对此不能接受的同学能够尽早降低预期以免浪费您宝贵的时间；同时能力有限，可能有误，希望不会被骂挂 98 😭。

## 关于课程展开

### 关于课程反馈

- 有**不理解之处可在直播时提出**，在一块内容讲解完成后再统一解释[^2]；
- 有**建议请在钉钉群提出**，可以反映出总体对这个建议的支持度；
- 有**意见/明显讲错的地方请钉钉私聊**，如确实存在我会在群内对讲解进行纠正；
- 有错字或**其他任何理由可在对应内容下方评论区留言**，感谢大家的支持！

[^2]: 基于直播延迟和课程流畅性，不太可能看到了就进行解释。

### 关于问题提出

一些同学可能在安装工具/配置环境时会遇到这样那样的问题，理论上来说我们这门课不提供相关支持，但是我不反对对相关问题进行**尝试性**的私下解答；但是期望先按照下面顺序进行：**将有效信息在浏览器查询 > 将有效信息询问 LLM > 查询官方相关文档/issues > 将有效信息向我展示**[^3]。询问浏览器/LLM 其实本身就应该和询问人一样的提供足够的信息，[一项研究](https://arxiv.org/abs/2402.14531) 表明，对 LLM 礼貌其实也一定程度上影响了回答的质量，询问人获得的回答质量受到影响当然是更大的。

[^3]: 实话说，按照这个过程，也到不了最后一步；真到了最后一步，问题能被我解决的可能性也大大降低。

> [!question]- 什么是有效信息？
>
> 我认为也不必搬出老生常谈的[提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way)了，一个简单的学习方式是看那些[大型项目的 issue 模板](https://github.com/freeCodeCamp/freeCodeCamp/tree/main/.github/ISSUE_TEMPLATE)是怎样的；当然不必那么死板，重要的是 **“问题描述/操作复现”+“出现的报错信息”**，可能还需要环境版本等；我也许可以从你的截图中推断出，所以截图建议全面，但同时将重点标出。

### 关于一些读法

> [!tip]-
>
> 在搜索引擎中搜索 "pronunciation of xxx" 或者在 [forvo](https://forvo.com/)、[wiktionary](https://en.wiktionary.org/wiki/Wiktionary:Main_Page) 等网站搜索。

| 单词     | 音标                                                  | 简单解释                                                                  |
| ------ | --------------------------------------------------- | --------------------------------------------------------------------- |
| unix   | [/ˈjuːnɪks/](https://forvo.com/word/unix/)          | 一种多用户、多进程的计算机操作系统                                                     |
| linux  | [/ˈlɪnəks/](https://en.wiktionary.org/wiki/Linux)   | 一种开源的类 Unix 操作系统                                                      |
| ubuntu | [/ʊˈbʊntuː/](https://zh.wikipedia.org/zh-cn/Ubuntu) | 一个 [Linux 发行版](https://101.lug.ustc.edu.cn/Ch01/#linux-distributions) |
| github | /ˈɡɪthʌb/                                           | 一个用于托管和管理Git代码的在线平台                                                   |
| latex  | /ˈleɪtɛk/                                           | 一种排版系统，常用于学术文档                                                        |
| typst  | [/taɪpst/](https://typst.app/legal/brand/)          | 一种基于文本的排版工具                                                           |
| rsync  | /ˈɑːr.sɪŋk/                                         | 文件同步和备份工具                                                             |
