from neoera.ui.ui_button import UIButton
from neoera.ui.ui_panel import UIPanel


class PauseMenu:
    def __init__(self, screen_w, screen_h, ui_manager):
        self.visible = False
        self.ui_manager = ui_manager

        panel_w, panel_h = 400, 300
        panel_x = (screen_w - panel_w) // 2
        panel_y = (screen_h - panel_h) // 2

        self.panel = UIPanel(panel_x, panel_y, panel_w, panel_h)

        spacing = 70

        self.panel.add(UIButton("继续游戏", panel_x + 50, panel_y + 40, 300, 50,
                                callback=self.on_resume))
        self.panel.add(UIButton("设置", panel_x + 50, panel_y + 40 + spacing, 300, 50,
                                callback=self.on_settings))
        self.panel.add(UIButton("返回主菜单", panel_x + 50, panel_y + 40 + spacing * 2, 300, 50,
                                callback=self.on_back))

    def on_resume(self):
        self.visible = False
        self.ui_manager.resume_game()

    def on_settings(self):
        self.ui_manager.show_settings()

    def on_back(self):
        self.visible = False
        self.ui_manager.goto_title()

    def handle_event(self, event):
        if not self.visible:
            return
        self.panel.handle_event(event)

    def draw(self, screen):
        if self.visible:
            self.panel.draw(screen)
