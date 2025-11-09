# /neoera/parser.py
"""
NSL Parser v3.5 — 行级解析 + 多媒体扩展
支持：
- echo / 隐式文本
- set
- if / else / end
- choice
- bg / bgm / stop_bgm
- show_sprite / hide_sprite
"""

import re

STR_RE = re.compile(r'"([^"]*)"')

def _parse_choice_items(line: str):
    return STR_RE.findall(line)

def _is_blank(s: str) -> bool:
    return len(s.strip()) == 0


class Parser:
    def __init__(self):
        self.ast = []

    def parse(self, script: str):
        # 统一换行符
        lines = script.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        block, _ = self._parse_block(lines, 0)
        self.ast = block
        return self.ast

    # 递归解析代码块
    def _parse_block(self, lines, i):
        out = []
        n = len(lines)
        while i < n:
            raw = lines[i]
            line = raw.strip()
            i += 1

            if _is_blank(line):
                continue
            if line.startswith("#"):  # <-- 新增
                continue
            if line == 'end' or line == 'else':
                return out, i - 1

            # ========== 基础命令 ==========
            if line.startswith('echo '):
                txt = line[5:].strip()
                if len(txt) >= 2 and txt[0] == '"' and txt[-1] == '"':
                    txt = txt[1:-1]
                out.append({"type": "echo", "expression": {"type": "string", "value": txt}})
                continue

            if line.startswith('set '):
                rest = line[4:].strip()
                m = re.match(r'^([A-Za-z_]\w*)\s*=\s*(.+)$', rest)
                if m:
                    name, expr = m.group(1), m.group(2)
                    out.append({"type": "set", "name": name, "expr": expr})
                continue

            if line.startswith('choice'):
                options = _parse_choice_items(line)
                out.append({"type": "choice", "options": options})
                continue

            if line.startswith('if '):
                condition = line[3:].strip()
                then_block, i_then_end = self._parse_block(lines, i)
                i = i_then_end
                tag = lines[i].strip() if i < n else ''
                if tag == 'else':
                    i += 1
                    else_block, i_else_end = self._parse_block(lines, i)
                    i = i_else_end
                    if i < n and lines[i].strip() == 'end':
                        i += 1
                    out.append({"type": "if", "condition": condition, "then": then_block, "else": else_block})
                elif tag == 'end':
                    i += 1
                    out.append({"type": "if", "condition": condition, "then": then_block, "else": []})
                continue

            # ========== 多媒体扩展 ==========
            if line.startswith('bg '):
                path = line.split(' ', 1)[1].strip()
                out.append({"type": "bg", "path": path})
                continue

            if line.startswith('bgm '):
                path = line.split(' ', 1)[1].strip()
                out.append({"type": "bgm", "path": path})
                continue

            if line.startswith('stop_bgm'):
                out.append({"type": "stop_bgm"})
                continue

            if line.startswith('show_sprite'):
                parts = line.split()
                path = parts[1] if len(parts) > 1 else ""
                pos = parts[2] if len(parts) > 2 else "center"
                out.append({"type": "sprite_show", "path": path, "pos": pos})
                continue

            if line.startswith('hide_sprite'):
                parts = line.split()
                path = parts[1] if len(parts) > 1 else ""
                out.append({"type": "sprite_hide", "path": path})
                continue

            # ========== 隐式文本 ==========
            out.append({"type": "text", "text": raw.strip()})

        return out, i
