import pygame
from neoera.core.config import CONFIG


class UIButton:
    def __init__(self, props=None):
        props = props or {}

        self.text = props.get("text", "Button")
        self.font_size = props.get("font_size", 28)
        self.color = props.get("color", (255, 255, 255))
        self.bg_color = props.get("bg_color", (50, 50, 50))
        self.hover_color = props.get("hover_color", (80, 80, 80))

        self.x = props.get("x", 0)
        self.y = props.get("y", 0)
        self.padding = props.get("padding", 10)

        self.font = pygame.font.Font(CONFIG.FONT_PATH, self.font_size)
        self.children = []
        self.parent = None

        # 是否处于 hover 状态
        self.is_hover = False

        # 点击事件绑定
        self.events = {}   # { "on_click": handler_name }

        # 表达式绑定
        self.bindings = {}
        for k, v in props.items():
            if isinstance(v, tuple) and v[0] == "binding":
                self.bindings[k] = v[1]

    # --------------------------------------------------
    # 动态绑定更新
    # --------------------------------------------------
    def update(self, ctx):
        for k, expr_ast in self.bindings.items():
            val = ctx.eval.eval(expr_ast)
            if k == "text":
                self.text = str(val)

    # --------------------------------------------------
    # 绘制
    # --------------------------------------------------
    def draw(self, screen):
        # 文字 surface
        text_surf = self.font.render(self.text, True, self.color)
        tw, th = text_surf.get_size()

        w = tw + self.padding * 2
        h = th + self.padding * 2

        rect = pygame.Rect(self.x, self.y, w, h)

        bg = self.hover_color if self.is_hover else self.bg_color
        pygame.draw.rect(screen, bg, rect, border_radius=8)
        screen.blit(text_surf, (self.x + self.padding, self.y + self.padding))

        for c in self.children:
            c.draw(screen)

    # --------------------------------------------------
    # 事件绑定（由 UIBuilder 调用）
    # --------------------------------------------------
    def bind_event(self, event_type, handler_name):
        self.events[event_type] = handler_name

    # --------------------------------------------------
    # 鼠标事件响应
    # （由 UIManager 或 Renderer 调用）
    # --------------------------------------------------
    def handle_event(self, event, ui_manager):
        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self.is_hover = self._contains(mx, my)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if self._contains(mx, my):
                if "on_click" in self.events:
                    handler = self.events["on_click"]
                    ui_manager.set_action(handler)  # 通知 UIManager
                    return True

        return False

    # --------------------------------------------------
    # hit test
    # --------------------------------------------------
    def _contains(self, x, y):
        text_surf = self.font.render(self.text, True, self.color)
        tw, th = text_surf.get_size()
        w = tw + self.padding * 2
        h = th + self.padding * 2
        rect = pygame.Rect(self.x, self.y, w, h)
        return rect.collidepoint(x, y)
