import pygame
from neoera.ui.ui_button import UIButton
from neoera.ui.ui_panel import UIPanel


class MainMenu:
    def __init__(self, screen_w, screen_h, ui_manager):
        self.visible = True
        self.ui_manager = ui_manager

        panel_w, panel_h = 400, 400
        panel_x = (screen_w - panel_w) // 2
        panel_y = (screen_h - panel_h) // 2

        self.panel = UIPanel(panel_x, panel_y, panel_w, panel_h)

        btn_y = panel_y + 60
        spacing = 70

        self.panel.add(UIButton("开始游戏", panel_x + 50, btn_y, 300, 50,
                                callback=self.on_start))
        self.panel.add(UIButton("读取存档", panel_x + 50, btn_y + spacing, 300, 50,
                                callback=self.on_load))
        self.panel.add(UIButton("设置", panel_x + 50, btn_y + spacing * 2, 300, 50,
                                callback=self.on_settings))
        self.panel.add(UIButton("退出游戏", panel_x + 50, btn_y + spacing * 3, 300, 50,
                                callback=self.on_exit))

    def on_start(self):
        self.visible = False
        self.ui_manager.request_start_game()

    def on_load(self):
        pass  # TODO: save system

    def on_settings(self):
        self.ui_manager.show_settings()

    def on_exit(self):
        pygame.quit()
        exit()

    def handle_event(self, event):
        if not self.visible:
            return
        self.panel.handle_event(event)

    def draw(self, screen):
        if not self.visible:
            return
        self.panel.draw(screen)
