#!/usr/bin/env python3
"""
JLU Course Material Aggregator
从五个资料仓库中提取课程资料链接，生成统一的课程页面

性能与可靠性设计:
- 并发抓取多个仓库 (ThreadPoolExecutor)
- ETag 条件请求 + 本地缓存: 304 命中时不重新下载且不消耗 GitHub API 配额
- 支持 GITHUB_TOKEN / GH_TOKEN 环境变量提升 API 限额 (60/h -> 5000/h)
- 网络失败自动重试 (指数退避), 重试耗尽后回退到本地缓存
- 课程名标准化带 memoization, 大文件树只做一遍扫描

用法:
  python3 scripts/aggregate_courses.py                # 常规运行 (走缓存)
  python3 scripts/aggregate_courses.py --no-cache     # 强制全量刷新
  python3 scripts/aggregate_courses.py --offline      # 只用本地缓存, 不联网
"""

import argparse
import json
import os
import re
import socket
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote

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

# 预展开的别名查找表, 顺序与 COURSE_MAPPING 一致以保证匹配结果不变
_ALIAS_LOOKUP = [
    (standard_name, alias.lower())
    for standard_name, aliases in COURSE_MAPPING.items()
    for alias in aliases
]

# 课程名称正则模式（捕获常见课程命名模式）
COURSE_PATTERNS = [
    re.compile(r"^\d{6}\s+(.+)$"),   # 542003 数据结构
    re.compile(r"^(.+)\s+\d{6}$"),   # 数据结构 542003
    re.compile(r"^(.+)\s*[（(].*[)）]$"),  # 数据结构（卓越班）
    re.compile(r"^(.+)\s*-\s*.*$"),  # 数据结构 - 朱允刚
]

# 需要过滤的无关目录关键词
SKIP_KEYWORDS = [
    '.git', 'image', 'img', 'assets', 'readme', 'license',
    'docs', 'examples', 'test', 'build', 'dist', '__pycache__',
    '图片', '素材', '资源', '工具', '说明', '其他', '笔记', '技术',
    '实践', '经验', '分享', '模板', '额外', '非计算机',
]
_SKIP_KEYWORDS_LOWER = [k.lower() for k in SKIP_KEYWORDS]

# 学期目录模式（需要过滤）
SEMESTER_RE = re.compile(r'^(?:大[一二三四][上下]|freshman|sophomore|junior|senior)$', re.IGNORECASE)

# 无意义的通用词
GENERIC_WORDS = {'笔记', '技术', '实践', '资料', '模板', '工具', '其他'}

RETRYABLE_STATUS = {500, 502, 503, 504, 429}


class RateLimitError(RuntimeError):
    """GitHub API 配额耗尽"""


def _get_token() -> Optional[str]:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


class GitHubTreeFetcher:
    """GitHub 文件树抓取器: ETag 缓存 + 重试 + 限流提示"""

    def __init__(self, cache_path: Path, timeout: float = 15.0,
                 no_cache: bool = False, offline: bool = False):
        self.cache_path = cache_path
        self.timeout = timeout
        self.no_cache = no_cache
        self.offline = offline
        self.token = _get_token()
        self._lock = threading.Lock()
        self._cache: Dict[str, Dict] = self._load_cache()
        # 统计
        self.hits = 0        # 304 缓存命中
        self.downloads = 0   # 200 全量下载
        self.fallbacks = 0   # 网络失败回退本地缓存

    def _load_cache(self) -> Dict:
        if self.no_cache or not self.cache_path.exists():
            return {}
        try:
            return json.loads(self.cache_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_cache(self) -> None:
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_text(
                json.dumps(self._cache, ensure_ascii=False), encoding="utf-8")
        except OSError as e:
            print(f"⚠️  缓存写入失败: {e}")

    def _stale(self, key: str) -> Optional[Dict]:
        entry = self._cache.get(key)
        return entry.get("data") if entry else None

    @staticmethod
    def _cache_key(owner: str, repo: str, branch: str) -> str:
        return f"{owner}/{repo}@{branch}"

    def fetch(self, owner: str, repo: str, branch: str) -> Dict:
        """抓取仓库文件树, 优先走 ETag 条件请求"""
        key = self._cache_key(owner, repo, branch)
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

        if self.offline:
            stale = self._stale(key)
            if stale is not None:
                print(f"  💤 离线模式, 使用缓存: {owner}/{repo}")
                return stale
            raise RuntimeError(f"离线模式下无缓存可用: {owner}/{repo}")

        headers = {
            "User-Agent": "JLU-Course-Guide-Aggregator",
            "Accept": "application/vnd.github+json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        cached = self._cache.get(key)
        if cached and not self.no_cache and cached.get("etag"):
            headers["If-None-Match"] = cached["etag"]

        last_error: Optional[Exception] = None
        for attempt in range(3):
            if attempt:
                time.sleep(2 ** attempt)  # 重试退避: 2s, 4s
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    etag = resp.headers.get("ETag")
                    if etag:
                        with self._lock:
                            self._cache[key] = {"etag": etag, "fetched_at": int(time.time()), "data": data}
                            self._save_cache()
                    self.downloads += 1
                    return data
            except urllib.error.HTTPError as e:
                if e.code == 304 and cached and not self.no_cache:
                    self.hits += 1
                    return cached["data"]
                if e.code in (403, 429):
                    remaining = e.headers.get("X-RateLimit-Remaining") if e.headers else None
                    if remaining == "0":
                        reset = e.headers.get("X-RateLimit-Reset") if e.headers else None
                        hint = ""
                        if reset:
                            wait_min = max(0, int(reset) - int(time.time())) // 60 + 1
                            hint = f", 约 {wait_min} 分钟后重置"
                        raise RateLimitError(
                            f"GitHub API 配额已耗尽{hint}。"
                            f"可设置 GITHUB_TOKEN 环境变量提升限额 (60/h -> 5000/h)"
                        ) from e
                    last_error = e
                    continue
                if e.code in RETRYABLE_STATUS:
                    last_error = e
                    continue
                raise RuntimeError(f"HTTP {e.code}: {owner}/{repo}") from e
            except (urllib.error.URLError, socket.timeout, TimeoutError,
                    ConnectionError, json.JSONDecodeError) as e:
                last_error = e
                continue

        raise RuntimeError(f"重试 3 次后仍失败: {owner}/{repo} ({last_error})")

    def fetch_with_fallback(self, owner: str, repo: str, branch: str) -> Dict:
        """抓取失败时回退到过期的本地缓存"""
        try:
            return self.fetch(owner, repo, branch)
        except RateLimitError:
            raise
        except Exception as e:
            key = self._cache_key(owner, repo, branch)
            stale = self._stale(key)
            if stale is not None:
                self.fallbacks += 1
                print(f"  ⚠️  {owner}/{repo} 抓取失败 ({e}), 回退到本地缓存")
                return stale
            print(f"  ⚠️  {owner}/{repo} 抓取失败且无缓存: {e}")
            return {"tree": []}


@lru_cache(maxsize=None)
def normalize_course_name(name: str) -> Optional[str]:
    """
    智能标准化课程名称 (带缓存, 同名目录只计算一次)

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

    cleaned_lower = cleaned_name.lower()

    # 尝试匹配已知课程
    for standard_name, alias_lower in _ALIAS_LOOKUP:
        if alias_lower in cleaned_lower or cleaned_lower in alias_lower:
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
        match = pattern.match(cleaned)
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
    - 不是学期目录（大一上、大二下等）
    """
    if not name or len(name) < 2 or len(name) > 20:
        return False

    # 过滤学期目录
    if SEMESTER_RE.match(name):
        return False

    # 过滤无意义的通用词
    if name in GENERIC_WORDS:
        return False

    # 包含中文
    if any('一' <= c <= '鿿' for c in name):
        return True

    # 英文课程名（首字母大写）
    if name[0].isupper() and name.replace(' ', '').isalpha():
        return True

    return False


def _top_dir_skipped(top_dir: str) -> bool:
    """顶层目录名本身命中过滤词, 则整棵子树都跳过"""
    top_lower = top_dir.lower()
    return any(k in top_lower for k in _SKIP_KEYWORDS_LOWER)


def extract_courses(tree_data: Dict, repo_config: Dict) -> Dict[str, List[str]]:
    """从文件树中提取课程相关的目录和文件 (单遍扫描, 顶层名标准化走缓存)"""
    courses: Dict[str, List[Dict]] = {}
    tree = tree_data.get("tree") or []

    owner = repo_config["owner"]
    repo = repo_config["repo"]
    branch = repo_config["branch"]
    repo_name = repo_config["name"]
    url_prefix = f"https://github.com/{owner}/{repo}/tree/{branch}/"

    top_skipped: Dict[str, bool] = {}

    for item in tree:
        if item.get("type") != "tree":
            continue

        path = item["path"]
        top_dir = path.split("/", 1)[0]

        # 顶层目录命中过滤词 -> 整棵子树跳过, 无需逐条检查
        if top_dir not in top_skipped:
            top_skipped[top_dir] = _top_dir_skipped(top_dir)
        if top_skipped[top_dir]:
            continue

        # 跳过子路径中含过滤词的目录
        path_lower = path.lower()
        if any(k in path_lower for k in _SKIP_KEYWORDS_LOWER):
            continue

        normalized = normalize_course_name(top_dir)
        if not normalized:
            continue

        github_url = url_prefix + quote(path)
        courses.setdefault(normalized, []).append({
            "path": path,
            "url": github_url,
            "repo": repo_name,
            "original_name": top_dir  # 保留原始名称用于调试
        })

    return courses


def aggregate_all_repos(fetcher: GitHubTreeFetcher, workers: int = 5) -> Dict[str, List]:
    """并发聚合所有仓库的课程资料"""
    all_courses: Dict[str, List] = {}

    def job(repo_config: Dict):
        tree_data = fetcher.fetch_with_fallback(
            repo_config["owner"], repo_config["repo"], repo_config["branch"])
        return repo_config, extract_courses(tree_data, repo_config)

    print(f"📥 并发抓取 {len(REPOS)} 个仓库 (workers={workers})...")
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # 并发抓取, 但按 REPOS 固定顺序合并, 保证 course_data.json 输出稳定可 diff
        futures = [executor.submit(job, rc) for rc in REPOS]
        for repo_config, future in zip(REPOS, futures):
            try:
                _, courses = future.result()
            except RateLimitError as e:
                print(f"❌ {repo_config['name']}: {e}")
                continue
            except Exception as e:
                print(f"❌ 获取 {repo_config['name']} 失败: {e}")
                continue

            # 合并到总结果中
            for course_name, resources in courses.items():
                all_courses.setdefault(course_name, []).extend(resources)
            print(f"  ✅ {repo_config['name']}: 找到 {len(courses)} 门课程")

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
        by_repo.setdefault(res["repo"], []).append(res)

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
    parser = argparse.ArgumentParser(description="聚合吉大课程资料索引")
    parser.add_argument("--no-cache", action="store_true", help="忽略缓存, 强制全量抓取")
    parser.add_argument("--offline", action="store_true", help="只使用本地缓存, 不联网")
    parser.add_argument("--workers", type=int, default=5, help="并发抓取线程数 (默认 5)")
    parser.add_argument("--timeout", type=float, default=15.0, help="单请求超时秒数 (默认 15)")
    args = parser.parse_args()

    started = time.perf_counter()
    print("🚀 开始聚合吉大课程资料...")
    print()

    cache_path = Path(__file__).resolve().parent / ".cache" / "github_trees.json"
    fetcher = GitHubTreeFetcher(cache_path, timeout=args.timeout,
                                no_cache=args.no_cache, offline=args.offline)
    if _get_token():
        print("🔑 已检测到 GITHUB_TOKEN, 使用认证请求")
    if args.offline:
        print("💤 离线模式: 只读取本地缓存")
    print()

    # 抓取所有仓库
    all_courses = aggregate_all_repos(fetcher, workers=max(1, args.workers))

    print()
    print(f"📊 统计结果: 共找到 {len(all_courses)} 门课程")
    print()

    # 生成课程页面
    # 注意: 课程页面现已按分类存放(content/courses/{core,programming,...}),
    # 聚合脚本只补充"尚不存在"的课程页,不会覆盖或重复生成已有页面,
    # 避免再次出现同一课程多个页面的情况。
    output_dir = Path("content/courses/_incoming")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 收集现有课程页的标题/文件名,用于去重
    existing = set()
    courses_dir = Path("content/courses")
    for p in courses_dir.rglob("*.md"):
        existing.add(p.stem.lower())
        m = re.match(r"^---\n(.*?)\n---", p.read_text(encoding="utf-8"), re.S)
        if m:
            tm = re.search(r'^title:\s*"?([^"\n]*)"?', m.group(1), re.M)
            if tm:
                existing.add(tm.group(1).strip().lower())

    generated_count = 0
    skipped_count = 0
    for course_name, resources in sorted(all_courses.items()):
        if len(resources) < 1:  # 至少一个资源就生成
            continue

        # 已有同名课程页(标题或文件名匹配)则跳过,避免产生重复页面
        if course_name.lower() in existing:
            skipped_count += 1
            continue

        filename = course_name.lower().replace(" ", "-").replace("/", "-")
        # 移除特殊字符
        filename = re.sub(r'[^\w\s-]', '', filename)
        if filename.lower() in existing:
            skipped_count += 1
            continue
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

    elapsed = time.perf_counter() - started
    print()
    print(f"✨ 完成! 新生成 {generated_count} 个课程页面,跳过 {skipped_count} 个已有课程")
    print(f"📁 新页面已生成到 content/courses/_incoming/ (请人工审核后移入对应分类目录)")
    print(f"📄 原始数据已保存到 course_data.json")
    print(f"⏱  总耗时 {elapsed:.2f}s | 缓存命中 {fetcher.hits} | 全量下载 {fetcher.downloads} | 回退缓存 {fetcher.fallbacks}")
    print()
    print("💡 提示: 查看 course_data.json 可以看到课程名称映射详情")


if __name__ == "__main__":
    main()
