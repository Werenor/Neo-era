import pygame
from neoera.ui.ui_menu_main import MainMenu
from neoera.ui.ui_menu_pause import PauseMenu
from neoera.ui.ui_menu_settings import SettingsMenu
from neoera.core.config import CONFIG


class UIManager:
    def __init__(self, renderer):
        self.renderer = renderer

        w, h = CONFIG.RESOLUTION
        self.main_menu = MainMenu(w, h, self)
        self.pause_menu = PauseMenu(w, h, self)
        self.settings_menu = SettingsMenu(w, h, self)

        self.in_game = False

    def request_start_game(self):
        self.in_game = True

    def goto_title(self):
        self.in_game = False
        self.main_menu.visible = True

    def resume_game(self):
        self.pause_menu.visible = False

    def show_settings(self):
        self.settings_menu.visible = True

    def change_resolution(self, res):
        print(f"[UI] Change resolution to {res}")
        CONFIG.set_resolution(*res)
        pygame.display.set_mode(res)

    # external hooks
    def handle_event(self, event):
        if not self.in_game:
            # 主菜单状态
            self.main_menu.handle_event(event)
        else:
            # 游戏内状态
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.pause_menu.visible = not self.pause_menu.visible

            self.pause_menu.handle_event(event)
            self.settings_menu.handle_event(event)

    def draw(self, screen):
        if not self.in_game:
            self.main_menu.draw(screen)
        else:
            self.pause_menu.draw(screen)
            self.settings_menu.draw(screen)
