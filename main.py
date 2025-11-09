# /neoera/main.py
"""
非阻塞主循环版：渲染与逻辑分离
"""

import threading
from neoera.parser import Parser
from neoera.interpreter import Interpreter
from neoera.core import ctx
from neoera import renderer_gui as renderer


def run_script():
    """在后台线程运行脚本逻辑"""
    parser = Parser()
    with open("test.neo", "r", encoding="utf-8") as f:
        script = f.read()
    parser.parse(script)

    interpreter = Interpreter(ctx)
    interpreter.execute(parser.ast)


def main():
    renderer.load_background("assets/bg/test_bg.jpg")
    renderer.queue_echo("[Neo-era] 引擎启动中……")



    # 启动脚本执行线程（不阻塞渲染）
    script_thread = threading.Thread(target=run_script, daemon=True)
    script_thread.start()

    # 启动事件循环（渲染线程）
    renderer.start_main_loop()


if __name__ == "__main__":
    main()

