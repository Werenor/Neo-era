"""
Neo-era Runtime Context
管理全局状态、变量与标志位
"""


import json, os

class Context:
    def __init__(self):
        self.vars = {}
        self.flags = {}

    def set(self, key, value):
        self.vars[key] = value

    def get(self, key, default=None):
        return self.vars.get(key, default)

    def flag(self, name, value=True):
        self.flags[name] = value

    def check(self, name):
        return self.flags.get(name, False)

    def save(self, file_path="save.json"):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({"vars": self.vars, "flags": self.flags}, f, ensure_ascii=False, indent=2)

    def load(self, file_path="save.json"):
        if not os.path.exists(file_path): return
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.vars, self.flags = data["vars"], data["flags"]
