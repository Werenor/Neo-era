import pygame
from neoera.render.renderer_core import RenderLayer
from neoera.ui.manager.ui_overlay_layer import UIOverlayLayer


class BackgroundLayer(RenderLayer):
    """
    背景层：管理 Background 对象
    """
    def __init__(self, background_obj):
        self.bg = background_obj

    def update(self, dt):
        self.bg.update(dt)

    def draw(self, screen):
        self.bg.draw(screen)


class SpriteLayer(RenderLayer):
    """
    Sprite 层：管理所有立绘 / 角色 / 动态对象
    """
    def __init__(self, sprite_manager):
        self.sprites = sprite_manager

    def update(self, dt):
        self.sprites.update(dt)

    def draw(self, screen):
        self.sprites.draw(screen)


class DialogueLayer(RenderLayer):
    """
    对话框层（对话框、名字框、文本均由 DialogueBox 控制）
    """
    def __init__(self, dialogue_box):
        self.dialogue_box = dialogue_box

    def update(self, dt):
        self.dialogue_box.update(dt)

    def draw(self, screen):
        self.dialogue_box.draw(screen)

    def handle_event(self, event):
        # 对话框一般不吞事件，文本推进由 Executor/RendererCore 捕捉点击
        pass


class ChoiceLayer(RenderLayer):
    """
    选项 UI 层
    """
    def __init__(self, choice_ui, renderer_core):
        self.choice_ui = choice_ui
        self.core = renderer_core

    def update(self, dt):
        self.choice_ui.update(dt)

    def draw(self, screen):
        self.choice_ui.draw(screen)

    def handle_event(self, event):
        if not self.choice_ui.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            idx = self.choice_ui.handle_click(event.pos)
            if idx is not None:
                self.core.choice_result = idx


class InputLayer(RenderLayer):
    """
    输入框层
    """
    def __init__(self, input_box, renderer_core):
        self.input_box = input_box
        self.core = renderer_core

    def update(self, dt):
        self.input_box.update(dt)

    def draw(self, screen):
        self.input_box.draw(screen)

    def handle_event(self, event):
        if not self.input_box.visible:
            return

        if event.type == pygame.KEYDOWN:
            self.input_box.handle_key(event)
            if self.input_box.has_result():
                self.core.input_result = self.input_box.get_result()



class DebugLayer(RenderLayer):
    """
    Debug 层：显示 FPS、状态机状态、进入/退出日志等
    """
    def __init__(self, renderer_core, executor, clock):
        self.core = renderer_core
        self.executor = executor
        self.clock = clock
        pygame.font.init()
        self.font = pygame.font.SysFont("Consolas", 18)

    def update(self, dt):
        pass

    def draw(self, screen):
        txt = [
            f"FPS: {int(self.clock.get_fps())}",
            f"State: {self.executor.state.name}",
            f"Animating: {self.core.is_animating}",
        ]
        y = 10
        for line in txt:
            surf = self.font.render(line, True, (255,255,0))
            screen.blit(surf, (10, y))
            y += 20


# ============================================================
# 工厂函数：初始化 Pipeline 所需的所有层
# ============================================================

def create_render_pipeline(renderer_core, renderer_components, ui_manager, executor, clock):
    """
    renderer_components = {
        "background": Background,
        "sprites": SpriteManager,
        "dialogue": DialogueBox,
        "choice_ui": ChoiceUI,
        "input_box": InputBox
    }
    """

    pipeline = [
        BackgroundLayer(renderer_components["background"]),
        SpriteLayer(renderer_components["sprites"]),
        DialogueLayer(renderer_components["dialogue"]),
        ChoiceLayer(renderer_components["choice_ui"], renderer_core),
        InputLayer(renderer_components["input_box"], renderer_core),
        UIOverlayLayer(ui_manager),
        DebugLayer(renderer_core, executor, clock),
    ]

    # 注册进 RendererCore
    for layer in pipeline:
        renderer_core.add_layer(layer)

    return pipeline
