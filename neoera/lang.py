# /neoera/lang.py

from typing import Callable, List, Optional
from neoera import renderer_gui as renderer
from neoera.core import ctx


def say(who: str, text: str):
    text = text.replace("<玩家>", ctx.get("player_name", "玩家"))
    renderer.echo(f"{who}：{text}")


def narrate(text: str):
    text = text.replace("<玩家>", ctx.get("player_name", "玩家"))
    renderer.echo(text)


def choose(options: List[str]) -> int:
    """显示 GUI 选项"""
    return renderer.print_choice(options)


def branch(cond: bool, then: Callable, otherwise: Optional[Callable] = None):
    if cond:
        then()
    elif otherwise:
        otherwise()


def wait(seconds: float = None):
    import time
    if seconds:
        time.sleep(seconds)
    else:
        renderer.wait_for_key()


def setvar(path: str, value):
    parts = path.split(".")
    ref = ctx
    for p in parts[:-1]:
        ref = ref.setdefault(p, {})
    key = parts[-1]
    if isinstance(ref.get(key), (int, float)) and isinstance(value, (int, float)):
        ref[key] = ref.get(key, 0) + value
    else:
        ref[key] = value
