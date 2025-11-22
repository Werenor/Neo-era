import pygame
from neoera.core.resource_manager import ResourceManager


class UIImage:
    def __init__(self, props=None):
        props = props or {}

        self.src = props.get("src", None)      # 图片路径（资源名）
        self.x = props.get("x", 0)
        self.y = props.get("y", 0)

        self.width = props.get("width", None)
        self.height = props.get("height", None)

        self.alpha = props.get("alpha", 255)

        self.children = []
        self.parent = None

        # 绑定表达式
        self.bindings = {}
        for k, v in props.items():
            if isinstance(v, tuple) and v[0] == "binding":
                self.bindings[k] = v[1]

        # 加载图像
        self.surface = None
        if self.src:
            self.surface = ResourceManager.load_image(self.src)
            if self.surface and (self.width or self.height):
                self.surface = pygame.transform.scale(
                    self.surface,
                    (
                        self.width or self.surface.get_width(),
                        self.height or self.surface.get_height()
                    )
                )
            if self.surface:
                self.surface.set_alpha(self.alpha)

    # ------------------------------------------------------
    # 绑定表达式更新
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
                if self.surface:
                    self.surface.set_alpha(self.alpha)
            elif k == "src":
                self._update_image_source(val)

    def _update_image_source(self, new_src):
        self.src = str(new_src)
        self.surface = ResourceManager.load_image(self.src)

    # ------------------------------------------------------
    # 绘制
    # ------------------------------------------------------
    def draw(self, screen):
        if self.surface:
            screen.blit(self.surface, (self.x, self.y))

        for c in self.children:
            c.draw(screen)

    # ------------------------------------------------------
    # 图片不处理点击事件
    # ------------------------------------------------------
    def bind_event(self, event_type, handler_name):
        pass
