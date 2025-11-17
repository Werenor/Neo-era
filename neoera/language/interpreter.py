# neoera/language/interpreter.py

from neoera.language.expr_eval import ExprEvaluator
from neoera.language.commands import COMMANDS


class Interpreter:
    def __init__(self, context, renderer):
        self.ctx = context
        self.renderer = renderer
        self.eval = ExprEvaluator(context)

    def execute(self, ast):
        for stmt in ast:
            self.execute_statement(stmt)

    def execute_statement(self, s):
        t = s["type"]

        # --------------------------
        # echo
        # --------------------------
        if t == "echo":
            text = self.eval.eval(s["expr"])
            self.renderer.echo(text)
            return

        # --------------------------
        # set
        # --------------------------
        if t == "set":
            v = self.eval.eval(s["expr"])
            self.ctx.set(s["name"], v)
            return

        # --------------------------
        # choice
        # --------------------------
        if t == "choice":
            idx = self.renderer.print_choice(s["options"])
            self.ctx.set("choice", idx)
            return

        # --------------------------
        # if
        # --------------------------
        if t == "if":
            if self.eval.eval(s["condition"]):
                for sub in s["then"]:
                    self.execute_statement(sub)
            else:
                handled = False
                if "elseif" in s:
                    for e in s["elseif"]:
                        if self.eval.eval(e["condition"]):
                            for sub in e["then"]:
                                self.execute_statement(sub)
                            handled = True
                            break
                if not handled and "else" in s and s["else"]:
                    for sub in s["else"]:
                        self.execute_statement(sub)
            return

        # --------------------------
        # simple commands
        # --------------------------
        if t == "bg":
            self.renderer.load_background(s["path"])
            return

        if t == "bgm":
            self.renderer.play_bgm(s["path"])
            return

        if t == "stop_bgm":
            self.renderer.stop_bgm()
            return

        if t == "sprite_show":
            self.renderer.show_sprite(s["path"], s["pos"])
            return

        if t == "sprite_hide":
            self.renderer.hide_sprite(s["path"])
            return

        print(f"[WARN] 未知语句类型: {t}")
