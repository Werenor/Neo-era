import pygame
from neoera.core.resource_manager import RESOURCE_MANAGER
from neoera.render.animation.tween import Tween
from neoera.render.animation.animation import Animation
from neoera.render.animation.animation_queue import AnimationQueue


class InputBox:
    """
    v2.5 InputBox:
    - 动画出现（alpha + y 移动）
    - 光标闪烁
    - 回车提交
    - 中文输入兼容：直接接收 unicode
    """

    def __init__(self):
        self.font = RESOURCE_MANAGER.load_font(size=32)

        self.visible = False
        self.prompt = ""
        self.text = ""
        self.result = None

        self.alpha = 0
        self.offset_y = 20

        self.rect = pygame.Rect(320, 280, 640, 70)

        self.anim = AnimationQueue()

        # 光标闪烁
        self.cursor_timer = 0
        self.cursor_visible = True

    # --------------------------------------------------------
    # 显示输入框
    # --------------------------------------------------------
    def show(self, prompt):
        self.visible = True
        self.prompt = prompt
        self.text = ""
        self.result = None

        self.alpha = 0
        self.offset_y = 20

        # 动画
        tw1 = Tween(self, "alpha", 0, 255, 0.3, easing="ease_out")
        tw2 = Tween(self, "offset_y", 20, 0, 0.3, easing="ease_out")

        self.anim.push(Animation([tw1, tw2]), parallel=True)

    # --------------------------------------------------------
    # 输入完成？
    # --------------------------------------------------------
    def has_result(self):
        return self.result is not None

    def get_result(self):
        r = self.result
        self.visible = False
        self.result = None
        return r

    # --------------------------------------------------------
    # 输入字符 / 删除 / 回车
    # --------------------------------------------------------
    def handle_key(self, event):
        if not self.visible:
            return

        if event.key == pygame.K_RETURN:
            self.result = self.text
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            c = event.unicode
            if c:
                self.text += c

    # --------------------------------------------------------
    # 更新
    # --------------------------------------------------------
    def update(self, dt):
        if not self.visible:
            return

        self.anim.update(dt)

        # 光标闪烁
        self.cursor_timer += dt
        if self.cursor_timer > 0.5:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    # --------------------------------------------------------
    # 绘制
    # --------------------------------------------------------
    def draw(self, screen):
        if not self.visible:
            return

        r = pygame.Rect(
            self.rect.x,
            self.rect.y + self.offset_y,
            self.rect.width,
            self.rect.height
        )

        # 背景
        box = pygame.Surface((r.width, r.height))
        box.fill((30, 30, 30))
        box.set_alpha(int(self.alpha))
        screen.blit(box, r)

        # 文本
        content = f"{self.prompt}: {self.text}"
        txt = self.font.render(content, True, (255,255,255))
        screen.blit(txt, (r.x + 15, r.y + 20))

        # 光标
        if self.cursor_visible:
            cx = r.x + 15 + txt.get_width() + 5
            cy = r.y + 25
            pygame.draw.rect(screen, (255, 255, 255), (cx, cy, 15, 3))

    def handle_event(self, event):
        # 如果有可见 / 激活标记，按你的类实际字段来判断
        if hasattr(self, "visible"):
            if not self.visible:
                return None
        elif hasattr(self, "active"):
            if not self.active:
                # 如果你的逻辑是点到输入框才激活，就按需调整
                pass

        # 键盘输入交给原来的 handle_key 处理
        if event.type == pygame.KEYDOWN:
            # 这里假设 handle_key 自己处理文本、退格等逻辑
            self.handle_key(event)

            # 如果你希望在回车时返回最终输入给 Executor，可以这么写：
            # if event.key == pygame.K_RETURN:
            #     return self.text

        return None
