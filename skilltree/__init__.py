"""技能树跟踪包。

该包提供一个小而可扩展的框架，用于存储、查询和输出个人学习技能树。
"""

from skilltree.config import AppConfig
from skilltree.services import SkillTreeService

__all__ = ["AppConfig", "SkillTreeService"]
