import pygame
from neoera.core.resource_manager import RESOURCE_MANAGER


class UIButton:
    def __init__(self, text, x, y, w, h, callback=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

        self.font = RESOURCE_MANAGER.load_font(32)
        self.txt_surf = self.font.render(text, True, (255, 255, 255))
        self.callback = callback

        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()

    def draw(self, screen):
        color = (80, 80, 80) if not self.hover else (140, 140, 140)
        pygame.draw.rect(screen, color, self.rect)

        tx = self.rect.x + (self.rect.width - self.txt_surf.get_width()) // 2
        ty = self.rect.y + (self.rect.height - self.txt_surf.get_height()) // 2
        screen.blit(self.txt_surf, (tx, ty))
