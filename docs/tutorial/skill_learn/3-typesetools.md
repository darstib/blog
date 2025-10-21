---
comments: true
tags:
- notes
---

## Markdown

> [!wiki]- Markdown
>
> **Markdown**是一种[轻量级标记语言](https://zh.wikipedia.org/wiki/%E8%BD%BB%E9%87%8F%E7%BA%A7%E6%A0%87%E8%AE%B0%E8%AF%AD%E8%A8%80 "轻量级标记语言")，创始人为[约翰·格鲁伯](https://zh.wikipedia.org/wiki/%E7%B4%84%E7%BF%B0%C2%B7%E6%A0%BC%E9%AD%AF%E4%BC%AF "约翰·格鲁伯")。它允许人们使用易读易写的纯文本格式编写文档；它易于阅读和编写，使得作者能够专注于内容创作。
> 
> Markdown 最大的优势在于其语法简洁，上手快；同时可以很方便的转换为其他语言，cc98，知乎文章的编辑都能很好地支持 markdown 格式；顺带一提，由于其简洁但很好地保留了信息的结构，现有主流大语言模型的输入/输出都是使用 markdown 语法（html 扩展）的，大家对自然语言模型提示词结构化/回答结构化

创建之初，Markdown 的[基本语法](https://markdown.com.cn/basic-syntax/)只支持的标题、引用、列表、`代码`、**强调**、*斜体*、[链接](https://example.com)、内嵌 html 等；且后续发展并没有一个明确和统一的官方标准。而为了满足不同的需求，许多 Markdown 处理器引入了各种[扩展语法](https://markdown.com.cn/extended-syntax/)，导致不同的 Markdown 解释器以不同的方式实现 Markdown 语法[^1]。

[^1]: 据野史记载，曾经有一个组织试图将现有的 n 种 Markdown 规范进行统一，于是有了 n+1 种 Markdown 规范；不过似乎 [CommonMark](https://github.com/commonmark) 确实在试图规范化，尽请期待？但是实际使用不难发现还是得基于实际平台去修改。
[^4]: 更有用的是 markdown 一般还支持 TeX 数学公式、HTML 嵌入。

例如本网站使用 mkdocs 实现，支持一个称为 `admonition` 或者叫 `callout` 的块，即如上面的 wiki 内容，其语法如下，[实际样例](https://github.com/IsshikiHugh/notebook/blob/a820bce019868feb6e34cb410b6bad139dbc3197/docs/cour_note/D2CX_AdvancedDataStructure/Lec01.md?plain=1#L398) ：

```md
??? wiki "Markdown"
    
    Markdown ...    
```

而 GitHub 或者是我使用的笔记软件 obsidian 对此对应语法为：

```md
> [!wiki]+ Markdown
>
> Markdown ...
```

> 考虑到之后可能在 github 进行项目开发并攥写自述文件(README)，推荐大家优先学习 [Github 的基本撰写和格式语法](https://docs.github.com/zh/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#headings)。

对于 markdown 的基础语法实在太常见了，鹤翔学长的 [Markdown 教学](https://slides.tonycrane.cc/MarkdownLecture/#slide=1)也非常详细，我不准备全部讲解，

- 仅仅在 [markdown.com.cn](https://markdown.com.cn/editor/) 展示基本语法，
- 在 [`Arya` 在线 Markdown 编辑器](https://markdown.lovejade.cn/) 展示一些高级的用法；
- 有考虑到 markdown 中可以嵌入简单的 html，所以也以 [jyshare 的在线工具](https://www.jyshare.com/front-end/61/) 中的模块简单进行讲解。

如果还有不懂的地方，或者你只是单纯想系统地学语法而非听我巴拉巴拉扯一堆东西和演示，[markdown.cn](https://markdown.cn/) 可能是个很好的选择。

> [!tip]+ Useful tools
>
> - 对于数学公式，一个好用的工具是 [SimpleTex](https://www.simpletex.cn/)，其支持[图片识别](https://www.simpletex.cn/ai/latex_ocr)、[公式可视编辑](https://www.simpletex.cn/formula_editor)、[文档编辑](https://www.simpletex.cn/ai/editor)，当然基于其功能强大，也有不少工具使用其[API](https://www.simpletex.cn/api) 进行快捷工作，譬如 utool 上的一个插件，例如 $g(w)= \nabla f(w)$ ；
> - 当然有时我也在 [OEIS](https://en.wikipedia.org/wiki/On-Line_Encyclopedia_of_Integer_Sequences)[^2] 的 [List_of_LaTeX_mathematical_symbols](https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols) 上查找，但是基于网络原因可能公式加载比较慢；
> - 再不济可以在这个[手写公式识别](https://detexify.kirelabs.org/classify.html) 网站上写出来去找。

[^2]: On-Line Encyclopedia of Integer Sequences（在线整数序列百科全书, [OEIS](https://oeis.org/)）是一个整数序列的在线数据库。

抛弃对美化的高要求（事实上通过平台支持，设计好 css 样式、使用 html、引入扩展语法，同样会很好看），markdown 能够很好地实现**传递信息**的功能，同时 markdown 很容易转变为其它类型的文本标记语言（如 html），所以常用于记录笔记、转变为网页文章（个人网站也好，cc98、知乎、微信公众号等交流平台也好）；具体大家之后选择使用什么类型的工具这里仅以本人知晓的工具作推荐，不全、且 `-` 标记为未使用过（除 vscode 都支持实时渲染）：

- [vscode](https://code.visualstudio.com/) + [Markdown All in One](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one) + [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
	- 作为 ~~宇宙最强~~ [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment)，vscode 基本可以实现任何编辑工作，我们在之后讲解 vscode 时再来演示；
- [obsidian](https://obsidian.md/) or [-typora](https://typora.io/) or [-Marktext](https://www.marktext.cc/)
	- 本地 markdown 笔记软件代表；
	- 【私货】我主要使用 obsidian，简要介绍可见 [Obsidian_begin]()；
	- 【私货】cc98 帖：[markdown笔记软件推荐——obsidian](https://www.cc98.org/topic/5332436); [obsidian终极使用经验贴](https://www.cc98.org/topic/6171491)
- [飞书](https://www.feishu.cn/) or [语雀](https://www.yuque.com/dashboard) or [-notion](https://www.notion.so/)
	- 在线 markdown 笔记软件代表。

## Word

大家总是认为 word 排版 “不符合自己程序员/码农/..” 的身份，觉得其 “谁都能用” “排版丑陋”；但实际上下面要讲的 Latex/Typst 讲完后你同样会觉得谁都能用，且让一个自诩很懂的人来从头开始写也不见得能有多好看；有一个好的模板 word 同样能写出好看的论文。

又或许正是因为 word 本身功能太强大，编写者迷失于调节样式，同时批量调整样式时出现纰漏可能性极高（尽管 word 工具本身支持指定内容的样式调整），这是我们不常使用其在一些学术/出版领域的原因之一。

> [!extra]- 了解 docx 更多一点
>                        
>但是你是否注意到我们常见的 word 文件有两种类型的文件扩展名？`*.doc` `*.docx`
>
>> [!quote]+ [Fileformat - docx](https://docs.fileformat.com/word-processing/docx/)
>>
>> 微软开放了 DOC 文件格式的规范后，其竞争对手很容易逆向工程该格式并在自己的应用程序中提供相同支持。此外，来自 Open Office 的竞争，以其开放文档格式的形式，迫使微软采用更开放和广泛的标准。2000 年初，微软决定采用 Office Open XML 标准进行变革。根据这一新标准创建的文档被赋予了.docx 扩展名，其中的**“X”代表 XML**。到 2007 年，这种新的文件格式已成为 Office 2007 的一部分，并在 Microsoft Office 的新版本中继续使用。这种新文件类型具有文件大小小、损坏几率低和图像格式良好的优点。
>
>> [!quote]- [office家族虐恋情深之歌](https://baike.baidu.com/item/office%E5%AE%B6%E6%97%8F%E8%99%90%E6%81%8B%E6%83%85%E6%B7%B1%E4%B9%8B%E6%AD%8C/931236)
>>
>> 你伤害了 Word，还 Excel 而过，你 Access 的贪婪，我 Outlook 懦弱。One 泪 Note 过，回忆是多 Binder，只怪自己 Mail 你 PowerPoint……
>
>> [!quote]+ [Anatomy of a WordProcessingML File](http://officeopenxml.com/anatomyofOOXML.php)
>>
>> A WordprocessingML or docx file is a **zip file (a package) containing a number of "parts"**--typically UTF-8 or UTF-16 encoded XML files, though strictly defined, a part is a stream of bytes. 
>
>在 demo.docx 文件中添加一级标题、二级标题、一张图片后，使用解压缩软件及进行解压，可以得到一个文件夹，内容如下：
>
> ![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/17_250317-221550.png)
>
>我们无需看懂这些奇怪的标签内容，只需要了解编辑的文本不过是在内部使用这样那样的语法进行了修饰，便于我们稍后总结。
>
>> [!extra]- 那如果我用解压缩软件尝试解压缩 demo.doc 文件，会咋样？
>>
>> 可以自己试试将文件扩展名改为 `.zip` 解压，可以发现结果是几个无扩展名文件，使用文本编辑器打开也是“乱码”形式。

## LaTeX

> [!wiki]- $\LaTeX$
>
> LaTeX（/ˈlɑːtɛx/或/ˈleɪtɛx/，常被读作/ˈlɑːtɛk/或/ˈleɪtɛk/，风格化后写作 $\LaTeX$），是一种基于 TeX 的排版系统。
> 
> 发音介绍可见 [Latex 入门 - 熟悉 LaTeX](https://lrita.github.io/images/wiki/latex%E5%85%A5%E9%97%A8-%E7%AE%80%E7%89%88-%E5%88%98%E6%B5%B7%E6%B4%8B.pdf)；[TeX 引擎、格式、发行版之介绍](https://liam.page/2018/11/26/introduction-to-TeX-engine-format-and-distribution/)。

- 优点：编写者注重于内容，排版效果好，数学公式排版强大，开源模板众多，被广泛接受……
- 缺点：学习成本高，易排错，设置样式复杂，编译速度慢（线性执行、宏展开、重头编译……）

详细介绍、语法使用在鹤翔学长的 [LaTeX 排版简要介绍](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-spring-cs/lec4/#/) 中讲解得非常详细了，同时基于我自己也只是在 markdown 中使用其数学公式、或者是为了写论文用用模板，我同样不想进行详细地讲解，仅对 “命令，结构，宏包，环境，公式” 几个关键词在 [overleaf](https://www.overleaf.com/) or [中文站](https://cn.overleaf.com/) 进行讲解演示（overleaf 简单介绍），居于此你也足够学会使用一个模板。

### Overleaf 基本介绍

打开 [overleaf](https://www.overleaf.com/),登入后往往进入你的 "project" 仓库，帮我们保留着 projects；右上角是其收集的 [Template](https://www.overleaf.com/latex/templates)，当然大家也可以去浏览器中搜寻符合自己需求的模板；由于 LaTeX 的广泛使用，你需要的所有功能应该都能够找到模板。我们新建一个项目，之后从 [A quick guide to LaTeX](https://www.overleaf.com/latex/templates/a-quick-guide-to-latex/fghqpfgnxggz) 这个模板开始。

一般我们更加习惯于 Code Editor，左边为源码， `ctrl+s / commands+s` 或者点击 Recopile 进行编译，右边展示内容。

### 命令

LaTeX 的指令，告诉 LaTeX “做什么”，一般包含

- 反斜杠 `\` ：放在开头，作为 LaTeX 识别命令的标志对。
- 命令名称：反斜杠后紧跟命令的名称，通常由字母组成，**大小写敏感**。例如，`\documentclass`、`\begin`、`\end`、`\usepackage`。
- 参数：有些命令需要参数来指定命令的作用对象或行为
	- **必须参数**放在 `{}` 中，命令必须有这些参数才能正常工作。
	- **可选参数**放在 `[]` 中，命令可以根据需要选择性地使用这些参数。
	- $\LaTeX$ ？

在 LaTeX 中，宏是一种预定义的命令序列，可以用来简化重复性任务、创建自定义命令或修改现有命令的行为。宏本质上是一种文本替换机制：当你使用一个宏时，LaTeX 会将它替换为预定义的文本或命令序列。相信大家在学习 C 语言的时候也有所理解了。

#### \newcommand

LaTeX 中，主要使用 `\newcommand` 和 `\renewcommand` 命令来定义宏。

- `\newcommand{\命令名}[参数个数]{定义}`：定义一个新的宏。如果命令名已存在，则会报错。
- `\renewcommand{\命令名}[参数个数]{定义}`：重新定义一个已存在的宏。

> [!extra]- How do TeX macros actually work?
>
> 如果你希望了解更多关于 TeX 的宏，可以看看 overleaf 的 [How do TeX macros actually work?](https://www.overleaf.com/learn/latex/A_six-part_series%3A_How_do_TeX_macros_actually_work%3F)

### 文件结构

对于一篇（短）论文，其内容结构一般如下：

```tex
\documentclass{article}  % I am a comment.
% Introduction Area
% use package; set info; new command; set style; ...
% use package
\usepackage{graphicx} % Required for inserting images
\usepackage{lipsum} % generate lore ipsum
\usepackage{subfiles} % import sub files
% set info
\title{demo}
\author{Darstib Reed}
\date{April 2025} % [option], or \date{\today}
% new command
\newcommand{\mybinomial}[3][2]{(#2 + #3)^{#1}}

\begin{document}
% content

\maketitle

\begin{abstract} This is the abstract for this paper. \end{abstract}

\section{Introduction} % generate a 1-level title

Hello world!

\subsection{}

\mybinomial[3]{x}{y}

\end{document} % content after this line will be ignored.
```

#### \documentclass

> [!quote]- [What is a documentclass in LaTeX?](https://docs.aspose.com/tex/java/latex-document-classes/)
>
> Typically, the first command in the preamble has to be \documentclass, which takes a single required argument that is the name of the document class. The document class itself is a set of formatting parameters, layout metrics, macros, etc. that are suitable and useful for developing documents of a certain type and collected under the single name. In this article, we will discuss the LaTeX predefined document classes that are built-in LaTeX and show their uses, differences, and similarities. We will also mention some optional arguments that the \documentclass command can take, and that customize the appearance of the document.
> 
> 通常，前导部分中的第一个命令必须是 \documentclass ，它需要一个单个必需的参数，即文档类的名称。文档类本身是一组适合和有用的格式化参数、布局度量、宏等，这些参数适用于开发特定类型的文档，并收集在单个名称下。在本文中，我们将讨论 LaTeX 预定义的文档类，它们是内置在 LaTeX 中的，并展示它们的用途、差异和相似之处。我们还将提到 \documentclass 命令可以接受的某些可选参数，以及它们可以定制文档的外观。

简单来说，documentclass 是决定接下来要生成的文档是什么类型的，一般包括：article, report, book, slides, letter ，大多情况下我们使用 article 。

关于可选参数，可以参考：[LaTeX documentclass options illustrated](https://texblog.org/2013/02/13/latex-documentclass-options-illustrated/)

#### \usepackage

就像很多编程语言将常用功能/类进行封装，方便调用以提高效率；TeX 中将具有特定功能的宏打包成宏包；经过发布/采用，我们可以使用 `\usepackage{package}` 来使用其中的宏。

一般来说，`\documentclass{article}` 引入的宏包中没有直接支持中文的宏，往往导致："LaTeX Error: Unicode character"；我们可以通过引入 "ctex" 宏包或者使用ctexart ctexrep ctexbook 等文档类 `\documentclass{ctexart}` 。

> [!help]- 下面是综合多方来源的常用宏包，大家可以自行了解使用，部分可能在 docume class 中已有
> 
> |    宏包名     |                     描述                      |
> | :--------: | :-----------------------------------------: |
> | **数学与公式**  |                                             |
> |  amsmath   |         **必备**，增强数学公式排版（多行公式、矩阵等）。          |
> |  amssymb   |           提供大量数学符号（黑板粗体、花体、箭头等）。            |
> | mathtools  |          amsmath 的扩展，提供更多数学工具和修正。           |
> | **图形与颜色**  |                                             |
> |  graphicx  |    **必备**，用于插入和控制图片 (\includegraphics)。     |
> |  caption   |            自定义图表标题（caption）的样式。             |
> | subcaption |              创建包含子图或子表的图形/表格。               |
> |   xcolor   |         提供颜色支持，功能比 color 更强大，推荐使用。          |
> |  **页面布局**  |                                             |
> |  geometry  |                方便地设置页面尺寸和边距。                |
> |  fancyhdr  |               自定义页眉和页脚的内容与样式。               |
> |  setspace  |            调整行间距（单倍、1.5 倍、双倍等）。             |
> | **链接与引用**  |                                             |
> |  hyperref  |       创建 PDF 内的超链接（目录、引用、URL），建议最后加载。       |
> |    url     |    排版 URL 地址，支持特殊字符和断行（通常 hyperref 会加载）。    |
> |   **表格**   |                                             |
> |  booktabs  |             绘制更美观的专业表格线条（三线表）。              |
> | longtable  |                 创建可以跨页的长表格。                 |
> |  multirow  |                使表格单元格可以跨越多行。                |
> |  **代码排版**  |                                             |
> |  listings  |              在文档中排版源代码，支持语法高亮。              |
> |   minted   | 使用 Pygments 进行高质量语法高亮的代码排版（需 shell-escape）。 |
> |   **绘图**   |                                             |
> | tikz (PGF) |        功能强大的矢量绘图宏包，可在 LaTeX 代码中直接绘图。        |
> |  **语言支持**  |                                             |
> |    ctex    |         **提供完整的中文排版支持**（字体、标点、格式等）。         |
> |  inputenc  |       （主要用于 pdfLaTeX）指定源文件编码（如 utf8）。       |
> |  fontenc   |        （主要用于 pdfLaTeX）选择字体编码（如 T1）。         |
> |   babel    |          提供多语言排版规则支持（断字、日期、固定文本）。           |
> |  **其他实用**  |                                             |
> |  enumitem  |       高度自定义列表（itemize, enumerate）的样式。       |
> | todonotes  |             在文档中添加 TODO 笔记和评论。              |
> | microtype  |              改进文本的微观排版，提升阅读体验。              |
> 
> 借助 AI 整理，部分可能有误或者过时。

#### \begin \end

在 LaTeX 中，**环境**是用于对文档中的特定区域应用特定格式或样式的命令，通常用于创建列表、表格、居中内容、数学公式等，使用 `\begin{}` 和 `\end{}` 进行包裹，一般形式如下：

```tex
\begin{environment}[optional args]{required args}
... 
\end{environment}
```


```tex
\begin{center}
    center content
\end{center}
```

#### \maketitle

- `\maketitle` 命令会调用 LaTeX 内部的 `\@maketitle` 命令来实际生成标题；
- `\@maketitle` 命令的定义取决于所使用的文档类（`article`、`report`、`book` 等）；
- [生成标题页](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-spring-cs/lec4/#/3/2) & [how does '\maketitle' work?](https://tex.stackexchange.com/questions/452971/how-does-maketitle-work) 了解更多。

### 内容排版

对于我们排版时常用内容如下（各行具体功能在课上简单提及）：

```tex title="document content"
\begin{document} % content

\maketitle % title

\begin{abstract} This is the abstract for this paper. \end{abstract}

\tableofcontents % toc

\newpage

\section{1-level title} % generate a 1-level title

Hello world! \mybinomial[3]{x}{y}

\subsection{2-level title}

\paragraph{sub part 1:}
\lipsum[30]
\subparagraph{sub part 2:}
\lipsum[30] 

\lipsum[30]

\vspace{1 em}

\lipsum[30]

\indent \lipsum[30] \hspace{2 em} \lipsum[30]

\subsubsection{Text Formatting Commands}
\label{3-level title}

\% is a special char % special char

\textbf{This text will be bold.}

\textit{This text will be italic.}
\emph{This text will be emphasized (usually italic).}

\underline{This text will be underlined.}

\texttt{This text will be in monospace font.}

1, 2, \ldots, n

\begin{itemize} % unordered list
    \item Item 1
    \item Item 2
\end{itemize}

\begin{enumerate} % ordered list
    \item Item 1
    \item Item 2
\end{enumerate}

This is an inline formula: $E=mc^2$. Here are Displayed math formulas:

$$ % without number
    E=mc^2
$$
\begin{equation} % with number
    E=mc^2
\end{equation}

\newpage
% \includegraphics[width=0.5\textwidth]{imgs/map.jpeg}

\begin{figure}[t] % placement: h 当前位置，t 页面顶部，b 页面底部，p 单独一页
    \centering
    \includegraphics[width=0.5\textwidth]{imgs/map.jpeg}
    \caption{Figure caption}
    \label{fig:zjg-map}
\end{figure}

Footnote\footnote{this is a footnote} is enable.

\begin{table}[b]
    \centering
    \begin{tabular}{|c|c|}
        \hline
        Column 1 & Column 2\\
        \hline
        Data 1 & Data 2 \\
        \hline
    \end{tabular}
    \caption{Table caption}
    \label{tab:demo_table}
\end{table}

Figure \ref{fig:zjg-map} is the map of zjg of ZJU.
Title \ref{3-level title} is what 3-level title looks like. 

\cite{einstein1905} is a bib cite article. 

\subfile{sub.tex}

\section*{Conclusion} % * for not numbering

\bibliographystyle{ieeetr} % format
\bibliography{refs.bib} % bib source

\end{document} % content after this line will be ignored.
```

当然，也许你觉得现在展现出来很难看；更多时候（或者说对绝大多数人的每次使用）都是从一个模板开始，那里的样式往往会整齐美观；我们不关注那些，也不在此讲解；我们只需要看懂需要修改的部分即可。

自己稍加尝试后，相信你应该能够看懂 [latex sheet](https://wch.github.io/latexsheet/latexsheet-a4.pdf) 了；再之后，你应该具备了依据模板（借助搜索引擎和人工智能）完成一篇报告/论文的排版工作的能力，试试在撰写课程报告时使用、（各类文件掌握几个模板）练习即可。

## Typst

- [Typst_begin](../begin/Typst_begin.md)

## 概览总结

各个工具的比较如下，大家可以自主选择使用的工具：

|  特性  |              Markdown              |          Word           |                       Typst                        |                    LaTeX                    |
| :--: | :--------------------------------: | :---------------------: | :------------------------------------------------: | :-----------------------------------------: |
|  性质  |              轻量级标记语言               |     所见即所得[^3]的排版软件      |                      新一代排版系统                       |                基于 TeX 的排版系统                 |
|  优势  | **语法简单**，易于阅读和书写；**跨平台**，易于转换为其他格式 | **操作直观**，功能丰富；兼容性好，用户群广 | **编译速度快**，语法现代，**错误提示友好**；结合了 Markdown 和 LaTeX 的优点 | 专业排版，公式、图表处理能力强；文档结构清晰，被广泛使用，适合**长文档和学术论文** |
|  难度  |                 极低                 |            低            |                         中等                         |                      高                      |
| 实用场景 |      快速笔记、博客文章、技术文档、README 等       |       日常文档、报告、简历等       |               学术论文、技术文档、书籍、需要快速编译的场景               |             学术论文、书籍、技术报告、复杂排版需求             |

[^3]: **所见即所得 (WYSIWYG)**：Word 是一种所见即所得的编辑器，意味着你在编辑时看到的样子就是最终打印或显示的样子。

## 参考资料

- 链接很多，均在文中指出
