#!/usr/bin/env python3
"""
JLU Course Material Aggregator
从五个资料仓库中提取课程资料链接，生成统一的课程页面
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Optional
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

# 课程名称标准化映射（核心课程）
COURSE_MAPPING = {
    "数据结构": ["数据结构", "Data Structure", "data-structure", "ds", "数据结构与算法"],
    "操作系统": ["操作系统", "Operating System", "os", "操作系统原理"],
    "计算机组成原理": ["计算机组成原理", "计组", "computer-organization", "组成原理"],
    "编译原理": ["编译原理", "Compiler", "compiler", "编译器", "编译"],
    "数据库": ["数据库", "Database", "database", "数据库系统"],
    "计算机网络": ["计算机网络", "Computer Network", "network", "网络"],
    "算法": ["算法", "Algorithm", "algorithm", "算法设计", "算法分析"],
    "离散数学": ["离散数学", "Discrete Mathematics", "discrete", "离散"],
    "数字逻辑": ["数字逻辑", "Digital Logic", "数字电路"],
    "概率论与数理统计": ["概率论", "概率", "Probability", "数理统计"],
    "线性代数": ["线性代数", "Linear Algebra", "线代"],
    "高等数学": ["高等数学", "高数", "Calculus", "微积分"],
    "大学物理": ["大学物理", "物理", "Physics"],
    "计算机导论": ["计算机导论", "导论", "Introduction to Computer Science"],
    "C语言程序设计": ["C语言", "C程序设计", "C Programming"],
    "C++程序设计": ["C++", "Cpp", "C++ Programming"],
    "Java程序设计": ["Java", "Java Programming"],
    "Python程序设计": ["Python", "Python Programming"],
    "软件工程": ["软件工程", "Software Engineering", "软工"],
    "计算机图形学": ["计算机图形学", "图形学", "Computer Graphics"],
    "人工智能": ["人工智能", "AI", "Artificial Intelligence"],
    "机器学习": ["机器学习", "Machine Learning", "ML"],
    "深度学习": ["深度学习", "Deep Learning", "DL"],
}

# 课程名称正则模式（捕获常见课程命名模式）
COURSE_PATTERNS = [
    r"^\d{6}\s+(.+)$",  # 542003 数据结构
    r"^(.+)\s+\d{6}$",  # 数据结构 542003
    r"^(.+)\s*[（(].*[)）]$",  # 数据结构（卓越班）
    r"^(.+)\s*-\s*.*$",  # 数据结构 - 朱允刚
]

# 需要过滤的无关目录关键词
SKIP_KEYWORDS = [
    '.git', 'image', 'img', 'assets', 'readme', 'license',
    'docs', 'examples', 'test', 'build', 'dist', '__pycache__',
    '图片', '素材', '资源', '工具', '说明', '其他', '笔记', '技术',
    '实践', '经验', '分享', '模板', '额外', '非计算机',
]

# 学期目录模式（需要过滤）
SEMESTER_PATTERNS = [
    r'^大[一二三四]上$',
    r'^大[一二三四]下$',
    r'^freshman|sophomore|junior|senior$',
]


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

        # 跳过无关目录
        if any(skip in path.lower() for skip in SKIP_KEYWORDS):
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
                    "repo": repo_config["name"],
                    "original_name": course_name  # 保留原始名称用于调试
                })

    return courses


def normalize_course_name(name: str) -> Optional[str]:
    """
    智能标准化课程名称

    处理逻辑:
    1. 清理课程名（去除课程代码、教师名、班级标注等）
    2. 匹配到已知课程映射表
    3. 如果是新课程，提取核心课程名
    """
    if not name or len(name.strip()) == 0:
        return None

    original_name = name.strip()
    cleaned_name = clean_course_name(original_name)

    if not cleaned_name:
        return None

    # 尝试匹配已知课程
    for standard_name, aliases in COURSE_MAPPING.items():
        for alias in aliases:
            if alias.lower() in cleaned_name.lower() or cleaned_name.lower() in alias.lower():
                return standard_name

    # 未匹配到，但看起来像课程名，返回清理后的名称
    if is_valid_course_name(cleaned_name):
        return cleaned_name

    return None


def clean_course_name(name: str) -> Optional[str]:
    """
    清理课程名称，去除冗余信息

    处理案例:
    - "542003 数据结构" -> "数据结构"
    - "数据结构（卓越班）" -> "数据结构"
    - "数据结构 - 朱允刚" -> "数据结构"
    - "Operating System 操作系统" -> "操作系统"
    """
    cleaned = name.strip()

    # 应用正则模式提取核心课程名
    for pattern in COURSE_PATTERNS:
        match = re.match(pattern, cleaned)
        if match:
            cleaned = match.group(1).strip()

    # 去除课程代码（6位数字）
    cleaned = re.sub(r'\b\d{6}\b', '', cleaned).strip()

    # 去除括号内容（班级、教师等）
    cleaned = re.sub(r'[（(][^)）]*[)）]', '', cleaned).strip()

    # 去除横杠后的内容（通常是教师名）
    if ' - ' in cleaned or ' -' in cleaned or '- ' in cleaned:
        cleaned = cleaned.split('-')[0].strip()

    # 如果包含中英文，优先保留中文
    if any('一' <= c <= '鿿' for c in cleaned):
        # 提取中文部分
        chinese_parts = re.findall(r'[一-鿿]+', cleaned)
        if chinese_parts:
            cleaned = ''.join(chinese_parts)

    # 去除多余空格
    cleaned = re.sub(r'\s+', '', cleaned)

    return cleaned if len(cleaned) >= 2 else None


def is_valid_course_name(name: str) -> bool:
    """
    判断是否是有效的课程名称

    规则:
    - 长度在 2-20 个字符之间
    - 包含中文或大写字母开头的英文
    - 不包含特殊字符（除了常见的课程用词）
    - 不是学期目录（大一上、大二下等）
    """
    if not name or len(name) < 2 or len(name) > 20:
        return False

    # 过滤学期目录
    for pattern in SEMESTER_PATTERNS:
        if re.match(pattern, name, re.IGNORECASE):
            return False

    # 过滤无意义的通用词
    generic_words = ['笔记', '技术', '实践', '资料', '模板', '工具', '其他']
    if name in generic_words:
        return False

    # 包含中文
    if any('一' <= c <= '鿿' for c in name):
        return True

    # 英文课程名（首字母大写）
    if name[0].isupper() and name.replace(' ', '').isalpha():
        return True

    return False


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

    generated_count = 0
    for course_name, resources in sorted(all_courses.items()):
        if len(resources) < 1:  # 至少一个资源就生成
            continue

        filename = course_name.lower().replace(" ", "-").replace("/", "-")
        # 移除特殊字符
        filename = re.sub(r'[^\w\s-]', '', filename)
        filepath = output_dir / f"{filename}.md"

        content = generate_course_page(course_name, resources)
        filepath.write_text(content, encoding="utf-8")

        # 显示原始名称映射（调试用）
        original_names = set(res.get("original_name", course_name) for res in resources)
        if len(original_names) > 1:
            print(f"  ✅ {course_name} ({len(resources)} 个资源)")
            print(f"     原始名称: {', '.join(sorted(original_names)[:3])}...")
        else:
            print(f"  ✅ {course_name} ({len(resources)} 个资源)")

        generated_count += 1

    # 保存原始数据
    with open("course_data.json", "w", encoding="utf-8") as f:
        json.dump(all_courses, f, ensure_ascii=False, indent=2)

    print()
    print(f"✨ 完成! 共生成 {generated_count} 个课程页面")
    print(f"📁 课程页面已生成到 content/courses/generated/")
    print(f"📄 原始数据已保存到 course_data.json")
    print()
    print("💡 提示: 查看 course_data.json 可以看到课程名称映射详情")


if __name__ == "__main__":
    main()
