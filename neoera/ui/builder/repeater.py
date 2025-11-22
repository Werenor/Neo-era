# ui/builder/repeater.py

from neoera.language.ui_ast import UIElement, UIFor


def build_repeater(node: UIFor, builder):
    """
    将 UIFor 转换为多个 UIComponent（模板展开）
    """
    components = []

    # 不评估 expr，在 UIManager.update() 时进行动态再构建
    # 这里仅构建模板副本（浅构建）
    # 后续 UIManager 将处理动态更新

    for child in node.children:
        if isinstance(child, UIElement):
            elem = builder.build_element(child)
            components.append(elem)

        elif isinstance(child, UIFor):
            # nested for
            nested = build_repeater(child, builder)
            components.extend(nested)

    return components
