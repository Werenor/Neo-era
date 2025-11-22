"""
简单事件总线，用于引擎内部模块互相通信。
"""


class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name, callback):
        self.subscribers.setdefault(event_name, []).append(callback)

    def emit(self, event_name, *args, **kwargs):
        if event_name not in self.subscribers:
            return
        for cb in self.subscribers[event_name]:
            cb(*args, **kwargs)


EVENT_BUS = EventBus()
