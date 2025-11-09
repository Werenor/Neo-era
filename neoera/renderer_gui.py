"""
Neo-era GUI Renderer v4.3
支持：
- 点击推进文本
- 选项按钮
- 背景切换
- BGM 播放 / 停止（含淡出）
- Sprite 立绘淡入淡出（修复路径问题）
- hide_sprite all 支持一键清场
"""

import os
import sys
import pygame
from queue import Queue

pygame.init()
pygame.mixer.init()

WINDOW_SIZE = (960, 640)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Neo-era")

clock = pygame.time.Clock()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_render_queue = Queue()
_choice_queue = Queue()
_choice_result = Queue()
_sprites = {}  # path: {img, pos, layer, mode, fade, target}
current_bg = None

# --------------------------------------------------
# 字体
font_name = (
    pygame.font.match_font("Microsoft YaHei UI")
    or pygame.font.match_font("simhei")
    or pygame.font.get_default_font()
)
font_main = pygame.font.Font(font_name, 24)
font_choice = pygame.font.Font(font_name, 22)

# --------------------------------------------------
# 背景与音乐
def load_background(path: str):
    """加载背景"""
    global current_bg
    try:
        if not os.path.isabs(path):
            path = os.path.join(PROJECT_ROOT, path)
        img = pygame.image.load(path).convert()
        current_bg = pygame.transform.scale(img, WINDOW_SIZE)
        print(f"[Neo-era] 背景加载: {path}")
    except Exception as e:
        print(f"[WARN] 无法加载背景 {path}: {e}")
        current_bg = None


def play_bgm(path: str):
    """播放 BGM"""
    try:
        if not os.path.isabs(path):
            path = os.path.join(PROJECT_ROOT, path)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        print(f"[Neo-era] 播放 BGM: {path}")
    except Exception as e:
        print(f"[WARN] 无法播放 BGM {path}: {e}")


def stop_bgm(fade_ms: int = 1000):
    """支持淡出停止"""
    try:
        pygame.mixer.music.fadeout(fade_ms)
    except Exception as e:
        print(f"[WARN] 停止 BGM 失败: {e}")

# --------------------------------------------------
# Sprite 立绘系统
def show_sprite(path, pos="center", fade_frames=20):
    """加载并淡入显示立绘"""
    global _sprites
    try:
        if not os.path.isabs(path):
            path = os.path.join(PROJECT_ROOT, path)
        img = pygame.image.load(path).convert_alpha()
        w, h = img.get_size()

        # 自动缩放（高度不超过窗口 80%）
        max_h = int(WINDOW_SIZE[1] * 0.8)
        if h > max_h:
            scale = max_h / h
            img = pygame.transform.smoothscale(img, (int(w * scale), max_h))
            w, h = img.get_size()

        # 位置与层
        if pos == "left":
            x, layer = 60, 0
        elif pos == "right":
            x, layer = WINDOW_SIZE[0] - w - 60, 2
        else:
            x, layer = (WINDOW_SIZE[0] - w) // 2, 1
        y = WINDOW_SIZE[1] - h - 40

        # 初始 alpha = 0
        surf = img.copy()
        surf.set_alpha(0)
        _sprites[path] = {
            "img": surf,
            "pos": (x, y),
            "layer": layer,
            "target": img,
            "fade": fade_frames,
            "mode": "fadein"
        }
        print(f"[Neo-era] 淡入立绘 {path} @ {pos} 缩放后=({w},{h})")
    except Exception as e:
        print(f"[WARN] 无法加载立绘 {path}: {e}")


def hide_sprite(path, fade_frames=20):
    """淡出立绘并删除（带主动刷新 + 路径统一 + 支持 all）"""
    global _sprites

    # ✅ 一键清场：hide_sprite all
    if path.strip().lower() == "all":
        print("[Neo-era] 清除全部立绘")
        for k in list(_sprites.keys()):
            hide_sprite(k, fade_frames)
        return

    # ✅ 路径标准化（修复相对路径问题）
    if not os.path.isabs(path):
        path = os.path.join(PROJECT_ROOT, path)

    if path not in _sprites:
        print(f"[WARN] 立绘未在场景中: {path}")
        print("[DEBUG] 当前立绘 keys:", list(_sprites.keys()))
        return

    sprite = _sprites[path]
    sprite["fade"] = fade_frames
    sprite["mode"] = "fadeout"
    print(f"[Neo-era] 淡出立绘 {path}")

    # 主动渲染淡出动画（防止解释器立即跳过）
    for frame in range(fade_frames + 10):
        _draw_background()
        _draw_sprites()
        pygame.display.update()
        clock.tick(60)

# --------------------------------------------------
# 绘制逻辑
def _draw_background():
    if current_bg:
        screen.blit(current_bg, (0, 0))
    else:
        screen.fill((0, 0, 0))


def _draw_sprites():
    """按层次绘制并处理淡入淡出动画"""
    remove_list = []
    for path, data in sorted(_sprites.items(), key=lambda d: d[1]["layer"]):
        img = data["img"]
        pos = data["pos"]

        # --- 淡入 ---
        if data.get("mode") == "fadein":
            alpha = img.get_alpha() if img.get_alpha() is not None else 0
            alpha = min(255, alpha + int(255 / max(1, data["fade"])))
            surf = data["target"].copy()
            surf.set_alpha(alpha)
            data["img"] = surf
            if alpha >= 255:
                data["mode"] = None

        # --- 淡出 ---
        elif data.get("mode") == "fadeout":
            alpha = img.get_alpha() if img.get_alpha() is not None else 255
            alpha = max(0, alpha - int(255 / max(1, data["fade"])))
            surf = data["img"].copy()
            surf.set_alpha(alpha)
            data["img"] = surf
            if alpha <= 0:
                remove_list.append(path)
                continue

        screen.blit(data["img"], pos)

    # 清除已完全淡出的立绘
    for r in remove_list:
        if r in _sprites:
            del _sprites[r]
            print(f"[Neo-era] 已移除立绘: {r}")


def _draw_text(lines):
    base_y = 420
    for i, text in enumerate(lines[-6:]):
        surf = font_main.render(text, True, (0, 255, 0))
        screen.blit(surf, (40, base_y + i * (surf.get_height() + 4)))


def _build_choice_buttons(options):
    rects = []
    spacing = 16
    btn_w, btn_h = 280, 48
    total_h = len(options) * (btn_h + spacing)
    start_y = (WINDOW_SIZE[1] - total_h) // 2 + 60
    for i, opt in enumerate(options):
        rect = pygame.Rect(WINDOW_SIZE[0] // 2 - btn_w // 2,
                           start_y + i * (btn_h + spacing),
                           btn_w, btn_h)
        surf = font_choice.render(opt, True, (0, 255, 0))
        rects.append((rect, surf))
    return rects


def _draw_buttons(buttons):
    for rect, surf in buttons:
        pygame.draw.rect(screen, (30, 30, 30), rect)
        pygame.draw.rect(screen, (0, 255, 0), rect, 2)
        screen.blit(surf, (rect.x + (rect.width - surf.get_width()) // 2,
                           rect.y + (rect.height - surf.get_height()) // 2))

# --------------------------------------------------
# 主循环
def queue_echo(text):
    _render_queue.put(text)

def queue_choice(options):
    _choice_queue.put(options)

def wait_for_choice():
    return _choice_result.get()

def start_main_loop():
    text_buffer = []
    active_buttons = []
    waiting_for_choice = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 点击推进
            if event.type == pygame.MOUSEBUTTONDOWN or (
                event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE)
            ):
                if not waiting_for_choice and not _render_queue.empty():
                    text_buffer.append(_render_queue.get())

            # 点击选项
            if event.type == pygame.MOUSEBUTTONDOWN and active_buttons:
                for i, (rect, _) in enumerate(active_buttons):
                    if rect.collidepoint(event.pos):
                        _choice_result.put(i)
                        active_buttons = []
                        waiting_for_choice = False
                        text_buffer.append(f"[选项] -> {i + 1}")
                        break

        # 处理选项出现
        if not _choice_queue.empty() and not active_buttons and _render_queue.qsize() == 0:
            opts = _choice_queue.get()
            active_buttons = _build_choice_buttons(opts)
            waiting_for_choice = True

        # 绘制画面
        _draw_background()
        _draw_sprites()
        _draw_text(text_buffer)
        _draw_buttons(active_buttons)
        pygame.display.update()
        clock.tick(60)
