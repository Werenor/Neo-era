# /neoera/parser.py

import re

class Parser:
    def __init__(self):
        self.tokens = []
        self.ast = []

    def tokenize(self, script):
        """ 将脚本分解成词法单元（tokens） """
        token_specification = [
            ('NUMBER', r'\d+'),            # 整数
            ('ASSIGN', r'='),              # 赋值符号
            ('ID', r'[A-Za-z_][A-Za-z_0-9]*'),  # 标识符（变量名）
            ('KEYWORD', r'if|else|for|while|func|call|return|echo'),  # 关键字
            ('LPAREN', r'\('),             # 左括号
            ('RPAREN', r'\)'),             # 右括号
            ('LBRACE', r'\{'),             # 左大括号
            ('RBRACE', r'\}'),             # 右大括号
            ('EQUAL', r'=='),              # 等于
            ('PLUS', r'\+'),               # 加法
            ('MINUS', r'-'),               # 减法
            ('TIMES', r'\*'),              # 乘法
            ('DIVIDE', r'/'),              # 除法
            ('STRING', r'"[^"]*"'),        # 字符串
            ('SKIP', r'[ \t]+'),           # 跳过空格和制表符
            ('NEWLINE', r'\n'),            # 换行符
            ('MISMATCH', r'.'),            # 错误匹配
        ]

        regex_parts = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
        regex = re.compile(regex_parts)

        for mo in regex.finditer(script):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP':
                continue
            if kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected')
            self.tokens.append((kind, value))

    def parse(self, script):
        """ 解析脚本并生成 AST """
        self.tokenize(script)
        self.ast = self.parse_statements()

    def parse_statements(self):
        """ 解析一系列语句 """
        statements = []
        while self.tokens:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def parse_statement(self):
        """ 解析一个语句 """
        if self.tokens[0][0] == 'KEYWORD':
            keyword = self.tokens.pop(0)[1]
            if keyword == 'echo':
                return self.parse_echo()
            elif keyword == 'if':
                return self.parse_if()
            elif keyword == 'for':
                return self.parse_for()
            elif keyword == 'while':  # 新增：while 循环
                return self.parse_while()
            elif keyword == 'func':  # 新增：函数定义
                return self.parse_func()
            elif keyword == 'return':  # 新增：return 语句
                return self.parse_return()
            # 可以扩展更多命令
        return None

    def parse_echo(self):
        """ 解析 echo 命令 """
        self.tokens.pop(0)  # 去掉 'echo'
        expression = self.parse_expression()
        return {'type': 'echo', 'expression': expression}

    def parse_expression(self):
        """ 解析表达式（简单的 ID 或数字） """
        token_type, token_value = self.tokens.pop(0)
        if token_type == 'ID':
            return {'type': 'variable', 'name': token_value}
        elif token_type == 'NUMBER':
            return {'type': 'number', 'value': int(token_value)}
        elif token_type == 'STRING':
            return {'type': 'string', 'value': token_value[1:-1]}  # 去掉引号
        return None

    def parse_if(self):
        """ 解析 if 语句 """
        self.tokens.pop(0)  # 去掉 'if'
        condition = self.parse_expression()
        statements = self.parse_statements()
        return {'type': 'if', 'condition': condition, 'statements': statements}

    def parse_for(self):
        """ 解析 for 循环 """
        self.tokens.pop(0)  # 去掉 'for'
        var_name = self.tokens.pop(0)[1]  # 获取变量名
        self.tokens.pop(0)  # 去掉 '='
        start = self.parse_expression()
        self.tokens.pop(0)  # 去掉 'to'
        end = self.parse_expression()
        statements = self.parse_statements()
        return {'type': 'for', 'var': var_name, 'start': start, 'end': end, 'statements': statements}

    def parse_while(self):
        """ 解析 while 循环 """
        self.tokens.pop(0)  # 去掉 'while'
        condition = self.parse_expression()
        statements = self.parse_statements()
        return {'type': 'while', 'condition': condition, 'statements': statements}

    def parse_func(self):
        """ 解析 func 语句 """
        self.tokens.pop(0)  # 去掉 'func'
        func_name = self.tokens.pop(0)[1]
        self.tokens.pop(0)  # 去掉 '('
        params = self.parse_params()
        self.tokens.pop(0)  # 去掉 ')'
        statements = self.parse_statements()
        return {'type': 'func', 'name': func_name, 'params': params, 'statements': statements}

    def parse_return(self):
        """ 解析 return 语句 """
        self.tokens.pop(0)  # 去掉 'return'
        expression = self.parse_expression()
        return {'type': 'return', 'expression': expression}

    def parse_params(self):
        """ 解析函数参数 """
        params = []
        while self.tokens[0][0] != 'RPAREN':
            param = self.tokens.pop(0)[1]
            params.append(param)
            if self.tokens[0][0] == 'COMMA':
                self.tokens.pop(0)  # 去掉逗号
        return params
