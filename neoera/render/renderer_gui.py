import pygame
from neoera.core.config import CONFIG
from neoera.render.sprite_manager import SPRITE_MANAGER
from neoera.render.dialogue_box import DIALOGUE_BOX

SCREEN = None


def init_display(w, h):
    global SCREEN
    SCREEN = pygame.display.set_mode((w, h))
    return SCREEN


def render_frame(screen, ui_manager):
    screen.fill((0, 0, 0))

    # 背景 + 立绘
    SPRITE_MANAGER.render_all(screen)

    # 对话框
    if DIALOGUE_BOX.visible:
        DIALOGUE_BOX.draw(screen)

    # 覆盖 UI
    ui_manager.draw(screen)

    pygame.display.flip()
