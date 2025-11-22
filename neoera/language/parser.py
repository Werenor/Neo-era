from neoera.language.commands import *
from neoera.language.expr_parser import ExprParser


class Parser:
    def __init__(self):
        self.lines = []
        self.i = 0
        self.expr = ExprParser()

    # ---------------------------------------------
    # Public Entry
    # ---------------------------------------------
    def parse(self, text):
        self.lines = text.splitlines()
        self.i = 0
        return self.parse_lines()

    # ---------------------------------------------
    # Helpers
    # ---------------------------------------------
    def eof(self):
        return self.i >= len(self.lines)

    def peek(self):
        if self.eof():
            return ""
        return self.lines[self.i].strip()

    def next(self):
        if not self.eof():
            self.i += 1

    def parse_args(self, arg_list):
        """
        arg_list: ["x=200", "y=300", "duration=1"]
        returns dict
        """
        result = {}
        for token in arg_list:
            if "=" in token:
                k, v = token.split("=", 1)
                result[k.strip()] = self.expr.parse(v.strip())
        return result

    # ---------------------------------------------
    # Main parse loop
    # ---------------------------------------------
    def parse_lines(self):
        program = []
        while not self.eof():
            line = self.peek()
            if not line:
                self.next()
                continue
            stmt = self._parse_line(line)
            if stmt is not None:
                program.append(stmt)
            self.next()
        return program

    # ---------------------------------------------
    # Parse one line
    # ---------------------------------------------
    def _parse_line(self, line):
        if not line or line.startswith("#"):
            return None

        parts = line.split()
        head = parts[0]
        args = parts[1:]

        # ------------------------------------------------
        # echo "text..."
        # ------------------------------------------------
        if head == "echo":
            text = line[len("echo"):].strip()
            return EchoNode(text)

        # ------------------------------------------------
        # var = expr
        # ------------------------------------------------
        if "=" in line and not head.startswith("sprite_"):
            # assignment form
            name, expr_text = line.split("=", 1)
            name = name.strip()
            expr = self.expr.parse(expr_text.strip())
            return AssignmentNode(name, expr)

        # ------------------------------------------------
        # if expr
        # ------------------------------------------------
        if head == "if":
            condition = self.expr.parse(" ".join(args))
            self.next()
            true_block = self._parse_block()

            false_block = None
            line2 = self.peek()
            if line2.startswith("else"):
                self.next()
                false_block = self._parse_block()

            return IfNode(condition, true_block, false_block)

        # ------------------------------------------------
        # while expr
        # ------------------------------------------------
        if head == "while":
            condition = self.expr.parse(" ".join(args))
            self.next()
            body = self._parse_block()
            return WhileNode(condition, body)

        # ------------------------------------------------
        # choice:
        #   "text" -> idx
        # ------------------------------------------------
        if head == "choice":
            self.next()
            items = []
            while not self.eof():
                ln = self.peek()
                if ln == "end":
                    break
                if "->" in ln:
                    text, target = ln.split("->", 1)
                    text = text.strip().strip('"').strip("'")
                    target = int(target.strip())
                    items.append(ChoiceItemNode(text, target))
                self.next()
            return ChoiceNode(items)

        # ------------------------------------------------
        # input var prompt="xxx"
        # ------------------------------------------------
        if head == "input":
            var = args[0]
            params = self.parse_args(args[1:])
            prompt = params.get("prompt", None)
            return InputNode(var, prompt)

        # ------------------------------------------------
        # delay seconds
        # ------------------------------------------------
        if head == "delay":
            sec = self.expr.parse(args[0])
            return DelayNode(sec)

        # ------------------------------------------------
        # end
        # ------------------------------------------------
        if head == "end":
            return EndNode()

        # ------------------------------------------------
        # background
        # bg name
        # ------------------------------------------------
        if head == "bg":
            return BackgroundNode(args[0])

        # ------------------------------------------------
        # sprite_show hero x=100 y=200
        # ------------------------------------------------
        if head == "sprite_show":
            name = args[0]
            params = self.parse_args(args[1:])
            return SpriteShowNode(name, params.get("x"), params.get("y"))

        # ------------------------------------------------
        # sprite_hide hero
        # ------------------------------------------------
        if head == "sprite_hide":
            return SpriteHideNode(args[0])

        # ------------------------------------------------
        # BGM
        # ------------------------------------------------
        if head == "bgm_play":
            return BGMPlayNode(args[0])
        if head == "bgm_stop":
            return BGMStopNode()

        # ------------------------------------------------
        # UI
        # ------------------------------------------------
        if head == "ui_show":
            return UIScreenShowNode(args[0])
        if head == "ui_hide":
            return UIScreenHideNode()

        # ------------------------------------------------
        # NEW ANIMATION COMMANDS (v0.4.2)
        # ------------------------------------------------

        # sprite_move hero x=200 y=100 duration=1
        if head == "sprite_move":
            name = args[0]
            params = self.parse_args(args[1:])
            return SpriteMoveNode(
                name,
                params.get("x", 0),
                params.get("y", 0),
                params.get("duration", 1.0)
            )

        # sprite_fadein hero duration=0.6
        if head == "sprite_fadein":
            name = args[0]
            params = self.parse_args(args[1:])
            return SpriteFadeInNode(
                name,
                params.get("duration", 0.6)
            )

        # sprite_fadeout hero duration=0.6
        if head == "sprite_fadeout":
            name = args[0]
            params = self.parse_args(args[1:])
            return SpriteFadeOutNode(
                name,
                params.get("duration", 0.6)
            )

        # sprite_scale hero to=1.4 duration=0.4
        if head == "sprite_scale":
            name = args[0]
            params = self.parse_args(args[1:])
            return SpriteScaleNode(
                name,
                params.get("to", 1.0),
                params.get("duration", 0.4)
            )

        # ------------------------------------------------
        # Unknown line → treat as echo fallback
        # ------------------------------------------------
        return EchoNode(line)

    # ---------------------------------------------
    # Parse block used by if/while
    # ---------------------------------------------
    def _parse_block(self):
        block = []
        while not self.eof():
            line = self.peek()
            if line == "end":
                break
            stmt = self._parse_line(line)
            if stmt:
                block.append(stmt)
            self.next()
        return block
