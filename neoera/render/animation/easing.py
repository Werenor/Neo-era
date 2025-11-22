import math


class Easing:
    """
    标准动画缓动函数
    未来可扩展：elastic、bounce、back、expo 等
    """

    @staticmethod
    def linear(t):
        return t

    @staticmethod
    def ease_in(t):
        return t * t

    @staticmethod
    def ease_out(t):
        return 1 - (1 - t) * (1 - t)

    @staticmethod
    def ease_in_out(t):
        if t < 0.5:
            return 2 * t * t
        return 1 - pow(-2 * t + 2, 2) / 2

    # 未来扩展
    @staticmethod
    def cubic(t):
        return t**3

    @staticmethod
    def quartic(t):
        return t**4
