# neoera/runtime/executor.py

import pygame
from neoera.core.event_bus import EVENT_BUS


class Executor:
    def __init__(self, interpreter, renderer, ast):
        self.interpreter = interpreter
        self.renderer = renderer
        self.ast = ast
        self.index = 0

    def start(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                EVENT_BUS.emit(event)

            # 帧更新
            self.renderer.update(dt)
            self.renderer.render()

            # 推进脚本
            if self.renderer.wait_click:
                # echo 或 choice 阻塞中
                continue

            if self.index < len(self.ast):
                stmt = self.ast[self.index]
                self.interpreter.execute_statement(stmt)
                self.index += 1
