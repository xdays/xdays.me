---
title: JavaScript基础语法
date: 2013-10-30
author: admin
category: javascript
tags: javascript
slug: javascript基础语法
---

特点
====

-   解释型，基于原型（prototype）的面向对象高级语言；
-   应用广泛，常见但不仅限于Web开发，[node.js](http://nodejs.org)日渐流行；
-   编写灵活，这是一把双刃剑
-   性能强大，非阻塞
-   开放，ECMAScript规范
-   厂商扩展，看具体引擎实现

数据类型
========

-   字符串，Unicode
-   数字，64位二进制表示
-   布尔，即true和false
-   null，实际上null不是一种数据类型，而是一个对象值。
-   undefined
-   对象，理解JavaScript的关键所在，键值对的集合，包括数组，函数，正则，日期等

操作符和表达式
==============

操作符
------

-   操作符列表如下：  

    ![operator](/wp-content/uploads/2013/10/operator.png)

-   操作符优先级，与其他语言类似，记住用括号显示表达优先级就可以了。

表达式
------

-   原始表达式，如`1.0`就是表达式
-   数组和对象初始化，如`[1,2]`和`{'foo': 'bar'}`
-   函数定义，如`function f() {}`
-   属性访问，如`o.attr`
-   调用，如`f()`
-   对象创建，如`new Array`

语句
====

语句块
------

-   用`{}`将语句包含起来就是语句块
-   语句块不会创建作用域

条件语句
--------

### if

    if (expression) {
        statement;
    }

### if...else...

    if (expression) {
        statement;
    }
    else {
        statement;
    }

### if...else if...else

    if (expression) {
        statement;
    }
    else if {
        statement;
    }
    else {
        statement;
    }

### switch

    swith () {
        case value1:
            statement;
        case value2:
            statement;
        default:
            statement;
    }

循环语句
--------

### while

    while (expression) {
        statement
    }

### do...while

    do {
        statemnet
    } while (expression)

### for

    for (foo=0; foo<=10;foo++) {
        statement;
    }

### for in

    for (foo in obj) {
        statement;
    }

数组
====

概述
----

-   数组是一种特殊的对象
-   一组对象的有序集合

定义
----

    var arr = [1, 2, 3];
    var arr = new Array;

数组的方法
----------

-   join连接
-   reverse反向
-   sort排序
-   concat拼接
-   slice切片
-   splice插入或删除
-   push和pop入栈和出栈
-   unshift和shift移位
-   toString和toLocalSting字符串表示
-   forEach遍历
-   map映射
-   filter过滤
-   every和some每一个和有些
-   reduce和reduceRight聚合
-   indexOf和lastIndexOf索引

函数
====

概述
----

-   函数是一种特殊的对象，定义一组语句用于重复利用

定义
----

    var fun = function() {};
    var fun = new Function(arg, body);
    function name() {
        statement;
    }

对象
====

概述
----

-   一组属性（包括值或者函数）的集合

定义
----

    var obj = {'foo': 'bar'};
    var obj = {'method': fuction(){}};
    var obj = new Object;
