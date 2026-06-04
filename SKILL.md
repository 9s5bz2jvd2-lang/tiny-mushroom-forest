---
name: tiny-mushroom-forest
description: |
  Tiny Mushroom Forest（蘑菇森林）桌面疗愈小玩具的标准调用技能。用户想安装、运行、演示、介绍、二次开发、维护、改 README/SKILL、添加水彩蘑菇、点击泡泡、营养泡泡低语、制作人简介，或想用 LingTai 做一个温柔桌面小应用/AI vibe coding 示例时使用。也覆盖：蘑菇单棵或成簇缓慢生长直至铺满屏幕、真实蘑菇造型变体（圆伞菇/鸡油菌/平菇/香菇/金针菇/牛肝菌/墨汁鬼伞/羊肚菌等；禁止毒蝇伞/fly agaric/amanita 形态）、以及黑色加粗花体、不透明、显示至少 3 秒的英文营养低语。包含仓库地址、运行方式、功能边界、营养文案安全规则、贡献/PR 身份纪律与制作人中英双语简介。
version: 1.3.0
author: Wang Runyuan / LingTai
---

# Tiny Mushroom Forest（蘑菇森林）标准技能

## 何时调用

当用户提到以下任一需求时，调用本技能：

- “蘑菇森林 / Tiny Mushroom Forest / tiny-mushroom-forest”。
- 想安装、运行、演示这个桌面小玩具。
- 想做一个透明桌面 overlay / cozy desktop toy / PySide6 小应用。
- 想让蘑菇变水彩、半透明、从下往上生长、点击后变泡泡。
- 想让蘑菇“单棵或成簇”随机、缓慢地出现，并随时间逐渐铺满整个屏幕。
- 想新增更多真实蘑菇造型变体（如圆伞菇/鸡油菌/平菇/香菇/金针菇/牛肝菌/墨汁鬼伞/羊肚菌等；不要使用毒蝇伞/fly agaric/amanita 形态）。
- 想修改或新增点击蘑菇后的英文营养泡泡低语，或调整其字体、颜色、显示时长。
- 想给该项目补 README、制作人介绍、LingTai attribution、发布说明或 GitHub PR。
- 想学习“AI vibe coding”如何从一个小而完整的项目开始。

## 项目事实

- GitHub 仓库：`https://github.com/9s5bz2jvd2-lang/tiny-mushroom-forest`
- 项目定位：一个温柔的桌面透明蘑菇森林小玩具；蘑菇会从屏幕各处缓慢长出（有时单棵、有时成簇），点击后化成上升泡泡，并出现一句简短、诗意、与主流营养学常识相关的英文低语。
- 介绍页安全警示：项目介绍必须保留中英双语提醒——请勿食用任何来源不明或无法识别的蘑菇；请在正规渠道购买野生菌；如果进食蘑菇后出现任何不适，请立即就医，以免耽搁病情。英文口径：Do not eat any mushroom from an unknown source or any mushroom you cannot confidently identify. Please buy wild mushrooms only through reputable channels. If you feel unwell after eating mushrooms, seek medical attention immediately to avoid delaying care.
- 生长方式：调度器随机决定“单棵”或“成簇”生长；成簇时成员会带轻微错峰、自然散布在一个中心附近，而不是同一瞬间同一位置出现。容量较高（默认上限约 240 朵），随时间可逐渐铺满屏幕；超出上限时回收最早的一朵以保证性能。
- 造型变体：保留多种取材自真实蘑菇的造型，但删除容易误导使用者的毒蝇伞/fly agaric/amanita 形态——当前包括 `button`（普通圆伞菇/无白点）、`chanterelle`（鸡油菌/喇叭漏斗）、`oyster`（平菇/侧生扇形）、`shiitake`（香菇/低褐色凸帽）、`enoki`（金针菇/细高小帽）、`porcini`（牛肝菌/粗壮宽帽）、`inkcap`（墨汁鬼伞/高钟形）、`morel`（羊肚菌/蜂窝锥帽）。全部用 `QPainter` 程序化绘制，保留手绘水彩风，无图片素材。
- 低语样式：点击后浮现的英文营养低语为 **黑色、加粗、花体（cursive/script）、完全不透明**，并至少显示 3 秒（低语生命周期与较短的泡泡动画解耦，蘑菇在低语显示窗口结束前不会被回收）。
- 技术栈：Python + PySide6 / Qt；窗口/调度在 `main.py`，蘑菇造型/泡泡/低语绘制在 `mushroom.py`，营养低语短句在 `whispers.py`。
- 许可证：以仓库 README / LICENSE 为准。
- Attribution：README 中保留 `Created with LingTai.`。

## 制作人 / Creator

**王润圆（Wang Runyuan）**

- 昆明医科大学营养与食品卫生学硕士（已毕业）
- 中国注册营养师
- 天文爱好者
- 正在努力学习 AI vibe coding，希望能为营养学科普和人类健康做出一点贡献。

**Wang Runyuan**

- M.S. in Nutrition and Food Hygiene, Kunming Medical University (graduated)
- Chinese Registered Dietitian
- Astronomy enthusiast
- Learning AI vibe coding, with the hope of contributing a little to nutrition science communication and human health.

## 给用户的快速运行说明

```bash
git clone https://github.com/9s5bz2jvd2-lang/tiny-mushroom-forest.git
cd tiny-mushroom-forest
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

常见退出方式：按 `ESC`，或使用系统托盘菜单退出。

如果用户是 Windows，命令可改为：

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 功能说明口径

对外介绍时可用：

> Tiny Mushroom Forest 是一个用 Python/PySide6 做的透明桌面小玩具：彩色水彩蘑菇会从屏幕各处缓慢长出，有时单棵、有时成簇，随时间逐渐铺满屏幕；造型取材自多种真实蘑菇（圆伞菇、鸡油菌、平菇、香菇、金针菇、牛肝菌、墨汁鬼伞、羊肚菌等；不含毒蝇伞形态）。点击蘑菇后，它会变成上升泡泡，并浮现一句黑色加粗花体、显示至少 3 秒的温柔英文营养小低语。它不是医学建议，只是一点日常营养常识与桌面陪伴感。安全提醒：请勿食用任何来源不明或无法识别的蘑菇；请在正规渠道购买野生菌；如果进食蘑菇后出现任何不适，请立即就医，以免耽搁病情。

英文可用：

> Tiny Mushroom Forest is a gentle transparent desktop toy built with Python and PySide6. Watercolor-style mushrooms slowly grow across your screen — sometimes one at a time, sometimes in small clusters — and can gradually fill the whole screen over time. Their shapes are inspired by real fungi (plain button-style rounded caps, chanterelle, oyster, shiitake, enoki, porcini, inky cap, morel, and more), while intentionally excluding fly agaric / amanita forms. When clicked, a mushroom dissolves into rising bubbles with a short comforting nutrition-themed whisper rendered in black, bold, cursive script and shown for at least 3 seconds. It is not medical advice — just everyday nutrition basics wrapped in a cozy desktop companion. Safety warning: do not eat any mushroom from an unknown source or any mushroom you cannot confidently identify; buy wild mushrooms only through reputable channels; if you feel unwell after eating mushrooms, seek medical attention immediately to avoid delaying care.

## 造型安全规则（禁止毒蝇伞形态）

- 不要加入、恢复或宣传 `amanita` / fly agaric / 毒蝇伞 / 红帽白点等强识别性有毒蘑菇形态，避免给使用者造成食用或识别联想。
- 普通圆帽造型必须保持无白点、无“毒蝇伞标志性白色疣点”；水彩颗粒只能作为低透明度纸面纹理。
- README / SKILL / 对外介绍中不得再把毒蝇伞列为参考形态；若需要说明造型来源，写“圆伞菇、鸡油菌、平菇、香菇、金针菇、牛肝菌、墨汁鬼伞、羊肚菌等”。
- 此项目不是蘑菇识别指南；安全警示必须保留。

## 蘑菇食用安全警示（介绍页必须保留）

- 中文：请勿食用任何来源不明或无法识别的蘑菇。请在正规渠道购买野生菌。如果进食蘑菇后出现任何不适，请立即就医，以免耽搁病情。
- English: Do not eat any mushroom from an unknown source or any mushroom you cannot confidently identify. Please buy wild mushrooms only through reputable channels. If you feel unwell after eating mushrooms, seek medical attention immediately to avoid delaying care.
- 这是项目介绍中的安全提示，不是营养泡泡低语；不要把它改写成玩笑、诗句或降低严肃性。

## 营养泡泡低语安全规则

`whispers.py` 里的短句必须遵守：

1. 只写主流日常营养学常识：水、膳食纤维、全谷物、蛋白质、彩色蔬果、钙、坚果、酸奶、燕麦、豆类等。
2. 语气温柔、诗意、短句化；适合花体英文浮在泡泡旁边。
3. 不写医疗建议，不写疾病治疗，不写排毒，不写减肥，不写“提高免疫力”等容易过度承诺的话。
4. 不写具体文献、年份、指南名；这是桌面玩具，不是医学科普图或临床建议。
5. 新增短句后，至少检查是否含以下风险词：`detox`, `cleanse`, `cure`, `heal`, `disease`, `diagnos`, `treat`, `weight loss`, `lose weight`, `fat burn`, `calorie`, `diet`, `slim`, `immunity`, `immune`, `toxin`, `metabolism`, `supplement`, `remedy`, `prevent`, `lower your`, `reduce risk`。

安全示例：

- `A glass of water is a quiet kindness.`
- `Fiber feeds the garden within.`
- `Whole grains offer steady energy.`
- `Protein helps the body mend softly.`
- `Colorful plants bring gentle micronutrients.`

避免示例：

- `This mushroom cures anxiety.`
- `Detox your body tonight.`
- `Lose weight with one magic bite.`
- `Boost immunity instantly.`

## 修改与验证流程

修改代码后，至少运行：

```bash
python3 -m py_compile main.py mushroom.py whispers.py
```

如环境可用，建议再做 Qt offscreen smoke test：

- `QT_QPA_PLATFORM=offscreen`
- 检查 `mushroom.SHAPES` 里每个造型变体 `Mushroom.draw()` 都不报错。
- 检查 `Mushroom.pop()` 后有 bubbles 与 whisper。
- 检查 `Mushroom.draw()` 在 pop + whisper 的多个进度点不报错。
- 检查 `bounding_rect()` / `contains()` 覆盖高/宽造型（inkcap、morel、enoki、oyster 等）的轮廓，文字不会被窗口 mask 裁剪。
- 检查低语时长：`WHISPER_SECONDS >= 3`，且不透明保持窗口 `WHISPER_SECONDS * (1 - WHISPER_FADE_TAIL) >= 3`；低语字体 `bold` 且 `Cursive`，墨色为纯黑。
- 检查 `Mushroom.is_dead` 在低语窗口结束前为 False（蘑菇不会被提前回收）。
- 检查 overlay 的 `max_mushrooms` 足够大、`add_mushroom()` 单棵生长、`_spawn_cluster()` 成簇生长且超上限会回收最早的一朵。
- 检查短句列表长度、空值、禁词。

## 贡献 / GitHub 操作纪律

若你正在替王润圆维护这个仓库：

1. 默认使用 GitHub 账号 `9s5bz2jvd2-lang`，不要顺手用其他账号。
2. 在 push / PR / merge 前显式确认：

```bash
gh api user --jq .login
```

输出必须是：

```text
9s5bz2jvd2-lang
```

3. 不要读取、打印、提交 token / password / secret / API key。
4. 默认走 PR；只有用户明确说“直接 merge / merge / 继续”且上下文明确指向该 PR 时，才合并。
5. 合并前确认 PR 的 author、head branch、base branch、mergeable 状态。

## 维护提示

- `main.py`：窗口、托盘、输入 mask、蘑菇生命周期调度；`_spawn_then_reschedule` 决定单棵/成簇，`_spawn_cluster` 负责错峰、自然散布的成簇生长，`max_mushrooms` 控制铺满屏幕的容量上限。
- `mushroom.py`：蘑菇绘制、水彩风格、点击检测、泡泡、低语绘制。造型变体见模块级 `SHAPES`（禁止加入 `amanita` / fly agaric / 毒蝇伞白点红帽形态），每个 `_cap_*` 方法画一种帽形，`_stem_proportions` / `_silhouette_extent` 控制不同造型的茎比例与包围盒。低语样式/时长由 `WHISPER_SECONDS`、`WHISPER_FADE_TAIL`、`_whisper_font`、`_draw_whisper` 决定（黑、粗、花体、显示≥3 秒且窗口内不透明）。
- `whispers.py`：营养主题低语短句库。
- `README.md`：面向人类的介绍、运行方式、制作人信息。
- `SKILL.md`：面向 LingTai/Agent 的标准调用说明；更新项目能力时同步维护，并同步复制到本地与共享技能目录（见下）。

## 技能同步路径

更新仓库 `SKILL.md` 后，需同步复制到以下两处，确保本地/共享的所有 agent 都能调用最新技能：

- 本地：`.../mimo-2-5-pro/.library/custom/tiny-mushroom-forest/SKILL.md`
- 共享：`.../.lingtai/.library_shared/tiny-mushroom-forest/SKILL.md`

两份副本必须保留有效 YAML frontmatter：`name: tiny-mushroom-forest` 与触发词丰富的 `description`。
