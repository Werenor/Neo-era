class Interpreter:
    def __init__(self, story):
        self.story = story
        self.ctx = {}

    def run(self, node="start"):
        for line in self.story[node]:
            if "say" in line:
                print(f"{line['say']}：{line['text']}")
            if "choice" in line:
                for i, opt in enumerate(line["choice"], 1):
                    print(f"[{i}] {opt['text']}")
                sel = int(input("> ")) - 1
                return self.run(line["choice"][sel]["goto"])
