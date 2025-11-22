from neoera.runtime.variables import Variables

class RuntimeContext:
    """
    Neo-era v0.4.2 运行时上下文
    - variables: 变量存储（新版 interpreter 依赖）
    - get/set: 兼容旧版 API
    """
    def __init__(self):
        # 新版：interpreter 需要访问 context.variables
        self.variables = Variables()

    # --------- 新版接口（interpreter 使用） ---------
    def set_var(self, key, value):
        self.variables.set(key, value)

    def get_var(self, key):
        return self.variables.get(key)

    # --------- 兼容旧版 API（保持不破坏旧逻辑） ---------
    def set(self, key, value):
        self.variables.set(key, value)

    def get(self, key):
        return self.variables.get(key)


# 兼容旧引用方式（保持名字不变）
Context = RuntimeContext
