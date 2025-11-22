from enum import Enum, auto

class ExecState(Enum):
    IDLE = auto()           # 可执行下一条语句
    WAIT_CLICK = auto()     # echo / wait 等待点击
    WAIT_CHOICE = auto()    # choice 等待玩家选择
    WAIT_DELAY = auto()     # delay N 秒
    WAIT_ANIMATION = auto() # 渲染动画未完成
    WAIT_INPUT = auto()     # 输入框等待
    FINISHED = auto()       # 程序结束
