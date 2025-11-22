import pygame

class VBox:
    """
    垂直布局：
        spacing: 元素间距
        align: left/center/right
    """

    def __init__(self, props=None):
        props = props or {}

        self.x = props.get("x", 0)
        self.y = props.get("y", 0)
        self.spacing = props.get("spacing", 10)
        self.align = props.get("align", "left")

        self.children = []
        self.parent = None

        self.bindings = {}
        for k, v in props.items():
            if isinstance(v, tuple) and v[0] == "binding":
                self.bindings[k] = v[1]

    def update(self, ctx):
        for k, expr_ast in self.bindings.items():
            val = ctx.eval.eval(expr_ast)
            if k == "x": self.x = int(val)
            elif k == "y": self.y = int(val)

        # 更新子节点
        for c in self.children:
            c.update(ctx)

        # 重新布局
        cur_y = self.y
        for c in self.children:
            c.y = cur_y
            cur_y += getattr(c, "height", 30) + self.spacing

    def draw(self, screen):
        for c in self.children:
            c.draw(screen)

    def bind_event(self, event_type, handler_name):
        pass
