"""CLI 输出格式化的文本工具。"""

from __future__ import annotations

from typing import Iterable


def bullet_list(lines: Iterable[str], indent: int = 2) -> str:
    """将多行文本格式化为项目符号列表。"""

    prefix = " " * indent + "- "
    return "\n".join(f"{prefix}{line}" for line in lines)
