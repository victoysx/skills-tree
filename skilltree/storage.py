"""技能树的存储层。

该模块隔离了 JSON 文件读写，其他代码无需关心文件系统或序列化细节。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from skilltree.models import Skill, SkillArea, SkillTree


class SkillTreeStorage:
    """以 JSON 文件形式读写技能树数据。"""

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> SkillTree:
        """从磁盘加载技能树。

        Raises:
            FileNotFoundError: 数据文件不存在时抛出。
        """

        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return self._deserialize(payload)

    def save(self, tree: SkillTree) -> None:
        """将技能树保存到磁盘。"""

        serialized = self._serialize(tree)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(serialized, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _serialize(self, tree: SkillTree) -> Dict[str, Any]:
        """把技能树转换为基础 Python 数据结构。"""

        return {
            "owner": tree.owner,
            "areas": [
                {
                    "name": area.name,
                    "skills": [
                        {
                            "name": skill.name,
                            "category": skill.category,
                            "completed": skill.completed,
                            "notes": skill.notes,
                        }
                        for skill in area.skills
                    ],
                }
                for area in tree.areas
            ],
        }

    def _deserialize(self, payload: Dict[str, Any]) -> SkillTree:
        """将字典数据转换为 SkillTree 实例。"""

        areas = []
        for area_payload in payload.get("areas", []):
            skills = [
                Skill(
                    name=skill_payload.get("name", ""),
                    category=skill_payload.get("category"),
                    completed=skill_payload.get("completed", False),
                    notes=skill_payload.get("notes", ""),
                )
                for skill_payload in area_payload.get("skills", [])
            ]
            areas.append(SkillArea(name=area_payload.get("name", ""), skills=skills))
        return SkillTree(owner=payload.get("owner", "unknown"), areas=areas)
