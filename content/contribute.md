---
title: 贡献指南
---

想搭把手的话,方式有好几种,从最简单的开始说。

## 写课程评价

不用懂技术,有 GitHub 账号就够了。

1. 打开一门课的页面,滚到最底下的评论区
2. 点"Sign in with GitHub"登录
3. 把你的经验写出来

### 什么样的评价有用

写具体的,比如:

```
这门课作业量适中,每周一次编程作业,期末有课程设计。
给分还算公平,平时作业 30%、课程设计 30%、期末考试 40%。
建议提前预习 C 语言指针和链表,这是数据结构的基础。
```

别写这种:

```
老师讲得不好,这门课太难了,不推荐。
```

写难度、作业量、考核方式、复习建议都行。只评课程,不评价老师个人,也别攻击别人。

## 补课程信息

发现哪门课信息不全或有错:

1. 到 [GitHub Issues](https://github.com/Chlx42/jlu-course-guide/issues/new) 提一个
2. 写清课程名称和要补的内容
3. 有人看到就会处理

懂 Git 的话也可以直接 fork 改完提 PR,课程页面都在 `content/courses/` 下按分类放(core / programming / foundation / elective / practice / general / semesters / resources)。

## 分享资料

有好的资料:

1. 提 [Issue](https://github.com/Chlx42/jlu-course-guide/issues/new)
2. 说明是什么(往年题 / PPT / 实验代码 / 笔记)
3. 附上链接

## 参与开发

1. Fork 本仓库,开个分支改
2. 提交 Pull Request

本地跑起来:

```bash
git clone https://github.com/Chlx42/jlu-course-guide.git
cd jlu-course-guide
brew install hugo   # macOS
hugo server -D      # 访问 http://localhost:1313
```

重新抓取课程资料:

```bash
python3 scripts/aggregate_courses.py
# 新抓到的页面在 content/courses/_incoming/,人工确认后再挪进分类目录
```

写代码时注意:

- 中英文之间加空格,用中文标点
- 代码块标注语言
- Commit 信息写清楚改了什么

## 目前缺什么

- 各门课的基本信息(课程代码、学分、难度)还没补全
- 核心课的学习建议和常见问题
- 真实的课程评价——这个最有价值
- 更多课程的往年题链接

## 联系

- 问题或建议:[Issues](https://github.com/Chlx42/jlu-course-guide/issues)
- 讨论:[Discussions](https://github.com/Chlx42/jlu-course-guide/discussions)

贡献者会出现在[贡献者列表](https://github.com/Chlx42/jlu-course-guide/graphs/contributors)里,重要的贡献会在 README 里单独感谢。谢谢每一位贡献的人。
