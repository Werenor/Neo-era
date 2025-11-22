class AnimationQueue:
    """
    AnimationQueue：
    - 支持 push(animation)
    - 自动更新 animation 队列
    - 支持并行动画（parallel=True）
    """

    def __init__(self):
        self.queue = []          # [(animation, parallel_flag)]
        self.active_list = []    # 正在播放的 animation

    def push(self, animation, parallel=False):
        self.queue.append((animation, parallel))

    def update(self, dt):
        # 先更新正在播放的 animation
        for anim in self.active_list[:]:
            anim.update(dt)
            if anim.finished:
                self.active_list.remove(anim)

        # 若 active_list 空了 → 拉下一个 animation
        if not self.active_list and self.queue:
            anim, parallel = self.queue.pop(0)

            self.active_list.append(anim)

            # 若 parallel → 同时启动所有 parallel 项
            if parallel:
                while self.queue and self.queue[0][1] == True:
                    a2, p2 = self.queue.pop(0)
                    self.active_list.append(a2)

    def active(self):
        """RendererCore 用于判断是否在动画中"""
        return bool(self.active_list or self.queue)
