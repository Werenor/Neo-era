import time
from enum import Enum, auto


class ExecState(Enum):
    IDLE = auto()
    WAIT_CLICK = auto()
    WAIT_CHOICE = auto()
    WAIT_INPUT = auto()
    WAIT_DELAY = auto()
    WAIT_ANIMATION = auto()
    WAIT_UI = auto()


class Executor:
    """
    Neo-era v0.4.2 Executor
    驱动 Interpreter / Renderer / UI 的状态机
    """

    def __init__(self, interpreter, renderer):
        self.interpreter = interpreter
        self.renderer = renderer

        self.state = ExecState.IDLE
        self.delay_end_time = 0.0

        self.choice_result = None
        self.input_result = None
        self.ui_result = None

    # --------------------------------------------------
    # 外部回调接口（预留给 UI/选择系统用）
    # --------------------------------------------------
    def set_choice_result(self, index):
        self.choice_result = index

    def set_input_result(self, value):
        self.input_result = value

    def set_ui_result(self, value):
        self.ui_result = value

    # --------------------------------------------------
    # 每帧驱动
    # --------------------------------------------------
    def tick(self, dt):
        # 状态机分支
        if self.state == ExecState.IDLE:
            self._run_next()
            return

        # 等待点击推进文本
        if self.state == ExecState.WAIT_CLICK:
            if self._dialogue_can_advance():
                self.state = ExecState.IDLE
            return

        # 等待选择
        if self.state == ExecState.WAIT_CHOICE:
            if self.choice_result is not None:
                # 这里仅清空等待状态，跳转逻辑留给后续扩展
                self.choice_result = None
                self.state = ExecState.IDLE
            return

        # 等待输入
        if self.state == ExecState.WAIT_INPUT:
            if self.input_result is not None:
                # 同上，赋值逻辑留给后续完善
                self.input_result = None
                self.state = ExecState.IDLE
            return

        # 等待 delay
        if self.state == ExecState.WAIT_DELAY:
            if time.time() >= self.delay_end_time:
                self.state = ExecState.IDLE
            return

        # 等待动画完成（SpriteManager）
        if self.state == ExecState.WAIT_ANIMATION:
            if not self.renderer.sprites.animating():
                self.state = ExecState.IDLE
            return

        # 等待 UI 关闭
        if self.state == ExecState.WAIT_UI:
            if self.ui_result is not None:
                self.ui_result = None
                self.state = ExecState.IDLE
            return

    # --------------------------------------------------
    # 执行下一条指令
    # --------------------------------------------------
    def _run_next(self):
        result, payload = self.interpreter.exec_stmt()

        if result is None:
            return

        # 文本输出
        if result == "ECHO":
            self.renderer.dialogue.set_text(payload)
            self.state = ExecState.WAIT_CLICK
            return

        # UI 显示 / 隐藏
        if result == "UI_SHOW":
            screen_name = payload
            if self.renderer.ui_manager:
                self.renderer.ui_manager.show(screen_name)
            self.state = ExecState.WAIT_UI
            return

        if result == "UI_HIDE":
            if self.renderer.ui_manager:
                self.renderer.ui_manager.hide()
            self.state = ExecState.IDLE
            return

        # 选择
        if result == "CHOICE":
            self.renderer.choice_ui.show(payload)
            self.state = ExecState.WAIT_CHOICE
            return

        # 输入
        if result == "INPUT":
            self.renderer.input_box.show(payload)
            self.state = ExecState.WAIT_INPUT
            return

        # delay
        if result == "DELAY":
            seconds = payload
            self.delay_end_time = time.time() + seconds
            self.state = ExecState.WAIT_DELAY
            return

        # 渲染 / 动画
        if result == "RENDER":
            self.renderer.apply_instruction(payload)
            # 如果 payload 标记了需要等待动画，则进入 WAIT_ANIMATION
            if payload.get("wait_animation"):
                self.state = ExecState.WAIT_ANIMATION
            return

        # 结束
        if result == "END":
            return

    # --------------------------------------------------
    # 对话框推进判定（简单实现）
    # --------------------------------------------------
    def _dialogue_can_advance(self):
        dlg = self.renderer.dialogue
        # 这里假设 DialogueBox 暴露 finished / wait_for_click 标记；
        # 如果你的实现不同，可以在这里改判断逻辑。
        finished = getattr(dlg, "finished", True)
        clicked = getattr(dlg, "clicked", False)

        if finished and clicked:
            # 重置点击状态，防止连续触发
            if hasattr(dlg, "clicked"):
                dlg.clicked = False
            return True
        return False
