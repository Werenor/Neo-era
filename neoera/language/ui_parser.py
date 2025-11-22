import re
from neoera.language.expr_parser import ExprParser
from neoera.language.ui_ast import (
    UIRoot, UIElement, UIFOR, UIEvent, UIAnim
)


class UIToken:
    def __init__(self, indent, raw, stripped, line_no):
        self.indent = indent
        self.raw = raw
        self.stripped = stripped
        self.line_no = line_no

    def __repr__(self):
        return f"UIToken({self.indent}, '{self.stripped}', line={self.line_no})"


class UIParser:
    """
    Neo-era v0.4.2 UI DSL Parser
    Features:
        - ui <name>:
        - Nested elements
        - for loops
        - events: on_click handler="xxx"
        - anim blocks: anim fade_in duration=1
        - props: key=value, text="xxx", x=100, y=200
        - indentation-based structure
    """

    def __init__(self, text):
        self.text = text
        self.lines = []
        self.idx = 0
        self.expr = ExprParser()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def parse(self):
        self._tokenize()
        self.idx = 0
        if not self.lines:
            return {}

        screens = {}
        while self.idx < len(self.lines):
            token = self.lines[self.idx]

            if not token.stripped:
                self.idx += 1
                continue

            if token.stripped.startswith("ui "):
                root = self.parse_ui_block()
                screens[root.name] = root
            else:
                raise self._syntax("Expected 'ui <name>:'", token)

        return screens

    # ---------------------------------------------------------
    # Tokenizer
    # ---------------------------------------------------------

    def _tokenize(self):
        raw_lines = self.text.splitlines()
        out = []

        for i, ln in enumerate(raw_lines, 1):
            if not ln.strip():
                out.append(UIToken(0, ln, "", i))
                continue

            # allow TAB → convert to 4 spaces
            ln2 = ln.replace("\t", "    ")

            indent = len(ln2) - len(ln2.lstrip(" "))
            stripped = ln2.strip()

            out.append(UIToken(indent, ln2, stripped, i))

        self.lines = out

    # ---------------------------------------------------------
    # Block parsing helpers
    # ---------------------------------------------------------

    def cur(self):
        if self.idx >= len(self.lines):
            return None
        return self.lines[self.idx]

    def peek(self):
        c = self.cur()
        return c.stripped if c else ""

    def advance(self):
        self.idx += 1

    def _syntax(self, msg, token):
        return SyntaxError(f"[UI Syntax Error @ line {token.line_no}] {msg}: '{token.stripped}'")

    # ---------------------------------------------------------
    # Parse ui root
    # ---------------------------------------------------------

    def parse_ui_block(self):
        token = self.cur()
        m = re.match(r"ui\s+([A-Za-z0-9_]+):?", token.stripped)
        if not m:
            raise self._syntax("Invalid ui declaration", token)

        name = m.group(1)
        base_indent = token.indent
        self.advance()

        children = self.parse_children(base_indent)
        return UIRoot(name, children, token.line_no)

    # ---------------------------------------------------------
    # Parse children under a parent indent
    # ---------------------------------------------------------

    def parse_children(self, parent_indent):
        result = []
        while self.idx < len(self.lines):
            token = self.cur()
            if not token.stripped:
                self.advance()
                continue

            if token.indent <= parent_indent:
                break

            node = self.parse_any_element(parent_indent)
            if node:
                result.append(node)

        return result

    # ---------------------------------------------------------
    # Determine element type
    # ---------------------------------------------------------

    def parse_any_element(self, parent_indent):
        token = self.cur()
        stripped = token.stripped

        # for-block
        if stripped.startswith("for "):
            return self.parse_for(parent_indent)

        # event-block
        if stripped.startswith("on_"):
            return self.parse_event(parent_indent)

        # anim-block
        if stripped.startswith("anim "):
            return self.parse_anim(parent_indent)

        # basic element or layout
        return self.parse_element(parent_indent)

    # ---------------------------------------------------------
    # for-block
    # ---------------------------------------------------------

    def parse_for(self, parent_indent):
        token = self.cur()
        m = re.match(r"for\s+([A-Za-z_][A-Za-z0-9_]*)\s+in\s+(.+):", token.stripped)
        if not m:
            raise self._syntax("Invalid for syntax", token)

        var_name = m.group(1)
        iterable_expr = self.expr.parse(m.group(2))
        base_indent = token.indent
        self.advance()

        children = self.parse_children(base_indent)

        # expect end
        if self.peek() != "end":
            raise self._syntax("Expected 'end' to close for", self.cur())
        self.advance()

        return UIFOR(var_name, iterable_expr, children, token.line_no)

    # ---------------------------------------------------------
    # event-block
    # ---------------------------------------------------------

    def parse_event(self, parent_indent):
        token = self.cur()
        m = re.match(r"(on_[a-zA-Z_]+)\s+(.*)", token.stripped)
        if not m:
            raise self._syntax("Invalid event syntax", token)

        event_type = m.group(1)
        remainder = m.group(2).strip()
        base_indent = token.indent
        self.advance()

        # handler must exist
        handler = None
        if remainder.startswith("handler="):
            handler = remainder[len("handler="):].strip().strip('"')
        else:
            raise self._syntax("Event must include handler=\"name\"", token)

        # events may have sub-blocks (rare), but safe to parse children
        children = self.parse_children(base_indent)

        # expect end
        if self.peek() == "end":
            self.advance()

        return UIEvent(event_type, handler, token.line_no)

    # ---------------------------------------------------------
    # anim-block
    # ---------------------------------------------------------

    def parse_anim(self, parent_indent):
        token = self.cur()
        m = re.match(r"anim\s+([A-Za-z_][A-Za-z0-9_]*)\s*(.*)", token.stripped)
        if not m:
            raise self._syntax("Invalid anim syntax", token)

        anim_type = m.group(1)
        remainder = m.group(2).strip()

        props = self.parse_props(remainder, token)
        base_indent = token.indent
        self.advance()

        children = self.parse_children(base_indent)

        # optional end
        if self.peek() == "end":
            self.advance()

        return UIAnim(anim_type, props, token.line_no)

    # ---------------------------------------------------------
    # basic element: label/button/image/panel/layout...
    # ---------------------------------------------------------

    def parse_element(self, parent_indent):
        token = self.cur()
        stripped = token.stripped

        # element with block
        if stripped.endswith(":"):
            elem_type, remainder = self.split_head(stripped[:-1])
            base_indent = token.indent
            self.advance()

            props = self.parse_props(remainder, token)
            children = self.parse_children(base_indent)

            # expect end
            if self.peek() == "end":
                self.advance()

            return UIElement(elem_type, props, children, token.line_no)

        # single-line element
        elem_type, remainder = self.split_head(stripped)
        props = self.parse_props(remainder, token)
        self.advance()

        return UIElement(elem_type, props, [], token.line_no)

    # ---------------------------------------------------------
    # Utility: split head (elem_type + props)
    # ---------------------------------------------------------

    def split_head(self, text):
        if not text:
            return "", ""
        parts = text.split()
        elem_type = parts[0]
        remainder = text[len(elem_type):].strip()
        return elem_type, remainder

    # ---------------------------------------------------------
    # props: key=value pairs
    # ---------------------------------------------------------

    def parse_props(self, text, token):
        if not text:
            return {}

        parts = self._split_props(text, token)
        props = {}

        for k, v in parts:
            props[k] = self.expr.parse(v)

        return props

    def _split_props(self, text, token):
        parts = []
        current = ""
        quote = None

        def flush():
            nonlocal current
            if current.strip():
                if "=" not in current:
                    raise self._syntax("Expected key=value", token)
                k, v = current.split("=", 1)
                parts.append((k.strip(), v.strip()))
            current = ""

        for ch in text:
            if quote:
                current += ch
                if ch == quote:
                    quote = None
                continue

            if ch in ("'", '"'):
                quote = ch
                current += ch
            elif ch.isspace():
                flush()
            else:
                current += ch

        flush()
        return parts
