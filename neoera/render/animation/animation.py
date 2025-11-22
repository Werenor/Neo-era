class Animation:
    """
    一个 Animation 由多个 Tween 组成。
    当所有 Tween 完成时，Animation 完成。
    """

    def __init__(self, tweens):
        self.tweens = tweens
        self.finished = False

    def update(self, dt):
        if self.finished:
            return

        active = False
        for tw in self.tweens:
            if not tw.finished:
                tw.update(dt)
                active = True

        if not active:
            self.finished = True
