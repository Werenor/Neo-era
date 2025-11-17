import pygame
from neoera.core.engine import Engine
from neoera.render.renderer_gui import init_display, render_frame
from neoera.core.config import CONFIG
from neoera.ui.ui_manager import UIManager


def main():
    pygame.init()

    # 1. 初始化显示与 renderer
    screen = init_display(*CONFIG.RESOLUTION)

    print("[Neo-era] 初始化中……")

    # 2. 初始化 Engine（加载脚本）
    engine = Engine("test.neo")

    # 3. 初始化 UI 管理器
    ui_manager = UIManager(engine.renderer)
    engine.bind_ui(ui_manager)

    engine.start_gameplay()

    clock = pygame.time.Clock()

    # 4. 主循环
    running = True
    while running:
        dt = clock.tick(CONFIG.FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 交给 UI
            ui_manager.handle_event(event)

            # 游戏内点击推进
            if ui_manager.in_game and not ui_manager.pause_menu.visible:
                engine.handle_input(event)

        # 执行一帧
        engine.update(dt)

        # 渲染：UI + Renderer
        render_frame(screen, ui_manager)

    pygame.quit()


if __name__ == "__main__":
    main()
