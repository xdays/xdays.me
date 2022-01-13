---
title: Ansible状态管理
date: 2014-06-19
author: admin
category: devops
tags: ['ansible', 'devops']
slug: ansible状态管理
---

# 简介

就像所有服务器批量管理工具（puppet 有 DSL，salt 有 state）一样，ansible 也有自己的状态管理组件，叫做 playbook。所有这些类似的概念的东西都是让你用一种更简单的语言（而不是用脚本）来描述你的服务应该是什么样子的，然后这些工具根据你的描述将服务器变成你希望的样子。有了这么一层抽象后，服务部署和配置就变得更加的跨平台了，也提高了可复用性。但请注意，playbook 不是万能的，因为 playbook 底层是在用模块来完成任务，因为模块有限，所以很多时候还是需要写 shell 脚本（ansible 提供了 script 模块）来完成。

提前说明下要使用 ansible 的状态管理你需要学习哪些东西：

- YAML 语法，playbook 用到的语法很少，这部分学习成本很低；
- playbook 的基本指令，这是基础；
- 模块的用法，这种重点；
- jinja2 语法，无论是在 playbook 还是在 template 里都支持 jinja2 语法，这是另一个重要的基础，关于 jina2 的语法不在本文范围内，具体参考[官方文档](http://jinja.pocoo.org/)。

# 概念

- yaml，数据交换格式，类似 json 和 xml，但是比它们更具有可读性，通常用于作为程序的配置文件。ansible 的 playbook 配置使用 yaml 格式来表达。
- task，由模块来完成的一个单位任务，如修改文件或者启动服务
- play，一组 task 的集合，ansible 会自上而下执行
- handler，task 可以触发一定的事件，而处理该事件的 task 即为 handler
- host，应用 play 的主机范围
- user，在这些主机上以什么用户运行 playbook
- role，角色，一组 playbook 以及和其配合的元素（vars, files 等）的集合

# 示例

    ---
    - hosts: webservers
      vars:
        http_port: 80
        max_clients: 200
      remote_user: root
      tasks:
      - name: ensure apache is at the latest version
        yum: pkg=httpd state=latest
      - name: write the apache config file
        template: src=/srv/httpd.j2 dest=/etc/httpd.conf
        notify:
        - restart apache
      - name: ensure apache is running
        service: name=httpd state=started
      handlers:
        - name: restart apache
          service: name=httpd state=restarted

# YAML 快餐

playbook 是用 yaml 语法编写的，但你只需要了解如下几条简单的规则即可：

- 文档以`---`开头
- `-`代表列表，也可以写成[a, b]
- `:`代表字典，也可以写成{a: b}
- 如果字符冲突用双引号把对应字符串引起来

# 指令

## host

定义 playbook 的执行主机范围，与命令模式下的 ansible 匹配规则一样。

## remote_user

定义 playbook 的执行用户，执行任务也可以定义在任务级别，如：

      tasks:
        - name: test connection
          ping:
          remote_user: yourname
          sudo: yes

注意：也可以用 sudo 指令来说明所有或者部分任务以 sudo 方式执行

## vars

定义变量

## vars_files

定义变量文件

## tasks

### 功能

定义任务列表，由模块来执行完成

### name

定义 playbook 或者 task 的名称

### notify

任务执行结果如果是发生更改了的则触发定义在 handler 的任务执行

## handlers

定义被触发的任务列表，由模块来执行完成

## include

- 能包含的包括 task，handler 和 playbook
- 可以在 include 的时候传递变量

示例如下:

    tasks:
      - include: wordpress.yml
        vars:
            remote_user: timmy
            some_list_variable:
              - alpha
              - beta
              - gamma

## roles

定义主机对应的角色，角色是一组按照目录组合的配置，ansible 自动完成文件搜索，去找对应目录下的 main.yml 文件来执行，具体目录结构如下：

- defaults/ 默认的变量保存在这个目录下
- files/ 文件
- templates/ 模板
- tasks/ 任务
- handlers/ 处理器
- vars/ 变量
- meta/ 角色本身的信息，如通过 dependencies 指令指定依赖
- library/ 私有模块

另外，你也可以给 role 传递变量。

这里重点说明下，role 是使 ansible 的状态管理可复用很重要的一个概念，很多时候你只需要在自己的 playbook 里引用下别人的 role 即可，大家写的 role 可以相互共享，相互参考。官方也提供了 ansible-galaxy 这个命令用于安装社区分享的 role，具体可参考[Galaxy 官网](https://galaxy.ansible.com/)

## pre_task 和 post_task

在 role 被应用之前和之后执行的任务列表

# 变量

变量本来是个很简单的东西，但是变量在 Playbook 里是个很复杂的，其复杂的原因在于你不知道它从哪里来到哪里去了，下面我们也从这两个方面来剖析它。

## 从哪里来

### inventory

在 group 和 host 中都可以定义变量，示例如下：

    [atlanta]
    host1 http_port=80 maxRequestsPerChild=808
    host2 http_port=303 maxRequestsPerChild=909
    [southeast:vars]
    some_server=foo.southeast.example.com
    halon_system_timeout=30
    self_destruct_countdown=60
    escape_pods=2

### vars 和 vars_files

在 playbook 的开头可以用这俩指令来定义一些初始变量，这个可以参考上文中的 playbook 的 demo

### include

通过在 playbook 的 include 指令可以其他 task 的时候，可以给文件传递变量，示例如下：

    tasks:
      - include: wordpress.yml user=timmy

### roles

当给一个主机应用角色的时候可以传递变量，然后在角色内使用这些变量，示例如下：

    - hosts: webservers
      roles:
        - common
        - { role: foo_app_instance, dir: '/opt/a',  port: 5000 }

### facts

默认在每次执行 playbook 前都获取设备信息，所有这些信息都可以作为变量应用到 playbook 中，要查看这些变量可以执行：

    ansible cloud -m setup

### register

把任务的输出定义为变量，然后用于其他任务，示例如下:

      tasks:
         - shell: /usr/bin/foo
           register: foo_result
           ignore_errors: True

### 内置变量

ansible 内置了一些变量以方便主机之间相互调用各自的变量。这些变量包括：  
\*
hostvars 允许你访问另一个主机的变量，当然前提是 ansible 已经收集到这个主机的变量了：

- group_names 是当前主机所在的 group 列表
- groups 是所有 inventory 的 group 列表
- inventory_hostname 是在 inventory 里定义的主机名
- play_hosts 是当前的 playbook 范围内的主机列表
- inventory_dir 和 inventory_file 是定义 inventory 的目录和文件

### 命令行

在运行 playbook 的时候也可以传递一些变量供 playbook 使用，示例如下：

    ansible-playbook release.yml --extra-vars "hosts=vipers user=starbuck"

也可以从 json 文件里读取变量，示例如下；

    ansible-playbook main.yml -e "@vars.json"

## 用到哪里

所有变量都可以在 playbook 或者 jinja2 模板中通过`{{ varname }}`中使用。另外，当变量和 jinja2 的管道配合起来的时候能提供各种灵活的条件判断和变量处理。具体看下边两个例子。

如果第一个任务执行失败了才会执行第二个任务，可以这么写：

    tasks:
      - shell: /usr/bin/foo
        register: result
        ignore_errors: True
      - debug: msg="it failed"
        when: result|failed

去重一个列表，可以这么写：

    {{ list | uniq }}

## 变量的优先级

- -e 命令行指定的最高
- inventory 文件定义的变量次之，其实 inventory 文件也分全局，group 级别的和 hosts 级别的变量定义
- fact 变量次之
- 角色的 default 变量优先级最低

# 条件

## when

可用于 task，role 和 include，在满足条件时 task 才会被执行。至于 when 指令后跟的逻辑表达式也是标准的逻辑表达式，示例如下：

    tasks:
      - shell: echo "only on Red Hat 6, derivatives, and later"
        when: ansible_os_family == "RedHat" and ansible_lsb.major_release|int >= 6
      - shell: echo "This certainly is epic!"
        when: epic is defined

# 循环

## 标准遍历

用 with_items 可以遍历一个列表，注意这里只会遍历一层。示例如下：

    - name: add several users
      user: name={{ item }} state=present groups=wheel
      with_items:
         - testuser1
         - testuser2

## 嵌套遍历

用 with_nested 可以遍历一个列表，注意这里会遍历多层，直到最内层。示例如下：

    - name: give users access to multiple databases
      mysql_user: name={{ item[0] }} priv={{ item[1] }}.*:ALL append_privs=yes password=foo
      with_nested:
        - [ 'alice', 'bob', 'eve' ]
        - [ 'clientdb', 'employeedb', 'providerdb' ]

## 遍历字典

用 with_dict 可以遍历一个字典，用 key 和 value 来表示。示例如下：

变量文件

    ---
    users:
      alice:
        name: Alice Appleworth
        telephone: 123-456-7890
      bob:
        name: Bob Bananarama
        telephone: 987-654-3210

playbook 文件

    tasks:
      - name: Print phone records
        debug: msg="User {{ item.key }} is {{ item.value.name }} ({{ item.value.telephone }})"
        with_dict: users

## 文件通配符循环

用 with_fileglob 可以获取本地文件列表。示例如下：

        # copy each file over that matches the given pattern
        - copy: src={{ item }} dest=/etc/fooapp/ owner=root mode=600
          with_fileglob:
            - /playbooks/files/fooapp/*

## 对齐的列表

用 with_together 可以达到类似 python 里的 zip 函数的功能。示例如下：

变量文件：

    ---
    alpha: [ 'a', 'b', 'c', 'd' ]
    numbers:  [ 1, 2, 3, 4 ]

playbook 文件

    tasks:
        - debug: msg="{{ item.0 }} and {{ item.1 }}"
          with_together:
            - alpha
            - numbers

## 子元素循环

with_subelements 这个比较费解。

## 数字序列循环

可以通过 with_sequence 来生成一个数字序列，其参数包括：

- start 起始数字
- end 结束数字
- stride 步长
- count 个数
- format 输出的字符串

示例如下：

    ---
    - hosts: all
      tasks:
        # create groups
        - group: name=evens state=present
        - group: name=odds state=present
        # create some test users
        - user: name={{ item }} state=present groups=evens
          with_sequence: start=0 end=32 format=testuser%02x
        # create a series of directories with even numbers for some reason
        - file: dest=/var/stuff/{{ item }} state=directory
          with_sequence: start=4 end=16 stride=2
        # a simpler way to use the sequence plugin
        # create 4 groups
        - group: name=group{{ item }} state=present
          with_sequence: count=4

## 随机循环

通过 with_random_choice 从一个序列里随机取一个元素。示例如下：

    - debug: msg={{ item }}
      with_random_choice:
         - "go through the door"
         - "drink from the goblet"
         - "press the red button"
         - "do nothing"

## until 循环

这种循环由三个指令完成：  
\* until 是一个条件表达式，如果满足条件循环结束  
\* retry 是重试的次数  
\* delay 是延迟时间

示例如下：

    - action: shell /usr/bin/foo
      register: result
      until: result.stdout.find("all systems go") != -1
      retries: 5
      delay: 10

## 循环直到找到文件

与 with_items 类似，只是 with_first_found 找到列表里的第一个文件就会终止循环。示例如下：

    - name: INTERFACES | Create Ansible header for /etc/network/interfaces
      template: src={{ item }} dest=/etc/foo.conf
      with_first_found:
        - "{{ansible_virtualization_type}}_foo.conf"
        - "default_foo.conf"

## 循环一个 task 的输出

with_lines 指令后跟一个命令，ansible 会遍历命令的输出。示例如下：

    - name: Example of looping over a command result
      shell: /usr/bin/frobnicate {{ item }}
      with_lines: /usr/bin/frobnications_per_host --param {{ inventory_hostname }}

## 带索引地循环列表

与 with_items 类似，with_indexed_items 会把列表索引和对应元素放到一个列表里。示例如下：

    - name: indexed loop demo
      debug: msg="at array position {{ item.0 }} there is a value {{ item.1 }}"
      with_indexed_items: some_list

## 扁平化循环列表

with_flattened 会先拍扁一个列表，然后执行 with_items。示例如下：

    - name: flattened loop demo
      yum: name={{ item }} state=installed
      with_flattened:
      - ['nc','git', ['nmap', 'vim']]

## 配合 register 循环列表

register 注册一个变量后，可以配合 with_items 来遍历变量结果。示例如下：

    - shell: echo "{{ item }}"
      with_items:
        - one
        - two
      register: echo
    - name: Fail if return code is not 0
      fail:
        msg: "The command ({{ item.cmd }}) did not have a 0 return code"
      when: item.rc != 0
      with_items: echo.results
