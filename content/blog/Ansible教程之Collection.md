---
title: Ansible教程之Collection
date: 2020-09-28
author: admin
category: devops
tags: ['ansible', 'devops']
slug: ansible教程之collection
---

# 简介

Ansible 最新版(v2.10)已经切换到 collection 了，简单来说 collection 是一种分发 playbook, role, module 和 plugin 的方式，相比之前所有的东西都在一个仓库里管理，每个 collection 都有自己单独的仓库更便于维护。

# 创建

创建 Collection 很简单，只需要按照规范把响应的资源放进去就可以了，标准目录结构：

```
collection/
├── docs/
├── galaxy.yml
├── meta/
│   └── runtime.yml
├── plugins/
│   ├── modules/
│   │   └── module1.py
│   ├── inventory/
│   └── .../
├── README.md
├── roles/
│   ├── role1/
│   ├── role2/
│   └── .../
├── playbooks/
│   ├── files/
│   ├── vars/
│   ├── templates/
│   └── tasks/
└── tests/
```

Collection 开发文档可以[参考这里](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html)

可以参考下[我的 Ansible Collection)(https://github.com/xdays/ansible)

# 安装

```
# install from galaxy
ansible-galaxy collection install my_namespace.my_collection:==1.0.0-beta.1

# install from github
ansible-galaxy collection install git+https://github.com/organization/repo_name.git,devel

# list installed collections
ansible-galaxy collection list
```

# 使用

可以使用模块的绝对路径来引用模块:

```
- hosts: all
  tasks:
    - my_namespace.my_collection.mymodule:
        option1: value
```

因为每次都写 collection 的 namespace 有些麻烦，可以预先声明 collection 的 namespace

在 role 里可以写在 meta data 里:

```
# myrole/meta/main.yml
collections:
  - my_namespace.first_collection
  - my_namespace.second_collection
  - other_namespace.other_collection
```

在 playbook 里可以这么写:

```
- hosts: all
  collections:
    - my_namespace.my_collection

  tasks:
    - import_role:
        name: role1

    - mymodule:
        option1: value
```

这样就可以像之前的版本一样继续使用模块了。

# Inventory

因为在最新版里 inventory 脚本也都是放在了 collection 里，使用 inventory 脚本也和之前不一样了，这里整理了下 aws 的配置方法

1. 在配置文件`ansible.cfg`里声明`aws_ec2`这个 plugin

```
[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml, aws_ec2
```

2. 编写 inventory 配置文件，注意这里一定要以`_aws_ec2.yml`结尾才行，我这里命名为`test_aws_ec2.yml`

```
plugin: aws_ec2
regions:
  - us-west-2
cache: yes
keyed_groups:
  - key: tags
    prefix: tag
  - key: architecture
    prefix: arch
  - key: instance_type
    prefix: aws_instance_type
  - key: placement.region
    prefix: aws_region
  - key: image_id
    prefix: aws_image
  - key: hypervisor
    prefix: aws_hypervisor
  - key: 'security_groups|json_query("[].group_id")'
    prefix: 'security_groups'
hostnames:
  - private-ip-address
  - ip-address
```

[配置参考官方文档](https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html)

3. 使用这个 inventory plugin 和以前的方法一样，可以直接放到配置文件里定义的 inventory 目录里，也可以直接命令行引用

```
# 在配置文件里定义inventory目录
inventory=/etc/ansible/inventory/

# 命令行直接引用
ansible -i test_aws_ec2.yml all --list-hosts
```
