"""
Neo-era 渲染器：pygame 中文直显版
--------------------------------
绕开 pygame_gui 的字体系统，直接用 pygame.font 渲染中文。
"""

import os
import sys
import pygame
import pygame_gui
from typing import List

pygame.init()
WINDOW_SIZE = (960, 640)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Neo-era")

clock = pygame.time.Clock()
current_bg = None
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- 背景 ---
def load_background(path: str):
    global current_bg
    try:
        if not os.path.isabs(path):
            path = os.path.join(PROJECT_ROOT, path)
        img = pygame.image.load(path).convert()
        current_bg = pygame.transform.scale(img, WINDOW_SIZE)
        print(f"[Neo-era] 加载背景: {path}")
    except Exception as e:
        print(f"[WARN] 无法加载背景 {path}: {e}")
        current_bg = None

def _draw_background():
    if current_bg:
        screen.blit(current_bg, (0, 0))
    else:
        screen.fill((0, 0, 0))

# --- 字体初始化 ---
font_name = pygame.font.match_font("simhei") or pygame.font.match_font("notosanssc") or pygame.font.match_font("microsoftyahei")
if font_name:
    print("[DEBUG] 使用字体:", font_name)
else:
    print("[WARN] 找不到中文字体，使用默认字体。")
font_main = pygame.font.Font(font_name, 24)

# --- 对话框 ---
def echo(text: str):
    """逐行显示中文对白"""
    running = True
    lines = text.split("\n")
    rendered = [font_main.render(line, True, (0, 255, 0)) for line in lines]
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False
        _draw_background()
        y = 440
        for r in rendered:
            screen.blit(r, (50, y))
            y += r.get_height() + 5
        pygame.display.update()

# --- 选项 ---
def print_choice(options: List[str]) -> int:
    """pygame 原生按钮"""
    btn_font = pygame.font.Font(font_name, 22)
    rects = []
    spacing = 20
    btn_w, btn_h = 220, 48
    total_h = len(options) * (btn_h + spacing)
    start_y = (WINDOW_SIZE[1] - total_h) // 2 + 80

    for i, opt in enumerate(options):
        text_surf = btn_font.render(opt, True, (0, 255, 0))
        rect = pygame.Rect(WINDOW_SIZE[0] // 2 - btn_w // 2, start_y + i * (btn_h + spacing), btn_w, btn_h)
        rects.append((rect, text_surf))

    choice = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, (rect, _) in enumerate(rects):
                    if rect.collidepoint(event.pos):
                        choice = i
                        running = False
        _draw_background()
        for rect, surf in rects:
            pygame.draw.rect(screen, (32, 32, 32), rect)
            pygame.draw.rect(screen, (0, 255, 0), rect, 2)
            screen.blit(surf, (rect.x + (rect.width - surf.get_width()) // 2,
                               rect.y + (rect.height - surf.get_height()) // 2))
        pygame.display.update()
        clock.tick(60)
    return choice

# --- 等待 ---
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return
        _draw_background()
        pygame.display.update()
        clock.tick(60)

# --- 测试 ---
if __name__ == "__main__":
    load_background("assets/bg/test_bg.jpg")
    echo("爱宕：早安，指挥官。")
    idx = print_choice(["回应", "装作没听见"])
    echo(f"你选择了第 {idx + 1} 项。")
    wait_for_key()
