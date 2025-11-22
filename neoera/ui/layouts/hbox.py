import pygame

class HBox:
    """
    水平布局：
        spacing: 元素水平间距
        align: top/center/bottom
    """

    def __init__(self, props=None):
        props = props or {}
        self.x = props.get("x", 0)
        self.y = props.get("y", 0)
        self.spacing = props.get("spacing", 10)
        self.align = props.get("align", "top")

        self.children = []
        self.parent = None

        self.bindings = {}
        for k, v in props.items():
            if isinstance(v, tuple) and v[0] == "binding":
                self.bindings[k] = v[1]

    def update(self, ctx):
        # 绑定更新
        for k, expr_ast in self.bindings.items():
            val = ctx.eval.eval(expr_ast)
            if k == "x": self.x = int(val)
            elif k == "y": self.y = int(val)

        for c in self.children:
            c.update(ctx)

        # 布局
        cur_x = self.x
        for c in self.children:
            c.x = cur_x
            cur_x += getattr(c, "width", 50) + self.spacing

    def draw(self, screen):
        for c in self.children:
            c.draw(screen)

    def bind_event(self, event_type, handler_name):
        pass
