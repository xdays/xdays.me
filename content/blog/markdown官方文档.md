---
title: Markdown官方文档
date: 2013-03-10
author: admin
category: tool
tags: ['markdown']
slug: markdown官方文档
---

# 说明

本文翻译自官方的英文文档，主要目的是个人学习 Markdown 语法和锻炼英语能力。

**注意：** 这篇文档本身就是用 Markdown 写的，你可以
[在 URL 中添加.text 来查看源码](http://daringfireball.net/projects/markdown/syntax.text).

---

# 概述

## 思想

Markdown 置力于尽可能的易读写。

可读性是最终要的。一片用 Markdown 格式化的文档应该可以作为文本原样发布，不许要看上去已经被一些标签或者格式化指令标记。Markdown 的语法受目前已有的文本转 html 的过滤器影响--包括[Setext](http://docutils.sourceforge.net/mirror/setext.html),
[atx](http://www.aaronsw.com/2002/atx/),
[Textile](http://textism.com/tools/textile/),
[reStructuredText](http://docutils.sourceforge.net/rst.html),
[Grutatext](http://www.triptico.com/software/grutatxt.html), and
[EtText](http://ettext.taint.org/doc/)--对 Markdown 语法影响最大的是 email 的文本格式

Markdown 的语法是由标点符号组成，这些标点符号都是精心挑选的以便来表达他们本意。例如，围绕单词的型号看起啦就像是强调。列表看起来像是，哦，列表。甚至是块引用看起来就像是引用的文本，假设你曾经使用过邮件。

## 内联 HTML

Markdown 的语法是为了一个目的：用来*编写 web*的一种格式。

Markdown 不是 HTML 的替代品，也不像它。他的语法很少，仅对应于 HTML 的标签的子集。其重点不是制定一些更便捷的插入 HTML 标签的语法。在我看来，HTML 标签已经很容易插入了。Markdown 的重点在于更容易的读，写和编辑文章。HTML 是一种*发布*格式；Markdown 是一种*编写*格式。这样来看，Markdown 的语法仅用来解决可以用普通文本来传播的话题。

对于任何不能用 Markdown 语法来解决的标记，你就用 HTML。不需要事先说你已经从 Markdown 转向了 HTML，或者划清界限；你就是在使用标签罢了。

唯有一些限制是一些块级的 HTML 元素 -- 例如`<div>`, `<table>`, `<pre>`,
`<p>`,等 --
必须和周围的内容以空行分开，另外块标签的开始和结束不能用空行或者 tab 来缩进。Markdown 足够聪明不会在 HTML 的块标签周围添加额外的（不想要的）`<p>`标签。

比如，在 Markdown 的文章里添加一个 HTML 表格：

    This is a regular paragraph.

    <table>
        <tr>
            <td>Foo</td>
        </tr>
    </table>

    This is another regular paragraph.

注意观察 Markdown 的格式语法在 HTML 的块标签里并没有生效。比如，你不能在 HTML 块里添加`*强调*`

像`<span>`, `<cite>`, or
`<del>`的 span 级的 HTML 标签可以在 Markdown 的任何段落，列表或者标题内使用。如果你乐意，你可以不用 Markdown 而使用 HTML 标签，例如相比 markdown 你可能更愿意使用 HTML 的`<a>`
或者 `<img>`标签，这样完全可以。

不像块级标签，Markdown 的语法 _可以_ 在 span 级标签内处理。

## 自动转意特殊字符

在 HTML 里，有两个字符需要特殊对待：`<` 和
`&`。小于号用来开始一个标签；与符号用来表示 HTML 实体。如果你想要使用他们本身，你需要转意为实体，如`&lt;`和`&amp;`。

与符号特别让网页作者痛苦。如果你想要写关于'AT&T'，你需要写成'`AT&amp;T`'。你甚至需要在 URL 中转义与符号。于是，你想要链接到：

    http://images.google.com/images?num=30&q=larry+bird

你需要将你`href`属性的 URL 编码成：

    http://images.google.com/images?num=30&amp;q=larry+bird

不用多说了，这样很容易忘记，而且可能是编码良好的网页站点唯一的 HTML 验证错误。

Markdown 允许你直接使用这些字符，它来帮你完成转意。如果你在一个 HTML 实体中使用与符号，他将保持不变；否则它将被翻译成`&amp;`。

所以，如果你想在文章中包含一个版权图标，你可以直接写：

    &copy;

Markdown 会保持原样。但是如果你写：

    AT&T

Markdown 会将其翻译成：

    AT&amp;T

类似的，因为 Markdown 支持[行内 HTML](#html)，如果你使用尖括号作为 HTML 标签的分割符，Markdown 将把它们当作本意，但是如果你写：

    4 < 5

Markdown 会将其翻译为：

    4 &lt; 5

但是，在 Markdown 的 span 和块级代码内，尖括号和与符号 _总是_
自动被编码。这样就可以更方便的编写 HTML 代码。（相对的对于 HTML 来说，这是一个很恐怖的格式，因为在你每个示例代码的
`<` 和 `&` 都需要转义。）

---

# 块元素

## 段落和换行

段落是由空行分隔的一个或多个连贯的句子。（空行就是看上去一个空行 --
一行除了包含空格或者 tab 啥也没有的行就是空行。）正常情况下空行不能用空格或者 tab 缩进。

"一个或者多个连贯的句子"这句话暗示了 Markdown 支持“硬嵌”文本段落。这和其他 text-to-HTML 的格式器有很大不同（包括 Movable
Type 的转换换行的选项），他们都将段落的每一次换行转化为`<br />`标签。

当你在使用 Markdown*确实*需要插入一个`<br />`标签时，你可以在行尾写两个或则更多个空格，然后回车。

是的，插入`<br />`标签更费功夫些，但是简单通过换行插入对 Markdown 来说不行。当你用硬换行来格式化的时候，Markdown 的邮件风格的[块引用](#blockquote)和多段落的[列表](#list)工作的更好而且看起来更好。

## 标题

Markdown 支持两种分割的标题，[Setext](http://docutils.sourceforge.net/mirror/setext.html)和[atx](http://www.aaronsw.com/2002/atx/)。

Setext 风格的标题用等于号（一级标题）或者减号（二级标题）。例如：

    This is an H1
    =============

    This is an H2
    -------------

Atx 风格的标题在开头使用 1-6 个\#来表示 1-6 级标题。例如：

    # This is an H1

    ## This is an H2

    ###### This is an H6

是否关闭 atx 风格的标题是可选的。这纯粹是一种装饰，如果你觉得好看可以使用。关闭的\#都不用和开头的在数目上匹配（开头的数目决定了标题的等级。）：

    # This is an H1 #

    ## This is an H2 ##

    ### This is an H3 ######

## 块引用

Markdown 使用邮件风格的 `>`
作为块引用。如果你熟悉邮件中的块引用，你也就知道如何在 Markdown 里创建一个块引用。在每一行前放一个
`>`最好.

    > This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
    > consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
    > Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.
    >
    > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
    > id sem consectetuer libero luctus adipiscing.

Markdown 允许你懒一些,尽在每个段落的开头放一个 `>`

    > This is a blockquote with two paragraphs. Lorem ipsum dolor sit amet,
    consectetuer adipiscing elit. Aliquam hendrerit mi posuere lectus.
    Vestibulum enim wisi, viverra nec, fringilla in, laoreet vitae, risus.

    > Donec sit amet nisl. Aliquam semper ipsum sit amet velit. Suspendisse
    id sem consectetuer libero luctus adipiscing.

块引用可以通过添加额外的`>`嵌套(例如,块中块)：

    > This is the first level of quoting.
    >
    > > This is nested blockquote.
    >
    > Back to the first level.

块引用中可以包含其他的 Markdown 标签，包括标题，列表和代码块：

    > ## This is a header.
    >
    > 1.   This is the first list item.
    > 2.   This is the second list item.
    >
    > Here's some example code:
    >
    >     return shell_exec("echo $input | $markdown_script");

任何主流的编辑器都可以很方便的编写邮件风格的引用。例如，通过 BBEdit，你可以从菜单中选择增加引用。

## 列表

Markdown 支持有序列表和无序列表。

无序列表使用\*,+和-作为列表生成器：

    *   Red
    *   Green
    *   Blue

等同于：

    +   Red
    +   Green
    +   Blue

和：

    -   Red
    -   Green
    -   Blue

有序列表使用数字生成：

    1.  Bird
    2.  McHale
    3.  Parish

有一点很重要需要指出，你所使用的数字和 Markdown 生成的 HTML 没有关联，上边生成的 HTML 是：

    <ol>
    <li>Bird</li>
    <li>McHale</li>
    <li>Parish</li>
    </ol>

你也可以这么来写：

    1.  Bird
    1.  McHale
    1.  Parish

甚至这样：

    3. Bird
    1. McHale
    8. Parish

你会得到相同的输出。关键点是，只要你原因，你可以在你的 Markdown 列表内使用有序的数字，以便你源码的数字可以和生成的 HTML 的数字对应起来。如果你很懒，这也没必要。

如果你真是很懒，你也应该以 1 开头。将来，Markdown 可能会支持从任意数字开始有序列表。

列表生成器通常左对齐，但也有可能缩进三个空格。列表生成器必须后跟一个或者多个空格。

为了更好看些，你可以让条目保持相同的缩进：

    *   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
        Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
        viverra nec, fringilla in, laoreet vitae, risus.
    *   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
        Suspendisse id sem consectetuer libero luctus adipiscing.

但是如果你很懒，你不需要：

    *   Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Aliquam hendrerit mi posuere lectus. Vestibulum enim wisi,
    viverra nec, fringilla in, laoreet vitae, risus.
    *   Donec sit amet nisl. Aliquam semper ipsum sit amet velit.
    Suspendisse id sem consectetuer libero luctus adipiscing.

如果条目由空行分开了，Markdown 会把他们嵌入`<p>`标签中，例如：

    *   Bird
    *   Magic

会变成：

    <ul>
    <li>Bird</li>
    <li>Magic</li>
    </ul>

但这样：

    *   Bird

    *   Magic

会变成：

    <ul>
    <li><p>Bird</p></li>
    <li><p>Magic</p></li>
    </ul>

列条条目可能会包含多个段落，每个条目的子段扩至少要缩进 4 个空格或者一个 tab：

    1.  This is a list item with two paragraphs. Lorem ipsum dolor
        sit amet, consectetuer adipiscing elit. Aliquam hendrerit
        mi posuere lectus.

        Vestibulum enim wisi, viverra nec, fringilla in, laoreet
        vitae, risus. Donec sit amet nisl. Aliquam semper ipsum
        sit amet velit.

    2.  Suspendisse id sem consectetuer libero luctus adipiscing.

缩进每一行看起来很漂亮，但是 Markdown 允许你懒惰：

    *   This is a list item with two paragraphs.

        This is the second paragraph in the list item. You're
    only required to indent the first line. Lorem ipsum dolor
    sit amet, consectetuer adipiscing elit.

    *   Another item in the same list.

要想把块引用放到列表里，块引用的 `>` 分割符需要缩进：

    *   A list item with a blockquote:

        > This is a blockquote
        > inside a list item.

想要把代码块放到列表中，代码块需要缩进*两次*，也就是 8 个空格或者两个 tab：

    *   A list item with a code block:

            <code goes here>

有时可能会触发一些有序列表，比如这样写：

    1986. What a great season.

换句话说，有一些空格开头，后跟日期时间段。为避免这样，你可以转义时间段：

    1986. What a great season.

## 代码块

预格式化代码块用于编写程序或者标记的源代码。代码段是字面意思直译，而非形成段落。Markdown 将代码段放到
`<pre>` 和 `<code>` 标签里。

要生成代码块，只需要每行缩进至少 4 个空格或者 1 个 tab，例如这么写：

    This is a normal paragraph:

        This is a code block.

Markdown 将产生：

    <p>This is a normal paragraph:</p>

    <pre><code>This is a code block.

```

代码块的每行的一级缩进，4个空格或者1个tab将会被删除，例如：

    Here is an example of AppleScript:

        tell application "Foo"
            beep
        end tell

将变成：

    <p>Here is an example of AppleScript:</p>

    <pre><code>tell application "Foo"
        beep
    end tell
```

代码块一直到没有缩进为止（或者文章的结束）

在一个代码块中，与符号和尖括号会自动转换成 HTML 实体。这样就很容易在 Markdown 里包含示例 HTML 源码，只需要拷贝进来然后缩进，Markdown 会处理对与符号和尖括号的编码工作。比如，这样：

        <div class="footer">
            &copy; 2004 Foo Corporation
        </div>

会变成：

    <pre><code>&lt;div class="footer"&gt;
        &amp;copy; 2004 Foo Corporation
    &lt;/div&gt;

```

标准的Markdown语法在代码块中不会被处理。比如星号就只是字面意义的星号。这意味着可以很容易的用Markdown写Markdown自己的语法。

水平线
------

你可以通过三个或者多个减号，星号或者下划线来生成一个平平线。如果你乐意，可以在星号和减号间加空格，下边都能生成水平线：

    * * *

    ***

    *****

    - - -

    ---------------------------------------

* * * * *

span元素
========

链接
----

Markdown支持两种链接的方式：*内联*和*参考*。

每种方式，链接文字都放于方括号内。

要添加一个链接，将一个用括号包含起来放在链接文本之后，链接文本用方括号扩起来。括号内是你想要链接的URL和可选的链接名称，链接名称用引号引起来。例如：

    This is [an example](http://example.com/ "Title") inline link.

    [This link](http://example.net/) has no title attribute.

生成：

    <p>This is <a href="http://example.com/" title="Title">
    an example</a> inline link.</p>

    <p><a href="http://example.net/">This link</a> has no
    title attribute.</p>

如果你链接到同一服务器的本地资源，你可以使用相对路径：

    See my [About](/about/) page for details.

参考风格的链接使用另一个方括号，在这个方括号里你放一个标识这个链接的标签：

    This is [an example][id] reference-style link.

空格是可选的：

    This is [an example] [id] reference-style link.

再在同一篇文档里用一行像这样定义链接标签：

    [id]: http://example.com/  "Optional Title Here"

也就是：

-   方括号包含链接标识（缩进三个空格是可选的）;
-   后跟冒号；
-   后跟一个或者多个空格（tab）；
-   后跟链接URL
-   可选地后跟任意链接的属性，用单引号，双引号或者括号引起来

下边的链接定义方法都一样：

    [foo]: http://example.com/  "Optional Title Here"
    [foo]: http://example.com/  'Optional Title Here'
    [foo]: http://example.com/  (Optional Title Here)

**注意：** Markdown.pl 1.0.1发现bug，不能用但因号来引链接名称。

链接URL可以可选择的放到尖括号里：

    [id]: <http://example.com/>  "Optional Title Here"

链接的属性可以换行写，但需要用额外的空格或者tab来缩进，对于长URL这样看起来更好：

    [id]: http://example.com/longish/path/to/resource/here
        "Optional Title Here"

定义链接只能被用于Markdown处理是来生成链接，最终将从你的生成的HTML中删除掉。

链接名称可能包含字符，数字，空格和标点符号，但是他们是大小写*不*敏感的。这两个链接：

    [link text][a]
    [link text][A]

是一回事。

*隐式链接名*技巧允许你不些链接名，这种情况下链接本身作为名称。使用空方括号来链接“Google”到google.com，你可以写：

    [Google][]

然后定义链接：

    [Google]: http://google.com/

因为链接名可能包含空格，这个技巧对多个单词的链接也生效：

    Visit [Daring Fireball][] for more information.

然后定义链接：

    [Daring Fireball]: http://daringfireball.net/

链接定义可以放到文档的任何部分。我倾向于将他们放到紧随使用他们的段落的下方。但是你可以随意将它们放到文档的最后，想脚注一样排序。

这是一个参考链接的例子：

    I get 10 times more traffic from [Google] [1] than from
    [Yahoo] [2] or [MSN] [3].

      [1]: http://google.com/        "Google"
      [2]: http://search.yahoo.com/  "Yahoo Search"
      [3]: http://search.msn.com/    "MSN Search"

使用隐式链接名技巧，你可以这样写：

    I get 10 times more traffic from [Google][] than from
    [Yahoo][] or [MSN][].

      [google]: http://google.com/        "Google"
      [yahoo]:  http://search.yahoo.com/  "Yahoo Search"
      [msn]:    http://search.msn.com/    "MSN Search"

两个例子最终都生成如下的HTML：

    <p>I get 10 times more traffic from <a href="http://google.com/"
    title="Google">Google</a> than from
    <a href="http://search.yahoo.com/" title="Yahoo Search">Yahoo</a>
    or <a href="http://search.msn.com/" title="MSN Search">MSN</a>.</p>

为了对比一下，这里用Markdown的内联格式写了相同的段落：

    I get 10 times more traffic from [Google](http://google.com/ "Google")
    than from [Yahoo](http://search.yahoo.com/ "Yahoo Search") or
    [MSN](http://search.msn.com/ "MSN Search").

重点不是使用参考样式的链接更容易写，而是写出的文档更具有可读性。对比上边的这个例子：用参考样式写的段落有81个字符，用内联样式的有176个字符，原生的HTML有234个字符，用原声的HTML要比标签用更多的字符。

使用参考样式的链接，一篇文章随着被浏览器解析更接近最终的输出。因为从段落中把相关标记的元信息提取出来，你就可以不中断行文回路的情况下增加链接。

强调
----

Markdown把星号(`*`)和下划线 (`_`)当作强调. 包含于`*`或者
`_`的文本都会被打上`<em>`标签;
两个`*`或者`_`会被打上`<strong>`标签。比如这样的输入：

    *single asterisks*

    _single underscores_

    **double asterisks**

    __double underscores__

会生成：

    <em>single asterisks</em>

    <em>single underscores</em>

    <strong>double asterisks</strong>

    <strong>double underscores</strong>

你可以使用任意的格式；唯一的限制是必须在一个强盗span里使用相同的字符。

强调可以用在单词中间：

    un*frigging*believable

但是如果你在`*`和`_`周围使用空格，他们将被当作星号和下划线。

要生成一个字面意思的星号或者下划线而不是左强调用，你可以转义：

    *this text is surrounded by literal asterisks*

代码
----

要之处一块代码，就把它放到反引号里（`` ` ``）。和预格式化代码块不一样，代码块标识正常段落里的代码，例如：

    Use the `printf()` function.

会输出：

    <p>Use the <code>printf()</code> function.</p>

要在代码里包含反引号，你可以使用多个反引号引起来这段代码：

    ``There is a literal backtick (`) here.``

会输出：

    <p><code>There is a literal backtick (`) here.</code></p>

包含代码的分割符可能包含空格，开始一个结束一个。这样你就可以在代码的开始或者结尾插入反引号：

    A single backtick in a code span: `` ` ``

    A backtick-delimited string in a code span: `` `foo` ``

将输出：

    <p>A single backtick in a code span: <code>`</code></p>

    <p>A backtick-delimited string in a code span: <code>`foo`</code></p>

在代码中，与符号和尖括号自动被编码为HTML实体，这样就可以很容易的嵌入HTML标签。Markdown将把如下：

    Please don't use any `<blink>` tags.

变成：

    <p>Please don't use any <code>&lt;blink&gt;</code> tags.</p>

你可以这样写：

    `&#8212;` is the decimal-encoded equivalent of `&mdash;`.

来生成：

    <p><code>&amp;#8212;</code> is the decimal-encoded
    equivalent of <code>&amp;mdash;</code>.</p>

图片
----

不可否认，在普通文本格式里设计一个自然的表示图片的方式相当困难。

Markdown用表示链接相同的语法来表示图片，有两种方式：*内联*和*参考*。

内联图片语法如下所示：

    ![Alt text](/path/to/img.jpg)

    ![Alt text](/path/to/img.jpg "Optional title")

就是说：

-   一个感叹号： `!`；
-   后跟方括号，内包含图片的alt文本；
-   后跟一对括号，包含图片的URL，和一个可选的名称，名称用单或者双引号引起来。

参考风格的图片语法是这样的：

    ![Alt text][id]

"id"是预先定义号的图片的参考。图片参考用和定义链接参考一样的语法来定义：

    [id]: url/to/image  "Optional title attribute"

写这篇文档时，Markdown没有制定图片尺寸的语法；如果这对你很重要，你可以使用HTML的`<img>`标签。

* * * * *

杂项
====

自动链接
--------

Markdown支持一个自动为链接和邮件地址创建链接的技巧；只需要把链接或者邮件地址放到尖括号里。这意味着你想要战士实际的链接URL或者邮件地址，而且让它成为一个可点击的链接，你可以这样：

    <http://example.com/>

Markdown会将其变成：

    <a href="http://example.com/">http://example.com/</a>

针对邮件地址的自动链接也一样，此外，Markdown会进行随机数和编码工作来模糊你的邮件地址以防垃圾邮件，例如Markdown将把如下：

    <address@example.com>

转变为：

    <a href="&#x6D;&#x61;i&#x6C;&#x74;&#x6F;:&#x61;&#x64;&#x64;&#x72;&#x65;
    &#115;&#115;&#64;&#101;&#120;&#x61;&#109;&#x70;&#x6C;e&#x2E;&#99;&#111;
    &#109;">&#x61;&#x64;&#x64;&#x72;&#x65;&#115;&#115;&#64;&#101;&#120;&#x61;
    &#109;&#x70;&#x6C;e&#x2E;&#99;&#111;&#109;</a>

这在浏览器中将被解析为一个可点击的链接“address@example.com”

这一类的实体编码技巧确实可以愚弄很多，即使不是大多数地址收获机器人，但不能欺骗所有的。有总比没有强，但是这样发布的邮件地址最终也可能会收到垃圾邮件。

右斜线转义
----------

Markdown
允许你使用斜线转义一般文本字符，这些文本如果不转义将会在Markdown的格式化语法中有特殊意义。例如，你需要用星号包含一句话（不是HTML的`<em>`标签），你可以在星号前使用斜线，像这样：

    *literal asterisks*

Markdown为下边的字符提供转义：

       backslash
    `   backtick
    *   asterisk
    _   underscore
    {}  curly braces
    []  square brackets
    ()  parentheses
    #   hash mark
    +   plus sign
    -   minus sign (hyphen)
    .   dot
    !   exclamation mark

[官方文档原文](http://daringfireball.net/projects/markdown/syntax "markdown manual")
```
