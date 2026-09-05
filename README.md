# 吉大课程攻略

[![Deploy to GitHub Pages](https://github.com/userElaina/jlu-course-guide/actions/workflows/deploy.yml/badge.svg)](https://github.com/userElaina/jlu-course-guide/actions/workflows/deploy.yml)

> 吉林大学课程攻略共享计划 - 汇总分散的课程资料、往年题、学习经验

🔗 **在线访问**: [https://userelaina.github.io/jlu-course-guide/](https://userelaina.github.io/jlu-course-guide/)

## 这是什么

吉大有很多同学开源了课程资料，但它们分散在多个 GitHub 仓库中，找起来很麻烦。

**吉大课程攻略**把这些资料聚合起来，按课程和老师归类，提供统一的搜索入口。

## 致谢

本站聚合以下开源项目:

- [JLU-CS-Courses](https://github.com/Geraldxm/JLU-CS-Courses) - 计算机学院课程资料
- [JLU-Courses](https://github.com/JLU-NightsWatch/JLU-Courses) - 软件学院课程资料
- [ChenGeng0102/JLU](https://github.com/ChenGeng0102/JLU) - 综合课程资料
- [WilliamPockey/JLU_CS](https://github.com/WilliamPockey/JLU_CS) - 计算机学院学术生存技巧
- [autumn529/JLU](https://github.com/autumn529/JLU) - 软件学院学习资料

感谢 [HITSZ-OpenAuto](https://hoa.moe/) 提供的技术方案参考。

## 技术栈

- [Hugo](https://gohugo.io/) - 静态站点生成器
- [Hextra](https://github.com/imfing/hextra) - Hugo 主题
- [FlexSearch](https://github.com/nextapps-de/flexsearch) - 全文搜索引擎
- GitHub Pages - 托管
- GitHub Actions - 自动构建和部署

## 本地开发

```bash
# 克隆仓库(包含 submodule)
git clone --recursive https://github.com/userElaina/jlu-course-guide.git
cd jlu-course-guide

# 安装 Hugo
brew install hugo  # macOS
# 或者从 https://github.com/gohugoio/hugo/releases 下载

# 启动开发服务器
hugo server -D

# 构建静态文件
hugo
```

## 参与贡献

欢迎通过 Issue 和 Pull Request 参与:

- 报告失效链接
- 补充遗漏的资料源
- 完善课程分类和归档
- 分享学习经验和评价

## 开源协议

- 本站代码: MIT License
- 聚合内容: 遵循各原始仓库的开源协议
- 用户贡献: CC BY-NC-SA 4.0

---

**免责声明**: 本站不存储任何课程资料文件，仅提供索引和链接。如有侵权，请提 Issue 联系删除。
