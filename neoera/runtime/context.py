from neoera.runtime.variables import Var


class Context:
    def __init__(self):
        self.data = {}

    def set(self, name, value):
        print(f"[DEBUG] Context set: {name} = {value}")
        self.data[name] = Var(value)

    def get(self, name):
        if name not in self.data:
            return None
        return self.data[name].get()

    def exists(self, name):
        return name in self.data
