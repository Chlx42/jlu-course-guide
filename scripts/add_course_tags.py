#!/usr/bin/env python3
"""
批量为手写的核心课程添加标签的脚本
"""

import os
import re

# 核心课程信息
CORE_COURSES = {
    "data-structure.md": {
        "code": "542003",
        "type": "专业必修",
        "semester": "大二上",
        "difficulty_tag": "difficulty-medium",
        "difficulty_text": "中等"
    },
    "operating-system.md": {
        "code": "542005",
        "type": "专业必修",
        "semester": "大三上",
        "difficulty_tag": "difficulty-hard",
        "difficulty_text": "较难"
    },
    "computer-organization.md": {
        "code": "551004",
        "type": "专业必修",
        "semester": "大二下",
        "difficulty_tag": "difficulty-hard",
        "difficulty_text": "较难"
    },
    "compiler.md": {
        "code": "542007",
        "type": "专业必修",
        "semester": "大三下",
        "difficulty_tag": "difficulty-hard",
        "difficulty_text": "极难"
    },
    "computer-network.md": {
        "code": "542006",
        "type": "专业必修",
        "semester": "大三上",
        "difficulty_tag": "difficulty-medium",
        "difficulty_text": "中等"
    },
    "database.md": {
        "code": "542008",
        "type": "专业必修",
        "semester": "大三上",
        "difficulty_tag": "difficulty-medium",
        "difficulty_text": "中等"
    },
    "algorithm.md": {
        "code": "542009",
        "type": "专业必修",
        "semester": "大三下",
        "difficulty_tag": "difficulty-hard",
        "difficulty_text": "较难"
    }
}

def add_tags_to_course(filepath, info):
    """为课程文件添加标签"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经有标签
    if '{{< course-tag' in content:
        print(f"  已有标签,跳过")
        return False

    # 添加课程代码(如果是"待补充")
    if '课程代码**: 待补充' in content:
        content = content.replace('课程代码**: 待补充', f'课程代码**: {info["code"]}')

    # 在课程类型后添加标签
    if '- **开课学院**:' in content and '- **课程类型**:' not in content:
        # 需要插入课程类型行
        pattern = r'(- \*\*开课学院\*\*:.*?\n)'
        replacement = r'\1- **课程类型**: {{< course-tag type="required" text="' + info["type"] + '" >}}\n'
        content = re.sub(pattern, replacement, content)

    # 在开课学期后添加(如果没有)
    if '- **开课学院**:' in content and '- **开课学期**:' not in content:
        pattern = r'(- \*\*课程类型\*\*:.*?\n)'
        replacement = r'\1- **开课学期**: ' + info["semester"] + '\n'
        content = re.sub(pattern, replacement, content)

    # 在难度后添加标签
    difficulty_patterns = [
        (r'(- \*\*难度\*\*: ⭐⭐⭐⭐⭐)$', rf'\1 (5/5) {{{{< course-tag type="{info["difficulty_tag"]}" text="{info["difficulty_text"]}" >}}}}'),
        (r'(- \*\*难度\*\*: ⭐⭐⭐⭐)$', rf'\1 (4/5) {{{{< course-tag type="{info["difficulty_tag"]}" text="{info["difficulty_text"]}" >}}}}'),
        (r'(- \*\*难度\*\*: ⭐⭐⭐)$', rf'\1 (3/5) {{{{< course-tag type="{info["difficulty_tag"]}" text="{info["difficulty_text"]}" >}}}}'),
    ]

    for pattern, replacement in difficulty_patterns:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    courses_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'courses')

    updated_count = 0

    for filename, info in CORE_COURSES.items():
        filepath = os.path.join(courses_dir, filename)

        if not os.path.exists(filepath):
            print(f"✗ 文件不存在: {filename}")
            continue

        print(f"处理: {filename}")
        if add_tags_to_course(filepath, info):
            updated_count += 1
            print(f"  ✓ 已添加标签")

    print(f"\n完成! 成功更新 {updated_count} 个文件")

if __name__ == '__main__':
    main()
