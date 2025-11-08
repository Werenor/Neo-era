# /neoera/runtime.py

import json
import time
import os
import heapq

class Timer:
    def __init__(self):
        self.timers = []

    def add(self, delay, event_name):
        event_time = time.time() + delay
        heapq.heappush(self.timers, (event_time, event_name))  # 使用 heapq 进行堆排序

    def update(self):
        current_time = time.time()
        while self.timers and self.timers[0][0] <= current_time:
            _, event_name = heapq.heappop(self.timers)  # 获取并移除最早的定时事件
            self.execute_event(event_name)

    def execute_event(self, event_name):
        """ 根据事件名执行相应的事件 """
        print(f"触发事件: {event_name}")
        if event_name == "change_background":
            self.change_background()

    def change_background(self):
        """ 示例事件 - 更改背景 """
        print("背景已改变！")


class Context:
    def __init__(self):
        self.vars = {}  # 临时变量
        self.perm = {}  # 持久变量
        self.flags = {}  # 事件标志位（新增）
        self.timer = Timer()  # 初始化定时器
        self.event_scheduler = EventScheduler()  # 事件调度器

    def set(self, key, value):
        """ 设置变量值 """
        self.vars[key] = value

    def get(self, key, default=None):
        """ 获取变量值 """
        return self.vars.get(key, default)

    def save(self, file_path="save.json"):
        """ 保存游戏状态，包括背景、音效等 """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        save_data = {
            "vars": self.vars,
            "perm": self.perm,
            "flags": self.flags,
            "background": current_background,  # 当前背景
            "bgm": current_bgm,  # 当前音乐
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

    def load(self, file_path="save.json"):
        """ 加载游戏状态，包括背景与音效 """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.vars = data.get("vars", {})
                self.perm = data.get("perm", {})
                self.flags = data.get("flags", {})
                self.load_background(data.get("background", ""))
                self.load_bgm(data.get("bgm", ""))
        except FileNotFoundError:
            print("没有找到存档文件。")

    def load_background(self, background):
        print(f"恢复背景: {background}")
        # 这里可以调用渲染器恢复背景

    def load_bgm(self, bgm):
        print(f"恢复背景音乐: {bgm}")
        # 这里可以调用音频系统恢复背景音乐

    def flag(self, name, value=True):
        """
        设置事件标志位
        :param name: 标志位名称
        :param value: 标志值，默认为True
        """
        self.flags[name] = value

    def check(self, name):
        """
        检查事件标志位
        :param name: 标志位名称
        :return: 如果标志位存在且为True，则返回True，否则返回False
        """
        return self.flags.get(name, False)  # 如果没有找到标志位，返回False


class Event:
    def __init__(self, event_name, trigger_time, callback, *args, **kwargs):
        self.event_name = event_name
        self.trigger_time = trigger_time
        self.callback = callback
        self.args = args  # 事件回调参数
        self.kwargs = kwargs  # 关键字参数

    def execute(self):
        """ 执行事件回调，并传递参数 """
        print(f"触发事件: {self.event_name}")
        self.callback(*self.args, **self.kwargs)


class EventScheduler:
    def __init__(self):
        self.event_queue = []  # 事件队列

    def add_event(self, event_name, delay, callback, priority=1):
        """ 添加优先级事件 """
        trigger_time = time.time() + delay
        event = Event(event_name, trigger_time, callback, priority)
        heapq.heappush(self.event_queue, (event.trigger_time, event))

    def update(self):
        current_time = time.time()
        while self.event_queue and self.event_queue[0][0] <= current_time:
            _, event = heapq.heappop(self.event_queue)
            event.execute()  # 执行事件


def change_background():
    print("切换背景！")

# 启动一个定时事件
ctx.event_scheduler.add_event("background_change", 5.0, change_background)

# 每帧更新事件调度器，触发到期事件
ctx.event_scheduler.update()
