from neoera.language.expr_eval import ExprEvaluator
from neoera.language.commands import *


class Interpreter:
    """
    Neo-era v0.4.2 解释器
    将 AST 节点转换为执行器使用的 (result, payload)
    """
    def __init__(self, script_ast, ctx, renderer):
        self.program = script_ast
        self.ctx = ctx
        self.renderer = renderer
        self.eval = ExprEvaluator(ctx)
        self.pc = 0

    # ------------------------------------------------
    # Public API
    # ------------------------------------------------
    def has_next(self):
        return self.pc < len(self.program)

    def exec_stmt(self):
        if not self.has_next():
            return ("END", None)

        stmt = self.program[self.pc]
        self.pc += 1

        # ============================================================
        # echo
        # ============================================================
        if isinstance(stmt, EchoNode):
            return ("ECHO", stmt.text)

        # ============================================================
        # assignment
        # ============================================================
        if isinstance(stmt, AssignmentNode):
            val = self.eval.eval(stmt.expr)
            self.ctx.variables.set(stmt.name, val)
            return (None, None)

        # ============================================================
        # if
        # ============================================================
        if isinstance(stmt, IfNode):
            cond = self.eval.eval(stmt.condition)
            if cond:
                block = stmt.true_block
            else:
                block = stmt.false_block or []
            # inline execution of block
            self.program[self.pc:self.pc] = block
            return (None, None)

        # ============================================================
        # while
        # ============================================================
        if isinstance(stmt, WhileNode):
            cond = self.eval.eval(stmt.condition)
            if cond:
                block = stmt.body
                # re-insert while + its block
                self.program[self.pc:self.pc] = block + [stmt]
            return (None, None)

        # ============================================================
        # choice
        # ============================================================
        if isinstance(stmt, ChoiceNode):
            return ("CHOICE", stmt.items)

        # ============================================================
        # input
        # ============================================================
        if isinstance(stmt, InputNode):
            return ("INPUT", {
                "var": stmt.var_name,
                "prompt": stmt.prompt
            })

        # ============================================================
        # delay
        # ============================================================
        if isinstance(stmt, DelayNode):
            seconds = self.eval.eval(stmt.seconds)
            return ("DELAY", seconds)

        # ============================================================
        # end
        # ============================================================
        if isinstance(stmt, EndNode):
            return ("END", None)

        # ============================================================
        # background
        # ============================================================
        if isinstance(stmt, BackgroundNode):
            return ("RENDER", {
                "type": "BG",
                "name": stmt.name
            })

        # ============================================================
        # sprite_show / sprite_hide
        # ============================================================
        if isinstance(stmt, SpriteShowNode):
            x = self.eval.eval(stmt.x) if stmt.x is not None else 0
            y = self.eval.eval(stmt.y) if stmt.y is not None else 0
            return ("RENDER", {
                "type": "SPRITE_SHOW",
                "name": stmt.name,
                "x": x,
                "y": y
            })

        if isinstance(stmt, SpriteHideNode):
            return ("RENDER", {
                "type": "SPRITE_HIDE",
                "name": stmt.name
            })

        # ============================================================
        # BGM
        # ============================================================
        if isinstance(stmt, BGMPlayNode):
            return ("RENDER", {
                "type": "BGM_PLAY",
                "name": stmt.name
            })

        if isinstance(stmt, BGMStopNode):
            return ("RENDER", {
                "type": "BGM_STOP"
            })

        # ============================================================
        # UI
        # ============================================================
        if isinstance(stmt, UIScreenShowNode):
            return ("UI_SHOW", stmt.screen_name)

        if isinstance(stmt, UIScreenHideNode):
            return ("UI_HIDE", None)

        # ============================================================
        # NEW Animation Commands (v0.4.2)
        # ============================================================

        # sprite_move
        if isinstance(stmt, SpriteMoveNode):
            return ("RENDER", {
                "type": "SPRITE_MOVE",
                "name": stmt.name,
                "x": self.eval.eval(stmt.x),
                "y": self.eval.eval(stmt.y),
                "duration": self.eval.eval(stmt.duration),
                "wait_animation": True
            })

        # sprite_fadein
        if isinstance(stmt, SpriteFadeInNode):
            return ("RENDER", {
                "type": "SPRITE_FADE_IN",
                "name": stmt.name,
                "duration": self.eval.eval(stmt.duration),
                "wait_animation": True
            })

        # sprite_fadeout
        if isinstance(stmt, SpriteFadeOutNode):
            return ("RENDER", {
                "type": "SPRITE_FADE_OUT",
                "name": stmt.name,
                "duration": self.eval.eval(stmt.duration),
                "wait_animation": True
            })

        # sprite_scale
        if isinstance(stmt, SpriteScaleNode):
            return ("RENDER", {
                "type": "SPRITE_SCALE",
                "name": stmt.name,
                "scale": self.eval.eval(stmt.scale),
                "duration": self.eval.eval(stmt.duration),
                "wait_animation": True
            })

        # ============================================================
        # fallback: echo
        # ============================================================
        return ("ECHO", str(stmt))
