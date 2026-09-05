---
title: 关于本站
---

# 关于吉大课程攻略

## 我们的使命

**把不确定的、口口相传的资料和经验,变成公开的、易于获取的,以及大家能够共同完善、共同积累的共享资料。**

每学期都有无数吉大学生在重复问:
- "某某课往年题在哪?"
- "某某老师给分怎么样?"
- "这门课要准备什么?"

而答案散落在群聊记录里、学长的私人笔记里、快要断更的仓库里。我们要做的,就是把这些**隐性知识显性化,把私人经验公共化**。

## 为什么做这个

### 这个需求确实存在

虽然吉大会用 GitHub 的人不多,但对课程资料和学习经验的需求是客观存在的、普遍的、强烈的。

现状是:
- 📚 资料分散在 5+ 个 GitHub 仓库,找起来很麻烦
- 💬 经验靠口口相传,学长毕业了信息就断了
- ❓ 选课全靠盲选,课程信息不透明
- ⏰ 每届新生都在重复踩同样的坑

我们要做的是:
- ✅ 一个地方找到所有资料
- ✅ 经验沉淀下来,一届传一届
- ✅ 课程信息公开透明,选课有据可依
- ✅ 后来人少走弯路,把时间花在真正重要的事上

### 我们的原则

1. **极致易用** - 像用百度一样简单,不假设用户懂技术
2. **简单美观** - 界面清爽,信息层级清晰,手机电脑都好用
3. **开放共享** - 所有人都能贡献,所有人都能受益
4. **站在巨人肩膀上** - 复用优秀开源项目,不重复造轮子

## 技术实现

本站完全基于成熟的开源技术构建,不闭门造车:

| 组件 | 方案 | 为什么选它 |
|---|---|---|
| 静态站点生成 | [Hugo](https://gohugo.io/) | 最快的生成器,无需 Node.js |
| UI 主题 | [Hextra](https://imfing.github.io/hextra/) | 响应式、暗色模式、中文友好 |
| 搜索引擎 | [FlexSearch](https://github.com/nextapps-de/flexsearch) | 浏览器端搜索,零服务端开销 |
| 评论系统 | [giscus](https://giscus.app/) | 基于 GitHub Discussions,免后端 |
| 托管 | [GitHub Pages](https://pages.github.com/) | 免费、免备案、全球 CDN |
| 自动化 | [GitHub Actions](https://github.com/features/actions) | 定时更新、链接检查全自动 |

**设计哲学**: 优先使用 GitHub 生态方案,优先使用浏览器端方案,优先使用 star 1k+ 的成熟项目。

## 资料来源

本站不存储任何课程文件,只做索引。所有资料来自以下开源仓库:

- [JLU-CS-Courses](https://github.com/Geraldxm/JLU-CS-Courses) - 计算机学院课程资料
- [JLU-Courses](https://github.com/JLU-NightsWatch/JLU-Courses) - 软件学院课程资料
- [ChenGeng0102/JLU](https://github.com/ChenGeng0102/JLU) - 综合课程资料
- [WilliamPockey/JLU_CS](https://github.com/WilliamPockey/JLU_CS) - 计算机学院学术生存技巧
- [autumn529/JLU](https://github.com/autumn529/JLU) - 软件学院学习资料

感谢所有资料贡献者的无私分享!

## 如何贡献

这是一个**共建**项目,欢迎每一位吉大人参与:

### 💬 最简单: 评价课程
直接在课程页面底部评论区写下你的学习经验(需要 GitHub 账号)。

### 📝 补充信息
发现课程信息不全? 提交 [Issue](https://github.com/Chlx42/jlu-course-guide/issues) 告诉我们。

### 🔗 分享资料
有好的课程资料? 告诉我们链接,我们会加进来。

### 👨‍💻 改进网站
懂技术的同学可以直接提 [Pull Request](https://github.com/Chlx42/jlu-course-guide/pulls)。

## 开源协议

- **网站代码**: [MIT License](https://github.com/Chlx42/jlu-course-guide/blob/main/LICENSE)
- **网站内容**: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **课程资料**: 版权归原作者所有,请遵守各源仓库的开源协议

## 联系我们

- 📮 提交 Issue: [GitHub Issues](https://github.com/Chlx42/jlu-course-guide/issues)
- 💬 参与讨论: [GitHub Discussions](https://github.com/Chlx42/jlu-course-guide/discussions)
- 📦 查看源码: [GitHub Repository](https://github.com/Chlx42/jlu-course-guide)

## 致谢

- [Open-JLU](https://github.com/userElaina/Open-JLU) - 吉大开源项目索引,给了我们灵感
- [HITSZ-OpenAuto](https://hoa.moe/) - 哈工大深圳的课程攻略,技术架构参考
- [浙大课程攻略](https://github.com/QSCTech/zju-icicles) - 证明了这件事的价值
- 所有资料贡献者和课程评价者

---

**免责声明**: 本站仅提供课程资料索引服务,不存储具体文件。所有资料版权归原作者所有。课程评价仅代表个人观点,不代表本站立场。如有侵权或不当内容,请通过 Issue 联系我们删除。
