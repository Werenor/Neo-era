class UIBaseNode:
    def __init__(self, line_no):
        self.line_no = line_no


class UIRoot(UIBaseNode):
    """
    ui screen root node
    """
    def __init__(self, name, children, line_no):
        super().__init__(line_no)
        self.name = name
        self.children = children or []


class UIElement(UIBaseNode):
    """
    Basic UI element node (label, button, image, bar, panel, layouts...)
    """
    def __init__(self, elem_type, props, children, line_no):
        super().__init__(line_no)
        self.elem_type = elem_type
        self.props = props or {}          # 强制 dict
        self.children = children or []    # 强制 list


class UIFOR(UIBaseNode):
    """
    for u in list:
        ...
    end
    """
    def __init__(self, var_name, iterable_expr, children, line_no):
        super().__init__(line_no)
        self.var_name = var_name
        self.iterable_expr = iterable_expr
        self.children = children or []


class UIEvent(UIBaseNode):
    """
    on_click handler="xxx"
    on_hover ...
    """
    def __init__(self, event_type, handler_name, line_no):
        super().__init__(line_no)
        self.event_type = event_type
        self.handler_name = handler_name


class UIAnim(UIBaseNode):
    """
    anim fade_in duration=1
    anim move_to x=100 y=200 duration=0.4
    """
    def __init__(self, anim_type, props, line_no):
        super().__init__(line_no)
        self.anim_type = anim_type
        self.props = props or {}
