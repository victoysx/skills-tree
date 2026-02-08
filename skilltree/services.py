"""协调存储与分析的服务层。"""

from __future__ import annotations

from dataclasses import dataclass

from skilltree.analytics import TreeSummary, summarize_tree
from skilltree.config import AppConfig, load_default_config
from skilltree.models import Skill, SkillArea, SkillTree
from skilltree.storage import SkillTreeStorage


@dataclass
class SkillTreeService:
    """与技能树交互的高层服务。"""

    config: AppConfig

    @classmethod
    def with_default_config(cls) -> "SkillTreeService":
        """使用默认配置构建服务实例。"""

        return cls(config=load_default_config())

    def load_tree(self) -> SkillTree:
        """从配置的数据路径加载技能树。"""

        storage = SkillTreeStorage(self.config.default_path)
        return storage.load()

    def save_tree(self, tree: SkillTree) -> None:
        """将技能树保存到配置的数据路径。"""

        storage = SkillTreeStorage(self.config.default_path)
        storage.save(tree)

    def summarize(self, tree: SkillTree) -> TreeSummary:
        """计算技能树的汇总信息。"""

        return summarize_tree(tree)

    def add_skill(
        self,
        tree: SkillTree,
        area_name: str,
        skill_name: str,
        category: str | None = None,
        notes: str = "",
    ) -> SkillTree:
        """向技能树添加技能，必要时创建领域。"""

        area = tree.find_area(area_name)
        if area is None:
            area = SkillArea(name=area_name)
            tree.areas.append(area)
        area.add_skill(Skill(name=skill_name, category=category, notes=notes))
        return tree
