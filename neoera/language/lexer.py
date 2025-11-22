import re


class Lexer:
    """
    行级脚本 lexer：
    输入：脚本的一行
    输出：(cmd, args[])
    """

    COMMANDS = {
        "echo", "set", "if", "elseif", "else", "endif",
        "choice",
        "bg", "bgm", "stop_bgm",
        "sprite_show", "sprite_hide",
        "show_sprite", "hide_sprite",
        "delay", "wait",
        "input", "font",
    }

    def tokenize_line(self, line):
        """
        将一行脚本拆成：“命令 + 参数 tokens”
        返回格式：
            ("cmd", ["arg1", "arg2", ...])
        or
            ("text", [text])
        """

        s = line.strip()
        if not s:
            return None

        if s.startswith("#"):
            return None

        # TEXT（隐式 echo）
        if not any(s.lower().startswith(c + " ") for c in self.COMMANDS) and \
           not s.lower().split(" ")[0] in self.COMMANDS:
            # TEXT 行 → 转为 text 命令
            return "text", [s]

        parts = s.split()
        cmd = parts[0].lower()
        args = parts[1:]

        return cmd, args
