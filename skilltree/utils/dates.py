"""用于日志和报告的时间格式化工具。"""

from __future__ import annotations

from datetime import datetime


def format_timestamp(value: datetime | None = None) -> str:
    """返回报告用的 ISO 风格时间戳。"""

    value = value or datetime.utcnow()
    return value.strftime("%Y-%m-%d %H:%M:%S UTC")
