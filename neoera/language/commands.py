from neoera.language.ast import ASTNode


# ============================================================
# 基础语句节点
# ============================================================

class EchoNode(ASTNode):
    def __init__(self, text):
        self.text = text


class AssignmentNode(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class IfNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block


class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ChoiceNode(ASTNode):
    def __init__(self, items):
        self.items = items


class ChoiceItemNode(ASTNode):
    def __init__(self, text, target_idx):
        self.text = text
        self.target_idx = target_idx


class InputNode(ASTNode):
    def __init__(self, var_name, prompt):
        self.var_name = var_name
        self.prompt = prompt


class DelayNode(ASTNode):
    def __init__(self, seconds):
        self.seconds = seconds


class EndNode(ASTNode):
    pass


# ============================================================
# 背景、立绘
# ============================================================

class BackgroundNode(ASTNode):
    def __init__(self, name):
        self.name = name


class SpriteShowNode(ASTNode):
    def __init__(self, name, x=None, y=None):
        self.name = name
        self.x = x
        self.y = y


class SpriteHideNode(ASTNode):
    def __init__(self, name):
        self.name = name


# ============================================================
# BGM
# ============================================================

class BGMPlayNode(ASTNode):
    def __init__(self, name):
        self.name = name


class BGMStopNode(ASTNode):
    pass


# ============================================================
# UI
# ============================================================

class UIScreenShowNode(ASTNode):
    def __init__(self, screen_name):
        self.screen_name = screen_name


class UIScreenHideNode(ASTNode):
    pass


# ============================================================
# 动画指令（v0.4.2，全新风格）
# ============================================================

class SpriteMoveNode(ASTNode):
    def __init__(self, name, x, y, duration=1.0):
        self.name = name
        self.x = x
        self.y = y
        self.duration = duration


class SpriteFadeInNode(ASTNode):
    def __init__(self, name, duration=0.6):
        self.name = name
        self.duration = duration


class SpriteFadeOutNode(ASTNode):
    def __init__(self, name, duration=0.6):
        self.name = name
        self.duration = duration


class SpriteScaleNode(ASTNode):
    def __init__(self, name, scale, duration=0.4):
        self.name = name
        self.scale = scale
        self.duration = duration
