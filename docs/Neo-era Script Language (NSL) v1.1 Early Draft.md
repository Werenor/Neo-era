# Neo-era Script Language (NSL) v1.1 Specification

---

## 1. 概述

Neo-era Script Language（简称 **NSL**）是一门为剧情驱动型游戏设计的脚本语言。
它融合了 **Ren’Py 的自然可读性**、**Era 的系统逻辑表达能力** 与 **可视化扩展潜力**，
用于驱动 Neo-era 引擎的剧情逻辑、UI 表现、角色状态和交互事件。

NSL 的设计目标是：

* **可读性高**：剧本即剧情；
* **结构统一**：无歧义、无多余符号；
* **轻量可解析**：简单文本即可解释执行；
* **高度可扩展**：支持函数、模块、系统命令。

---

## 2. 文件结构与基本语法

### 2.1 文件扩展名

所有 Neo-era 脚本文件以 `.neo` 结尾。

### 2.2 注释语法

```python
# 单行注释
# 任意位置均可使用，行首或行尾
echo 爱宕：早安，指挥官。  # 这是一条注释
```

多行注释与 Python 一致，使用三引号括起来：

```python
'''
这是多行注释示例
可以写任意说明
解释剧情逻辑或作者提示
'''
```

或：

```python
"""
同样可以使用双引号版本
多行注释常用于说明函数或模块用途
"""
```

### 2.3 基本行结构

每一行是一个独立语句。
空行会被忽略。

```python
bg assets/bg/room.jpg
echo 爱宕：早安，指挥官。
```

### 2.4 命令与文本

* 以关键字开头 → 命令；
* 其他行 → 被视作 `echo`（隐式输出文本）。

```python
爱宕：早安，指挥官。     # 隐式 echo
echo 指挥官：早安。       # 显式 echo
```

---

## 3. 变量系统

### 3.1 定义变量

```python
var favor = 0            # 临时变量
pvar player_name = "指挥官"  # 持久变量（保存进档）
```

### 3.2 修改变量

```python
set favor += 2
set player_name = "指挥官大人"
```

### 3.3 设置布尔变量

```python
setbool seen_atago true
setbool debug_mode off
setbool music_enabled yes
```

#### 说明

* `setbool` 始终将右侧参数解析为布尔值；
* 不进行算术或表达式计算；
* 用于定义、切换或更新逻辑开关；
* 在保存、载入、逻辑判断中确保类型安全。

#### 布尔值解析规则

| 真值（True）                                  | 假值（False）                                     |
| ----------------------------------------- | --------------------------------------------- |
| true, t, yes, on, 1, one, enable, enabled | false, f, no, off, 0, zero, disable, disabled |

* 不区分大小写；
* 自动忽略前后空格；
* 未识别值默认视为 `False`（安全策略）。

#### 解析逻辑（伪代码）

```python
def to_bool(val):
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    if s in {"true","t","1","one","yes","on","enable","enabled"}:
        return True
    if s in {"false","f","0","zero","no","off","disable","disabled"}:
        return False
    return False
```

#### 示例

```python
setbool auto true
if auto
    echo 自动播放模式已开启。
end

setbool debug off
if not debug
    echo 调试模式已关闭。
end
```

### 3.4 删除与清空

```python
del favor
clear temp     # 清空所有临时变量
clear perm     # 清空所有持久变量
```

### 3.5 变量插值

```python
echo 当前好感度：{favor}
```

---

## 4. 条件与循环

### 4.1 条件结构

```python
if favor >= 5
    echo 爱宕：真贴心呢~
else
    echo 爱宕：哼。
end
```

### 4.2 循环结构

```python
for i = 1 to 3
    echo 第 {i} 次测试。
end

while favor < 10
    set favor += 1
    echo 好感度：{favor}
end
```

### 4.3 跳出控制

```python
break
continue
```

---

## 5. 模块与函数

```python
func add_favor amount
    set favor += amount
    echo 好感度增加 {amount}
endfunc

call add_favor 5
return ok
```

模块导入：

```python
import sys/save.neo as sys
call sys.quicksave()
```

---

## 6. 资源与图层

```python
bg assets/bg/room.jpg
bgm assets/bgm/theme.mp3
se assets/se/click.wav
```

### 图层操作

```python
layer.create char 100
layer.alpha char 0.8
fadein char 0.3
fadeout char 0.3
```

### 精灵与立绘

```python
sprite.add char atago assets/chars/atago_normal.png x=200 y=360 scale=1.0
sprite.move char atago 260 360 duration=0.4
sprite.flip char atago true
sprite.rotate char atago 5
sprite.tint char atago r=0.7 g=0.7 b=0.7 saturation=0.4 duration=0.3
```

---

## 7. 输入与分支

```python
choice 回应|装作没听见|保持沉默
if choice == 0
    echo 你：早安。
else
    echo 爱宕：哼。
end

input.text player_name "请输入名字：" default="指挥官" max=16 required=true
```

---

## 8. 节奏与演出系统

```python
auto on
delay 0.8
wait
auto off
```

```python
speed 1.0
printmode char
window hide
voice play assets/voice/atago_happy.ogg
waitvoice
window show
```

---

## 9. 存档与上下文

```python
save 1
load 1
```

持久变量 (`pvar`) 会被保存，
临时变量自动在场景结束时清空。

---

## 10. 配置与控制

```python
config talk_highlight = true
config talk_dim_color = r=0.7 g=0.7 b=0.7 saturation=0.4
config auto.speed = 1.0
config printmode = char
skip on
skip off
```

---

## 11. 调试与日志

```python
log "Debug message"
printvar favor
trace
```

---

## 12. 调用顺序示意

```python
bg assets/bg/room.jpg
echo 爱宕：早安，指挥官。
choice 回应|装作没听见
if choice == 0
    echo 指挥官：早安。
    set favor += 1
else
    echo 爱宕：哼。
end
save 1
```

---

## 附录 A：关键字表（更新）

```
bg, bgm, se, layer, sprite, fadein, fadeout,
echo, choice, input, var, pvar, set, setbool, del, clear,
if, elif, else, end, for, while, break, continue,
func, call, return, import, auto, wait, delay,
speed, printmode, window, voice, waitvoice,
save, load, config, skip, log, trace
```

---

## 附录 B：执行模型简图

```
        ┌──────────────┐
        │  Parser(.neo)│
        └─────┬────────┘
              ↓
        ┌──────────────┐
        │ Interpreter  │
        │  (Context)   │
        └─────┬────────┘
              ↓
        ┌──────────────┐
        │  Renderer    │
        │ (pygame_gui) │
        └─────┬────────┘
              ↓
        ┌──────────────┐
        │ Player Input │
        │  Auto/Wait   │
        └──────────────┘
```

