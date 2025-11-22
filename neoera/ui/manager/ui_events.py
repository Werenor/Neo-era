# ui/manager/ui_events.py

class UIEventResult:
    """当用户点击 UI 的按钮时产生的事件结果"""
    def __init__(self, handler_name):
        self.handler = handler_name
