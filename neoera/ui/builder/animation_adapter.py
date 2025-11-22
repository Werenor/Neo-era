# ui/builder/animation_adapter.py

from neoera.render.animation.tween import Tween


def apply_anim(component, anim_node):
    """
    将 UIAnim 转化为 Tween 对象，并加入 animation_queue。
    """
    anim_type = anim_node.anim_type
    props = anim_node.props

    # （可扩展）支持 fade_in / fade_out / move_to / scale_to
    if anim_type == "fade_in":
        duration = props.get("duration", 0.5)
        anim = Tween(component, "alpha", 0, 255, duration)

    elif anim_type == "move_to":
        duration = props.get("duration", 1.0)
        x = props.get("x", component.x)
        y = props.get("y", component.y)
        anim = Tween(component, ("x", "y"), (component.x, component.y), (x, y), duration)

    else:
        return

    component.add_animation(anim)
