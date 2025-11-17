import re


class Lexer:
    def __init__(self):
        self.tokens = []

    def lex(self, text):
        text = text.replace("\r\n", "\n")
        lines = text.split("\n")
        tokens = []

        for line_no, raw_line in enumerate(lines, 1):
            line = raw_line.strip()
            if not line:
                continue

            if line.startswith("#"):
                continue

            # 指令类
            if line.startswith(("if ", "elif ", "else", "fi",
                                "while ", "wend",
                                "set ", "echo ", "bg ", "bgm ", "stop_bgm",
                                "choice ", "sprite_show ", "sprite_hide ",
                                "scene ", "goto ", "return")):
                tokens.append(("CMD", line, line_no))
                continue

            # 其他全部视作纯文本
            tokens.append(("TEXT", line, line_no))

        self.tokens = tokens
        return tokens
