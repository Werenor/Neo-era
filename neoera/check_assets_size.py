# /neoera/check_assets_size.py
"""
检测所有立绘、背景、音乐文件是否存在及尺寸安全。
"""

import os
import pygame

pygame.init()
WINDOW_SIZE = (960, 640)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_images(folder):
    path = os.path.join(PROJECT_ROOT, folder)
    if not os.path.exists(path):
        print(f"[WARN] 目录不存在: {path}")
        return
    print(f"[检查] {folder}")
    for file in os.listdir(path):
        if not file.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        fpath = os.path.join(path, file)
        try:
            img = pygame.image.load(fpath)
            w, h = img.get_size()
            print(f"  {file:25} 尺寸=({w}x{h})", end="")
            if w > WINDOW_SIZE[0] or h > WINDOW_SIZE[1]:
                print("  ⚠️ 超出窗口大小，建议缩放")
            else:
                print("  ✅ OK")
        except Exception as e:
            print(f"  {file} 无法加载: {e}")

def check_audio(folder):
    path = os.path.join(PROJECT_ROOT, folder)
    if not os.path.exists(path):
        print(f"[WARN] 目录不存在: {path}")
        return
    print(f"[检查] {folder}")
    for file in os.listdir(path):
        if not file.lower().endswith((".ogg", ".mp3", ".wav")):
            continue
        fpath = os.path.join(path, file)
        size_kb = os.path.getsize(fpath) / 1024
        print(f"  {file:25} 大小={size_kb:.1f}KB")

if __name__ == "__main__":
    print("=== Neo-era 素材检查 ===")
    check_images("assets/bg")
    check_images("assets/sprite")
    check_audio("assets/bgm")
    print("========================")
