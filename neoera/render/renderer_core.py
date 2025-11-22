# neoera/render/renderer_core.py

class RenderLayer:
    """
    Base class for pipeline layers.
    Each subclass should implement:
        - update(dt)
        - draw(screen)
        - handle_event(event)
    """
    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass


class RendererCore:
    def __init__(self):
        from neoera.render.animation.animation_queue import AnimationQueue
        from neoera.render.animation.animation import Animation
        from neoera.render.animation.tween import Tween

        self.layers = []
        self.click = False
        self.choice_result = None
        self.input_result = None
        self.anim_queue = AnimationQueue()

    def add_animation(self, block_type, item):
        """
        block_type: "sprite", "bg", etc
        item: dict, from RenderBlockNode.items
        Example:
            {"name": "hero", "type": "move", "x": 200, "y": 100, "duration": 1.0}
            {"name": "hero", "type": "fade_in", "duration": 0.6}
        """
        t = item.get("type")

        # -------------------------
        # SPRITE 动画
        # -------------------------
        if block_type == "sprite":
            name = item["name"]
            sprite = self.sprite_manager.get(name)
            if sprite is None:
                print(f"[RendererCore] Sprite not found: {name}")
                return

            duration = item.get("duration", 0.6)

            # 移动
            if t == "move":
                tx = item.get("x", sprite.x)
                ty = item.get("y", sprite.y)

                tw_x = Tween(sprite, "x", sprite.x, tx, duration)
                tw_y = Tween(sprite, "y", sprite.y, ty, duration)
                anim = Animation([tw_x, tw_y])
                self.anim_queue.push(anim)
                return

            # 淡入
            if t == "fade_in":
                sprite.alpha = 0
                tw = Tween(sprite, "alpha", 0, 255, duration)
                anim = Animation([tw])
                self.anim_queue.push(anim)
                return

            # 淡出
            if t == "fade_out":
                tw = Tween(sprite, "alpha", sprite.alpha, 0, duration)
                anim = Animation([tw])
                self.anim_queue.push(anim)
                return

        print("[RendererCore] Unknown animation:", block_type, item)

    def update(self, dt):
        # 驱动动画队列
        if self.anim_queue:
            self.anim_queue.update(dt)

    def is_animating(self):
        return self.anim_queue.active()

    def add_layer(self, layer):
        self.layers.append(layer)

    def update(self, dt):
        for layer in self.layers:
            layer.update(dt)

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)

    def handle_event(self, event):
        result = None
        for layer in reversed(self.layers):
            r = layer.handle_event(event)
            if r is not None:
                result = r

        return result

    def reset_click(self):
        self.click = False
