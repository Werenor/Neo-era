import pygame


class UIManager:
    """
    Neo-era v0.4.2
    管理 UI Screens 的创建、显示、事件处理、返回值。
    """

    def __init__(self, ui_screens, builder, ctx):
        """
        ui_screens: { name : UIRoot }
        builder: UIBuilder 实例
        ctx: RuntimeContext（用于动态绑定）
        """
        self.ui_screens = ui_screens
        self.builder = builder
        self.ctx = ctx

        # 当前 UI 组件树
        self.current = None

        # 按钮事件返回值（handler 名称）
        self._action = None

    # ------------------------------------------------------
    # 显示 UI
    # ------------------------------------------------------
    def show(self, screen_name):
        if screen_name not in self.ui_screens:
            print(f"[UIManager] UI screen '{screen_name}' not found.")
            self.current = None
            return

        root_ast = self.ui_screens[screen_name]
        self.current = self.builder.build(root_ast)
        self._action = None

    # ------------------------------------------------------
    # 隐藏 UI
    # ------------------------------------------------------
    def hide(self):
        self.current = None
        self._action = None

    # ------------------------------------------------------
    # 消费动作（供 Executor 使用）
    # ------------------------------------------------------
    def consume_action(self):
        act = self._action
        self._action = None
        return act

    # ------------------------------------------------------
    # 被 UIButton 调用，用来通知 Executor
    # ------------------------------------------------------
    def set_action(self, handler_name):
        self._action = handler_name

    # ------------------------------------------------------
    # 更新 UI（动态绑定）
    # ------------------------------------------------------
    def update(self, dt):
        if not self.current:
            return
        self.current.update(self.ctx)

    # ------------------------------------------------------
    # 绘制 UI
    # ------------------------------------------------------
    def draw(self, screen):
        if not self.current:
            return
        self.current.draw(screen)

    # ------------------------------------------------------
    # 事件处理
    # ------------------------------------------------------
    def handle_event(self, event):
        if not self.current:
            return None
        return self._bubble_event(self.current, event)

    # ------------------------------------------------------
    # 冒泡事件传递：从根向下传递到可点击组件
    # ------------------------------------------------------
    def _bubble_event(self, comp, event):
        # 子组件优先
        for child in comp.children:
            r = self._bubble_event(child, event)
            if r:
                return True

        # 自身处理
        if hasattr(comp, "handle_event"):
            r = comp.handle_event(event, self)
            if r:
                return True

        return False
