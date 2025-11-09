# /neoera/renderer_gui.py
"""
Neo-era GUI 渲染器 v3.1
- 点击推进文本（不锁主线程）
- 支持选项按钮
- 保持事件响应
"""

import os
import sys
import pygame
from queue import Queue

pygame.init()

# ============================================================
# 基础配置
# ============================================================
WINDOW_SIZE = (960, 640)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Neo-era")

clock = pygame.time.Clock()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_render_queue: Queue[str] = Queue()
_choice_queue: Queue[list[str]] = Queue()
_choice_result: Queue[int] = Queue()

current_bg = None

# ============================================================
# 字体
# ============================================================
font_name = (
    pygame.font.match_font("Microsoft YaHei UI")
    or pygame.font.match_font("simhei")
    or pygame.font.get_default_font()
)
font_main = pygame.font.Font(font_name, 24)
font_choice = pygame.font.Font(font_name, 22)

# ============================================================
# 背景绘制
# ============================================================
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

# ============================================================
# 文本绘制
# ============================================================
def _draw_text_lines(lines):
    base_y = 420
    for i, text in enumerate(lines[-6:]):
        surf = font_main.render(text, True, (0, 255, 0))
        screen.blit(surf, (40, base_y + i * (surf.get_height() + 4)))

# ============================================================
# 选项按钮
# ============================================================
def _build_choice_buttons(options):
    rects = []
    spacing = 16
    btn_w, btn_h = 280, 48
    total_h = len(options) * (btn_h + spacing)
    start_y = (WINDOW_SIZE[1] - total_h) // 2 + 60

    for i, opt in enumerate(options):
        rect = pygame.Rect(
            WINDOW_SIZE[0] // 2 - btn_w // 2,
            start_y + i * (btn_h + spacing),
            btn_w,
            btn_h,
        )
        surf = font_choice.render(opt, True, (0, 255, 0))
        rects.append((rect, surf))
    return rects


def _draw_buttons(buttons):
    for rect, surf in buttons:
        pygame.draw.rect(screen, (30, 30, 30), rect)
        pygame.draw.rect(screen, (0, 255, 0), rect, 2)
        screen.blit(
            surf,
            (
                rect.x + (rect.width - surf.get_width()) // 2,
                rect.y + (rect.height - surf.get_height()) // 2,
            ),
        )

# ============================================================
# 逻辑接口
# ============================================================
def queue_echo(text: str):
    """加入文本到渲染队列（非阻塞）"""
    _render_queue.put(text)


def queue_choice(options):
    """加入选项到任务队列"""
    _choice_queue.put(options)


def wait_for_choice() -> int:
    """阻塞等待玩家选项"""
    return _choice_result.get()

# ============================================================
# 主循环
# ============================================================
def start_main_loop():
    """统一事件循环，点击推进"""
    text_buffer = []
    active_buttons = []
    waiting_for_choice = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 推进文本
            if event.type == pygame.MOUSEBUTTONDOWN or (
                event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)
            ):
                # 若存在选项，忽略推进
                if not waiting_for_choice and not _render_queue.empty():
                    text_buffer.append(_render_queue.get())

            # 处理按钮点击
            if event.type == pygame.MOUSEBUTTONDOWN and active_buttons:
                for i, (rect, _) in enumerate(active_buttons):
                    if rect.collidepoint(event.pos):
                        _choice_result.put(i)
                        active_buttons = []
                        waiting_for_choice = False
                        text_buffer.append(f"[选项] -> {i + 1}")
                        break

        # 检查是否有新选项任务
        if not _choice_queue.empty() and not active_buttons and not _render_queue.qsize():
            opts = _choice_queue.get()
            active_buttons = _build_choice_buttons(opts)
            waiting_for_choice = True

        # 绘制画面
        _draw_background()
        _draw_text_lines(text_buffer)
        _draw_buttons(active_buttons)
        pygame.display.update()
        clock.tick(60)
