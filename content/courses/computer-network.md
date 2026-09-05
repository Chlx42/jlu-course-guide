---
title: 计算机网络
type: docs
weight: 6
---

# 计算机网络

## 课程信息

- **课程代码**: 待补充
- **学分**: 4
- **开课学院**: 计算机科学与技术学院
- **先修课程**: 数据结构、计算机组成原理
- **难度**: ⭐⭐⭐

## 课程简介

计算机网络是计算机专业核心课程,按 TCP/IP 五层模型讲授网络原理,包括物理层、数据链路层、网络层、传输层、应用层。理论为主,有 Wireshark 抓包分析、Socket 编程等实验。

## 资料链接

### 往年题

- [JLU-CS-Courses 计算机网络](https://github.com/Geraldxm/JLU-CS-Courses/tree/master/%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C)
- [WilliamPockey/JLU_CS 计算机网络](https://github.com/WilliamPockey/JLU_CS)
- [ChenGeng0102/JLU 网络资料](https://github.com/ChenGeng0102/JLU)

### 课程笔记

- 待补充

### 实验代码

- 待补充

### 推荐教材

- 《计算机网络 - 自顶向下方法》(Computer Networking: A Top-Down Approach) - James F. Kurose
- 《计算机网络》(第 7/8 版) - 谢希仁

### 在线资源

- [Stanford CS144 计算机网络](https://cs144.github.io/)
- [Wireshark 官方教程](https://www.wireshark.org/docs/)

## 课程评价

{{< callout type="info" >}}
评价功能即将上线,敬请期待
{{< /callout >}}

## 学习建议

- **理论部分**:
  - 物理层: 编码、调制、多路复用
  - 数据链路层: 差错检测(CRC)、MAC 协议(CSMA/CD)、以太网、交换机
  - 网络层: IP 地址、子网划分、路由算法(距离向量、链路状态)、ICMP
  - 传输层: TCP/UDP、可靠传输(停等、滑动窗口、GBN、SR)、流量控制、拥塞控制
  - 应用层: HTTP/HTTPS、DNS、FTP、SMTP 等协议

- **实验部分**:
  - Wireshark 抓包分析: 熟悉各层协议报文格式
  - Socket 编程: 实现简单的 C/S 通信(TCP/UDP)
  - 网络配置: IP 地址配置、路由表、ping/traceroute 等工具使用

- **考试重点**:
  - 子网划分和 IP 地址计算(必考)
  - 各层协议的工作原理和报文格式
  - TCP 三次握手、四次挥手、可靠传输机制
  - 路由算法的计算过程
  - 差错检测(CRC、校验和)

## 常见问题

**Q: 这门课难吗?**  
A: 内容多但不算很难,理解各层协议的作用和交互即可。计算题(子网划分、路由算法)需要多练习。

**Q: 需要很强的数学基础吗?**  
A: 不需要高深数学,主要是二进制、逻辑运算、简单概率统计。

**Q: TCP/IP 和 OSI 有什么区别?**  
A: OSI 是七层理论模型,TCP/IP 是五层(或四层)实际模型。课程一般按 TCP/IP 讲,但会对比 OSI。

**Q: 需要配置路由器交换机吗?**  
A: 取决于实验安排,可能会用 Packet Tracer 或 GNS3 仿真。

---

*信息有误或需要补充? 欢迎提 [Issue](https://github.com/Chlx42/jlu-course-guide/issues) 或 PR*
