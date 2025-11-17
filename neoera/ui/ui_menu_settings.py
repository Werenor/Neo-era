from neoera.ui.ui_button import UIButton
from neoera.ui.ui_panel import UIPanel


class SettingsMenu:
    RESOLUTIONS = [
        (1280, 720),
        (1600, 900),
        (1920, 1080),
        (2560, 1440),
    ]

    def __init__(self, screen_w, screen_h, ui_manager):
        self.visible = False
        self.ui_manager = ui_manager

        panel_w, panel_h = 600, 500
        panel_x = (screen_w - panel_w) // 2
        panel_y = (screen_h - panel_h) // 2

        self.panel = UIPanel(panel_x, panel_y, panel_w, panel_h)

        y = panel_y + 60
        spacing = 60

        for res in self.RESOLUTIONS:
            label = f"{res[0]} × {res[1]}"
            self.panel.add(
                UIButton(label, panel_x + 50, y, 500, 40,
                         callback=lambda r=res: self.on_resolution(r))
            )
            y += spacing

        self.panel.add(
            UIButton("返回", panel_x + 50, panel_y + 400, 500, 40,
                     callback=self.on_back)
        )

    def on_resolution(self, res):
        self.ui_manager.change_resolution(res)

    def on_back(self):
        self.visible = False
        self.ui_manager.resume_game()

    def handle_event(self, event):
        if self.visible:
            self.panel.handle_event(event)

    def draw(self, screen):
        if self.visible:
            self.panel.draw(screen)
