#!/usr/bin/env python3
"""
将项目中所有包含 SKILL.md 的 skill 目录复制到 ~/.cursor/skills/，
使这些 skill 在 Cursor 中全局可用。
"""
import argparse
import shutil
import sys
from pathlib import Path

# 从 .cursor/commands/install-skills/ 得到 workspace 根目录（含 skills 的最近上级）
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = SCRIPT_DIR.parents[3]
for p in (SCRIPT_DIR.parents[i] for i in range(2, 6)):
    if (p / "skills").is_dir():
        WORKSPACE_ROOT = p
        break
SKILLS_ROOT = WORKSPACE_ROOT / "skills"

# 复制时排除的目录和文件模式
EXCLUDE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
EXCLUDE_SUFFIXES = (".pyc", ".pyo", ".egg-info")


def is_excluded(path: Path) -> bool:
    """判断路径是否应被排除。"""
    name = path.name
    if name in EXCLUDE_DIRS:
        return True
    if name.startswith(".") and name not in (".cursor", ".claude"):
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def find_skill_dirs(root: Path) -> list[tuple[Path, str]]:
    """
    递归查找所有包含 SKILL.md 的目录。
    返回 [(skill_dir_path, proposed_name), ...]
    proposed_name 优先为目录名，若有同名则用相对路径转成的唯一名。
    """
    skill_dirs: list[Path] = []
    for path in root.rglob("SKILL.md"):
        skill_dir = path.parent
        if skill_dir.is_dir():
            skill_dirs.append(skill_dir)

    # 去重并计算相对路径
    seen: dict[str, Path] = {}
    result: list[tuple[Path, str]] = []
    for skill_dir in sorted(skill_dirs):
        try:
            rel = skill_dir.relative_to(root)
        except ValueError:
            continue
        name = skill_dir.name
        path_key = str(rel).replace("\\", "/")
        if name not in seen:
            seen[name] = skill_dir
            result.append((skill_dir, name))
        else:
            # 同名冲突，使用路径前缀
            unique_name = path_key.replace("/", "-").replace("\\", "-")
            result.append((skill_dir, unique_name))
    return result


def copy_skill(
    source: Path,
    dest: Path,
    overwrite: bool,
) -> tuple[bool, str]:
    """
    复制单个 skill 目录到目标位置。
    返回 (成功, 消息)。
    """
    if dest.exists():
        if not overwrite:
            return False, "已存在，跳过"
        try:
            shutil.rmtree(dest)
        except OSError as e:
            return False, f"删除旧目录失败: {e}"

    def ignore_pattern(d: str, names: list[str]) -> list[str]:
        return [n for n in names if is_excluded(Path(d).joinpath(n))]

    try:
        shutil.copytree(source, dest, ignore=ignore_pattern, dirs_exist_ok=False)
        return True, "已安装"
    except OSError as e:
        return False, str(e)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="将项目 skills/ 下所有包含 SKILL.md 的 skill 复制到 ~/.cursor/skills/"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="若目标已存在则覆盖",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅列出将要安装的 skill，不实际复制",
    )
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=None,
        help="目标目录，默认 ~/.cursor/skills",
    )
    args = parser.parse_args()

    if not SKILLS_ROOT.is_dir():
        print(f"错误: 未找到 skills 目录: {SKILLS_ROOT}", file=sys.stderr)
        return 1

    target_root = args.target_dir or Path.home() / ".cursor" / "skills"
    target_root = target_root.resolve()
    if not args.dry_run:
        target_root.mkdir(parents=True, exist_ok=True)

    pairs = find_skill_dirs(SKILLS_ROOT)
    print(f"在 {SKILLS_ROOT} 下找到 {len(pairs)} 个 skill。")
    if args.dry_run:
        for src, name in pairs[:20]:
            print(f"  - {name} <- {src.relative_to(SKILLS_ROOT)}")
        if len(pairs) > 20:
            print(f"  ... 以及其余 {len(pairs) - 20} 个")
        return 0

    installed: list[str] = []
    skipped: list[str] = []
    errors: list[tuple[str, str]] = []

    for source, name in pairs:
        dest = target_root / name
        ok, msg = copy_skill(source, dest, args.overwrite)
        if ok:
            installed.append(name)
        elif msg == "已存在，跳过":
            skipped.append(name)
        else:
            errors.append((name, msg))

    print(f"\n安装完成: {len(installed)} 个")
    print(f"已存在跳过: {len(skipped)} 个")
    if errors:
        print(f"失败: {len(errors)} 个")
        for name, err in errors:
            print(f"  - {name}: {err}", file=sys.stderr)
    print(f"\n目标目录: {target_root}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
