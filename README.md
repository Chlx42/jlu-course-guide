# 吉大课程攻略 JLU Course Guide

> 把不确定的、口口相传的资料和经验，变成公开的、易于获取的，以及大家能够共同完善、共同积累的共享资料。

[![GitHub stars](https://img.shields.io/github/stars/Chlx42/jlu-course-guide?style=social)](https://github.com/Chlx42/jlu-course-guide)
[![GitHub forks](https://img.shields.io/github/forks/Chlx42/jlu-course-guide?style=social)](https://github.com/Chlx42/jlu-course-guide/fork)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 这是什么

**吉大课程攻略**是一个统一的课程资料索引平台，聚合了分散在多个 GitHub 仓库的课程资料、往年题、学习经验。

**不需要懂 GitHub，打开即用** - 像用百度一样简单，搜索、浏览、评价，一气呵成。

🔗 **网站地址**: https://chlx42.github.io/jlu-course-guide/ (部署后填写)

## ✨ 核心特性

- 🔍 **统一搜索** - 一次搜索，覆盖 5 个资料源，76 门课程
- 📚 **按学院/学期分类** - 不再翻目录找文件，直接定位到你要的课程
- 💬 **课程评价** - 学长学姐的真实经验：难度、给分、学习建议
- 📊 **难度标签** - 一眼看出哪些课是硬骨头
- 🎨 **简单美观** - 清爽界面，暗色模式，手机电脑都好用
- 🚀 **零成本** - 基于 GitHub Pages，免费、快速、无广告

## 🗂️ 资料来源

本站聚合以下开源仓库：

| 仓库 | Stars | 说明 |
|------|-------|------|
| [JLU-CS-Courses](https://github.com/Geraldxm/JLU-CS-Courses) | ![stars](https://img.shields.io/github/stars/Geraldxm/JLU-CS-Courses?style=social) | 计算机学院课程资料 |
| [JLU-Courses](https://github.com/JLU-NightsWatch/JLU-Courses) | ![stars](https://img.shields.io/github/stars/JLU-NightsWatch/JLU-Courses?style=social) | 软件学院课程资料 |
| [ChenGeng0102/JLU](https://github.com/ChenGeng0102/JLU) | ![stars](https://img.shields.io/github/stars/ChenGeng0102/JLU?style=social) | 综合课程资料 |
| [WilliamPockey/JLU_CS](https://github.com/WilliamPockey/JLU_CS) | ![stars](https://img.shields.io/github/stars/WilliamPockey/JLU_CS?style=social) | 学术经验分享 |
| [autumn529/JLU](https://github.com/autumn529/JLU) | ![stars](https://img.shields.io/github/stars/autumn529/JLU?style=social) | 软件学院学习资料 |

感谢所有资料贡献者的无私分享！

## 🚀 快速开始

### 作为用户

1. 访问网站 (部署后填写)
2. 搜索或浏览你感兴趣的课程
3. 查看资料链接和学习建议
4. 在评论区分享你的经验（需要 GitHub 账号）

### 作为贡献者

**💬 最简单：评价课程**

不需要懂技术，只需要有 GitHub 账号：
1. 打开任何课程页面
2. 滚动到底部评论区
3. 登录后写下你的学习经验

**📝 补充课程信息**

发现信息不全？[提交 Issue](https://github.com/Chlx42/jlu-course-guide/issues)

**👨‍💻 改进网站**

懂技术的同学可以直接提 PR，详见 [贡献指南](content/contribute.md)

## 🛠️ 技术架构

本项目完全基于成熟的开源技术构建：

- **静态站点生成**: [Hugo](https://gohugo.io/) 0.165+ (最快的生成器)
- **UI 主题**: [Hextra](https://imfing.github.io/hextra/) (响应式、暗色模式、中文友好)
- **搜索引擎**: [FlexSearch](https://github.com/nextapps-de/flexsearch) (浏览器端全文搜索)
- **评论系统**: [giscus](https://giscus.app/) (基于 GitHub Discussions)
- **托管平台**: [GitHub Pages](https://pages.github.com/) (免费、全球 CDN)
- **自动化**: [GitHub Actions](https://github.com/features/actions) (定时更新)

**设计哲学**: 复用优秀开源项目，不重复造轮子。

## 📁 项目结构

```
jlu-course-guide/
├── content/                 # 内容目录
│   ├── courses/            # 课程页面
│   │   ├── data-structure.md      # 手写的核心课程
│   │   └── generated/             # 自动生成的课程页面
│   ├── about.md            # 关于页面
│   └── contribute.md       # 贡献指南
├── layouts/                # 模板目录
│   ├── shortcodes/         # 自定义组件
│   └── partials/           # 部分模板
├── scripts/                # 脚本目录
│   ├── aggregate_courses.py       # 聚合脚本
│   ├── enrich_courses.py          # 信息补充脚本
│   └── add_course_tags.py         # 标签添加脚本
├── .github/workflows/      # 自动化工作流
│   ├── deploy.yml          # 部署工作流
│   ├── update.yml          # 定时更新
│   └── check-links.yml     # 链接检查
├── hugo.toml               # Hugo 配置
├── SPEC.md                 # 产品规格文档
└── NEXT_STEPS.md           # 下一步计划
```

## 🔧 本地开发

```bash
# 克隆仓库
git clone https://github.com/Chlx42/jlu-course-guide.git
cd jlu-course-guide

# 安装 Hugo (macOS)
brew install hugo

# 启动开发服务器
hugo server -D

# 浏览器访问 http://localhost:1313/jlu-course-guide/
```

### 运行聚合脚本

```bash
# 重新抓取课程资料
python3 scripts/aggregate_courses.py

# 补充课程基本信息
python3 scripts/enrich_courses.py

# 为核心课程添加标签
python3 scripts/add_course_tags.py
```

## 📊 当前进度

- ✅ **Phase 1 完成**: MVP 功能上线
  - 76 门课程索引
  - 全文搜索
  - 评论系统
  
- ✅ **Phase 2 完成**: 内容完善 🎉
  - 25 门课程信息已补充 (67.6%)
  - 课程标签系统
  - 热门课程推荐
  - **智能搜索**: 同义词、拼音、课程代码
  - **移动端优化**: iOS/Android 完全适配
  
- 🚀 **Phase 3 启动**: 社区建设
  - 联系原仓库作者
  - 提交 Open-JLU
  - 传播推广

详见 [NEXT_STEPS.md](NEXT_STEPS.md)

## 🎯 路线图

### 近期 (1 个月)
- [ ] 联系 5 个原仓库作者获得授权
- [ ] 给 Open-JLU 提 PR
- [ ] 积累 20+ 真实课程评价
- [ ] GitHub star 破 100

### 中期 (3 个月)
- [ ] 补充所有课程的基本信息
- [ ] 数据可视化
- [ ] 更丰富的筛选排序

### 长期 (6 个月+)
- [ ] 微信小程序版本
- [ ] 课表导入
- [ ] Push 通知

## 🤝 参与贡献

我们欢迎任何形式的贡献！

- 💬 评价课程 (最简单！)
- 📝 补充课程信息
- 🔗 分享资料链接
- 🐛 报告 Bug
- 💡 提出新功能建议
- 👨‍💻 提交代码

详见 [贡献指南](content/contribute.md)

## 📄 开源协议

- **网站代码**: [MIT License](LICENSE)
- **网站内容**: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)
- **课程资料**: 版权归原作者所有，请遵守各源仓库的开源协议

## 🙏 致谢

- [Open-JLU](https://github.com/userElaina/Open-JLU) - 吉大开源项目索引，给了我们灵感
- [HITSZ-OpenAuto](https://hoa.moe/) - 哈工大深圳的课程攻略，技术架构参考
- [浙大课程攻略](https://github.com/QSCTech/zju-icicles) - 证明了这件事的价值
- 所有资料贡献者和课程评价者

## 📮 联系我们

- 📋 提交 Issue: [GitHub Issues](https://github.com/Chlx42/jlu-course-guide/issues)
- 💬 参与讨论: [GitHub Discussions](https://github.com/Chlx42/jlu-course-guide/discussions)
- 📧 邮件联系: (待补充)

---

**免责声明**: 本站仅提供课程资料索引服务，不存储具体文件。所有资料版权归原作者所有。课程评价仅代表个人观点，不代表本站立场。如有侵权或不当内容，请通过 Issue 联系我们删除。

---

⭐ 如果这个项目对你有帮助，欢迎 Star 支持！

让我们一起让吉大的课程学习变得更轻松！💪
