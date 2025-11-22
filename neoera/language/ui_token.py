# language/ui_token.py
print("Loaded ui_token with TAB support")

class UILine:
    """
    UI DSL 的行单位：
    - indent 空格数
    - raw 原始文本
    - stripped 去掉前置空格后的内容
    - line_no 行号
    """
    def __init__(self, raw, line_no):
        # Remove UTF-8 BOM
        raw = raw.lstrip("\ufeff")
        raw = raw.replace("\t", "    ")
        self.raw = raw.rstrip("\n")
        self.line_no = line_no

        self.indent = len(self.raw) - len(self.raw.lstrip(" "))
        self.stripped = self.raw.strip()

    def is_empty(self):
        return self.stripped == ""

    def is_comment(self):
        return self.stripped.startswith("#")

    def __repr__(self):
        return f"UILine({self.line_no}, indent={self.indent}, '{self.stripped}')"


class UITokenStream:
    """
    比 NSL 简单的行流，但提供 peek/next/reset_indent 等能力。
    Parser 会用它来读取 UI 块。
    """
    def __init__(self, text):
        lines = text.split("\n")
        self.lines = [UILine(line, i+1) for i, line in enumerate(lines)]

        self.pos = 0

    def eof(self):
        return self.pos >= len(self.lines)

    def peek(self):
        return None if self.eof() else self.lines[self.pos]

    def next(self):
        line = self.peek()
        if line:
            self.pos += 1
        return line

    def expect(self, text):
        line = self.next()
        if not line or line.stripped != text:
            raise SyntaxError(f"Expected '{text}' at line {line.line_no if line else 'EOF'}")

    def rewind_line(self):
        if self.pos > 0:
            self.pos -= 1
