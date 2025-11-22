# ui/manager/ui_state.py

class UIState:
    """
    UI 的运行时状态：
    - active_screen: 当前显示的 UI 树（root component）
    - active_name: 屏幕名（字符串）
    - ui_result: UI 返回给 executor 的事件 id
    """

    def __init__(self):
        self.active_screen = None
        self.active_name = None
        self.ui_result = None

    def clear_result(self):
        self.ui_result = None
