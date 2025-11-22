# ui/components/base.py

import pygame
from neoera.render.animation.animation_queue import AnimationQueue


class UIComponent:
    """
    UIComponent 基类（所有 UI 元素的基础）
    ----------------------------------------------------
    子类必须：
    - 实现 draw(screen)
    - 实现 measure() 和 layout(x, y)

    属性系统（props）规则：
    - props 中的所有值已经由 UIBuilder 解析为
      literal / ExprNode（绑定） / Python 值

    每个组件有：
    - props
    - children
    - layout_info（供布局引擎计算）
    - animation_queue（动画支持）
    - bindings（表达式绑定）
    """

    def __init__(self, props=None):
        self.props = props or {}
        self.children = []

        # LayoutEngine 会使用这些字段
        self.x = 0
        self.y = 0
        self.width = None
        self.height = None

        self.layout_info = {}    # 给布局计算使用（尺寸、spacing 等）

        # 动画队列
        self.animations = AnimationQueue()

        # 表达式绑定：
        # prop_name → ExprNode
        self.bindings = {}

        # 是否可见
        self.visible = True

    # ----------------------------------------------------
    # 生命周期
    # ----------------------------------------------------
    def update(self, dt, ctx):
        """
        dt: delta time
        ctx: runtime context（变量访问）
        """
        # 更新动画
        self.animations.update(dt)

        # 更新绑定属性
        self.update_bindings(ctx)

        # 更新子节点
        for child in self.children:
            child.update(dt, ctx)

    def draw(self, screen):
        """由子类实现"""
        pass

    def handle_event(self, event):
        """事件向下传递"""
        for child in self.children:
            child.handle_event(event)

    # ----------------------------------------------------
    # layout 系统
    # ----------------------------------------------------
    def measure(self, max_width, max_height):
        """
        布局前测量组件大小。
        子类可重写。
        """
        return (self.width or 0), (self.height or 0)

    def layout(self, x, y):
        """
        布局系统调用：为组件设置最终位置
        """
        self.x = x
        self.y = y

    # ----------------------------------------------------
    # 绑定更新（ExprNode → 值）
    # ----------------------------------------------------
    def update_bindings(self, ctx):
        for k, expr in self.bindings.items():
            try:
                val = expr.eval(ctx)
                self.props[k] = val
            except Exception:
                pass  # 可增加调试输出

    # ----------------------------------------------------
    # 动画 API
    # ----------------------------------------------------
    def add_animation(self, animation, parallel=False):
        self.animations.push(animation, parallel=parallel)
