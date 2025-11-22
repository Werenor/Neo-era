import pygame


class UIBar:
    """
    通用条形组件，例如 HP 条 / 进度条。
    支持：
      - max / value
      - fg_color / bg_color
      - 宽高
      - 表达式绑定：{hp}, {max_hp}
    """

    def __init__(self, props=None):
        props = props or {}

        self.x = props.get("x", 0)
        self.y = props.get("y", 0)
        self.width = props.get("width", 100)
        self.height = props.get("height", 20)

        self.max_value = props.get("max", 100)
        self.value = props.get("value", 100)

        self.bg_color = props.get("bg_color", (40, 40, 40))
        self.fg_color = props.get("fg_color", (200, 0, 0))

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

            if k == "value":
                self.value = float(val)
            elif k == "max":
                self.max_value = float(val)
            elif k == "x":
                self.x = int(val)
            elif k == "y":
                self.y = int(val)
            elif k == "alpha":
                self.alpha = int(val)

    # ------------------------------------------------------
    # 绘制
    # ------------------------------------------------------
    def draw(self, screen):
        # 背景
        bg = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        bg.fill((*self.bg_color, self.alpha))
        screen.blit(bg, (self.x, self.y))

        # 前景（数值区间）
        if self.max_value > 0:
            ratio = max(0, min(1, self.value / self.max_value))
        else:
            ratio = 0

        fg_width = int(self.width * ratio)
        if fg_width > 0:
            fg = pygame.Surface((fg_width, self.height), pygame.SRCALPHA)
            fg.fill((*self.fg_color, self.alpha))
            screen.blit(fg, (self.x, self.y))

        # 子组件
        for c in self.children:
            c.draw(screen)

    # ------------------------------------------------------
    # bar 不处理点击事件
    # ------------------------------------------------------
    def bind_event(self, event_type, handler_name):
        pass
