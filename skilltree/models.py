"""项目中的数据模型。

该模块使用 dataclass 保持模型轻量，同时提供类型提示与清晰的字段说明。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional


@dataclass
class Skill:
    """表示技能树中的单个技能节点。

    属性：
        name: 技能的可读名称。
        category: 技能所属的可选分类。
        completed: 是否已完成该技能。
        notes: 额外备注（资源、提醒等）。
    """

    name: str
    category: Optional[str] = None
    completed: bool = False
    notes: str = ""


@dataclass
class SkillArea:
    """某个领域下的技能集合。"""

    name: str
    skills: List[Skill] = field(default_factory=list)

    def completion_rate(self) -> float:
        """计算该领域技能的完成率。"""

        if not self.skills:
            return 0.0
        completed_count = sum(1 for skill in self.skills if skill.completed)
        return completed_count / len(self.skills)

    def find_skill(self, name: str) -> Optional[Skill]:
        """按名称查找技能，未找到时返回 None。"""

        for skill in self.skills:
            if skill.name.lower() == name.lower():
                return skill
        return None

    def add_skill(self, skill: Skill) -> None:
        """向该领域添加一个新技能。"""

        self.skills.append(skill)


@dataclass
class SkillTree:
    """包含所有技能领域的根对象。"""

    owner: str
    areas: List[SkillArea] = field(default_factory=list)

    def iter_skills(self) -> Iterable[Skill]:
        """遍历所有领域中的技能。"""

        for area in self.areas:
            for skill in area.skills:
                yield skill

    def completion_rate(self) -> float:
        """计算整体技能完成率。"""

        skills = list(self.iter_skills())
        if not skills:
            return 0.0
        completed = sum(1 for skill in skills if skill.completed)
        return completed / len(skills)

    def find_area(self, name: str) -> Optional[SkillArea]:
        """按名称查找领域。"""

        for area in self.areas:
            if area.name.lower() == name.lower():
                return area
        return None
