---
title: Docker基础教程
date: 2016-11-04
author: admin
category: container
tags: docker
slug: docker基础教程
---

回首一看，又有一个多月没有更新博客了。最近工作上发生了一些变动：公司裁员，无论主动的还是被动的，多数人拿了补偿走人了；而因为我做的还可以公司希望我留下，然而当我选择离开时公司认为我是主动离职不支付赔偿，我问了下律师被告知公司从法律上没有什么问题，也就作罢。趁工作交接之际，我整理下近两年多自己的容器领域的技术积累，算是给自己的一个总结，如果能对于别人有所帮助，幸甚至哉！

我要总结的第一个系列是Docker，我从14年开始使用Docker，大概是0.5或者0.6的版本，一路过来见证了Docker从一个小而美发展成了大而全的项目，也见证了整个容器生态圈的蓬勃发展。简单整理了下这个系列的大纲：


* [基本概念](//docker基础教程之基本概念/)
    * cgroups
    * namespace
    * veth
    * bridge
    * nat
    * copy-on-write
    * image
    * container
* [镜像存储](//docker基础教程之镜像存储/)
    * registry
    * nexus
    * harbor
* [镜像构建](//docker基础教程之镜像构建/)
    * docker build
    * puppet
    * ansible
    * packer
* [镜像安全](//docker基础教程之镜像安全/)
    * anchore
    * clair

声明：我只是一个具备基础开发能力的运维，我没有能力解释清楚容器技术的底层原理，所有本系列的大多数知识都是我从实践中得来，但也不能保证百分百正确，如果你在阅读过程中发现错误或者疑问欢迎沟通。 
