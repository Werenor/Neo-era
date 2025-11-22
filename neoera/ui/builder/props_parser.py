# ui/builder/props_parser.py



def apply_props(component, props):
    """
    将 props 应用到 component
    含字面量值以外的动态表达式将在 binding pass 中处理
    """
    for key, val in props.items():
        # 动态绑定：ExprNode 留给 binding 处理
        # 如果是表达式绑定节点（AST dict），不在 props pass 处理
        if isinstance(val, dict) and "type" in val:
            continue
        component.props[key] = val

    # 通用属性注入
    if "x" in component.props:
        component.x = component.props["x"]
    if "y" in component.props:
        component.y = component.props["y"]
