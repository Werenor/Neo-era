# ui/builder/binding.py


def apply_bindings(component, props):
    """
    识别 props 中的 ExprNode，挂到 component.bindings 中
    update() 时自动评估
    """
    for key, val in props.items():
        if isinstance(val, dict) and "type" in val:
            component.bindings[key] = val
