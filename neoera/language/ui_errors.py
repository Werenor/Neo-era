# language/ui_errors.py

class UISyntaxError(Exception):
    def __init__(self, message, line_no=None):
        if line_no:
            super().__init__(f"[UI Syntax Error @ line {line_no}] {message}")
        else:
            super().__init__(f"[UI Syntax Error] {message}")
        self.line_no = line_no
