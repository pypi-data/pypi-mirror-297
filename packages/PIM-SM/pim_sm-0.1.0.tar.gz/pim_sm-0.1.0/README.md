# PIM-SM Packet Sender

## 项目简介

这是一个用于处理 PIM-SM（Protocol Independent Multicast - Sparse Mode）协议报文发送的 Python 项目，使用了 Scapy 和 PyShark 库。该项目旨在提供一种简单的方法来生成、发送和分析 PIM-SM 数据包。

## 主要功能

- 生成 PIM-SM 协议的报文
- 发送 IGMP 数据包
- 使用 Scapy 和 PyShark 进行数据包捕获和分析

## 调用方法

hello_packet('192.85.20.3', 'ether_5')
mac = returnMac('192.85.20.2', 'ether_5')
bootstrap_packet('192.85.20.3', '192.85.20.3', '192.85.20.3', '225.1.1.1', 'ether_5')
send_arp(src_mac='00:e0:fc:e2:7a:76', src='192.85.20.3', dst_mac='38:eb:47:59:c2:b2', dst='192.85.20.2',
            iface="ether_5")
send_arp(src_mac='00:e0:fc:e2:7a:77', src='192.85.10.3', dst_mac='38:eb:47:59:c2:b2', dst='192.85.10.2',
            iface="ether_5")
