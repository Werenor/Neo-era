# ui/layouts/base.py

class LayoutBase:
    """
    所有布局类的基础接口
    ----------------------------------
    layout(container):
        执行布局，对 container.children 计算位置

    container:
        UIComponent（必须有 children）
    """

    def layout(self, container):
        """子类必须实现"""
        raise NotImplementedError
