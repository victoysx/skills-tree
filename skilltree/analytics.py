"""技能树分析辅助函数。

这些函数用于计算汇总信息，不会修改原始数据。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from skilltree.models import SkillArea, SkillTree


@dataclass
class AreaSummary:
    """单个领域的汇总信息。"""

    name: str
    total_skills: int
    completed_skills: int
    completion_rate: float


@dataclass
class TreeSummary:
    """整个技能树的汇总信息。"""

    owner: str
    total_skills: int
    completed_skills: int
    completion_rate: float
    areas: List[AreaSummary]


def summarize_area(area: SkillArea) -> AreaSummary:
    """生成某个领域的汇总信息。"""

    total = len(area.skills)
    completed = sum(1 for skill in area.skills if skill.completed)
    rate = completed / total if total else 0.0
    return AreaSummary(
        name=area.name,
        total_skills=total,
        completed_skills=completed,
        completion_rate=rate,
    )


def summarize_tree(tree: SkillTree) -> TreeSummary:
    """生成整个技能树的汇总信息。"""

    area_summaries = [summarize_area(area) for area in tree.areas]
    total = sum(summary.total_skills for summary in area_summaries)
    completed = sum(summary.completed_skills for summary in area_summaries)
    rate = completed / total if total else 0.0
    return TreeSummary(
        owner=tree.owner,
        total_skills=total,
        completed_skills=completed,
        completion_rate=rate,
        areas=area_summaries,
    )
