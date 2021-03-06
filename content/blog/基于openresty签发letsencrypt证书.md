---
title: 基于OpenResty自动签发Let's Encrypt证书
date: 2017-03-30
author: admin
category: devops
tags: ['openresty', 'letsencrypt']
slug: 基于openresty签发letsencrypt证书
---

# 安装 OpenResty

```
curl -so /etc/yum.repos.d/openresty.repo  https://openresty.org/package/centos/openresty.repo && \
    yum install -y openresty gcc make diffutils openssl && \
```

OpenResty 所有的文件以及依赖包都安装在 `/usr/local/openresty` 目录下

# 安装配置 lua-resty-auto-ssl

## 安装 Luarocks

Luarocks 是 Lua 的包管理工具，很多 OpenResty 的包都可以通过 luarocks 来安装。

```
curl -so - http://luarocks.github.io/luarocks/releases/luarocks-3.3.1.tar.gz | tar xzf - && \
    cd luarocks-3.3.1 && ./configure --prefix=/usr/local/openresty/luajit/ \
    --with-lua=/usr/local/openresty/luajit/ \
    --with-lua-include=/usr/local/openresty/luajit/include/luajit-2.1/ && \
    make build && make install && cd .. && rm -rf ../luarocks-* && \
    ln -s /usr/local/openresty/luajit/bin/luarocks /usr/local/bin/
```

## 安装 lua-resty-auto-ssl

```
luarocks install lua-resty-auto-ssl
```

## 配置 lua-resty-auto-ssl

编辑配置文件 `vim conf/nginx.conf` ，内容如下：

```
env DOMAINS;

events {
  worker_connections 1024;
}

http {
  # The "auto_ssl" shared dict should be defined with enough storage space to
  # hold your certificate data. 1MB of storage holds certificates for
  # approximately 100 separate domains.
  lua_shared_dict auto_ssl 1m;
  # The "auto_ssl_settings" shared dict is used to temporarily store various settings
  # like the secret used by the hook server on port 8999. Do not change or
  # omit it.
  lua_shared_dict auto_ssl_settings 64k;

  # A DNS resolver must be defined for OCSP stapling to function.
  #
  # This example uses Google's DNS server. You may want to use your system's
  # default DNS servers, which can be found in /etc/resolv.conf. If your network
  # is not IPv6 compatible, you may wish to disable IPv6 results by using the
  # "ipv6=off" flag (like "resolver 8.8.8.8 ipv6=off").
  resolver 8.8.8.8;

  # Initial setup tasks.
  init_by_lua_block {
    auto_ssl = (require "resty.auto-ssl").new()

    -- Define a function to determine which SNI domains to automatically handle
    -- and register new certificates for. Defaults to not allowing any domains,
    -- so this must be configured.
    auto_ssl:set("allow_domain", function(domain)
      domains = os.getenv("DOMAINS")
      return ngx.re.match(domain, domains, "ijo")
    end)
    auto_ssl:set("dir", "/tmp/")

    auto_ssl:init()
  }

  init_worker_by_lua_block {
    auto_ssl:init_worker()
  }

  # HTTPS server
  server {
    listen 443 ssl;

    # Dynamic handler for issuing or returning certs for SNI domains.
    ssl_certificate_by_lua_block {
      auto_ssl:ssl_certificate()
    }

    # You must still define a static ssl_certificate file for nginx to start.
    #
    # You may generate a self-signed fallback with:
    #
    # openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 \
    #   -subj '/CN=sni-support-required-for-valid-ssl' \
    #   -keyout /etc/ssl/resty-auto-ssl-fallback.key \
    #   -out /etc/ssl/resty-auto-ssl-fallback.crt
    ssl_certificate /etc/ssl/resty-auto-ssl-fallback.crt;
    ssl_certificate_key /etc/ssl/resty-auto-ssl-fallback.key;
  }

  # HTTP server
  server {
    listen 80;

    # Endpoint used for performing domain verification with Let's Encrypt.
    location /.well-known/acme-challenge/ {
      content_by_lua_block {
        auto_ssl:challenge_server()
      }
    }
  }

  # Internal server running on port 8999 for handling certificate tasks.
  server {
    listen 127.0.0.1:8999;
    location / {
      content_by_lua_block {
        auto_ssl:hook_server()
      }
    }
  }
}
```

**注意**！以上配置文件来自项目的 README 的示例配置，我修改了两个地方：

1. 证书的输出路径，为了避免权限问题我将证书写到了/tmp/目录下，但是 **非常不建议** 在生产环境下降证书写到这里。
2. 默认配置允许给所有的域名签发证书，这样显然可能会被滥用，所以我对 `allow_domain` 这个配置项加了一些限制，只允许我自己的域名进来。

## 启动 OpenResty

```
openresty -t
openresty
```

# 容器化 lua-resty-auto-ssl

如果你觉得上边这个过程太复杂了，那么你也可以使用我自己 build 的[Let's encrypt image](https://github.com/xdays/dockerfiles/tree/master/letsencrypt)来运行

    docker run -d --name letsencrypt --net host -e DOMAINS=example.com -v $PWD:/tmp xdays/letsencrypt

# 使用

首先将你要签发证书的域名解析到运行 openresty 的机器上，然后直接向域名发送 https 请求即可拿到对应的证书：

```
curl https://i.xdays.me/
```
按照我的配置证书在 `/tmp/storage/` 下。
