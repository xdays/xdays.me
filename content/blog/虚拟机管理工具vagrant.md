---
title: 虚拟机管理工具vagrant
date: 2014-03-08
author: admin
category: devops
tags: ['devops', 'vagrant']
slug: 虚拟机管理工具vagrant
---

# 简介

vagrant 是一个基于业界成熟的虚拟化技术打造可配置，可重新生成和可移植的工作环境的工具，一个配置文件完成所有状态定义。

# 特性

- 简单，一个配置文件搞定
- 可通过多种方式自定义虚拟机配置，如 shell 脚本，ansible 等
- 网络配置，支持私有，共有网络配置
- 目录同步，保持 guest 和 host 文件同步，默认将当前目录映射到虚拟机的/vagrant 下
- 多虚拟机支持，构建自己的集群测试环境
- 多中虚拟技术支持，如 virtualbox，vmware，AWS 和 docker
- 插件机制，扩展灵活

# 概念

- box 就是已经制作好的虚拟机，倒入后保存在\~/vagrang.d 目录下，和标准的虚拟机区别就是加入了一些为支持 vagrant 管理的配置，如公钥
- Vagrantfile 描述和配置要创建的虚拟机的配置

# 安装

    sudo apt-get install vagrant

**注意** 最新的版本要到其官网下载

# 配置

## 添加 box

    vagrant box add name url

其中，name 为 box 的名字，url 为 box 的路径可远程可本地

## 初始化环境

    vagrant init

生成默认的 Vagrantfile

## 修改配置文件 Vagrantfile

详细的配置参考[官方文档](http://docs.vagrantup.com/v2/)

### 单机配置

    Vagrant.configure("2") do |config|
      config.vm.box = "base" #定义此虚拟机是从哪个box生成
      config.vm.provision :shell, :path => "bootstrap.sh" #通过shell配置
      config.vm.network :forwarded_port, host: 8080, guest: 80 #端口映射
      config.vm.network "private_network", ip: "192.168.110.100" #私有网络配置
      #awesome configuration goes here...
    end

### 多机配置

    Vagrant.configure("2") do |config|
      config.vm.provision "shell", inline: "echo Hello"
      config.vm.define "web" do |web|
        web.vm.box = "apache"
        #awesome configuration goes here...
      end
      config.vm.define "db" do |db|
        db.vm.box = "mysql"
        #awesome configuration goes here...
      end
    end

# 使用

- 开/关机 vagrant up/halt
- 重启 vagrant reload
- 状态 vagrant status
- 登录 vagrant ssh
- 销毁 vagrant destroy

# 参考链接

- [官方文档](http://docs.vagrantup.com/v2/)
- [box 资源站](http://www.vagrantbox.es/)
- [如何制作 box 文件](http://www.skoblenick.com/vagrant/creating-a-custom-box-from-scratch/)
