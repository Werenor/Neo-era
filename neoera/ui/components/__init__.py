from neoera.ui.components.label import UILabel
from neoera.ui.components.button import UIButton
from neoera.ui.components.image import UIImage
from neoera.ui.components.panel import UIPanel
from neoera.ui.components.bar import UIBar

from neoera.ui.layouts.vbox import VBox
from neoera.ui.layouts.hbox import HBox
from neoera.ui.layouts.grid import Grid
from neoera.ui.layouts.absolute import Absolute
from neoera.ui.layouts.stack import Stack
from neoera.ui.layouts.overlay import Overlay


UI_COMPONENTS = {
    # 基础元素
    "label": UILabel,
    "button": UIButton,
    "image": UIImage,
    "panel": UIPanel,
    "bar": UIBar,

    # 布局
    "vbox": VBox,
    "hbox": HBox,
    "grid": Grid,
    "absolute": Absolute,
    "stack": Stack,
    "overlay": Overlay,
}

__all__ = [
    "UILabel", "UIButton", "UIImage", "UIPanel", "UIBar",
    "VBox", "HBox", "Grid", "Absolute", "Stack", "Overlay",
    "UI_COMPONENTS",
]
