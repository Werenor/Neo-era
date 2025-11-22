class Overlay:
    """
    用于顶层覆盖的 UI。
    """

    def __init__(self, props=None):
        props = props or {}

        self.children = []
        self.parent = None

        self.bindings = {}

    def update(self, ctx):
        for c in self.children:
            c.update(ctx)

    def draw(self, screen):
        for c in self.children:
            c.draw(screen)

    def bind_event(self, event_type, handler_name):
        pass
