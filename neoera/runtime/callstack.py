class CallStack:
    """
    未来扩展：支持 scene / goto / return。
    当前版本为占位实现。
    """
    def __init__(self):
        self.stack = []

    def push(self, frame):
        self.stack.append(frame)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def empty(self):
        return len(self.stack) == 0
