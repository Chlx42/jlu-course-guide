---
title: 贡献指南
---

# 贡献指南

感谢你愿意为吉大课程攻略贡献力量!这是一个**共建**项目,我们欢迎每一位吉大人参与。

## 💬 最简单的贡献:评价课程

**不需要懂技术,不需要会用 Git,只需要有 GitHub 账号。**

1. 打开任何一门课程的页面
2. 滚动到页面底部的评论区
3. 点击"Sign in with GitHub"登录
4. 写下你的学习经验、课程建议或问题

### 好的评价长什么样?

✅ **客观具体**:
```
这门课作业量适中,每周一次编程作业,期末有课程设计。
给分还算公平,平时作业 30%、课程设计 30%、期末考试 40%。
建议提前预习 C 语言指针和链表,这是数据结构的基础。
```

❌ **避免这样**:
```
老师讲得不好,这门课太难了,不推荐。
```

### 评价规则

- ✅ 描述课程难度、作业量、考核方式
- ✅ 分享学习经验、复习建议、资料推荐
- ✅ 提出问题和讨论
- ❌ 禁止人身攻击或不当言论
- ❌ 只评课程,不评价教师个人

## 📝 补充课程信息

发现课程信息不全或有误?

### 方法一:提交 Issue (推荐)

1. 访问 [GitHub Issues](https://github.com/Chlx42/jlu-course-guide/issues/new)
2. 选择"课程信息补充"模板
3. 填写课程名称和需要补充的信息
4. 提交,我们会尽快处理

### 方法二:直接编辑文件 (适合懂 Git 的同学)

1. Fork 本仓库
2. 编辑 `content/courses/` 下的课程 Markdown 文件
3. 提交 Pull Request

## 🔗 分享资料链接

有好的课程资料想分享?

1. 提交 [Issue](https://github.com/Chlx42/jlu-course-guide/issues/new)
2. 说明资料类型(往年题/PPT/实验代码/笔记)
3. 附上资料链接
4. 我们会审核后添加

## 👨‍💻 参与开发

### 修复 Bug 或改进功能

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 本地开发环境

```bash
# 克隆仓库
git clone https://github.com/Chlx42/jlu-course-guide.git
cd jlu-course-guide

# 安装 Hugo (macOS)
brew install hugo

# 启动开发服务器
hugo server -D

# 浏览器访问 http://localhost:1313
```

### 运行聚合脚本

```bash
# 重新抓取课程资料
python3 scripts/aggregate_courses.py

# 查看生成的文件
ls content/courses/generated/
```

## 📋 开发规范

### 文件组织

- 手写的核心课程页面放在 `content/courses/`
- 自动生成的课程页面放在 `content/courses/generated/`
- 不要直接编辑 `generated/` 下的文件,它们会被脚本覆盖

### Markdown 规范

- 中英文之间加空格(例如:"这是 GitHub 仓库")
- 使用中文标点符号
- 代码块指定语言(```bash, ```python)
- 链接使用相对路径

### Commit 规范

```
类型: 简短描述

详细描述(可选)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

类型:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 格式调整
- `refactor`: 代码重构
- `chore`: 构建/工具相关

## 🎯 我们需要什么帮助

### 高优先级

- [ ] 补充 70 门课程的基本信息(课程代码、学分、难度)
- [ ] 核心课程的学习建议和常见问题
- [ ] 真实的课程评价(最有价值!)

### 中优先级

- [ ] 更多课程的往年题和资料链接
- [ ] 改进搜索体验(权重优化、同义词)
- [ ] 移动端体验优化

### 低优先级

- [ ] 数据可视化(课程难度分布、热门资料类型)
- [ ] 多语言支持(英文版)
- [ ] 微信小程序版本

## 💡 贡献激励

虽然这是一个非营利的开源项目,但我们会记住每一位贡献者:

- 你的名字会出现在 [贡献者列表](https://github.com/Chlx42/jlu-course-guide/graphs/contributors)
- 重要贡献者会在 README 中特别致谢
- 我们会为活跃贡献者准备小礼物(贴纸、T恤等)

## 📮 联系我们

- 📋 提交 Issue: [GitHub Issues](https://github.com/Chlx42/jlu-course-guide/issues)
- 💬 参与讨论: [GitHub Discussions](https://github.com/Chlx42/jlu-course-guide/discussions)
- 📧 邮件联系: (待补充)

---

再次感谢你的贡献!每一个小改进都让这个项目变得更好,让后来的吉大人少走一些弯路。
