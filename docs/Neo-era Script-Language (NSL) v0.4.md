# 📘 **Neo-era Script Language & UI DSL

Official Specification v0.4**

> Neo-era 引擎是一款脚本驱动、多图层渲染、可扩展 UI 的 AVG / 剧情演出引擎。
> 该文档描述 `v0.4` 版本下所有语言功能、执行模型、UI DSL、渲染规则与附录。

---

# 目录

1. 前言
2. Neo-era 架构概览
3. NSL（剧情脚本语言）
   　3.1 基础语法
   　3.2 文本与对话
   　3.3 变量与表达式
   　3.4 控制流
   　3.5 指令（背景、立绘、声音等）
   　3.6 特殊指令与扩展
4. 执行模型（Runtime Executor）
   　4.1 ExecState
   　4.2 执行流与 WAIT 状态
   　4.3 事件驱动模型
5. 渲染系统（Renderer）
   　5.1 渲染管线
   　5.2 背景系统
   　5.3 立绘系统
   　5.4 对话框
   　5.5 动画系统
   　5.6 UI Overlay
6. **UI DSL（Neo-era UI Screen Language）**
   　6.1 设计目标
   　6.2 UI Block
   　6.3 元素（label/button/image/bar/panel）
   　6.4 容器布局（vbox/hbox/grid/absolute/overlay/stack）
   　6.5 属性
   　6.6 表达式绑定 `{}`
   　6.7 for 循环（动态渲染）
   　6.8 动画
   　6.9 事件绑定
   　6.10 UI 与 NSL 结合：ui_show / wait_ui
7. UI Runtime（UIBuilder + UIManager）
   　7.1 AST→UI 树
   　7.2 Binding 更新
   　7.3 Layout Pass
   　7.4 Animation Pass
   　7.5 UI 事件回传
8. 示例（完整 NSL + UI DSL）
9. 附录（内置函数 / 错误 / 未来扩展）

---

# 1. 前言

Neo-era 是一个“脚本驱动、数据绑定、动画化 UI、可扩展布局”的 2D 表演引擎。
v0.4 是首次将：

* 剧情脚本语言（NSL）
* UI 布局语言（UI DSL）
* 动画系统
* 渲染流水线
* runtime 状态机

全部统一纳入文档的版本。

本版本特性：

* 全新 **UI DSL**
* 全新 **UIBuilder + UIManager**
* 完整 **layout 系统**
* 完整 **表达式/绑定系统**
* 完整 **WAIT_UI 执行流**
* 完整 **Renderer v2.5（背景/立绘/UI/动画）**

---

# 2. Neo-era 引擎架构概览

```
neoera/
    language/        ← NSL + UI DSL + expr
    runtime/         ← executor + context + state
    render/          ← Renderer v2.5 + pipeline + animations
    ui/              ← UI DSL runtime（components/layout/builder/manager）
    core/            ← engine 入口 + config + resources
```

执行链路：

```
NSL Script → Parser → AST
          → Interpreter → (Instruction)
          → Executor（状态机）
          → Renderer（update + render）
          → UIManager（UI 层逻辑）
```

---

# 3. NSL（剧情脚本语言）

## 3.1 注释

```
# 这是注释
```

## 3.2 文本 / 对话（echo）

```
"你好，我是主角。"
echo "显式文本"
```

文本默认触发 WAIT_CLICK。

## 3.3 变量

```
set x = 10
set hp = max_hp * 0.5
```

## 3.4 表达式

支持：

* 算术 + - * /
* 逻辑 and/or/not
* 比较 == != < <= >=
* 列表
* 函数调用

例：

```
set low = hp < (max_hp * 0.3)
```

## 3.5 控制流

### if / elseif / else

```
if hp < 30:
    echo "很危险！"
elseif hp < 60:
    echo "继续作战。"
else:
    echo "状态良好。"
endif
```

### choice

```
choice:
    "攻击" -> atk
    "防御" -> defend
endchoice
```

### delay

```
delay 1.5   # 等待 1.5 秒
```

---

# 3.6 指令（游戏演出）

## 背景

```
bg "bg/room.png"
```

## 立绘

```
sprite_show "alice.png" x=400 y=200 scale=1 fade=0.5
sprite_hide "alice"
```

## BGM / SE

```
bgm "music.ogg"
stop_bgm
```

---

# 4. 执行模型（Executor）

## 4.1 ExecState 列表

```
IDLE
WAIT_CLICK
WAIT_CHOICE
WAIT_INPUT
WAIT_DELAY
WAIT_ANIMATION
WAIT_UI        ← 新增
```

## 4.2 WAIT_UI 流程

```
ui_show "main_menu"
wait_ui
echo "你选择了 {ui_result}"
```

UIManager 捕获点击事件 → 返回 handler_name → script 继续执行。

---

# 5. 渲染系统（Renderer v2.5）

渲染器负责以下图层：

```
背景层 → 立绘层 → 对话框 → choice → input → UIOverlay → transitions
```

支持：

* Tween 动画（移动/缩放/透明度）
* Layered 图层
* 动态更新
* 高度模块化

---

# 6. UI DSL（NSL-UI）

# 6.1 设计目标

* 脚本定义 UI
* 数据驱动
* 动态渲染（for）
* 动画
* 完全布局
* 与 NSL 完整互动（WAIT_UI、ui_result）

---

# 6.2 UI Block

```
ui main_menu:
    ...
end
```

多个 UI block 可写在一个文件中。

---

# 6.3 基础组件

```
label "文本" font_size=30 color="#ffffff"
button "开始游戏" id=start
image "ui/logo.png" size=128
bar value={hp} max={hp_max} width=200
panel bg="#333"
```

---

# 6.4 布局容器

### vbox

```
vbox spacing=20 align=center:
    label "Neo-era"
    button "开始"
```

### hbox

```
hbox spacing=20:
    button "A"
    button "B"
```

### grid

```
grid rows=2 cols=3 spacing=10:
    image "icon1"
    image "icon2"
```

### absolute

```
absolute:
    label "HP" x=120 y=30
```

### overlay

```
overlay:
    image "bg.png"
    label "Time:{time}"
```

### stack

```
stack:
    image "bg"
    panel bg="#00000088"
```

---

# 6.5 属性（Props）

通用：

```
x=100 y=200 width=300 height=60
color="#ff0000"
visible={hp > 0}
```

---

# 6.6 表达式绑定

```
label "HP: {hp}"
button "攻击（{atk_cost} SP）"
x={unit.x}
color={hp < 30 ? "#ff4444" : "#ffffff"}
```

---

# 6.7 for 循环（动态列表）

```
for u in enemies:
    hbox spacing=10:
        image u.icon size=48
        bar value={u.hp} max={u.max_hp}
```

---

# 6.8 动画

```
image "unit.png":
    anim fade_in duration=0.4
    anim move_to x=300 y=200 duration=1
```

---

# 6.9 事件绑定

```
button "攻击":
    on_click="attack_pressed"
```

返回：

```
ui_result = "attack_pressed"
```

---

# 6.10 UI 与 NSL 结合

在 NSL 脚本：

```
ui_show "battle_menu"
wait_ui

if ui_result == "attack_pressed":
    echo "发动攻击！"
endif
```

---

# 7. UI Runtime（UIBuilder + UIManager）

## 7.1 UIBuilder

* AST → UIComponent 树
* 动态绑定
* 动画绑定
* for 模板展开
* 属性注入

## 7.2 UIManager

* 持有当前 UI 树
* update(dt) → binding + animation + layout
* draw(screen)
* handle_event(event) → 找到按钮的 on_click
* 返回 ui_result 给 executor

---

# 8. 示例

## 8.1 主菜单 UI（ui_screens.ui）

```
ui main_menu:
    vbox spacing=40 align=center:
        label "Neo-era Engine v0.4" font_size=42
        button "开始游戏" id=start:
            on_click="start_game"
        button "退出" id=quit:
            on_click="exit_game"
end
```

## 8.2 剧情脚本（main.nsl）

```
ui_show "main_menu"
wait_ui

if ui_result == "start_game":
    echo "欢迎来到世界。"
endif

bg "bg/room.png"
sprite_show "alice.png" x=300 y=200 fade=0.5

echo "你好，旅行者。"
```

---

# 9. 附录

## 内置函数

* len()
* random()
* int()
* float()
* list()
* 等…

## 错误

* UI Syntax Error
* NSL Parser Error
* RuntimeError

## 未来扩展（v0.5+）

* style DSL
* custom UI template
* camera
* sprite state machine
* 场景管理（scene/goto/import）
