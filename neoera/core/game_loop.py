import pygame
from neoera.core.config import CONFIG


class GameLoop:
    """
    Neo-era v2.0 GameLoop
    负责：
    - 事件处理
    - 更新 Renderer（动画 / UI）
    - 推进 Executor（脚本逻辑）
    - 绘制渲染结果 + UI
    """

    def __init__(self, screen, renderer, executor, ui_manager):
        self.running = True
        self.screen = screen
        self.renderer = renderer
        self.executor = executor
        self.ui_manager = ui_manager

        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            dt = self.clock.tick(CONFIG.FPS) / 1000.0

            # --- 1. Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # 给 UI → Renderer → Executor 的事件链
                self.ui_manager.handle_event(event)
                self.renderer.handle_event(event)
                self.executor.handle_event(event)

            # --- 2. Renderer Update (动画/淡入淡出等) ---
            self.renderer.update(dt)

            # --- 3. Executor Tick（脚本推进） ---
            self.executor.tick(dt)

            # --- 4. Draw (渲染所有元素 + UI 覆盖) ---
            self.renderer.render(self.screen)
            self.ui_manager.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
