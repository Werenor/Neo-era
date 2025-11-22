import pygame
from neoera.language.ui_ast import (
    UIRoot, UIElement, UIFOR, UIEvent, UIAnim
)
from neoera.language.expr_eval import ExprEvaluator

# component registry
# 每个组件类需要在这里注册： "label": UILabel, ...
# 在 main.py 或 __init__.py 中，你应该提前把所有 UI 组件注册到此字典
UI_COMPONENTS = {}


class UIBuilder:
    """
    Neo-era v0.4.2 UI Builder
    将 UI AST 构建为实际 UI 组件树
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.eval = ExprEvaluator(ctx)

    # ---------------------------------------------------------
    # 入口：构建整个 UI screen 树
    # ---------------------------------------------------------

    def build(self, root: UIRoot):
        # 根是一个 panel（UIRoot 不直接变成组件）
        from neoera.ui.components.panel import UIPanel
        root_panel = UIPanel({"id": root.name})

        root_panel.children = self.build_children(root.children, root_panel)
        return root_panel

    # ---------------------------------------------------------
    # 多子节点构建
    # ---------------------------------------------------------

    def build_children(self, ast_children, parent_comp):
        result = []

        for node in ast_children:
            comp = self.build_element(node)
            if comp:
                comp.parent = parent_comp
                result.append(comp)

        return result

    # ---------------------------------------------------------
    # 构建单个 UI 元素
    # ---------------------------------------------------------

    def build_element(self, node):
        # for-block
        if isinstance(node, UIFOR):
            return self.build_for(node)

        # event-block: 不单独生成组件，交给 parent 绑定事件
        if isinstance(node, UIEvent):
            return None

        # anim-block: 暂不直接生成 component，由上层处理
        if isinstance(node, UIAnim):
            return None

        # 基础元素
        if isinstance(node, UIElement):
            return self.build_basic_element(node)

        return None

    # ---------------------------------------------------------
    # 基础元素构造（label/button/image/panel/layout）
    # ---------------------------------------------------------

    def build_basic_element(self, node: UIElement):
        elem_type = node.elem_type

        if elem_type not in UI_COMPONENTS:
            raise Exception(f"Unknown UI element '{elem_type}' at line {node.line_no}")

        cls = UI_COMPONENTS[elem_type]

        # 强制 props 为 dict（绝不会为 None）
        props = node.props or {}

        # 绑定表达式：将 {expr} 转换为动态绑定
        bound_props = self.apply_bindings(props)

        # 构建组件
        comp = cls(bound_props)

        # 递归构建子节点
        comp.children = self.build_children(node.children, comp)

        # 绑定事件
        self.attach_events(node, comp)

        return comp

    # ---------------------------------------------------------
    # for-block 展开
    # ---------------------------------------------------------

    def build_for(self, node: UIFOR):
        items = self.eval.eval(node.iterable_expr)
        results = []

        for item in items:
            # 设置循环变量
            self.ctx.set_var(node.var_name, item)

            # 构建子节点
            from neoera.ui.components.panel import UIPanel
            for_root = UIPanel({})  # 临时容器，用于合并 children

            for_root.children = self.build_children(node.children, for_root)

            # 解包 for_root.children
            results.extend(for_root.children)

        return results

    # ---------------------------------------------------------
    # 绑定事件
    # ---------------------------------------------------------

    def attach_events(self, node, comp):
        if not hasattr(node, "children"):
            return

        for child in node.children:
            if isinstance(child, UIEvent):
                event = child.event_type  # e.g. "on_click"
                handler = child.handler_name
                comp.bind_event(event, handler)

    # ---------------------------------------------------------
    # 绑定表达式：把 {hp} 转成函数绑定
    # ---------------------------------------------------------

    def apply_bindings(self, props):
        result = {}
        for key, val in props.items():
            if isinstance(val, str) and "{" in val and "}" in val:
                # 表达式绑定
                expr_text = val.strip()[1:-1]
                expr_ast = self.expr.parse(expr_text)
                result[key] = ("binding", expr_ast)
            else:
                result[key] = val
        return result
