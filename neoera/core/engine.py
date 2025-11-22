import pygame
from neoera.core.game_loop import GameLoop
from neoera.core.resource_manager import RESOURCE_MANAGER
from neoera.core.config import CONFIG

from neoera.runtime.context import Context
from neoera.runtime.executor import Executor
from neoera.language.parser import Parser
from neoera.language.interpreter import Interpreter
from neoera.render.renderer import Renderer
from neoera.ui.manager.ui_manager import UIManager


class Engine:
    """
    Neo-era v2.0 Engine
    负责：
    - 初始化所有系统
    - 加载脚本
    - 创建 Renderer / Interpreter / Executor
    - 启动 GameLoop（主循环）
    """

    def __init__(self, script_path):
        pygame.init()

        self.script_path = script_path
        self.screen = pygame.display.set_mode(CONFIG.RESOLUTION)
        pygame.display.set_caption("Neo-era Engine v2.0")

        # ---- Context ----
        self.context = Context()

        # ---- Renderer ----
        self.renderer = Renderer(self.screen)

        # ---- UI Manager ----
        self.ui_manager = UIManager(self.renderer)

        # ---- Parser + AST ----
        parser = Parser()
        try:
            self.ast = parser.parse_file(script_path)
        except Exception as e:
            print("[Engine] Script parsing failed:", e)
            raise

        # ---- Interpreter ----
        self.interpreter = Interpreter(self.context, self.renderer)

        # ---- Executor ----
        self.executor = Executor(self.interpreter, self.renderer, self.ast)

        # ---- Game Loop ----
        self.loop = GameLoop(
            screen=self.screen,
            renderer=self.renderer,
            executor=self.executor,
            ui_manager=self.ui_manager
        )

    def start(self):
        print("[Engine] Starting game…")
        self.loop.run()
