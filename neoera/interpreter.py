# /neoera/interpreter.py

class Interpreter:
    def __init__(self, ctx):
        self.ctx = ctx  # 引擎的上下文（管理变量、标志位等）
        self.functions = {}

    def execute(self, ast):
        """ 执行抽象语法树（AST） """
        for statement in ast:
            self.execute_statement(statement)

    def execute_statement(self, statement):
        """ 执行单个语句 """
        if statement['type'] == 'echo':
            self.execute_echo(statement)
        elif statement['type'] == 'if':
            self.execute_if(statement)
        elif statement['type'] == 'for':
            self.execute_for(statement)
        elif statement['type'] == 'while':
            self.execute_while(statement)
        elif statement['type'] == 'func':
            self.define_func(statement)
        elif statement['type'] == 'return':
            return self.execute_return(statement)

    def execute_echo(self, statement):
        """ 执行 echo 语句 """
        expression = statement['expression']
        if expression['type'] == 'variable':
            print(self.ctx.get(expression['name'], '未知变量'))
        elif expression['type'] == 'number':
            print(expression['value'])
        elif expression['type'] == 'string':
            print(expression['value'])

    def execute_if(self, statement):
        """ 执行 if 语句 """
        condition = statement['condition']
        if self.evaluate_expression(condition):
            self.execute(statement['statements'])

    def execute_for(self, statement):
        """ 执行 for 循环 """
        var_name = statement['var']
        start = self.evaluate_expression(statement['start'])
        end = self.evaluate_expression(statement['end'])
        for i in range(start, end + 1):
            self.ctx.set(var_name, i)
            self.execute(statement['statements'])

    def execute_while(self, statement):
        """ 执行 while 循环 """
        while self.evaluate_expression(statement['condition']):
            self.execute(statement['statements'])

    def define_func(self, statement):
        """ 定义函数 """
        self.functions[statement['name']] = statement

    def execute_return(self, statement):
        """ 执行 return 语句 """
        return self.evaluate_expression(statement['expression'])

    def evaluate_expression(self, expression):
        """ 计算表达式的值 """
        if expression['type'] == 'variable':
            return self.ctx.get(expression['name'])
        elif expression['type'] == 'number':
            return expression['value']
        elif expression['type'] == 'string':
            return expression['value']
