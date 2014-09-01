Title: Ansible状态管理
Date: 2014-06-19 17:51
Author: admin
Category: devops
Tags: ansible, devops
Slug: ansible状态管理

简介
====

就像所有服务器批量管理工具（puppet有DSL，salt有state）一样，ansible也有自己的状态管理组件，叫做playbook。所有这些类似的概念的东西都是让你用一种更简单的语言（而不是用脚本）来描述你的服务应该是什么样子的，然后这些工具根据你的描述将服务器变成你希望的样子。有了这么一层抽象后，服务部署和配置就变得更加的跨平台了，也提高了可复用性。但请注意，playbook不是万能的，因为playbook底层是在用模块来完成任务，因为模块有限，所以很多时候还是需要写shell脚本（ansible提供了script模块）来完成。

提前说明下要使用ansible的状态管理你需要学习哪些东西：

-   YAML语法，playbook用到的语法很少，这部分学习成本很低；
-   playbook的基本指令，这是基础；
-   模块的用法，这种重点；
-   jinja2语法，无论是在playbook还是在template里都支持jinja2语法，这是另一个重要的基础，关于jina2的语法不在本文范围内，具体参考[官方文档](http://jinja.pocoo.org/)。

概念
====

-   yaml，数据交换格式，类似json和xml，但是比它们更具有可读性，通常用于作为程序的配置文件。ansible的playbook配置使用yaml格式来表达。
-   task，由模块来完成的一个单位任务，如修改文件或者启动服务
-   play，一组task的集合，ansible会自上而下执行
-   handler，task可以触发一定的事件，而处理该事件的task即为handler
-   host，应用play的主机范围
-   user，在这些主机上以什么用户运行playbook
-   role，角色，一组playbook以及和其配合的元素（vars, files等）的集合

示例
====

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

YAML快餐
========

playbook是用yaml语法编写的，但你只需要了解如下几条简单的规则即可：

-   文档以`---`开头
-   `-`代表列表，也可以写成[a, b]
-   `:`代表字典，也可以写成{a: b}
-   如果字符冲突用双引号把对应字符串引起来

指令
====

host
----

定义playbook的执行主机范围，与命令模式下的ansible匹配规则一样。

remote\_user
------------

定义playbook的执行用户，执行任务也可以定义在任务级别，如：

      tasks:
        - name: test connection
          ping:
          remote_user: yourname
          sudo: yes

注意：也可以用sudo指令来说明所有或者部分任务以sudo方式执行

vars
----

定义变量

vars\_files
-----------

定义变量文件

tasks
-----

### 功能

定义任务列表，由模块来执行完成

### name

定义playbook或者task的名称

### notify

任务执行结果如果是发生更改了的则触发定义在handler的任务执行

handlers
--------

定义被触发的任务列表，由模块来执行完成

include
-------

-   能包含的包括task，handler和playbook
-   可以在include的时候传递变量

示例如下:

    tasks:
      - include: wordpress.yml
        vars:
            remote_user: timmy
            some_list_variable:
              - alpha
              - beta
              - gamma

roles
-----

定义主机对应的角色，角色是一组按照目录组合的配置，ansible自动完成文件搜索，去找对应目录下的main.yml文件来执行，具体目录结构如下：

-   defaults/ 默认的变量保存在这个目录下
-   files/ 文件
-   templates/ 模板
-   tasks/ 任务
-   handlers/ 处理器
-   vars/ 变量
-   meta/ 角色本身的信息，如通过dependencies指令指定依赖
-   library/ 私有模块

另外，你也可以给role传递变量。

这里重点说明下，role是使ansible的状态管理可复用很重要的一个概念，很多时候你只需要在自己的playbook里引用下别人的role即可，大家写的role可以相互共享，相互参考。官方也提供了ansible-galaxy这个命令用于安装社区分享的role，具体可参考[Galaxy官网](https://galaxy.ansible.com/)

pre\_task和post\_task
---------------------

在role被应用之前和之后执行的任务列表

变量
====

变量本来是个很简单的东西，但是变量在Playbook里是个很复杂的，其复杂的原因在于你不知道它从哪里来到哪里去了，下面我们也从这两个方面来剖析它。

从哪里来
--------

### inventory

在group和host中都可以定义变量，示例如下：

    [atlanta]
    host1 http_port=80 maxRequestsPerChild=808
    host2 http_port=303 maxRequestsPerChild=909
    [southeast:vars]
    some_server=foo.southeast.example.com
    halon_system_timeout=30
    self_destruct_countdown=60
    escape_pods=2

### vars和vars\_files

在playbook的开头可以用这俩指令来定义一些初始变量，这个可以参考上文中的playbook的demo

### include

通过在playbook的include指令可以其他task的时候，可以给文件传递变量，示例如下：

    tasks:
      - include: wordpress.yml user=timmy

### roles

当给一个主机应用角色的时候可以传递变量，然后在角色内使用这些变量，示例如下：

    - hosts: webservers
      roles:
        - common
        - { role: foo_app_instance, dir: '/opt/a',  port: 5000 }

### facts

默认在每次执行playbook前都获取设备信息，所有这些信息都可以作为变量应用到playbook中，要查看这些变量可以执行：

    ansible cloud -m setup

### register

把任务的输出定义为变量，然后用于其他任务，示例如下:

      tasks:
         - shell: /usr/bin/foo
           register: foo_result
           ignore_errors: True

### 内置变量

ansible内置了一些变量以方便主机之间相互调用各自的变量。这些变量包括：  
\*
hostvars允许你访问另一个主机的变量，当然前提是ansible已经收集到这个主机的变量了：

-   group\_names是当前主机所在的group列表
-   groups是所有inventory的group列表
-   inventory\_hostname是在inventory里定义的主机名
-   play\_hosts是当前的playbook范围内的主机列表
-   inventory\_dir和inventory\_file是定义inventory的目录和文件

### 命令行

在运行playbook的时候也可以传递一些变量供playbook使用，示例如下：

    ansible-playbook release.yml --extra-vars "hosts=vipers user=starbuck"

也可以从json文件里读取变量，示例如下；

    ansible-playbook main.yml -e "@vars.json"

用到哪里
--------

所有变量都可以在playbook或者jinja2模板中通过`{{ varname }}`中使用。另外，当变量和jinja2的管道配合起来的时候能提供各种灵活的条件判断和变量处理。具体看下边两个例子。

如果第一个任务执行失败了才会执行第二个任务，可以这么写：

    tasks:
      - shell: /usr/bin/foo
        register: result
        ignore_errors: True
      - debug: msg="it failed"
        when: result|failed

去重一个列表，可以这么写：

    {{ list | uniq }}

变量的优先级
------------

-   -e 命令行指定的最高
-   inventory文件定义的变量次之，其实inventory文件也分全局，group级别的和hosts级别的变量定义
-   fact变量次之
-   角色的default变量优先级最低

条件
====

when
----

可用于task，role和include，在满足条件时task才会被执行。至于when指令后跟的逻辑表达式也是标准的逻辑表达式，示例如下：

    tasks:
      - shell: echo "only on Red Hat 6, derivatives, and later"
        when: ansible_os_family == "RedHat" and ansible_lsb.major_release|int >= 6
      - shell: echo "This certainly is epic!"
        when: epic is defined

循环
====

标准遍历
--------

用with\_items可以遍历一个列表，注意这里只会遍历一层。示例如下：

    - name: add several users
      user: name={{ item }} state=present groups=wheel
      with_items:
         - testuser1
         - testuser2

嵌套遍历
--------

用with\_nested可以遍历一个列表，注意这里会遍历多层，直到最内层。示例如下：

    - name: give users access to multiple databases
      mysql_user: name={{ item[0] }} priv={{ item[1] }}.*:ALL append_privs=yes password=foo
      with_nested:
        - [ 'alice', 'bob', 'eve' ]
        - [ 'clientdb', 'employeedb', 'providerdb' ]

遍历字典
--------

用with\_dict可以遍历一个字典，用key和value来表示。示例如下：

变量文件

    ---
    users:
      alice:
        name: Alice Appleworth
        telephone: 123-456-7890
      bob:
        name: Bob Bananarama
        telephone: 987-654-3210

playbook文件

    tasks:
      - name: Print phone records
        debug: msg="User {{ item.key }} is {{ item.value.name }} ({{ item.value.telephone }})"
        with_dict: users

文件通配符循环
--------------

用with\_fileglob可以获取本地文件列表。示例如下：

        # copy each file over that matches the given pattern
        - copy: src={{ item }} dest=/etc/fooapp/ owner=root mode=600
          with_fileglob:
            - /playbooks/files/fooapp/*

对齐的列表
----------

用with\_together可以达到类似python里的zip函数的功能。示例如下：

变量文件：

    ---
    alpha: [ 'a', 'b', 'c', 'd' ]
    numbers:  [ 1, 2, 3, 4 ]

playbook文件

    tasks:
        - debug: msg="{{ item.0 }} and {{ item.1 }}"
          with_together:
            - alpha
            - numbers

子元素循环
----------

with\_subelements这个比较费解。

数字序列循环
------------

可以通过with\_sequence来生成一个数字序列，其参数包括：

-   start起始数字
-   end结束数字
-   stride步长
-   count个数
-   format输出的字符串

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

随机循环
--------

通过with\_random\_choice从一个序列里随机取一个元素。示例如下：

    - debug: msg={{ item }}
      with_random_choice:
         - "go through the door"
         - "drink from the goblet"
         - "press the red button"
         - "do nothing"

until循环
---------

这种循环由三个指令完成：  
\* until是一个条件表达式，如果满足条件循环结束  
\* retry是重试的次数  
\* delay是延迟时间

示例如下：

    - action: shell /usr/bin/foo
      register: result
      until: result.stdout.find("all systems go") != -1
      retries: 5
      delay: 10

循环直到找到文件
----------------

与with\_items类似，只是with\_first\_found找到列表里的第一个文件就会终止循环。示例如下：

    - name: INTERFACES | Create Ansible header for /etc/network/interfaces
      template: src={{ item }} dest=/etc/foo.conf
      with_first_found:
        - "{{ansible_virtualization_type}}_foo.conf"
        - "default_foo.conf"

循环一个task的输出
------------------

with\_lines指令后跟一个命令，ansible会遍历命令的输出。示例如下：

    - name: Example of looping over a command result
      shell: /usr/bin/frobnicate {{ item }}
      with_lines: /usr/bin/frobnications_per_host --param {{ inventory_hostname }}

带索引地循环列表
----------------

与with\_items类似，with\_indexed\_items会把列表索引和对应元素放到一个列表里。示例如下：

    - name: indexed loop demo
      debug: msg="at array position {{ item.0 }} there is a value {{ item.1 }}"
      with_indexed_items: some_list

扁平化循环列表
--------------

with\_flattened会先拍扁一个列表，然后执行with\_items。示例如下：

    - name: flattened loop demo
      yum: name={{ item }} state=installed
      with_flattened:
      - ['nc','git', ['nmap', 'vim']]

配合register循环列表
--------------------

register注册一个变量后，可以配合with\_items来遍历变量结果。示例如下：

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
