class Transition:
    """
    简单过渡系统：用于淡入淡出背景、立绘
    """

    def __init__(self):
        self.active = False

    def fade_in(self, sprite, duration=0.5):
        sprite["alpha"] = 0
        sprite["target_alpha"] = 255
        self.active = True

    def fade_out(self, sprite, duration=0.5):
        sprite["target_alpha"] = 0
        self.active = True
