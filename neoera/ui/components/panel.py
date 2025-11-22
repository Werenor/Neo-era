import pygame


class UIPanel:
    """
    通用容器，可以拥有子组件。
    默认透明背景，可通过 bg_color 设置背景。
    """

    def __init__(self, props=None):
        props = props or {}

        self.x = props.get("x", 0)
        self.y = props.get("y", 0)

        self.width = props.get("width", None)
        self.height = props.get("height", None)

        self.bg_color = props.get("bg_color", None)  # e.g. (30,30,30)
        self.alpha = props.get("alpha", 255)

        self.children = []
        self.parent = None

        # 表达式绑定
        self.bindings = {}
        for k, v in props.items():
            if isinstance(v, tuple) and v[0] == "binding":
                self.bindings[k] = v[1]

    # ------------------------------------------------------
    # 动态绑定更新
    # ------------------------------------------------------
    def update(self, ctx):
        for k, expr_ast in self.bindings.items():
            val = ctx.eval.eval(expr_ast)

            if k == "x":
                self.x = int(val)
            elif k == "y":
                self.y = int(val)
            elif k == "alpha":
                self.alpha = int(val)

    # ------------------------------------------------------
    # 绘制
    # ------------------------------------------------------
    def draw(self, screen):
        # 背景颜色
        if self.bg_color:
            surf = pygame.Surface((self.width or 0, self.height or 0), pygame.SRCALPHA)
            surf.fill((*self.bg_color, self.alpha))
            screen.blit(surf, (self.x, self.y))

        # 子元素
        for c in self.children:
            c.draw(screen)

    # ------------------------------------------------------
    # Panel 不处理事件，但子组件会处理
    # ------------------------------------------------------
    def bind_event(self, event_type, handler_name):
        pass
