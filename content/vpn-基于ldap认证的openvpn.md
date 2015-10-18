Title: VPN-基于LDAP认证的OpenVPN
Date: 2015-10-18 09:05
Author: admin
Category: server
Tags: vpn
Slug: vpn-基于LDAP认证的openvpn
 
# 安装

    yum install -y openvpn openvpn-auth-ldap

# 配置

## 证书

关于生成证书请参考 [VPN-基于OpenVPN构建](/openvpn构建vpn.html)

## /etc/openvpn/server.conf

<pre>
port 1194
proto tcp
dev tun
ca /etc/openvpn/easy-rsa/keys/ca.crt
cert /etc/openvpn/easy-rsa/keys/BJ.crt
key /etc/openvpn/easy-rsa/keys/BJ.key  # This file should be kept secret
dh /etc/openvpn/easy-rsa/keys/dh2048.pem
server 172.16.100.0 255.255.255.0
ifconfig-pool-persist ipp.txt
duplicate-cn
keepalive 5 60
comp-lzo
persist-key
persist-tun
status openvpn-status.log
verb 3
push "redirect-gateway def1 bypass-dhcp bypass-dns"
push "dhcp-option DNS 8.8.8.8"
plugin /usr/lib64/openvpn/plugin/lib/openvpn-auth-ldap.so "/etc/openvpn/auth/ldap.conf  uid=%u "
client-cert-not-required
username-as-common-name
</pre>

## /etc/openvpn/auth/ldap.conf

<pre>
<LDAP>
    URL   ldaps://dir.example.com:636
    BindDN     uid=apps,ou=Operations,ou=People,dc=example,dc=com
    Password   changeme
    Timeout     15
    TLSEnable   no
    FollowReferrals yes
</LDAP>
<Authorization>
    BaseDN      "dc=example,dc=com"
    SearchFilter "(uid=%u)"
    RequireGroup    false
    <Group>
        BaseDN      "ou=Groups,dc=example,dc=com"
        SearchFilter    "(|(cn=developers)(cn=artists))"
        MemberAttribute uniqueMember
    </Group>
</Authorization>
</pre>

# /etc/openldap/ldap.conf

最后追加一行
<pre>
TLS_REQCERT never
</pre>

# 与桥接模式集成

openvpn-auth-ldap不支持桥接模式，需要打patch才能正常工作，具体参考[这里](https://code.google.com/p/openvpn-auth-ldap/issues/detail?id=4)

# 参考链接

* https://openvpn.net/index.php/open-source/documentation/howto.html#pki 
