---
title: Kafka基础
date: 2016-06-10
author: admin
category: server
tags: ['kafka']
slug: kafka基础
---

# 简介

Kafka 是一个分布式的，基于分区存储的，多副本提交的日志系统。其特点包括：

1. 高吞吐
2. 无缝扩展
3. 消息持久化

# 基本概念

## broker

broker 是 Kafka 集群的一个节点，负责接收 producer 发来的消息和响应 consumer 发来的消息请求。

## topic 和 partition

topic 是 Kafka 组织消息的方式，可以认为是消息的类别。一个 topic 可以有多个 partition 来保存消息，消息在 partition 里是顺序存储的。这里注意，需要注意的是，Kafka 保存数据是根据时间来决定的，而不是它是否被消费者消费。如果在数据的生命周期内，它被消费后仍然会存储在 Kafka 中。但如果它在生命周期内没有被消费，同样它也会在生命周期结束时被丢弃。

## 分布式

partition 分布在所有的 broker 上。partition 有 leader 和 follower，partition 的 leader broker 负责接收读写请求，而 follower broker 只负责从 leader 同步消息。当 leader broker 挂掉的时候，会通过 Zookeeper 的 failover 机制从 follower 中选举出新的 leader。

## producer

消息的生产者，producer 根据 topic 的 partition 策略讲消息发给 broker。

## consumer

消息的消费者，Kafka 在 consumer 之上引入了消费者组的概念，消费者会被被划分成一个个消费者组，属于某一个主题的消息会被分派到它的一个分区下，而该分区与订阅了该主题的消费组中的某一个消费者相对应，也就是说消息只会发送给订阅的消费者组中的一个消费者。可以把消费者组理解成消息的真正的订阅者，而它下面的消费者只是处理消息的线程池，这样做可以保证系统的扩展性和容错性。而消费者与分区的关系是，每个分区只能有一个消费者，这样保证了在这一分区中的所有消息都能按序处理。但不同分区中的消息处理顺序不能保证，如果要保证所有的数据都按序处理，可以使每个话题只有一个分区，每个消费者组只有一个消费者。

# 安装配置

安装配置 Java 略过

下载解压 Kafka

    wget http://apache.fayea.com/kafka/0.10.0.0/kafka_2.11-0.10.0.0.tgz && tar xzf kafka_2.11-0.10.0.0.tgz

启动 Zookeeper

    bin/zookeeper-server-start.sh config/zookeeper.properties

启动 Kafka broker

    bin/kafka-server-start.sh config/server.properties

启动 console producer

    bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test

启动 console consumer

    bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test --from-beginning

# 日常维护

## topic 管理

```
bin/kafka-topics.sh --zookeeper zk_host:port/chroot --create --topic my_topic_name
       --partitions 20 --replication-factor 3 --config x=y
bin/kafka-topics.sh --zookeeper zk_host:port/chroot --create --topic my_topic_name
       --partitions 20 --replication-factor 3 --config x=y
bin/kafka-topics.sh --zookeeper zk_host:port/chroot --alter --topic my_topic_name --config x=y
bin/kafka-topics.sh --zookeeper zk_host:port/chroot --alter --topic my_topic_name --delete-config x
bin/kafka-topics.sh --zookeeper zk_host:port/chroot --delete --topic my_topic_name
```

## 均衡 leader

    bin/kafka-preferred-replica-election.sh --zookeeper zk_host:port/chroot

## consumer group 管理

```
bin/kafka-consumer-groups.sh --zookeeper localhost:2181 --list
bin/kafka-consumer-groups.sh --zookeeper localhost:2181 --describe --group test-consumer-group
bin/kafka-consumer-groups.sh --new-consumer --bootstrap-server broker1:9092 --list
```

# 监控

## consumer lag

consumer 的当前 offset 和日志的最后位置的间隔

## producer time

producer 的响应时间

## consumer time

consumer 的响应时间

## metadata time

metadata 的更新时间

更多监控可参考 http://kafka.apache.org/documentation.html#monitoring

# 参考

http://kafka.apache.org/documentation.html
http://blog.csdn.net/yfkiss/article/details/17348693
http://blog.csdn.net/suifeng3051/article/details/48053965
http://blog.csdn.net/u013291394/article/details/50224491
