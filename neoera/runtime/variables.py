class Variables:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value
        print(f"[Variables] {key} = {value}")

    def get(self, key):
        return self.data.get(key, None)

    def all(self):
        return dict(self.data)
