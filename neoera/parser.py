# /neoera/parser.py
"""
NSL Parser v3 — 行级解析
支持：隐式echo、echo、set、choice、if/else/end（可嵌套）
跨平台换行：CRLF / LF / CR 全兼容
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
        # 统一换行，逐行解析
        lines = script.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        block, _ = self._parse_block(lines, 0)
        self.ast = block
        return self.ast

    # 解析一个代码块，直到 EOF 或遇到 end / else（由 caller 处理）
    def _parse_block(self, lines, i):
        out = []
        n = len(lines)
        while i < n:
            raw = lines[i]
            line = raw.strip()
            i += 1

            if _is_blank(line):
                continue

            # 结束或转到上层处理
            if line == 'end' or line == 'else':
                return out, i - 1  # 回到这一行，让上层决定如何消费

            # echo
            if line.startswith('echo '):
                txt = line[5:].strip()
                if len(txt) >= 2 and txt[0] == '"' and txt[-1] == '"':
                    txt = txt[1:-1]
                out.append({"type": "echo", "expression": {"type": "string", "value": txt}})
                continue

            # set  例：set mood = "good"
            if line.startswith('set '):
                rest = line[4:].strip()
                m = re.match(r'^([A-Za-z_]\w*)\s*=\s*(.+)$', rest)
                if m:
                    name, expr = m.group(1), m.group(2)
                    out.append({"type": "set", "name": name, "expr": expr})
                else:
                    # 语法容错：整行当文本
                    out.append({"type": "text", "text": raw.strip()})
                continue

            # choice  例：choice "A" "B" "C"
            if line.startswith('choice'):
                options = _parse_choice_items(line)
                out.append({"type": "choice", "options": options})
                continue

            # if / else / end
            if line.startswith('if '):
                condition = line[3:].strip()

                # 解析 then 块
                then_block, i_then_end = self._parse_block(lines, i)
                i = i_then_end

                # 看看 end/else 是谁
                tag = lines[i].strip() if i < n else ''
                if tag == 'else':
                    i += 1  # 吃掉 else
                    else_block, i_else_end = self._parse_block(lines, i)
                    i = i_else_end
                    # 现在必须是 end
                    if i < n and lines[i].strip() == 'end':
                        i += 1  # 吃掉 end
                    out.append({
                        "type": "if",
                        "condition": condition,
                        "then": then_block,
                        "else": else_block
                    })
                elif tag == 'end':
                    i += 1  # 吃掉 end
                    out.append({
                        "type": "if",
                        "condition": condition,
                        "then": then_block,
                        "else": []
                    })
                else:
                    # 结构不完整，容错：把 if/then 当普通文本回退
                    out.append({"type": "text", "text": f"if {condition}"})
                    out.extend(then_block)
                continue

            # 其它：隐式 echo
            out.append({"type": "text", "text": raw.strip()})

        return out, i
