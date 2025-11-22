import pygame
from neoera.core.config import CONFIG


class UILabel:
    def __init__(self, props=None):
        props = props or {}
        self.text = props.get("text", "")
        self.font_size = props.get("font_size", 28)
        self.color = props.get("color", (255, 255, 255))
        self.x = props.get("x", 0)
        self.y = props.get("y", 0)

        self.font = pygame.font.Font(CONFIG.FONT_PATH, self.font_size)
        self.children = []
        self.parent = None

        # 表达式绑定
        self.bindings = {}
        for k, v in props.items():
            if isinstance(v, tuple) and v[0] == "binding":
                self.bindings[k] = v[1]

    def update(self, ctx):
        # 动态绑定更新
        for k, expr_ast in self.bindings.items():
            val = ctx.eval.eval(expr_ast)
            if k == "text":
                self.text = str(val)

    def draw(self, screen):
        surf = self.font.render(self.text, True, self.color)
        screen.blit(surf, (self.x, self.y))

        # 注意：Label 没有子元素，但保持结构一致性
        for c in self.children:
            c.draw(screen)

    def bind_event(self, event_type, handler_name):
        # label 无点击事件（不处理）
        pass
