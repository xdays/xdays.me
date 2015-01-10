Title: Puppet之API操作
Date: 2014-12-31 23:38
Author: admin
Category: devops
Tags: puppet,api
Slug: Puppet之API操作
 
# 背景
最近在做一个自动部署实例的项目，大致流程是首先调用AWS的API来生成实例，然后用Puppet来部署相关服务。但是由于AWS的EIP是可回收的，也就是说新起的实例可能会被分配到一个之前已经使用过EIP，由于证书名称是根据EIP来的，就会导致有对应的证书名称已经在Puppet上记录了，这样就会导致Puppet这个环节失败。鉴于如此，需要在给实例绑定上EIP之后远程清除下Puppet上对应的证书，这样就用到了Puppet的API操作。

# 基础
Puppet支持RESTful的API：master端主要涉及catalog，certificate，report, resource, file, node, status,和fact；agent端主要涉及fact和run。关于这些资源的详细操作参考[这里](https://docs.puppetlabs.com/guides/rest_api.html)

关于API的另一方面就是安全方面，Puppet用一个单独的文件（文件名由rest_authconfig）来配置API的ACL，具体ACL的语法如下：

<pre>
path [~] {/path/to/resource|regex}
[environment {list of environments}]
[method {list of methods}]
[auth[enthicated] {yes|no|on|off|any}]
[allow {hostname|certname|*}]
</pre>

* path为请求的url
* environment为环境，如production
* method为请求方法，包括find, search, save和destroy
* auth为是否需要认证，包括yes, no和any(就是都可以)
* allow为匹配nodename，2.7.1之后支持正则
* allow_ip为匹配ip地址或者网段

# 配置
## 服务端
<pre>
path /certificate_status
environment production,stage
auth yes
method find, search, save, destroy
allow *
</pre>

## 客户端
<pre>
curl -s --insecure --cert /var/lib/puppet/ssl/certs/test2.xdays.info.pem --key /var/lib/puppet/ssl/private_keys/test2.xdays.info.pem --cacert /var/lib/puppet/ssl/certs/ca.pem -H "Accept: pson" https://puppet.xdays.info:8140/stage/certificate_statuses/no_key | python -m json.tool
</pre>

<pre>
curl -s --insecure  -X PUT --cert /var/lib/puppet/ssl/certs/test2.xdays.info.pem --key /var/lib/puppet/ssl/private_keys/test2.xdays.info.pem --cacert /var/lib/puppet/ssl/certs/ca.pem -H "Content-Type: text/pson" --data '{"desired_state":"signed"}' https://puppet.xdays.info:8140/stage/certificate_status/test2.xdays.info
</pre>

<pre>
curl -s -X DELETE --insecure --cert /var/lib/puppet/ssl/certs/test2.xdays.info.pem --key /var/lib/puppet/ssl/private_keys/test2.xdays.info.pem --cacert /var/lib/puppet/ssl/certs/ca.pem -H "Accept: pson" https://puppet.xdays.info:8140/stage/certificate_status/test2.xdays.info
"Deleted for test2.xdays.info: Puppet::SSL::Certificate"
</pre>

# 扩展
基于上一小节的curl操作，可以用Python简单封装一个Puppet的SDK用于日常操作，目前我发现已经有人做了[这个](https://github.com/daradib/pypuppet)。
 
