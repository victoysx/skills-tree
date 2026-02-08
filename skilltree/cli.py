"""skilltree 项目的命令行入口。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from skilltree.analytics import summarize_tree
from skilltree.config import load_default_config
from skilltree.services import SkillTreeService
from skilltree.storage import SkillTreeStorage
from skilltree.utils.dates import format_timestamp
from skilltree.utils.text import bullet_list


def _build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""

    parser = argparse.ArgumentParser(
        description="带有大量注释的技能树跟踪器。"
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=None,
        help="技能树 JSON 文件路径（默认 data/skilltree.json）。",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("summary", help="输出汇总报告。")

    add_parser = subparsers.add_parser("add-skill", help="新增技能条目。")
    add_parser.add_argument("area", help="领域名称，例如：AI 大模型")
    add_parser.add_argument("skill", help="要新增的技能名称")
    add_parser.add_argument("--category", default=None, help="可选的分类名称")
    add_parser.add_argument("--notes", default="", help="技能的补充备注")

    return parser


def _load_storage(path: Path | None) -> SkillTreeStorage:
    """根据路径创建存储对象。"""

    config = load_default_config()
    data_path = path or config.default_path
    return SkillTreeStorage(data_path)


def _command_summary(storage: SkillTreeStorage) -> str:
    """生成 CLI 输出用的汇总报告。"""

    tree = storage.load()
    summary = summarize_tree(tree)
    area_lines = [
        f"{area.name}: {area.completed_skills}/{area.total_skills} ({area.completion_rate:.0%})"
        for area in summary.areas
    ]

    report_lines = [
        f"Skill Tree Summary for {summary.owner}",
        f"Generated at {format_timestamp()}",
        "",
        f"Overall completion: {summary.completed_skills}/{summary.total_skills} ({summary.completion_rate:.0%})",
        "",
        "Areas:",
        bullet_list(area_lines),
    ]
    return "\n".join(report_lines)


def _command_add_skill(
    storage: SkillTreeStorage,
    area: str,
    skill: str,
    category: str | None,
    notes: str,
) -> str:
    """添加新技能并返回确认信息。"""

    tree = storage.load()
    service = SkillTreeService.with_default_config()
    updated_tree = service.add_skill(
        tree=tree, area_name=area, skill_name=skill, category=category, notes=notes
    )
    storage.save(updated_tree)
    return json.dumps(
        {"message": "Skill added", "area": area, "skill": skill},
        ensure_ascii=False,
    )


def main() -> None:
    """CLI 入口函数。"""

    parser = _build_parser()
    args = parser.parse_args()
    storage = _load_storage(args.data)

    if args.command == "summary":
        print(_command_summary(storage))
        return

    if args.command == "add-skill":
        print(
            _command_add_skill(
                storage=storage,
                area=args.area,
                skill=args.skill,
                category=args.category,
                notes=args.notes,
            )
        )
        return

    raise SystemExit(f"未知命令: {args.command}")


if __name__ == "__main__":
    main()
