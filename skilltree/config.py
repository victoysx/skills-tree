"""应用配置辅助模块。

该模块集中管理默认路径的计算方式，让其他代码无需关心操作系统细节。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """技能树应用的不可变配置。

    属性：
        data_dir: JSON 数据文件所在目录。
        default_filename: 技能树 JSON 的默认文件名。
    """

    data_dir: Path
    default_filename: str = "skilltree.json"

    @property
    def default_path(self) -> Path:
        """返回技能树数据文件的默认路径。"""

        return self.data_dir / self.default_filename


def load_default_config() -> AppConfig:
    """根据仓库目录结构生成默认配置。"""

    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    return AppConfig(data_dir=data_dir)
