# main.py — Neo-era v0.4.1 corrected main loop

import pygame
import sys
import os

# Neo-era imports
from neoera.language.parser import Parser
from neoera.language.ui_parser import UIParser
from neoera.runtime.executor import Executor
from neoera.runtime.context import RuntimeContext

from neoera.render.renderer import Renderer
from neoera.ui.builder.builder import UIBuilder
from neoera.ui.manager.ui_manager import UIManager

from neoera.language.interpreter import Interpreter
from neoera.core.config import CONFIG


def load_script(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_all_ui_screens():

    """
    自动加载 ui_screens/ 下的所有 .ui 文件
    并返回 {screen_name: UIRoot}
    """
    ui_screens = {}
    for filename in os.listdir("ui_screens"):
        if filename.endswith(".ui"):
            text = load_script(f"ui_screens/{filename}")
            parser = UIParser(text)
            ui_screens.update(parser.parse())
    return ui_screens

def main():
    pygame.init()
    pygame.display.set_caption("Neo-era Engine v2.5")
    screen = pygame.display.set_mode((CONFIG.WIDTH, CONFIG.HEIGHT))
    clock = pygame.time.Clock()

    # -------------------------
    # 1. Load NSL
    # -------------------------
    nsl_text = load_script("game_scripts/main.nsl")
    parser = Parser()
    script_ast = parser.parse(nsl_text)

    # -------------------------
    # 2. Load UI
    # -------------------------
    ui_screens = load_all_ui_screens()

    # -------------------------
    # 3. Context + UI
    # -------------------------
    ctx = RuntimeContext()

    ui_builder = UIBuilder(ctx)
    ui_manager = UIManager(ui_screens, ui_builder, ctx)

    # -------------------------
    # 4. Renderer
    # -------------------------
    renderer = Renderer(screen)

    # -------------------------
    # 5. Interpreter + Executor
    # -------------------------
    interpreter = Interpreter(script_ast, ctx, renderer)
    executor = Executor(interpreter, renderer)

    # -------------------------
    # 6. Build pipeline
    # -------------------------
    renderer.build_pipeline(ui_manager,executor,clock)

    # -------------------------
    # 7. Main Loop
    # -------------------------
    running = True
    while running:
        dt = clock.tick(CONFIG.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            renderer.handle_event(event)
            ui_manager.handle_event(event)
            # executor.handle_event(event)  # ← 删除！

        executor.tick(dt)
        renderer.update(dt)
        renderer.render(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
