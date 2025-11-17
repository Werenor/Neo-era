import pygame


class UIPanel:
    def __init__(self, x, y, w, h, children=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.children = children or []

    def add(self, widget):
        self.children.append(widget)

    def handle_event(self, event):
        for w in self.children:
            w.handle_event(event)

    def draw(self, screen):
        # 半透明背景
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        screen.blit(s, (self.rect.x, self.rect.y))

        for w in self.children:
            w.draw(screen)
