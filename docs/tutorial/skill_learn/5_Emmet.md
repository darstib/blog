---
comments: true
date: 2024-04-05
tags:
- blog
- web
- note
---

***

很多人想要搭建自己的一个网站，哪怕只是一个[很简单的、只有一个主要文件的页面](https://darstib.github.io/)。

首先可以看看 [Web 入门](https://developer.mozilla.org/zh-CN/docs/Learn/Getting_started_with_the_web)。但是纯手动写一整个网页会累死的，那么多 `< / >` 都够喝一壶的了，于是有了 **[Emmet](https://emmet.io/)** 语法。简而言之，Emmet 是 html 等语法的缩写格式，可以显著提高我们写简单前端 html 的速度。

## 介绍

对于 VScode 用户，"Support for [Emmet](https://emmet.io/) snippets and expansion is built right into Visual Studio Code, **no extension required**." 也就是说我们开盒即用，至多也就需要如下设置

> 如果要使用 Tab 键展开 Emmet 缩写，请在 `settings.json` 添加以下设置：

```json
"emmet.triggerExpansionOnTab": true
```

> 此设置允许在文本不是 Emmet 缩写时使用 Tab 键进行缩进。

## 使用

我们先主要介绍在 html 中的使用；请注意，需要手动输入，并且需要在 **html** 文件中，直接复制粘贴或者是其他文件种类中不能触发 emmet，触发后 `Tab` 键即可将当前选中输入。

### 符号

#### `!` 

只需一个 `!` 而后 `Tab` 即可构建一个大致的框架！

![|350](attachments/2-1%20Emmet.png)

下面是进阶用法，相信如果学习过 Tree 这个数据结构不难理解。

#### Multiplication: `*`

重复性标签（点名 `<li></li>`）太多了？使用乘号 `*` 是很符合我们认知的，将在下面一起演示。

#### child: `>`

我们使用 `>` 来表示标签之间的从属关系，例如：

```txt
nav>ul>li*5
```

![|250](attachments/2-1%20Emmet-1.png)

#### Item numbering: `$`

可以发现 `*` 只能重复，那我想来个 item 1、item 2 等等咋办？用 `$`

- `$` 用于编号，多个可表示多位数，自动补 0
- `@` 

```txt
ul>li.item$@3*5
```

#### Sibling: `+`

```txt
div+p+bq
```

![|350](attachments/2-1%20Emmet-2.png)

#### Climb-up: `^`

当嵌套使用的时候会有所混淆。

例如，我们想要让 p 和 bp 是 sibling 而 span 和 em 是 p 的 children 

难道我们这样写吗:

```txt
bq+q>span+em
```

![|350](attachments/2-1%20Emmet-5.png)

那我想要 q 在 bq 前面（多事的甲方）怎么办？

于是Emmet 为我们提供了一种更加方便的做法，即使用 `^` 来“向上爬”！

```txt
div+div>p>span+em^bq
```

![|350](attachments/2-1%20Emmet-4.png)

#### Grouping: `()`

当然，使用括号表示“一家子人” 是更加比较符合我们认知的行为

```txt
div>(header>ul>li*2>a)+footer>p
```

![|350](attachments/2-1%20Emmet-6.png)

#### Text: `{}`

在上面我们使用了 `<a>` 这个标签，我们知道一般需要在中间添加显示的文本，我们可以用 `{}` 包裹文本自动填入其中，当然 `<p>` 这类标签都能使用

```txt
p>{Click }+a{here}+{ to continue}
```

![|350](attachments/2-1%20Emmet-7.png)

#### ID and CLASS attributes `# .`

我们习惯于使用 `#` 来表示标题等（如 markdown）使用 `.` 来表示类成员（如 c++）

Emmet 引入了这些用法：

```txt
form#search.wide.other_class
```

![|350](attachments/2-1%20Emmet-8.png)

#### Custom attributes `[]`

对于其它的一些属性，可以用 `[]` 包裹实现

```txt
td[rowspan=2 colspan=3 title]
```

![|350](attachments/2-1%20Emmet-10.png)

#### Implicit tag names

最为厉害的是，由于很多时候我们标签嵌套或者是某些类主要出现在特定标签内，所以：

![|350](attachments/2-1%20Emmet-9.png)

#### Lorem Ipsum

在前端测试时常常会使用 Lorem Ipsum 作为文本，它们同样可以放入 Emmet 中使用

```txt
p*4>lorem
```

```html
    <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Dolorum nobis natus nulla, quam quia eum atque neque rem sapiente facilis, eaque eos laudantium distinctio a est qui. Veritatis, pariatur! Aperiam.</p>
    <p>Quod voluptatibus nam quidem perferendis obcaecati enim culpa laborum modi voluptatum? Incidunt, aliquid, quod nostrum dolorem ipsam libero eum ab, corrupti nisi sint excepturi ipsum veniam quisquam officiis. Magnam, dolor!</p>
    <p>Inventore, iste ea nemo molestias quisquam velit, facilis itaque repellat eos esse, sapiente ab. Blanditiis earum, aliquam corrupti quasi eum dolorem ipsa delectus ratione. Quasi consequatur ipsam corporis. Exercitationem, commodi.</p>
    <p>Quas voluptatem mollitia omnis corporis tempora adipisci suscipit maxime molestias in amet, ipsam consequuntur qui natus, earum nulla delectus, accusantium nisi ut odit explicabo alias commodi exercitationem? Iste, explicabo officia?</p>
```

### 缩写

那看了这么多，发现有些情况下使用了缩写（如用 bq 表示了 blockquote）还有哪些缩写？在

**Emmet document** 中进行了详细讲解，见参考文档。

个人认为无需记忆，需要时再搜索，或者等某些用法用得多了还记不住再做摘抄。

## 参考文档

-  [Emmet in Visual Studio Code](https://code.visualstudio.com/docs/editor/emmet)
-  [Emmet document](https://docs.emmet.io/cheat-sheet/)
- 选看：[Web 词汇表](https://www.runoob.com/web/web-glossary.html)