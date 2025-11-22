import pygame
from neoera.core.config import CONFIG
from neoera.render.renderer_core import RendererCore
from neoera.render.render_pipeline import create_render_pipeline

# 正确的 background 类名是 Background（不是 BackgroundLayer）
from neoera.render.background import Background

# sprite_manager 正确
from neoera.render.sprite_manager import SpriteManager

from neoera.render.dialogue_box import DialogueBox
from neoera.render.choice_ui import ChoiceUI

# InputUI 不存在，正确的类名为 InputBox
from neoera.render.input_box import InputBox

# UIOverlayLayer 在 ui/manager 下
from neoera.ui.manager.ui_overlay_layer import UIOverlayLayer


class Renderer:
    """
    Neo-era v0.4.2 CLEAN Renderer
    - 不再包含旧动画系统（RenderBlock）
    - 动画全部交给 SpriteManager (move/fade/scale)
    """

    def __init__(self, screen):
        self.screen = screen

        # 核心渲染层
        self.core = RendererCore()

        # 资源层
        self.background = Background()
        self.sprites = SpriteManager()

        # 事件交互层
        self.dialogue = DialogueBox()
        self.choice_ui = ChoiceUI()
        self.input_box = InputBox()

        # UI 管理器将稍后通过 build_pipeline 注入
        self.ui_manager = None
        self.ui_layer = None

        # 渲染管线
        self.pipeline = None

    # ----------------------------------------------------------
    # 构建渲染管线（由 main.py 注入 ui_manager/executor/clock）
    # ----------------------------------------------------------
    def build_pipeline(self, ui_manager, executor, clock):
        self.executor = executor
        self.ui_manager = ui_manager
        self.ui_layer = UIOverlayLayer(self.ui_manager)

        renderer_components = {
            "background": self.background,
            "sprites": self.sprites,
            "dialogue": self.dialogue,
            "choice_ui": self.choice_ui,
            "input_box": self.input_box,
            "ui_layer": self.ui_layer,
        }

        self.pipeline = create_render_pipeline(
            self.core,
            renderer_components,
            self.ui_manager,
            executor,
            clock
        )

    # ----------------------------------------------------------
    # Update
    # ----------------------------------------------------------
    def update(self, dt):
        self.core.update(dt)

    # ----------------------------------------------------------
    # Draw
    # ----------------------------------------------------------
    def render(self, screen):
        screen.fill((0, 0, 0))
        self.core.draw(screen)

    # ----------------------------------------------------------
    # Event Dispatch
    # ----------------------------------------------------------
    def handle_event(self, event):
        # 统一事件流：从最上层向下冒泡
        result = self.core.handle_event(event)

        # UI 层的 action → 通知 executor
        if self.ui_manager:
            ui_action = self.ui_manager.consume_action()
            if ui_action is not None:
                self.executor.set_ui_result(ui_action)

        return result

    # ----------------------------------------------------------
    # RENDER 指令入口（来自 Executor）
    # ----------------------------------------------------------
    def apply_instruction(self, payload):
        ptype = payload.get("type")

        # ------------------------------------------------------
        # Background
        # ------------------------------------------------------
        if ptype == "BG":
            name = payload["name"]
            self.background.set(name)
            return

        # ------------------------------------------------------
        # Sprite Show
        # ------------------------------------------------------
        if ptype == "SPRITE_SHOW":
            self.sprites.show(
                payload["name"],
                payload.get("x", 0),
                payload.get("y", 0)
            )
            return

        # ------------------------------------------------------
        # Sprite Hide
        # ------------------------------------------------------
        if ptype == "SPRITE_HIDE":
            self.sprites.hide(payload["name"])
            return

        # ------------------------------------------------------
        # BGM
        # ------------------------------------------------------
        if ptype == "BGM_PLAY":
            import pygame
            name = payload["name"]
            try:
                pygame.mixer.music.load(name)
                pygame.mixer.music.play(-1)
            except:
                print(f"[BGM] Failed to load {name}")
            return

        if ptype == "BGM_STOP":
            import pygame
            pygame.mixer.music.stop()
            return

        # ------------------------------------------------------
        # NEW ANIMATION COMMANDS (SpriteManager v2.5)
        # ------------------------------------------------------

        # sprite_move
        if ptype == "SPRITE_MOVE":
            self.sprites.move(
                payload["name"],
                payload["x"],
                payload["y"],
                payload.get("duration", 1.0)
            )
            return

        # sprite_fadein
        if ptype == "SPRITE_FADE_IN":
            self.sprites.fade_in(
                payload["name"],
                payload.get("duration", 0.6)
            )
            return

        # sprite_fadeout
        if ptype == "SPRITE_FADE_OUT":
            self.sprites.fade_out(
                payload["name"],
                payload.get("duration", 0.6)
            )
            return

        # sprite_scale
        if ptype == "SPRITE_SCALE":
            self.sprites.scale(
                payload["name"],
                payload["scale"],
                payload.get("duration", 0.4)
            )
            return

        print("[Renderer] Unknown instruction:", payload)
