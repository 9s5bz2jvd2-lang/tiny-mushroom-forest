---
name: tiny-mushroom-forest
description: |
  Tiny Mushroom Forest（蘑菇森林）桌面疗愈小玩具的标准调用技能。用户想安装、运行、演示、介绍、二次开发、维护、改 README/SKILL、添加水彩蘑菇、点击泡泡、营养泡泡低语、制作人简介，或想用 LingTai 做一个温柔桌面小应用/AI vibe coding 示例时使用。包含仓库地址、运行方式、功能边界、营养文案安全规则、贡献/PR 身份纪律与制作人中英双语简介。
version: 1.0.0
author: Wang Runyuan / LingTai
---

# Tiny Mushroom Forest（蘑菇森林）标准技能

## 何时调用

当用户提到以下任一需求时，调用本技能：

- “蘑菇森林 / Tiny Mushroom Forest / tiny-mushroom-forest”。
- 想安装、运行、演示这个桌面小玩具。
- 想做一个透明桌面 overlay / cozy desktop toy / PySide6 小应用。
- 想让蘑菇变水彩、半透明、从下往上生长、点击后变泡泡。
- 想修改或新增点击蘑菇后的英文营养泡泡低语。
- 想给该项目补 README、制作人介绍、LingTai attribution、发布说明或 GitHub PR。
- 想学习“AI vibe coding”如何从一个小而完整的项目开始。

## 项目事实

- GitHub 仓库：`https://github.com/9s5bz2jvd2-lang/tiny-mushroom-forest`
- 项目定位：一个温柔的桌面透明蘑菇森林小玩具；蘑菇会从屏幕边角长出，点击后化成上升泡泡，并出现一句简短、诗意、与主流营养学常识相关的英文低语。
- 技术栈：Python + PySide6 / Qt；绘制主要在 `main.py`、`mushroom.py`，营养低语在 `whispers.py`。
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

> Tiny Mushroom Forest 是一个用 Python/PySide6 做的透明桌面小玩具：彩色水彩蘑菇会从屏幕边角轻轻长出；点击蘑菇后，它会变成上升泡泡，并浮现一句温柔的英文营养小低语。它不是医学建议，只是一点日常营养常识与桌面陪伴感。

英文可用：

> Tiny Mushroom Forest is a gentle transparent desktop toy built with Python and PySide6. Watercolor-style mushrooms softly grow from the edges of your screen; when clicked, they dissolve into rising bubbles with a short comforting nutrition-themed whisper. It is not medical advice — just everyday nutrition basics wrapped in a cozy desktop companion.

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
- 检查 `Mushroom.pop()` 后有 bubbles 与 whisper。
- 检查 `Mushroom.draw()` 在 pop fade 的多个进度点不报错。
- 检查 `bounding_rect()` 足够大，文字不会被窗口 mask 裁剪。
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

- `main.py`：窗口、托盘、输入 mask、蘑菇生命周期调度。
- `mushroom.py`：蘑菇绘制、水彩风格、点击检测、泡泡、低语绘制。
- `whispers.py`：营养主题低语短句库。
- `README.md`：面向人类的介绍、运行方式、制作人信息。
- `SKILL.md`：面向 LingTai/Agent 的标准调用说明；更新项目能力时同步维护。
