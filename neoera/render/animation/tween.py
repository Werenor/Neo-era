from neoera.render.animation.easing import Easing


class Tween:
    """
    单属性补间（Tween）：
    - 支持任意对象的任意属性（如 sprite.alpha, sprite.x）
    - 使用 easing(t) 决定动画曲线
    """

    def __init__(self, obj, attr, start, end, duration, easing="linear"):
        self.obj = obj            # 要修改的对象
        self.attr = attr          # 属性名称，如 "alpha" / "x"
        self.start = start
        self.end = end
        self.duration = duration
        self.time = 0.0

        if isinstance(easing, str):
            self.easing = getattr(Easing, easing)
        else:
            self.easing = easing

        self.finished = False

    def update(self, dt):
        if self.finished:
            return

        self.time += dt
        t = min(self.time / self.duration, 1.0)
        k = self.easing(t)
        value = self.start + (self.end - self.start) * k

        setattr(self.obj, self.attr, value)

        if t >= 1.0:
            self.finished = True
