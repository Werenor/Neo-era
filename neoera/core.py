"""
Neo-era 核心模块（core.py）
--------------------------
负责：
  - 管理全局上下文 ctx
  - 初始化引擎（加载语言与渲染器）
  - 统一打印启动信息
"""

from __future__ import annotations
from typing import Any, Dict


# ============================================================
#  全局上下文（Context）
# ============================================================

class Context(dict):
    """
    游戏运行时上下文。
    主要用于保存全局变量（如玩家名、好感度等）。
    """
    def get_path(self, path: str, default=None) -> Any:
        """按 'a.b.c' 路径读取值"""
        node = self
        for key in path.split("."):
            if isinstance(node, dict) and key in node:
                node = node[key]
            else:
                return default
        return node

    def set_path(self, path: str, value: Any) -> None:
        """按 'a.b.c' 路径设置值"""
        parts = path.split(".")
        node = self
        for key in parts[:-1]:
            node = node.setdefault(key, {})
        node[parts[-1]] = value


# 全局上下文实例
ctx: Context = Context({
    "player_name": "指挥官",
    "love": {},
    "flags": {},
})


# ============================================================
#  引擎初始化
# ============================================================

def init_engine(use_gui: bool = True) -> None:
    """
    初始化 Neo-era 引擎。
    参数:
      use_gui - 是否启用 pygame_gui 渲染器（默认为 True）
    """
    if use_gui:
        from neoera import renderer_gui as renderer
        mode = "GUI"
    else:
        # 若未来想保留控制台版本，可切换
        from neoera import renderer_pygame as renderer
        mode = "CLI"

    from neoera import lang

    # 导入语言层函数到全局
    globals().update({k: v for k, v in vars(lang).items() if not k.startswith("_")})

    renderer.echo(f"[Neo-era] 引擎初始化完成。模式：{mode}")
    renderer.echo(f"[Neo-era] 当前玩家：{ctx.get('player_name')}")
    print(f"[Neo-era] 引擎初始化完成（{mode} 模式）")
