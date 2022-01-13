---
title: Docker基础教程之镜像构建
date: 2017-04-03
author: admin
category: container
tags: ['docker']
slug: Docker基础教程之镜像构建
---

这个系列已经好久没更新了，上一篇我总结了目前主流的镜像存储方案，这一篇总结下 Docker 的镜像构建

# Dockerfile

这是 Docker 官方的构建镜像的方案，其背后的思想和早在 Docker 诞生之前就已经广泛使用的配置管理工具(puppet, ansible, chef 等)是一样的，就是说你只需要用一个文件来描述你想要的镜像是什么样的，然后 Docker 会依据 Dockerfile 来 build 出来目标镜像，并且你在 Dockerfile 里的指令就是对应最终镜像的每一层，这样就可以充分利用镜像分层复用的优势了。只不过不同点在于目前主流的配置管理工具在你的描述文件和实际运行的系统命令之间进行了一层抽象，这样就大大降低了学习的成本也便于复用代码(puppet 的 module, ansible 的 role)，而 Dockerfile 来的就比较直接，你直接写 shell 命令，其优缺点也就是 shell 的优缺点了。总结来说，Dockerfile 通过定义一些指令提供了一种可重复构建镜像的方式。

这一小节我只针对常用的指令进行一个介绍，更多关于 Dockerfile 的每个指令的详细解释不是本文的重点，你可以在用的时候[参考这里](https://docs.docker.com/engine/reference/builder/)

```
FROM centos

ADD iami.txt /root/
RUN echo "Hello World!" > /root/iami.txt

EXPOSE 80
CMD ["cat", "/root/iami.txt"]
```

指令解释：

- FROM 指定要 build 的镜像是基于哪个镜像 build 的
- ADD 添加本地的文件到镜像中
- RUN 运行的 shell 命令的所做的修改都会体现在新 build 的镜像中
- EXPOSE 用于声明镜像对外暴露的端口
- CMD 指定启动镜像是的默认命令

然后我们运行如下命令新的镜像就 build 出来了

    docker build -t xdays/demo .

最后再说下 Dockerfile 的问题： 通过 `RUN` 指令来运行 shell 太过简陋，如果你之前用 ansible 之类的工具实现的复杂的软件构建流程，那么迁移到 Docker 上来是挺痛苦的，因为你要用 shell 把之前的逻辑全部写一遍。在这个过程中也会有些问题凸显，比如：

1. 如果你的软件需要编译安装，那么你就得先安装 gcc 和依赖库等软件包，而事实上一旦编译完成你并不需要这些软件包了，这样就导致最终 build 的 image 较大
2. 由于只能通过 shell 命令来构建镜像，那整个构建过程的可复用性就比较差，虽然 Docker 的分层机制能起到复用作用，但是还是不能瞒住更细粒度的复用，就像 puppet 的 module，ansible 的 role。这是硬伤。

既然 Dockerfile 有其自身的不足，那我们接下来就来看看社区有什么好的解决方案。

# habitus/source-to-image

[Habitus](http://www.habitus.io/)和[source-to-image](https://github.com/openshift/source-to-image)这两个项目都是优化镜像构建流程的工具，他们本质上还是基于 Dockerfile 的。这里我只是说下我对这个两个项目解决问题的思路，并不会用实例来演示如何使用他们，因为我觉得他们并没有解决根本问题。

先来说下 Habitus 吧，我觉得 Habitus 最大的亮点在于其解决了上一节我提到的 Dockerfile 的第一个问题，它提出了 artifacts 的概念，巧妙的将一个镜像 build 的过程拆分成两个，用一个 image 来编译代码，然后将编译的结果文件从结果镜像中拷贝出来，然后再将这些文件打包的运行时的镜像中去作为最终的镜像，这样最终 build 出来的镜像就不会特别大，用流程图来描述如下：

    builer image(javac) --> artifacts(war or jar) -> runtime imaage(java + jar)

此外，Habitus 还提供了两个功能也不错：

1. secrets，由 Habitus 内置的 webserver 来管理所有的隐私文件，然后镜像构建过程中通过 curl 或者 wget 来获取隐私文件，这样能保证隐私文件不会提交到代码仓库中去
2. squashing，合并 image，可以彻底清除一些不必要的文件，减小镜像的体积。

再来看下 source-to-image，基于 workflow 的描述：

1. s2i creates a container based on the build image and passes it a tar file that contains:
   a. The application source in src, excluding any files selected by .s2iignore
   b. The build artifacts in artifacts (if applicable - see incremental builds)
2. s2i sets the environment variables from .s2i/environment (optional)
3. s2i starts the container and runs its assemble script
4. s2i waits for the container to finish
5. s2i commits the container, setting the CMD for the output image to be the run script and tagging the image with the name provided.

我们就能明白 source-to-image 也是将一次 build 拆分成两次来做，只不过它的方式是对 builder image 定义了一个规范，需要你提前准备好 builder image。

好了，总结一下吧！Habitus 和 source-to-image 都解决了如何让最终 build 出来的镜像的体积变小，但是他们并没有从根本上能让镜像构建的过程变的在很小粒度上可复用。

另外，Docker 已经将[Multi-Stage building](http://blog.alexellis.io/mutli-stage-docker-builds/)合并到了 master 分支 ，不久的将来 Docker 会原生支持了。

# Ansible/Puppet/Packer

下面我来看下如何解决构建过程可复用的问题，目前主流的配置管理系统都对 Docker 镜像构建有所支持，他们的优势就是可以充分利用现在配置管理系统的生态，实现最大程度的可复用性，而做出的牺牲就是完全摒弃了 Dockerfile。具体支持方式如下：

- [ansible](https://www.ansible.com/) 直接用 ansible 来构建镜像
- [ansible-container](https://github.com/ansible/ansible-container) 管理应用的整个声明周期，包括 build 和部署等
- [puppet image_build](https://github.com/puppetlabs/puppetlabs-image_build) 用 puppet 来构建镜像
- [packer docker builder](https://www.packer.io/docs/builders/docker.html) 基于 packer 构建工具来构建镜像

## Ansible/Ansible-Container

虽然 ansible-container 是一个单独的致力于解决基于容器构建应用的整个生命周期，但是一向以小而美著称的 ansible 这次看上去并不是那么的“小”了，它把构建部署等过程绑定在一个工具里在我看来也不那么“美”了，所以我们还是先看看这个项目最终能发展成什么样子吧。

这里我主要说下如何把 ansible 纳入到镜像构建中来，我们目前用的一种简单粗暴的方式：直接在 base 镜像里集成了 ansible，然后在构建镜像的时候把 ansible 的 playbook 以及相关的 role 全部放入到 build 的 context 里，然后在 build 完成后再删掉相关的不需要的文件。举例来说，先看下目录结构：

```
.
├── Dockerfile
├── README.md
├── roles
│   └── README.md
└── site.yml
```

其中在构建镜像前要将 ansible 相关的 role 拷贝到 roles 目录下。

Dockerfile 如下：

```
FROM xdays/builder

WORKDIR /opt/xdays/
ADD . /tmp/
RUN cd /tmp && ansible-playbook site.yml

CMD ["/opt/xdays/start.sh"]
```

site.yml 如下：

```
- hosts: localhost
  connection: local

  vars_files:
  - global.yml

  roles:
  - top
```

有几点需要说明下：

1. `xdays/builder` 这个 image 里已经安装了 ansible，并且 inventory 里也包含了 localhost
2. ansible 的 playbook 需要的变量文件`global.yml`也需要在构建之前拷贝到当前目录下

这种方式的优点是可以复用 ansible 的 role；缺点也很明显，首先是虽然也有 Dockerfile 但是 build 缓存已经不存在了，因为所有的构建构成都在`RUN cd /tmp && ansible-playbook site.yml` 这一层完成的，其次把 ansible 安装到 base 镜像里会增大最终 build 出来的镜像。

## Puppet

Puppet 的 image_build 模块构建镜像的方式和我们的做法类似，也是将 puppet 安装到镜像里，然后构建过程中将 puppet 的 manifest 打包到 build 的 context 里，只不过`image_build`模块实现了将 puppet 的 manifest 转成 Dockerfile 的功能，这样就能充分里利用 Dockerfile 的缓存机制

官方给的例子也很好理解:

```
puppet module install puppetlabs/image_build
git clone https://github.com/puppetlabs/puppetlabs-image_build.git
cd puppetlabs-image_build/examples/nginx
puppet docker build
puppet docker dockerfile
```

这种方式要比上一节我们使用的 ansible 的方式要好，但还是有一个缺点就是 build 出来的镜像相对比较大。

## Packer

[Packer](https://www.packer.io/)是一个通用镜像构建工具，其大概思路就是将镜像构建拆分为 builder， provisioner 和 post-processor 三个阶段：

- builder 决定了镜像的格式，比如 AWS, Azure, GCP。而 Docker 也是其中的一种
- provisioner 决定了怎么构建镜像，其闪光点在于其只定义了怎么调用 provisioner 框架，具体构建的细节还是由 provisioner 自己来决定，这样足够开放，让所有的配置管理工具大放光彩
- post-processor 决定了镜像构建完成如何处理，比如上传到 AWS 还是上传到 Docker Hub。

Packer 构建 Docker 镜像的方式是从 base 镜像启动一个 container 然后对这个 container 运行 provisioner，最后将这个 container 提交为镜像，这种方式完全也脱离了 Dockerfile，但是有没有将配置管理工具打包到 base 镜像里，这样既保证了 build 的镜像体积较小也充分利用了配置管理工具。当然缺点还是没有办法充分利用 Dockerfile 的 build 缓存。

下面举个简单的例子，新建 template.json 文件如下：

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

然后编辑 playbook.yml 如下：

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

最后运行 packer:

    packer build template.json

至此，Packer 来构建 Docker 镜像也介绍完了。另外多说依据，build 缓存在 Packer 的开发计划之中， 官方文档的描述如下：

> Dockerfiles will snapshot the container at each step, allowing you to go back to any step in the history of building. Packer doesn't do this yet, but inter-step snapshotting is on the way.

# 总结

最后总结下吧，个人认为 Packer 是目前最接近我所期待的 Docker 镜像工具。当然我也更期待 Dockerfile 能够在未来的版本中和目前主流的配置管理工具更友好一些。
