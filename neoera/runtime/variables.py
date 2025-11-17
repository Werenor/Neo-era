class Var:
    def __init__(self, value):
        self.value = value

    def as_bool(self):
        if isinstance(self.value, bool):
            return self.value
        if isinstance(self.value, (int, float)):
            return self.value != 0
        if isinstance(self.value, str):
            return len(self.value) > 0
        return bool(self.value)

    def get(self):
        return self.value

    def set(self, v):
        self.value = v
