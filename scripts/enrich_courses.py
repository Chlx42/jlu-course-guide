#!/usr/bin/env python3
"""
补充课程基本信息脚本
根据课程名称和常见模式,为生成的课程页面填充基本信息
"""

import os
import re

# 课程信息数据库 - 基于吉大计算机/软件学院常见课程
COURSE_INFO = {
    # 计算机专业核心课
    "数据结构": {
        "code": "542003",
        "credit": 4,
        "department": "计算机科学与技术学院",
        "prerequisites": ["程序设计基础", "C语言程序设计"],
        "difficulty": 3,
        "type": "专业必修",
        "semester": "大二上"
    },
    "计算机组成原理": {
        "code": "551004",
        "credit": 4,
        "department": "计算机科学与技术学院",
        "prerequisites": ["数字逻辑"],
        "difficulty": 4,
        "type": "专业必修",
        "semester": "大二下"
    },
    "操作系统": {
        "code": "542005",
        "credit": 4,
        "department": "计算机科学与技术学院",
        "prerequisites": ["数据结构", "计算机组成原理"],
        "difficulty": 4,
        "type": "专业必修",
        "semester": "大三上"
    },
    "编译原理": {
        "code": "542007",
        "credit": 4,
        "department": "计算机科学与技术学院",
        "prerequisites": ["数据结构", "汇编语言"],
        "difficulty": 5,
        "type": "专业必修",
        "semester": "大三下"
    },
    "计算机网络": {
        "code": "542006",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": ["数据结构"],
        "difficulty": 3,
        "type": "专业必修",
        "semester": "大三上"
    },
    "数据库系统": {
        "code": "542008",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": ["数据结构"],
        "difficulty": 3,
        "type": "专业必修",
        "semester": "大三上"
    },
    "算法设计与分析": {
        "code": "542009",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": ["数据结构", "离散数学"],
        "difficulty": 4,
        "type": "专业必修",
        "semester": "大三下"
    },

    # 专业基础课
    "离散数学": {
        "code": "111009",
        "credit": 4,
        "department": "数学学院",
        "prerequisites": [],
        "difficulty": 3,
        "type": "专业基础必修",
        "semester": "大一下"
    },
    "程序设计基础": {
        "code": "542001",
        "credit": 4,
        "department": "计算机科学与技术学院",
        "prerequisites": [],
        "difficulty": 2,
        "type": "专业基础必修",
        "semester": "大一上"
    },
    "c语言程序设计": {
        "code": "542001",
        "credit": 4,
        "department": "计算机科学与技术学院",
        "prerequisites": [],
        "difficulty": 2,
        "type": "专业基础必修",
        "semester": "大一上"
    },
    "模拟与数字逻辑电路": {
        "code": "551002",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": [],
        "difficulty": 3,
        "type": "专业基础必修",
        "semester": "大二上"
    },
    "数字逻辑": {
        "code": "551002",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": [],
        "difficulty": 3,
        "type": "专业基础必修",
        "semester": "大二上"
    },
    "计算机科学导论": {
        "code": "542010",
        "credit": 2,
        "department": "计算机科学与技术学院",
        "prerequisites": [],
        "difficulty": 1,
        "type": "专业基础必修",
        "semester": "大一上"
    },

    # 专业选修课
    "人工智能基础": {
        "code": "542020",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": ["数据结构", "概率论"],
        "difficulty": 3,
        "type": "专业选修",
        "semester": "大三上"
    },
    "计算机系统结构": {
        "code": "542021",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": ["计算机组成原理"],
        "difficulty": 4,
        "type": "专业选修",
        "semester": "大三下"
    },
    "嵌入式系统": {
        "code": "542022",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": ["计算机组成原理"],
        "difficulty": 4,
        "type": "专业选修",
        "semester": "大三下"
    },
    "软件工程": {
        "code": "542023",
        "credit": 3,
        "department": "软件学院",
        "prerequisites": ["数据结构"],
        "difficulty": 2,
        "type": "专业必修",
        "semester": "大二下"
    },

    # 软件学院课程
    "java程序设计": {
        "code": "552001",
        "credit": 4,
        "department": "软件学院",
        "prerequisites": ["程序设计基础"],
        "difficulty": 3,
        "type": "专业必修",
        "semester": "大二上"
    },
    "面向对象的程序设计": {
        "code": "552002",
        "credit": 4,
        "department": "软件学院",
        "prerequisites": ["程序设计基础"],
        "difficulty": 3,
        "type": "专业必修",
        "semester": "大二上"
    },

    # 数学类通识课
    "微积分a1": {
        "code": "111001",
        "credit": 5,
        "department": "数学学院",
        "prerequisites": [],
        "difficulty": 3,
        "type": "通识必修",
        "semester": "大一上"
    },
    "微积分a2": {
        "code": "111002",
        "credit": 5,
        "department": "数学学院",
        "prerequisites": ["微积分A1"],
        "difficulty": 3,
        "type": "通识必修",
        "semester": "大一下"
    },
    "微积分a3": {
        "code": "111003",
        "credit": 5,
        "department": "数学学院",
        "prerequisites": ["微积分A2"],
        "difficulty": 3,
        "type": "通识必修",
        "semester": "大二上"
    },
    "微积分aii": {
        "code": "111004",
        "credit": 4,
        "department": "数学学院",
        "prerequisites": ["微积分A1"],
        "difficulty": 3,
        "type": "通识必修",
        "semester": "大一下"
    },
    "概率论与数理统计": {
        "code": "111005",
        "credit": 3,
        "department": "数学学院",
        "prerequisites": ["微积分"],
        "difficulty": 3,
        "type": "通识必修",
        "semester": "大二下"
    },
    "线性代数": {
        "code": "111006",
        "credit": 3,
        "department": "数学学院",
        "prerequisites": [],
        "difficulty": 2,
        "type": "通识必修",
        "semester": "大一下"
    },

    # 物理类
    "基础物理学": {
        "code": "121001",
        "credit": 4,
        "department": "物理学院",
        "prerequisites": [],
        "difficulty": 3,
        "type": "通识必修",
        "semester": "大一下"
    },
    "大学物理": {
        "code": "121001",
        "credit": 4,
        "department": "物理学院",
        "prerequisites": [],
        "difficulty": 3,
        "type": "通识必修",
        "semester": "大一下"
    },

    # 其他通识课
    "环境学导论": {
        "code": "131001",
        "credit": 2,
        "department": "环境与资源学院",
        "prerequisites": [],
        "difficulty": 1,
        "type": "通识选修",
        "semester": "任意学期"
    },

    # 实验课程
    "单片机控制实验": {
        "code": "551005",
        "credit": 2,
        "department": "计算机科学与技术学院",
        "prerequisites": ["计算机组成原理", "微机系统"],
        "difficulty": 3,
        "type": "专业必修实验",
        "semester": "大三上"
    },
    "局域网技术与工程组网实验": {
        "code": "542010",
        "credit": 2,
        "department": "计算机科学与技术学院",
        "prerequisites": ["计算机网络"],
        "difficulty": 2,
        "type": "专业选修实验",
        "semester": "大三下"
    },
    "微机系统": {
        "code": "551003",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": ["计算机组成原理"],
        "difficulty": 3,
        "type": "专业必修",
        "semester": "大三上"
    },
    "汇编语言": {
        "code": "542011",
        "credit": 3,
        "department": "计算机科学与技术学院",
        "prerequisites": ["计算机组成原理"],
        "difficulty": 3,
        "type": "专业必修",
        "semester": "大二下"
    },

    # 线性代数
    "线性代数": {
        "code": "111006",
        "credit": 3,
        "department": "数学学院",
        "prerequisites": [],
        "difficulty": 2,
        "type": "通识必修",
        "semester": "大一下"
    },
}

def normalize_course_name(name):
    """标准化课程名称用于匹配"""
    return name.lower().replace(" ", "").replace("-", "").replace("_", "")

def get_course_info(course_name):
    """根据课程名称获取信息"""
    normalized = normalize_course_name(course_name)

    for key, info in COURSE_INFO.items():
        if normalize_course_name(key) in normalized or normalized in normalize_course_name(key):
            return info

    return None

def generate_difficulty_stars(difficulty):
    """生成难度星级显示"""
    return "⭐" * difficulty

def enrich_course_file(filepath):
    """为单个课程文件补充信息"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取课程名称
    title_match = re.search(r'title:\s*(.+)', content)
    if not title_match:
        return False

    course_name = title_match.group(1).strip()
    info = get_course_info(course_name)

    if not info:
        return False

    # 替换课程信息部分
    new_info = f"""## 课程信息

- **课程代码**: {info['code']}
- **学分**: {info['credit']}
- **开课学院**: {info['department']}
- **课程类型**: {info['type']}
- **开课学期**: {info['semester']}
- **先修课程**: {", ".join(info['prerequisites']) if info['prerequisites'] else "无"}
- **难度**: {generate_difficulty_stars(info['difficulty'])} ({info['difficulty']}/5)"""

    # 替换内容
    pattern = r'## 课程信息\s+- \*\*课程代码\*\*:.*?- \*\*难度\*\*:.*?(?=\n\n##|\Z)'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, new_info, content, flags=re.DOTALL)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False

def main():
    generated_dir = os.path.join(os.path.dirname(__file__), '..', 'content', 'courses', 'generated')

    if not os.path.exists(generated_dir):
        print(f"目录不存在: {generated_dir}")
        return

    enriched_count = 0
    total_count = 0

    for filename in os.listdir(generated_dir):
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(generated_dir, filename)
        total_count += 1

        if enrich_course_file(filepath):
            enriched_count += 1
            print(f"✓ 已补充: {filename}")
        else:
            print(f"- 未匹配: {filename}")

    print(f"\n完成! 共处理 {total_count} 个文件,成功补充 {enriched_count} 个")

if __name__ == '__main__':
    main()
