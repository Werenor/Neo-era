# /neoera/interpreter.py
"""
Neo-era Interpreter v3 — 多媒体扩展
支持：
- text / echo / set / if / else / choice
- bg / bgm / stop_bgm
- sprite_show / sprite_hide
"""

from neoera import renderer_gui as renderer
import re


class Interpreter:
    def __init__(self, ctx):
        self.ctx = ctx

    def execute(self, ast):
        for statement in ast:
            print("[DEBUG]执行语句",statement)
            self.execute_statement(statement)

    def execute_statement(self, statement):
        stype = statement.get("type")
        if stype == "echo":
            self.execute_echo(statement)
        elif stype == "text":
            self.execute_text(statement)
        elif stype == "choice":
            self.execute_choice(statement)
        elif stype == "set":
            self.execute_set(statement)
        elif stype == "if":
            self.execute_if(statement)
        elif stype == "bg":
            renderer.load_background(statement.get("path"))
        elif stype == "bgm":
            renderer.play_bgm(statement.get("path"))
        elif stype == "stop_bgm":
            renderer.stop_bgm()
        elif stype == "sprite_show":
            renderer.show_sprite(statement.get("path"), statement.get("pos"))
        elif stype == "sprite_hide":
            renderer.hide_sprite(statement.get("path"))
        else:
            print(f"[WARN] 未知语句类型: {stype}")

    # --------------------------------------------------
    def execute_echo(self, statement):
        text = statement["expression"]["value"]
        text = self.interpolate(text)
        renderer.queue_echo(text)

    def execute_text(self, statement):
        text = self.interpolate(statement.get("text", ""))
        renderer.queue_echo(text)

    def execute_choice(self, statement):
        options = statement.get("options", [])
        renderer.queue_choice(options)
        result = renderer.wait_for_choice()
        self.ctx.set("choice", result)
        renderer.queue_echo(f"[选择] -> {options[result]}")

    def execute_set(self, statement):
        name = statement.get("name")
        expr = statement.get("expr")
        try:
            value = eval(expr, {}, dict(self.ctx))
        except Exception:
            value = expr.strip('"')
        self.ctx.set(name, value)

    def execute_if(self, statement):
        condition = statement.get("condition", "")
        try:
            result = bool(eval(condition, {}, dict(self.ctx)))
        except Exception:
            result = False
        if result:
            self.execute(statement.get("then", []))
        else:
            self.execute(statement.get("else", []))

    # --------------------------------------------------
    def interpolate(self, text: str) -> str:
        def repl(match):
            var = match.group(1)
            return str(self.ctx.get(var, f"{{{var}}}"))
        return re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", repl, text)
