---
title: 关于本站
---

## 为什么有这个站

每学期都有人在群里问同样的问题:「某某课往年题在哪?」「某某老师给分怎么样?」「这门课要准备什么?」

答案散在群聊记录、学长的私人笔记和一些快断更的 GitHub 仓库里,找不找得到全看运气。学长一毕业,这些也就跟着没了。

这个站做的事很简单:把 5 个仓库里的资料按课程归到一起,再让大家把各自的经验写在每门课的评论区,一届传给一届。

## 资料来源

本站不存任何课程文件,只放链接。资料全部来自这几个仓库:

- [JLU-CS-Courses](https://github.com/Geraldxm/JLU-CS-Courses) - 计算机学院
- [JLU-Courses](https://github.com/JLU-NightsWatch/JLU-Courses) - 软件学院
- [ChenGeng0102/JLU](https://github.com/ChenGeng0102/JLU) - 综合资料
- [WilliamPockey/JLU_CS](https://github.com/WilliamPockey/JLU_CS) - 学术经验
- [autumn529/JLU](https://github.com/autumn529/JLU) - 软件学院

内容都是这些仓库的贡献者攒下来的,谢谢他们。

## 怎么做的

不想重复造轮子,能用的现成方案就直接用:

| 组件 | 方案 | 说明 |
|---|---|---|
| 静态站点生成 | [Hugo](https://gohugo.io/) | 快,不用装 Node.js |
| UI 主题 | [Hextra](https://imfing.github.io/hextra/) | 响应式、暗色模式、中文友好 |
| 搜索 | [FlexSearch](https://github.com/nextapps-de/flexsearch) | 浏览器里搜,不需要服务端 |
| 评论 | [giscus](https://giscus.app/) | 挂在 GitHub Discussions 上,没有后端 |
| 托管 | [GitHub Pages](https://pages.github.com/) | 免费,不用备案 |
| 自动化 | [GitHub Actions](https://github.com/features/actions) | 定时更新、链接检查 |

## 怎么参与

- 每门课页面底部都有评论区,写点学习经验、给分情况,有 GitHub 账号就行
- 发现课程信息不对或缺了,提 [Issue](https://github.com/Chlx42/jlu-course-guide/issues) 说一声
- 有资料想分享,提 Issue 附上链接
- 想改代码,直接提 [Pull Request](https://github.com/Chlx42/jlu-course-guide/pulls)

详细步骤见[贡献指南](/contribute/)。

## 版权

- 网站代码:[MIT License](https://github.com/Chlx42/jlu-course-guide/blob/main/LICENSE)
- 网站内容:[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- 课程资料版权归原作者所有,请遵守各源仓库的协议
- 课程评价只代表个人观点。有侵权或不当内容,发 Issue 联系我们删除

## 致谢

- [Open-JLU](https://github.com/userElaina/Open-JLU) - 吉大开源项目索引
- [HITSZ-OpenAuto](https://hoa.moe/) - 哈工大深圳的课程攻略
- [浙大课程攻略](https://github.com/QSCTech/zju-icicles) - 证明这件事值得做
- 所有资料贡献者和写评价的同学
