Title: RocketMQ 主要概念
Date: 2018-05-12
Modified: 2018-05-12
Category: 开发
Tags: mq

## 主要概念

Topic：消息主题，它分布在多个Master节点上。Topic下有多个Topic分区，每个分区上有多个Que。Que是消息存储队列。要实现有序消息，只能有一个Que，这会影响高可用能力。

Broker：负责接收发送自生产者的消息，存储消息，处理消费者的拉取消息请求。存储消息元数据，如：消费组，消费偏移量和主题/队列关信息。

Tag：消息标签。消费端不指定Tag的时候可以接收到同一主题下不同的Tag的消息。

NameServer: 命名服务。用于生产者和消费者通过主题查找对应的Broker。

## 高可用
NameServer可以提供多个，互相之间没有通信关系，它们是无状态的。

单个Broker和所有NameServer保持长连接，且每隔30秒向所有NameServer发送心跳，心跳包含了自身的Topic配置信息。NameServer每隔10秒扫描存活的Broker连接，若某连接2分钟内没有发送心跳包，则断开连接。Broker挂掉时，NameServer会主动关闭连接。连接断开时，NameServer会立即感知，更新Topic与队列的对应关系，但不通知生产者和消费者。

Broker以Master/Slave节点来提供高可用，Master节点可以写入，Slave节点可以读取。4个节点的两对Master/Slave组合可以实现高可用。同一Topic的两个Topic分区分布两个Master节点上，Slave上存储了Master上消息的副本。当一个Master当掉时，它的Slave仍然可以提供消息；另一个Master节点上的Topic分区仍然可以写入。

## 可靠性
消息存储有同步刷盘和异步刷盘机制。同步刷盘时，消息写入物理文件时才返回。异步刷盘时，消息写入内存就返回，机器挂掉可能产生消息丢失，Broker挂掉并不会。

## 消息清理

扫描间隔，默认10秒。

空间阀值，当磁盘空间达到阀值时，不再接受消息。

定时清理

文件保留时长默认为72小时。
