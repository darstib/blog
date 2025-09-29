---
comments: true
date: 2024-08-13
tags:
- begin
---

***

这里主要介绍的是我对 chrome browser 的一些插件和设置分享；edge 上可能也有同名插件，但是下面提供的链接都是 chrome store ，自备魔法，或者自己找渠道试试。

> chrome_begin 这个名字取得有点唬人（主要是比较适合加入 begin 系列）。

<!-- more -->

## I Extensions

- [bilibili 哔哩哔哩下载助手](https://chromewebstore.google.com/detail/bilibili%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%E4%B8%8B%E8%BD%BD%E5%8A%A9%E6%89%8B/bfcbfobhcjbkilcbehlnlchiinokiijp)
    - 顾名思义。
- [Dark Reader](https://chromewebstore.google.com/detail/dark-reader/eimadpbcbfnmbkopoojfekhnkhdbieeh)
    - 比较好的将所有 Light 界面变为 Dark 模式，深夜降低屏幕亮度。
- [Kimi 浏览器助手](https://chromewebstore.google.com/search/Kimi%20%E6%B5%8F%E8%A7%88%E5%99%A8%E5%8A%A9%E6%89%8B)
    - Kimi 官方 2024/07 出台的插件；
    - 重点在于其能够划词/句，**并结合上下文** 解释。
- [Page Sidebar | Open any page in side panel](https://chromewebstore.google.com/search/Page%20Sidebar%20%7C%20Open%20any%20page%20in%20side%20panel)
    - chrome 没有 edge 的网页分屏功能，这个插件可以一定程度上平替；
- ~~[VertiTab - Vertical Tabs in Side Panel](https://chromewebstore.google.com/detail/vertitab-vertical-tabs-in/chejfhdknideagdnddjpgamkchefjhoi)~~
	- [Tab Groups Extension](https://chromewebstore.google.com/detail/tab-groups-extension/nplimhmoanghlebhdiboeellhgmgommi) 的自动分组嫩巩固满足我的需求了
	- 垂直便签栏（虽然 windows 上由于上边无法收起，mac 上可以自动回缩，所以基本没怎么用）
	- 标签页自分组（多种自分组模式，我比较喜欢按域名划分，经过反馈也是支持了多种匹配模式）
	- 快照生成（保留自己的工作状态）
- 广告拦截器
    - 个人评价一个广告拦截器主要看：
        - 能否很好地拦截广告，有些插件你不付费故意给你放出一些来；
        - DevTools 中的 Console 是否爆出许多错误；这一点 AdGuard 做的稍好一些。
    - [AdGuard](https://chromewebstore.google.com/detail/adguard-%E5%B9%BF%E5%91%8A%E6%8B%A6%E6%88%AA%E5%99%A8/bgnkhhnnamicmpeenaelnjfhikgbkllg)
    - [广告拦截器 - 1Block](https://chromewebstore.google.com/detail/%E5%B9%BF%E5%91%8A%E6%8B%A6%E6%88%AA%E5%99%A8-1block/jajikjbellknnfcomfjjinfjokihcfoi)
- ~~[沉浸式翻译 - 网页翻译插件 | PDF翻译 | 免费](https://chrome.google.com/webstore/detail/bpoadfkcbjbfhfodiogcnhhhpibjhbnh)~~
	- 2025 年 8 月被爆出某种程度上泄露了用户隐私，改用一个开源替代：[Kiss-translator](https://github.com/fishjar/kiss-translator)
    - 使用谷歌/微软/免费 llm 等进行翻译，可以自己接入主流模型的 api，个人使用前两个就够了；
    - 主要是可以对照翻译，即保留了原文，且可以设置译文格式，体验相对更好
        - ![|350](attachments/chrome_begin.png)
- [Tampermonkey](https://chromewebstore.google.com/detail/dhdgffkkebhmkfjojejmpbldmpobfkfo)
    - 用于执行众多脚本，网上介绍甚多，在此略过。
- [Tabliss](https://chromewebstore.google.com/detail/tabliss-a-beautiful-new-t/hipekcciheckooncpjeljhnekcoolahp)
    - 一个不错的高度可自定义标签页，简洁好看；
    - 比较奇怪的是，这个内存消耗居然只有 chrome 原生的一半😅。
- [Simple Outliner / 智能网页大纲](https://chromewebstore.google.com/detail/simple-outliner-%E6%99%BA%E8%83%BD%E7%BD%91%E9%A1%B5%E5%A4%A7%E7%BA%B2/ppdjhggfcaenclmimmdigbcglfoklgaf)
	- 依据文章内容自动生成可跳转目录/大纲，阅读知乎等不自动生成目录的长文友好。
- [GitZip for github](https://chromewebstore.google.com/detail/gitzip-for-github/ffabmkklhbepgcgfonabamgnfafbdlkn)
	- 方便下载 github 上的部分文件。
- [Ginsmooc](https://github.com/ginnnnnncc/GinsMooc)

## II setting

- chrome://flags/#enable-tab-audio-muting
    - 单独控制不同标签页声音；
- IP 变动导致的重定向/语言问题
	- [preferences](https://www.google.com/preferences?lang=1&prev=https://www.google.com/preferences)
		- 修改 “搜索结果区域” 为新加坡（几乎唯一一个中英文都为官方语言的国家）
	- [popups](chrome://settings/content/popups)
		- 拒绝部分网站自动重定向