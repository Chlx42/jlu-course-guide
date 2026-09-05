# 吉林大学课程攻略共享计划

[![部署状态](https://github.com/Chlx42/jlu-course-guide/actions/workflows/deploy.yml/badge.svg)](https://github.com/Chlx42/jlu-course-guide/actions/workflows/deploy.yml)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

🌐 **在线访问**: https://chlx42.github.io/jlu-course-guide/

一个统一的吉林大学课程资料索引站,聚合多个分散的课程资料仓库,提供搜索、分类、评价功能。

## ✨ 特性

- 📚 **统一索引**: 聚合来自 5 个主要资料仓库的 76 门课程资源
- 🔍 **全文搜索**: 快速查找课程、老师、资料
- 💬 **课程评价**: 基于 GitHub Discussions 的评价系统
- 📱 **响应式设计**: 支持手机、平板、PC
- 🌙 **暗色模式**: 自动适配系统主题

## 📖 资料来源

本站聚合并索引以下仓库的课程资料:

- [JLU-CS-Courses](https://github.com/Geraldxm/JLU-CS-Courses) - 计算机学院课程资料
- [JLU-Courses](https://github.com/JLU-NightsWatch/JLU-Courses) - 软件学院课程资料  
- [ChenGeng0102/JLU](https://github.com/ChenGeng0102/JLU) - 综合课程资料
- [WilliamPockey/JLU_CS](https://github.com/WilliamPockey/JLU_CS) - 计算机学院学术生存技巧
- [autumn529/JLU](https://github.com/autumn529/JLU) - 软件学院学习资料

感谢以上仓库维护者的辛勤付出!

## 🤝 贡献指南

### 补充课程信息

1. Fork 本仓库
2. 编辑 `content/courses/` 下的课程页面
3. 提交 Pull Request

### 添加新课程

运行聚合脚本会自动从源仓库提取新课程:

```bash
python3 scripts/aggregate_courses.py
```

### 评价课程

直接访问课程页面,使用底部的评论区即可(需要 GitHub 账号)。

## 📜 评价规则

- ✅ 客观描述课程难度、作业量、考核方式
- ✅ 分享学习经验、复习建议、资料推荐
- ✅ 提出课程相关的问题和讨论
- ❌ 禁止人身攻击或不当言论
- ❌ 只评课程,不评价教师个人

## 🔧 技术栈

- [Hugo](https://gohugo.io/) + [Hextra](https://imfing.github.io/hextra/) 主题
- [FlexSearch](https://github.com/nextapps-de/flexsearch) 浏览器端全文搜索
- [giscus](https://giscus.app/) 评论系统
- GitHub Pages 托管 + GitHub Actions 自动部署

## 📄 开源协议

- **网站内容**: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **网站代码**: [MIT License](LICENSE)
- **课程资料**: 版权归原作者所有,请遵守各源仓库的开源协议

## 🙏 致谢

- [Open-JLU](https://github.com/userElaina/Open-JLU) - 吉大开源项目索引
- [HITSZ-OpenAuto](https://github.com/HITSZ-OpenAuto) - 项目架构参考
- 所有资料贡献者和课程评价者

## 📮 联系方式

- 提交 Issue: [GitHub Issues](https://github.com/Chlx42/jlu-course-guide/issues)
- 参与讨论: [GitHub Discussions](https://github.com/Chlx42/jlu-course-guide/discussions)

---

**免责声明**: 本站仅提供课程资料索引服务,不存储具体文件。所有资料版权归原作者所有。课程评价仅代表个人观点,不代表本站立场。
