import pygame
from neoera.runtime.executor import Executor
from neoera.language.interpreter import Interpreter
from neoera.core.config import CONFIG
from neoera.render import renderer_gui


class Engine:
    def __init__(self, script_path):
        self.script_path = script_path

        # 初始化 Interpreter（解释 AST）
        self.interpreter = Interpreter()

        # 初始化 Executor（运行时推进剧情）
        self.executor = Executor(self.interpreter, script_path)

        # Renderer
        self.renderer = renderer_gui

        self.ui_manager = None
        self.in_game = False

    def bind_ui(self, ui_manager):
        self.ui_manager = ui_manager

    def start_gameplay(self):
        print("[Engine] 开始游戏……")
        self.in_game = True
        self.executor.prepare()

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 左键点击推进剧情
            self.executor.on_click()

    def update(self, dt):
        if self.in_game and not self.ui_manager.pause_menu.visible:
            self.executor.update(dt)
