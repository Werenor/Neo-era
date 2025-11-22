class Absolute:
    """
    保持子元素自己的 x,y，不改变位置。
    """

    def __init__(self, props=None):
        props = props or {}
        self.x = props.get("x", 0)
        self.y = props.get("y", 0)

        self.children = []
        self.parent = None

        self.bindings = {}
        for k, v in props.items():
            if isinstance(v, tuple) and v[0] == "binding":
                self.bindings[k] = v[1]

    def update(self, ctx):
        for k, expr_ast in self.bindings.items():
            val = ctx.eval.eval(expr_ast)
            if k == "x":
                self.x = int(val)
            elif k == "y":
                self.y = int(val)

        for c in self.children:
            c.update(ctx)

    def draw(self, screen):
        for c in self.children:
            c.draw(screen)

    def bind_event(self, event_type, handler_name):
        pass
