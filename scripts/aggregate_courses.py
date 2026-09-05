#!/usr/bin/env python3
"""
JLU Course Material Aggregator
从五个资料仓库中提取课程资料链接，生成统一的课程页面
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Set
from urllib.parse import quote
import urllib.request
import time

# 五个资料源配置
REPOS = [
    {
        "name": "JLU-CS-Courses",
        "owner": "Geraldxm",
        "repo": "JLU-CS-Courses",
        "branch": "main",
        "description": "计算机学院课程资料"
    },
    {
        "name": "JLU-Courses",
        "owner": "JLU-NightsWatch",
        "repo": "JLU-Courses",
        "branch": "main",
        "description": "软件学院课程资料"
    },
    {
        "name": "ChenGeng0102/JLU",
        "owner": "ChenGeng0102",
        "repo": "JLU",
        "branch": "main",
        "description": "综合课程资料"
    },
    {
        "name": "WilliamPockey/JLU_CS",
        "owner": "WilliamPockey",
        "repo": "JLU_CS",
        "branch": "main",
        "description": "计算机学院学术生存技巧"
    },
    {
        "name": "autumn529/JLU",
        "owner": "autumn529",
        "repo": "JLU",
        "branch": "main",
        "description": "软件学院学习资料"
    }
]

# 课程名称标准化映射
COURSE_MAPPING = {
    "数据结构": ["数据结构", "Data Structure", "data-structure", "ds"],
    "操作系统": ["操作系统", "Operating System", "os", "操作系统原理"],
    "计算机组成原理": ["计算机组成原理", "计组", "computer-organization", "组成原理"],
    "编译原理": ["编译原理", "Compiler", "compiler", "编译器"],
    "数据库": ["数据库", "Database", "database", "数据库系统"],
    "计算机网络": ["计算机网络", "Computer Network", "network", "网络"],
    "算法": ["算法", "Algorithm", "algorithm", "算法设计"],
}


def get_github_tree(owner: str, repo: str, branch: str = "master") -> Dict:
    """获取 GitHub 仓库的文件树"""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'JLU-Course-Guide-Aggregator')
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            return json.loads(data.decode('utf-8'))
    except Exception as e:
        print(f"❌ 获取 {owner}/{repo} 失败: {e}")
        return {"tree": []}


def extract_courses(tree_data: Dict, repo_config: Dict) -> Dict[str, List[str]]:
    """从文件树中提取课程相关的目录和文件"""
    courses = {}

    if "tree" not in tree_data:
        return courses

    for item in tree_data["tree"]:
        if item["type"] != "tree":
            continue

        path = item["path"]
        # 跳过一些无关目录
        if any(skip in path.lower() for skip in [".git", "image", "img", "assets", "readme"]):
            continue

        # 提取顶层目录作为课程名
        parts = path.split("/")
        if len(parts) >= 1:
            course_name = parts[0]

            # 标准化课程名
            normalized = normalize_course_name(course_name)
            if normalized:
                if normalized not in courses:
                    courses[normalized] = []

                # 生成 GitHub 链接
                github_url = f"https://github.com/{repo_config['owner']}/{repo_config['repo']}/tree/{repo_config['branch']}/{quote(path)}"
                courses[normalized].append({
                    "path": path,
                    "url": github_url,
                    "repo": repo_config["name"]
                })

    return courses


def normalize_course_name(name: str) -> str:
    """标准化课程名称"""
    name_lower = name.lower().strip()

    for standard_name, aliases in COURSE_MAPPING.items():
        for alias in aliases:
            if alias.lower() in name_lower or name_lower in alias.lower():
                return standard_name

    # 如果没有匹配到映射，但看起来像课程名（中文或长度合适），返回原名
    if len(name) >= 2 and (any('一' <= c <= '鿿' for c in name) or len(name.split()) <= 4):
        return name

    return None


def aggregate_all_repos() -> Dict[str, List]:
    """聚合所有仓库的课程资料"""
    all_courses = {}

    for repo_config in REPOS:
        print(f"📥 正在抓取 {repo_config['name']}...")
        tree_data = get_github_tree(repo_config["owner"], repo_config["repo"], repo_config["branch"])
        courses = extract_courses(tree_data, repo_config)

        # 合并到总结果中
        for course_name, resources in courses.items():
            if course_name not in all_courses:
                all_courses[course_name] = []
            all_courses[course_name].extend(resources)

        print(f"  ✅ 找到 {len(courses)} 门课程")
        time.sleep(1)  # 避免触发 GitHub API rate limit

    return all_courses


def generate_course_page(course_name: str, resources: List[Dict]) -> str:
    """生成课程页面的 Markdown"""
    # 去重
    seen_urls = set()
    unique_resources = []
    for res in resources:
        if res["url"] not in seen_urls:
            seen_urls.add(res["url"])
            unique_resources.append(res)

    # 按仓库分组
    by_repo = {}
    for res in unique_resources:
        repo = res["repo"]
        if repo not in by_repo:
            by_repo[repo] = []
        by_repo[repo].append(res)

    # 生成 Markdown
    md = f"""---
title: {course_name}
type: docs
---

# {course_name}

## 课程信息

- **课程代码**: 待补充
- **学分**: 待补充
- **开课学院**: 待补充
- **先修课程**: 待补充
- **难度**: 待补充

## 资料链接

"""

    for repo_name, repo_resources in by_repo.items():
        md += f"### {repo_name}\n\n"
        for res in repo_resources:
            path_name = res["path"].split("/")[-1] if "/" in res["path"] else res["path"]
            md += f"- [{path_name}]({res['url']})\n"
        md += "\n"

    md += """## 课程评价

{{< callout type="info" >}}
评价功能即将上线,敬请期待
{{< /callout >}}

## 学习建议

- 待补充

---

*信息有误或需要补充? 欢迎提 [Issue](https://github.com/Chlx42/jlu-course-guide/issues) 或 PR*
"""

    return md


def main():
    print("🚀 开始聚合吉大课程资料...")
    print()

    # 抓取所有仓库
    all_courses = aggregate_all_repos()

    print()
    print(f"📊 统计结果: 共找到 {len(all_courses)} 门课程")
    print()

    # 生成课程页面
    output_dir = Path("content/courses/generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    for course_name, resources in sorted(all_courses.items()):
        if len(resources) < 2:  # 至少两个来源才生成页面
            continue

        filename = course_name.lower().replace(" ", "-").replace("/", "-")
        filepath = output_dir / f"{filename}.md"

        content = generate_course_page(course_name, resources)
        filepath.write_text(content, encoding="utf-8")

        print(f"  ✅ 生成 {course_name} ({len(resources)} 个资源)")

    # 保存原始数据
    with open("course_data.json", "w", encoding="utf-8") as f:
        json.dump(all_courses, f, ensure_ascii=False, indent=2)

    print()
    print("✨ 完成! 课程页面已生成到 content/courses/generated/")
    print(f"📄 原始数据已保存到 course_data.json")


if __name__ == "__main__":
    main()
