# 📘 **Neo-era v0.4.1 官方技术文档**

**Neo-era：一款专注剧情表现、UI 表达与轻量可扩展性的原创新型脚本驱动引擎**
文档版本：**0.4.1**
引擎核心版本：**0.4**
文档状态：**完整、可执行、覆盖全系统**

---

# 0. 前言

Neo-era 是一套轻量但能力完整的剧情表现引擎，目标是让创作者可以：

* 用 **自然的脚本语言（NSL）** 撰写剧情
* 用 **简洁的 UI DSL** 写自定义界面
* 使用 **渲染 + 动画系统** 达成视觉表现
* 使用 **可扩展的执行器模型** 驱动游戏逻辑

它融合了：

* 类 Ren’Py 的剧情脚本美感
* 类 QML 的 UI 动态绑定模型
* 类 Unity 的 Update / Renderer pipeline
* 类 Godot 的节点/组件式 UI 设计

**设计哲学：**

1. **简洁优先** —— 谨慎扩展功能，保持语言美观
2. **表达力优先** —— UI 与剧情应能通过少量脚本实现复杂表达
3. **工程可维护** —— 所有系统模块化、可替换、可扩展
4. **稳定优先** —— 在 v0.4+ 阶段，增加功能不如增强稳定
5. **谦虚与可解释性** —— 文档尽可能解释设计理由，而非宣称先进

> 本文档为 Neo-era 历史上的首个「完整规范」。
> 它不仅描述功能，也描述结构、流程图、协议、扩展指南和调试建议。

---

# 1. 建议的项目结构

以下为推荐的 Neo-era 项目结构：

```
your_game/
│
├─ main.py               游戏入口
├─ neoera/               引擎核心（不可修改或可作为 submodule）
│
├─ game_scripts/         剧情脚本（.nsl）
│    └─ main.nsl
│
├─ ui_screens/           UI DSL （.ui）
│    └─ menu.ui
│
├─ assets/
│    ├─ sprites/
│    ├─ bg/
│    ├─ ui/
│    ├─ sound/
│    └─ font/
│
└─ config/               你的游戏的一些可选配置
```

---

# 2. CONFIG（配置系统）

`neoera/core/config.py`

| 配置项                  | 说明                     |
| -------------------- | ---------------------- |
| `RESOLUTION`         | 屏幕分辨率，如 (1280, 720)    |
| `FPS`                | 每秒帧数                   |
| `RESOURCE_PATHS`     | 图片、音频、字体等资源路径          |
| `FONT_NAME`          | 默认字体文件                 |
| `FONT_SIZE`          | 默认字体大小                 |
| `ENABLE_DEBUG_LAYER` | 是否显示 FPS / 状态 debug 内容 |

**说明**：
此配置影响整个渲染器、UI 系统、字体系统和资源加载系统。

---

# 3. NSL（Neo-era Script Language）

### NSL 既是剧情语言，也是游戏逻辑驱动语言

它类似 Ren’Py 的 script + 部分 Python 的表达式语法。

---

## 3.1 NSL 支持的语句总览

| 语句                 | 示例                                | 说明            |
| ------------------ | --------------------------------- | ------------- |
| 文本行                | `"你好"`                            | 打印文本（自动 echo） |
| echo               | `echo "Hello"`                    | 显式对话文本        |
| set                | `set hp = 10`                     | 设置变量          |
| if / elseif / else | `if hp < 0:`                      | 分支逻辑          |
| choice             | `choice:`                         | 分支选择          |
| input              | `input "你的名字？"`                   | 玩家输入          |
| delay              | `delay 1.0`                       | 等待毫秒/秒        |
| bg                 | `bg "room.png"`                   | 设置背景          |
| sprite_show        | `sprite_show "alice" x=200 y=300` | 显示立绘          |
| sprite_hide        | `sprite_hide "alice"`             | 隐藏立绘          |
| bgm                | `bgm "theme.mp3"`                 | 播放背景音乐        |
| stop_bgm           | `stop_bgm`                        | 停止音乐          |
| ui_show            | `ui_show "menu"`                  | 显示 UI         |
| ui_hide            | `ui_hide`                         | 关闭 UI         |

---

## 3.2 NSL 表达式系统（完整）

表达式语法是一个 Pratt Parser，支持：

* 加减乘除 + - * /
* 布尔逻辑 and/or/not
* 比较运算 == != < <= >=
* 变量访问 player.hp
* 数组 [1,2,3]
* 函数调用 fn(x, y)
* 字符串拼接 `"Hello " + name`
* 一元负号 `-x`

---

## 3.3 内置函数（文档新增）

已实现但旧文档未写：

| 函数       | 说明   |
| -------- | ---- |
| len(x)   | 长度   |
| max(a,b) | 最大值  |
| min(a,b) | 最小值  |
| int(x)   | 转整数  |
| float(x) | 转浮点  |
| str(x)   | 转字符串 |
| print(x) | 调试   |

---

## 3.4 IF / ELSE 执行栈（新增解释）

NSL 的分支语法使用 “执行栈（callstack）” 实现：

执行例子：

```
if cond:
    ...
elseif cond2:
    ...
else:
    ...
endif
```

Interpreter 会返回：

```
("PUSH_BLOCK", then_block)
```

Executor 负责将 then_block 推入栈进行执行，这使得 NSL 具备“子程序式的 block 执行”。

---

## 3.5 choice（选择系统）

```
choice:
    "攻击" -> "atk"
    "逃跑" -> "run"
endchoice
```

Executor 将进入 `WAIT_CHOICE`，玩家选择后：

```
ctx.vars["choice_result"]
```

将包含返回值。

---

## 3.6 input（输入系统）

```
input "请输入名字" -> name
```

输入完成后：

```
ctx.vars["name"]
```

更新为用户输入文本。

---

## 3.7 delay（等待）

```
delay 1.0
```

Executor 进入 WAIT_DELAY，直到 (current_time >= delay_end)

---

## 3.8 渲染指令协议（新增）

Interpreter 不直接渲染，而是返回指令：

```
("RENDER", ("BG", name))
("RENDER", ("SPRITE_SHOW", payload))
("RENDER", ("BGM_PLAY", name))
("RENDER", ("BGM_STOP", None))
```

Executor 负责调用 Renderer.apply_instruction。

---

# 4. UI DSL （完整语法与行为）

UI DSL 提供类似 QML / FXML 的界面语言。

---

## 4.1 UI 顶层语法

```
ui menu_screen:
    ...
end
```

UIParser 将 UI AST 转入 Builder，生成 UI 树。

---

## 4.2 组件（components）

| 名称     | 说明            |
| ------ | ------------- |
| label  | 文本标签          |
| button | 按钮            |
| image  | 图片组件          |
| bar    | 进度条           |
| panel  | 容器组件（带背景色、填充） |

---

## 4.3 组件属性

所有组件支持：

| 属性            | 示例                 | 说明      |
| ------------- | ------------------ | ------- |
| x, y          | `x=100`            | 坐标      |
| width, height | `width=200`        | 尺寸      |
| visible       | `visible={hp > 0}` | 是否显示    |
| alpha         | `alpha=0.8`        | 透明度     |
| scale         | `scale=1.2`        | 缩放      |
| rotation      | `rotation=45`      | 旋转      |
| color         | `color="#fff"`     | 文本或背景颜色 |

---

## 4.4 动态绑定（binding）

```
label text="{player.hp}"
```

绑定表达式每帧自动 update。

Binding 机制说明：

* parse → store AST → every frame evaluate
* 出错会被自动捕获（不导致 UI 崩溃）

---

## 4.5 事件（on_click）

```
button:
    text="OK"
    on_click="confirm"
```

UIManager 处理事件 → Executor → NSL → ctx.vars["ui_result"]

---

## 4.6 for 循环（repeater）

```
for u in enemies:
    label text="{u.name}"
end
```

Builder 自动展开子 UI。

支持：

* 多级嵌套 for
* 动态绑定
* 作用域变量

---

## 4.7 布局（layout）

### vbox（垂直）

```
vbox spacing=10:
    label text="A"
    label text="B"
end
```

### hbox（水平）

```
hbox spacing=20 align="center":
    ...
end
```

### grid

```
grid rows=2 cols=3:
    ...
end
```

### absolute（绝对布局）

### overlay（覆盖布局）

### stack（堆叠布局）

---

## 4.8 UI 动画（anim）

```
anim fade_in duration=0.4
anim move_to x=200 y=300 duration=1.0 easing="ease_out"
```

动画系统基于 Tween：

* 位置
* alpha
* scale
* rotation

支持 easing：

* linear
* ease_in
* ease_out
* cubic

---

# 5. Runtime（完整状态机）

### 状态机图

```
IDLE
  |
  |(ECHO)
  v
WAIT_CLICK --(click)--> IDLE

WAIT_CHOICE --(choice selected)--> IDLE

WAIT_INPUT --(input done)--> IDLE

WAIT_DELAY --(time reached)--> IDLE

WAIT_ANIMATION --(animation finished)--> IDLE

WAIT_UI --(ui_result ready)--> IDLE
```

---

## Interpreter → Executor 通信协议（正式表）

| result     | payload        | 意义         |
| ---------- | -------------- | ---------- |
| ECHO       | string         | 显示文本       |
| CHOICE     | [(text,val),…] | 显示选择       |
| INPUT      | prompt         | 输入框        |
| DELAY      | seconds        | 等待         |
| RENDER     | (type,data)    | 渲染指令       |
| UI_SHOW    | name           | 显示 UI      |
| UI_HIDE    |                | 隐藏         |
| PUSH_BLOCK | AST list       | 执行逻辑 block |
| END        |                | 结束脚本       |

---

# 6. Renderer（渲染系统）

完整 pipeline：

```
BackgroundLayer
SpriteLayer
DialogueLayer
ChoiceLayer
InputLayer
UILayer
DebugLayer
```

---

## 6.1 Dialogue（对话框）

* 打字机效果
* 文本换行
* 字体渲染
* 框体 UI（如需可扩展）

---

## 6.2 Sprite（立绘）

* x/y
* alpha
* scale
* 动画支持
* 多 sprite 覆盖
* 不遮挡 UI

---

## 6.3 Choice UI

按钮列表，返回 index。

---

## 6.4 Input Box

文本输入 UI。

---

## 6.5 Transitions（过场）

支持：

* fade(duration)
* slide(direction)
* composite 多组合
* WAIT_ANIMATION 阻塞

---

## 6.6 Animation 系统

### Tween(target, property, start, end, duration, easing)

### Animation([tween1, tween2…])

### AnimationQueue（用于排队）

支持：

* 位置动画
* alpha 动画
* scale 动画
* rotation 动画

---

# 7. ResourceManager（资源管理器）

* 图片缓存
* 字体缓存
* 声音缓存
* fallback Missing.png
* 动态加载路径来自 CONFIG

---

# 8. 主循环（Game Loop）

时序图：

```
while running:
    handle_events()
    executor.tick(dt)
    renderer.update(dt)
    renderer.draw(screen)
    flip()
```

事件流：

```
pygame event → UIManager + Renderer → Executor (click / text / ui_result)
```

---

# 9. 调试指南（FAQ）

### UI 不显示？

* 检查 ui_show 名字
* 检查 UI AST 正确
* 检查 parse_props 是否正确

### 文本不换行？

* 查看 DialogueBox 渲染逻辑

### 动画不播放？

* 检查 animation.finished
* 检查 WAIT_ANIMATION 状态

### 图片不显示？

* 查看资源路径
* ResourceManager fallback

---

# 10. 扩展指南（面向有开发能力者）

### 扩展 NSL 指令

在 interpreter 中新增 `_exec_old_stmt` case 即可。

### 扩展 UI 组件

在 builder.COMPONENT_TYPES 注册。

### 扩展 layout

在 builder.LAYOUT_TYPES 注册。

### 扩展渲染层

修改 render_pipeline。

---

# 11. 版本历史（从 v0.4.1 开始）

## 0.4.1（本版本）

* 文档体系首次完整化
* 明确 NSL / UI DSL 全规范
* 完善 Runtime、Renderer、Core 描述
* 引擎整体进入稳定阶段
