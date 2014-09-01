Title: OAuth2.0
Date: 2013-07-31 16:31
Author: admin
Category: cloud
Tags: cloud, oauth
Slug: oauth2-0

前言
====

OAuth在展过程中变化非常大，1.0的基础概念在2.0中完全不同了，整个模型也发生了翻天覆地的变化，这也给学习这门技术带来了困扰。好在OAuth2.0已经成为标准的[RFC6749](http://tools.ietf.org/html/rfc6749 "权威")，我就跟着时代走学习2.0吧！以下内容来自我学习过程对各种文档的总结，仅为个人理解。另外，1.0的相关资料见参考链接。

简介
====

OAuth是一种开放的授权标准，它解决的问题是如何更安全地让第三方应用访问用户的资源。随着开放平台等其他云计算形式的发展，OAuth也成了做平台或者平台开发很重要的一项技能。

概念
====

-   角色
    -   资源所有者（resource owner） 就是终端用户
    -   资源服务器（resource server） 资源托管的平台，如微博等
    -   客户端（client） 第三方应用，想要获取用户资源
    -   授权服务器（authorization server） 颁发授权信息的服务器
-   授权许可
    获取访问令牌的方式，2.0版本定义了四种授权方式（授权码，隐式授权，资源所有者密码凭据和客户端凭据）
-   访问令牌
    代表应用程序可以获取资源的一个凭证，看到这个凭证资源服务器就给资源
-   刷新令牌 用于延长访问令牌时间的令牌
-   协议端点
    一个服务的接口，客户端有自己的接口，授权服务器也有自己的接口

协议端点
========

-   授权端点 用于与资源所有者交互获取授权许可
-   令牌端点 用于获取访问令牌
-   重定向端点 用于授权服务器引导资源所有者的用户代理返回到客户端

获取授权
========

前边提到目前规范中定义了四种获取授权的方式，我看了下目前主流的开放平台，授权码和隐式授权是目前主流的方式，所以我只针对这两种做总结，另外两种参见相关文档。

授权码
------

### 流程图

     +----------+
     | Resource |
     |   Owner  |
     |          |
     +----------+
          ^
          |
         (B)
     +----|-----+          Client Identifier      +---------------+
     |         -+----(A)-- & Redirection URI ---->|               |
     |  User-   |                                 | Authorization |
     |  Agent  -+----(B)-- User authenticates --->|     Server    |
     |          |                                 |               |
     |         -+----(C)-- Authorization Code ---<|               |
     +-|----|---+                                 +---------------+
       |    |                                         ^      v
      (A)  (C)                                        |      |
       |    |                                         |      |
       ^    v                                         |      |
     +---------+                                      |      |
     |         |>---(D)-- Authorization Code ---------'      |
     |  Client |          & Redirection URI                  |
     |         |                                             |
     |         |<---(E)----- Access Token -------------------'
     +---------+       (w/ Optional Refresh Token)

### 详细过程

-   A
    客户端通过向授权端点引导资源所有者的用户代理开始流程，请求以GET方式发起格式如下：

<!-- -->

    https://foobar.com/authorize?
    response_type=code& 期望的响应类型，code表示授权码
    client_id=s6BhdRkqt3&state=xyz& 客户端id
    redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb& 重定向URI
    scope=scope_string& 访问请求的范围
    state=int 用于防止跨站请求伪造

-   B
    授权服务器通过用户代理（通常是浏览器）验证资源拥有者的身份，用户先登陆然后确认授权
-   C
    假设资源所有者许可访问，授权服务器使用之前（在请求时或客户端注册时）提供的重定向URI重定向用户代理回到客户端，响应302的location格式如下：

<!-- -->

    https://client.example.com/cb?
    code=SplxlOBeZQQYbYS6WxSbIA& 发放的授权令牌
    state=int 用于防止跨站请求伪造

-   D
    客户端通过包含上一步中收到的授权码从授权服务器的令牌端点请求访问令牌，请求以POST方式发起格式如下：

<!-- -->

    https://foobbar.com/token?
    grant_type=authorization_code& 授权类型
    code=SplxlOBeZQQYbYS6WxSbIA& 授权令牌，用于请求访问令牌
    redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb 重定向URI

**注意：这里具体的实现要参考各个开放平台的文档，有的是直接将参数写在URL中，有的是在POST的body中**  
\* E
授权服务器对客户端进行相关验证（身份，授权码，重定向URI等），通过则发放访问令牌和刷新令牌，响应JSON格式如下：

    {
      "access_token":"2YotnFZFEjr1zCsicMWpAA", 访问令牌，这是最终要的
      "token_type":"example", 类型
      "expires_in":3600, 寿命
      "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA", 刷新令牌
      "example_parameter":"example_value" 额外参数
    }

隐式授权
--------

### 流程图

     +----------+
     | Resource |
     |  Owner   |
     |          |
     +----------+
          ^
          |
         (B)
     +----|-----+          Client Identifier     +---------------+
     |         -+----(A)-- & Redirection URI --->|               |
     |  User-   |                                | Authorization |
     |  Agent  -|----(B)-- User authenticates -->|     Server    |
     |          |                                |               |
     |          |<---(C)--- Redirection URI ----<|               |
     |          |          with Access Token     +---------------+
     |          |            in Fragment
     |          |                                +---------------+
     |          |----(D)--- Redirection URI ---->|   Web-Hosted  |
     |          |          without Fragment      |     Client    |
     |          |                                |    Resource   |
     |     (F)  |<---(E)------- Script ---------<|               |
     |          |                                +---------------+
     +-|--------+
       |    |
      (A)  (G) Access Token
       |    |
       ^    v
     +---------+
     |         |
     |  Client |
     |         |
     +---------+

### 详细过程

-   A
    客户端通过向授权端点引导资源所有者的用户代理开始流程，请求以GET方式发起格式如下：

<!-- -->

    https://foobar.com/authorize?
    response_type=token& 期望的响应类型，token表示隐式授权
    client_id=s6BhdRkqt3& 客户端id
    redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb& 重定向URI
    scope=scope_string& 访问请求的范围
    state=int 用于防止跨站请求伪造

-   B
    授权服务器通过用户代理（通常是浏览器）验证资源拥有者的身份，用户先登陆然后确认授权
-   C
    假设资源所有者许可访问，授权服务器使用之前（在请求时或客户端注册时）提供的重定向URI重定向用户代理回到客户端，重定向URI在URI片段中包含访问令牌，响应302的location格式如下：

<!-- -->

    http://example.com/cb?
    access_token=2YotnFZFEjr1zCsicMWpAA& 访问令牌
    token_type=example& 类型
    expires_in=3600& 寿命
    scope=scope_string& 访问请求范围
    state=xyz& 用于防止跨站请求伪造

-   D 用户代理顺着重定向指示向Web托管的客户端资源发起请求
-   E
    Web托管的客户端资源返回一个网页（通常是带有嵌入式脚本的HTML文档），该网页能够访问包含用户代理保留的片段的完整重定向URI并提取包含在片段中的访问令牌（和其他参数）
-   F 用户代理在本地执行Web托管的客户端资源提供的提取访问令牌的脚本
-   G 用户代理传送访问令牌给客户端

颁发访问令牌
============

授权服务器可以办法两种令牌：授权令牌和访问令牌。

访问令牌结果是以JSON格式给出，具体如下：

    {
      "access_token":"2YotnFZFEjr1zCsicMWpAA",
      "token_type":"example",
      "expires_in":3600,
      "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA",
      "example_parameter":"example_value"
    }

具体参数可参考获取授权一节的相关介绍。

刷新访问令牌
============

刷新访问令牌是由客户端操作的，是在访问令牌过期以后通过刷新令牌来刷新访问令牌的操作，具体请求格式如下：

    POST /token HTTP/1.1
    Host: server.example.com
    Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
    Content-Type: application/x-www-form-urlencoded
    grant_type=refresh_token&refresh_token=tGzv3JOkF0XG5Qx2TlKWIA

**注意：grant\_type必须设置为refresh\_token**

访问受保护资源
==============

拿到访问令牌以后就可以带着令牌去问资源服务器要资源了，具体方式是在添加Bearer类型的Authorization报头，具体格式如下：

    GET /resource/1 HTTP/1.1
    Host: example.com
    Authorization: Bearer F_9.B5f-4.1JqM 这里就是访问令牌啦

参考链接
========

OAuth1.0相关
------------

[OAuth那些事儿](http://huoding.com/2010/10/10/8 "1.0的介绍")  

[OAuth的改变](http://huoding.com/2011/11/08/126 "1.0到1.0a再到2.0的发展")  
[The OAuth 1.0
Guide](http://hueniverse.com/oauth/guide/ "有生动的例子介绍该协议的实现机制")

OAuth2.0相关
------------

[RFC6749](https://github.com/jeansfish/RFC6749.zh-cn/blob/master/TableofContents.md "权威")
