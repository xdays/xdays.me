Title: Docker基础教程之镜像构建
Date: 2017-04-03 06:06
Author: admin
Category: container
Tags: docker
Slug: Docker基础教程之镜像构建

这个系列已经好久没更新了，上一篇我总结了目前主流的镜像存储方案，这一篇总结下Docker的镜像构建

# Dockerfile

这是Docker官方的构建镜像的方案，其背后的思想和早在Docker诞生之前就已经广泛使用的配置管理工具(puppet, ansible, chef等)是一样的，就是说你只需要用一个文件来描述你想要的镜像是什么样的，然后Docker会依据Dockerfile来build出来目标镜像，并且你在Dockerfile里的指令就是对应最终镜像的每一层，这样就可以充分利用镜像分层复用的优势了。只不过不同点在于目前主流的配置管理工具在你的描述文件和实际运行的系统命令之间进行了一层抽象，这样就大大降低了学习的成本也便于复用代码(puppet的module, ansible的role)，而Dockerfile来的就比较直接，你直接写shell命令，其优缺点也就是shell的优缺点了。总结来说，Dockerfile通过定义一些指令提供了一种可重复构建镜像的方式。

这一小节我只针对常用的指令进行一个介绍，更多关于Dockerfile的每个指令的详细解释不是本文的重点，你可以在用的时候[参考这里](https://docs.docker.com/engine/reference/builder/)

```
FROM centos

ADD iami.txt /root/
RUN echo "Hello World!" > /root/iami.txt

EXPOSE 80
CMD ["cat", "/root/iami.txt"]
```

指令解释：

* FROM 指定要build的镜像是基于哪个镜像build的
* ADD 添加本地的文件到镜像中
* RUN 运行的shell命令的所做的修改都会体现在新build的镜像中
* EXPOSE 用于声明镜像对外暴露的端口
* CMD 指定启动镜像是的默认命令

然后我们运行如下命令新的镜像就build出来了

    docker build -t xdays/demo .

最后再说下Dockerfile的问题： 通过 `RUN` 指令来运行shell太过简陋，如果你之前用ansible之类的工具实现的复杂的软件构建流程，那么迁移到Docker上来是挺痛苦的，因为你要用shell把之前的逻辑全部写一遍。在这个过程中也会有些问题凸显，比如：

1. 如果你的软件需要编译安装，那么你就得先安装gcc和依赖库等软件包，而事实上一旦编译完成你并不需要这些软件包了，这样就导致最终build的image较大
2. 由于只能通过shell命令来构建镜像，那整个构建过程的可复用性就比较差，虽然Docker的分层机制能起到复用作用，但是还是不能瞒住更细粒度的复用，就像puppet的module，ansible的role。这是硬伤。

既然Dockerfile有其自身的不足，那我们接下来就来看看社区有什么好的解决方案。

# habitus/source-to-image

[Habitus](http://www.habitus.io/)和[source-to-image](https://github.com/openshift/source-to-image)这两个项目都是优化镜像构建流程的工具，他们本质上还是基于Dockerfile的。这里我只是说下我对这个两个项目解决问题的思路，并不会用实例来演示如何使用他们，因为我觉得他们并没有解决根本问题。

先来说下Habitus吧，我觉得Habitus最大的亮点在于其解决了上一节我提到的Dockerfile的第一个问题，它提出了artifacts的概念，巧妙的将一个镜像build的过程拆分成两个，用一个image来编译代码，然后将编译的结果文件从结果镜像中拷贝出来，然后再将这些文件打包的运行时的镜像中去作为最终的镜像，这样最终build出来的镜像就不会特别大，用流程图来描述如下：

    builer image(javac) --> artifacts(war or jar) -> runtime imaage(java + jar)

此外，Habitus还提供了两个功能也不错：

1. secrets，由Habitus内置的webserver来管理所有的隐私文件，然后镜像构建过程中通过curl或者wget来获取隐私文件，这样能保证隐私文件不会提交到代码仓库中去
2. squashing，合并image，可以彻底清除一些不必要的文件，减小镜像的体积。

再来看下source-to-image，基于workflow的描述：

1. s2i creates a container based on the build image and passes it a tar file that contains:
    a. The application source in src, excluding any files selected by .s2iignore
    b. The build artifacts in artifacts (if applicable - see incremental builds)
2. s2i sets the environment variables from .s2i/environment (optional)
3. s2i starts the container and runs its assemble script
4. s2i waits for the container to finish
5. s2i commits the container, setting the CMD for the output image to be the run script and tagging the image with the name provided.

我们就能明白source-to-image也是将一次build拆分成两次来做，只不过它的方式是对builder image定义了一个规范，需要你提前准备好builder image。

好了，总结一下吧！Habitus和source-to-image都解决了如何让最终build出来的镜像的体积变小，但是他们并没有从根本上能让镜像构建的过程变的在很小粒度上可复用。

另外，Docker已经将[Multi-Stage building](http://blog.alexellis.io/mutli-stage-docker-builds/)合并到了master分支 ，不久的将来Docker会原生支持了。

# Ansible/Puppet/Packer

下面我来看下如何解决构建过程可复用的问题，目前主流的配置管理系统都对Docker镜像构建有所支持，他们的优势就是可以充分利用现在配置管理系统的生态，实现最大程度的可复用性，而做出的牺牲就是完全摒弃了Dockerfile。具体支持方式如下：

* [ansible](https://www.ansible.com/) 直接用ansible来构建镜像
* [ansible-container](https://github.com/ansible/ansible-container) 管理应用的整个声明周期，包括build和部署等
* [puppet image_build](https://github.com/puppetlabs/puppetlabs-image_build) 用puppet来构建镜像
* [packer docker builder](https://www.packer.io/docs/builders/docker.html) 基于packer构建工具来构建镜像

## Ansible/Ansible-Container

虽然ansible-container是一个单独的致力于解决基于容器构建应用的整个生命周期，但是一向以小而美著称的ansible这次看上去并不是那么的“小”了，它把构建部署等过程绑定在一个工具里在我看来也不那么“美”了，所以我们还是先看看这个项目最终能发展成什么样子吧。

这里我主要说下如何把ansible纳入到镜像构建中来，我们目前用的一种简单粗暴的方式：直接在base镜像里集成了ansible，然后在构建镜像的时候把ansible的playbook以及相关的role全部放入到build的context里，然后在build完成后再删掉相关的不需要的文件。举例来说，先看下目录结构：

```
.
├── Dockerfile
├── README.md
├── roles
│   └── README.md
└── site.yml
```
其中在构建镜像前要将ansible相关的role拷贝到roles目录下。

Dockerfile如下：

```
FROM xdays/builder

WORKDIR /opt/xdays/
ADD . /tmp/
RUN cd /tmp && ansible-playbook site.yml

CMD ["/opt/xdays/start.sh"]
```

site.yml如下：

```
- hosts: localhost
  connection: local

  vars_files:
  - global.yml

  roles:
  - top
```

有几点需要说明下：

1. `xdays/builder` 这个image里已经安装了ansible，并且inventory里也包含了localhost
2. ansible的playbook需要的变量文件`global.yml`也需要在构建之前拷贝到当前目录下

这种方式的优点是可以复用ansible的role；缺点也很明显，首先是虽然也有Dockerfile但是build缓存已经不存在了，因为所有的构建构成都在`RUN cd /tmp && ansible-playbook site.yml` 这一层完成的，其次把ansible安装到base镜像里会增大最终build出来的镜像。

## Puppet

Puppet的image_build模块构建镜像的方式和我们的做法类似，也是将puppet安装到镜像里，然后构建过程中将puppet的manifest打包到build的context里，只不过`image_build`模块实现了将puppet的manifest转成Dockerfile的功能，这样就能充分里利用Dockerfile的缓存机制

官方给的例子也很好理解:

```
puppet module install puppetlabs/image_build
git clone https://github.com/puppetlabs/puppetlabs-image_build.git
cd puppetlabs-image_build/examples/nginx
puppet docker build
puppet docker dockerfile
```

这种方式要比上一节我们使用的ansible的方式要好，但还是有一个缺点就是build出来的镜像相对比较大。

## Packer

[Packer](https://www.packer.io/)是一个通用镜像构建工具，其大概思路就是将镜像构建拆分为builder， provisioner和post-processor三个阶段：

* builder决定了镜像的格式，比如AWS,  Azure, GCP。而Docker也是其中的一种
* provisioner决定了怎么构建镜像，其闪光点在于其只定义了怎么调用provisioner框架，具体构建的细节还是由provisioner自己来决定，这样足够开放，让所有的配置管理工具大放光彩
* post-processor决定了镜像构建完成如何处理，比如上传到AWS还是上传到Docker Hub。

Packer构建Docker镜像的方式是从base镜像启动一个container然后对这个container运行provisioner，最后将这个container提交为镜像，这种方式完全也脱离了Dockerfile，但是有没有将配置管理工具打包到base镜像里，这样既保证了build的镜像体积较小也充分利用了配置管理工具。当然缺点还是没有办法充分利用Dockerfile的build缓存。

下面举个简单的例子，新建template.json文件如下：

```
{
  "variables": {
    "ansible_host": "default",
    "ansible_connection": "docker"
  },
  "builders": [
    {
      "type": "docker",
      "image": "ubuntu",
      "commit": "true",
      "run_command": [
        "-d",
        "-i",
        "-t",
        "--name",
        "{{user `ansible_host`}}",
        "{{.Image}}",
        "/bin/bash"
      ]
    }
  ],
  "provisioners": [
    {
      "type": "shell",
      "inline": [
        "apt-get update",
        "apt-get install python -yq"
      ]
    },
    {
      "type": "ansible",
      "user": "root",
      "playbook_file": "./playbook.yml",
      "extra_arguments": [
        "--extra-vars",
        "ansible_host={{user `ansible_host`}} ansible_connection={{user `ansible_connection`}}"
      ]
    }
  ],
  "post-processors": [
    [
      {
        "type": "docker-tag",
        "repository": "xdays/demo"
      }
    ]
  ]
}
```

然后编辑playbook.yml如下：

```
---
- hosts: all
  tasks:
    - name: create a foobar file
      copy:
        dest: /root/foobar
        content: Hello World!
        owner: root
```

最后运行packer:

    packer build template.json

至此，Packer来构建Docker镜像也介绍完了。另外多说依据，build缓存在Packer的开发计划之中， 官方文档的描述如下：

> Dockerfiles will snapshot the container at each step, allowing you to go back to any step in the history of building. Packer doesn't do this yet, but inter-step snapshotting is on the way.

# 总结

最后总结下吧，个人认为Packer是目前最接近我所期待的Docker镜像工具。当然我也更期待Dockerfile能够在未来的版本中和目前主流的配置管理工具更友好一些。
