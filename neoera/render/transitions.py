import pygame
from neoera.render.animation.tween import Tween
from neoera.render.animation.animation import Animation
from neoera.render.animation.animation_queue import AnimationQueue
from neoera.core.config import CONFIG


class BaseTransition:
    """
    抽象基类
    """
    def __init__(self, duration=0.6):
        self.duration = duration
        self.finished = False

    def start(self, renderer):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def draw(self, screen):
        pass


# --------------------------------------------------------
# Fade Transition（淡入淡出）
# --------------------------------------------------------
class FadeTransition(BaseTransition):
    def __init__(self, duration=0.6):
        super().__init__(duration)
        self.alpha = 255

    def start(self, renderer):
        self.renderer = renderer
        self.tw = Tween(self, "alpha", 255, 0, self.duration, easing="ease_out")
        self.anim = Animation([self.tw])

    def update(self, dt):
        if not self.finished:
            self.anim.update(dt)
            if self.anim.finished:
                self.finished = True

    def draw(self, screen):
        surf = pygame.Surface(CONFIG.RESOLUTION)
        surf.fill((0,0,0))
        surf.set_alpha(int(self.alpha))
        screen.blit(surf, (0,0))


# --------------------------------------------------------
# Slide Transition（滑动过场）
# --------------------------------------------------------
class SlideTransition(BaseTransition):
    def __init__(self, direction="left", duration=0.6):
        super().__init__(duration)
        self.direction = direction
        self.x = 0

    def start(self, renderer):
        self.renderer = renderer
        w, h = CONFIG.RESOLUTION

        if self.direction == "left":
            start = 0
            end = -w
        else:
            start = 0
            end = w

        self.tw = Tween(self, "x", start, end, self.duration, easing="ease_in_out")
        self.anim = Animation([self.tw])

    def update(self, dt):
        if not self.finished:
            self.anim.update(dt)
            if self.anim.finished:
                self.finished = True

    def draw(self, screen):
        tmp = screen.copy()
        screen.blit(tmp, (self.x, 0))


# --------------------------------------------------------
# 组合过渡
# --------------------------------------------------------
class CompositeTransition(BaseTransition):
    def __init__(self, transitions):
        super().__init__(duration=0)    # duration 由子项决定
        self.transitions = transitions

    def start(self, renderer):
        self.renderer = renderer
        for t in self.transitions:
            t.start(renderer)

    def update(self, dt):
        active = False
        for t in self.transitions:
            t.update(dt)
            if not t.finished:
                active = True
        if not active:
            self.finished = True

    def draw(self, screen):
        for t in self.transitions:
            t.draw(screen)


# --------------------------------------------------------
# 管理器
# --------------------------------------------------------
class TransitionManager:
    """
    允许同时管理多个 transition
    """
    def __init__(self):
        self.queue = []
        self.current = None

    def push(self, transition):
        self.queue.append(transition)

    def update(self, dt):
        if self.current is None:
            if self.queue:
                self.current = self.queue.pop(0)
                self.current.start(None)
            else:
                return

        self.current.update(dt)
        if self.current.finished:
            self.current = None

    def active(self):
        return self.current is not None or len(self.queue) > 0

    def draw(self, screen):
        if self.current:
            self.current.draw(screen)
