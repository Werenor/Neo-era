import pygame

class Grid:
    """
    网格布局：
        rows: 行数
        cols: 列数
        spacing: 单元格之间的空隙
    """

    def __init__(self, props=None):
        props = props or {}

        self.x = props.get("x", 0)
        self.y = props.get("y", 0)
        self.rows = props.get("rows", 1)
        self.cols = props.get("cols", 1)
        self.spacing = props.get("spacing", 10)

        self.children = []
        self.parent = None

        self.bindings = {}
        for k, v in props.items():
            if isinstance(v, tuple) and v[0] == "binding":
                self.bindings[k] = v[1]

    def update(self, ctx):
        # 动态绑定
        for k, expr_ast in self.bindings.items():
            val = ctx.eval.eval(expr_ast)
            if k == "x":
                self.x = int(val)
            elif k == "y":
                self.y = int(val)

        for c in self.children:
            c.update(ctx)

        # 布局
        w = getattr(self.children[0], "width", 50) if self.children else 50
        h = getattr(self.children[0], "height", 30) if self.children else 30

        for index, c in enumerate(self.children):
            r = index // self.cols
            col = index % self.cols
            c.x = self.x + col * (w + self.spacing)
            c.y = self.y + r * (h + self.spacing)

    def draw(self, screen):
        for c in self.children:
            c.draw(screen)

    def bind_event(self, event_type, handler_name):
        pass
