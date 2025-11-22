class UIOverlayLayer:
    """
    Neo-era v0.4.2
    UI 叠加层：渲染 UIManager 管理的 UI Screen。
    Renderer 会把此 Layer 放在最上层。
    """

    def __init__(self, ui_manager):
        self.ui_manager = ui_manager

    # ------------------------------------------------------
    # 每帧更新（动态绑定）
    # ------------------------------------------------------
    def update(self, dt):
        if not self.ui_manager:
            return
        self.ui_manager.update(dt)

    # ------------------------------------------------------
    # 绘制 UI
    # ------------------------------------------------------
    def draw(self, screen):
        if not self.ui_manager:
            return
        self.ui_manager.draw(screen)

    # ------------------------------------------------------
    # 事件处理：交给 UIManager
    # ------------------------------------------------------
    def handle_event(self, event):
        if not self.ui_manager:
            return None
        return self.ui_manager.handle_event(event)
