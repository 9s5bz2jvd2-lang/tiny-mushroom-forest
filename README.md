# 🍄 Tiny Mushroom Forest

中文 | [English](#english)

Tiny Mushroom Forest 是一片会偷偷住进你屏幕里的小蘑菇森林，也是一枚轻量的桌面生活美学小玩具 / cozy mini game。它很轻、很安静、透明得像一层晨雾：每隔几秒，就会有小蘑菇从桌面各处悄悄冒头——有时是单独一朵，有时是带着轻微错峰、自然散开的一小簇，像在说：今天也辛苦啦，给你长一点点可爱。

蘑菇会随时间慢慢变多，逐渐铺满屏幕；当数量达到上限时，最早的旧朋友会轻轻让位给新朋友。造型取材自多种真实蘑菇——圆伞菇、鸡油菌、平菇、香菇、金针菇、牛肝菌、墨汁鬼伞、羊肚菌……全部由 `QPainter` 现场手绘，不需要任何图片素材。适合搜索「桌面美化」「生活美学」「治愈小游戏」「桌面小玩具」「cozy game」「desktop toy」的人。

> **安全警示 / Safety warning**  
> 请勿食用任何来源不明或无法识别的蘑菇。请在正规渠道购买野生菌。如果进食蘑菇后出现任何不适，请立即就医，以免耽搁病情。  
> Do not eat any mushroom from an unknown source or any mushroom you cannot confidently identify. Please buy wild mushrooms only through reputable channels. If you feel unwell after eating mushrooms, seek medical attention immediately to avoid delaying care.

> 给忙碌的桌面种一小片不会打扰人的森林。

## ✨ 功能

- Python 3.11+ / PySide6
- 桌面生活美学 / desktop toy / cozy mini game
- 透明、无边框、置顶 overlay
- 蘑菇缓慢出现：有时单棵，有时成簇（成簇成员带轻微错峰、自然散布在一个中心附近）
- 随时间逐渐变多，可铺满屏幕；达到上限后回收最早的一朵，性能可控
- 多种取材自真实蘑菇的造型变体：圆伞菇（简洁圆帽、无白点）、鸡油菌（漏斗）、平菇（侧生扇形）、香菇（低褐凸帽）、金针菇（细高小帽）、牛肝菌（粗壮宽帽）、墨汁鬼伞（高钟形）、羊肚菌（蜂窝锥帽）
- 红、橙、黄、绿、蓝、紫、粉随机颜色
- 半透明水彩 / 手绘风格的蘑菇笔触
- 从底部向上生长的 2 秒生长动画（10% → 100%）
- 点一下蘑菇，它会化成一串上升的小气泡 🫧
- 气泡升起时，会浮现一句**黑色、加粗、花体（cursive）、完全不透明**的营养主题暖心悄悄话（如「A glass of water is a quiet kindness.」），并**至少显示 3 秒**后才轻轻淡出
  - 文案取材于大众营养常识（水、纤维、全谷、蛋白质、五彩蔬果等），只是温柔的小提醒；不含任何医疗、疾病、排毒或减肥相关说法
- `ESC` 退出，系统托盘菜单也可退出
- 托盘菜单可手动 `Grow one mushroom`
- 蘑菇完全由代码绘制，无图片依赖

## 🚀 运行

```bash
git clone https://github.com/9s5bz2jvd2-lang/tiny-mushroom-forest.git
cd tiny-mushroom-forest
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

> Windows 用户可将激活命令替换为：`.venv\\Scripts\\activate`

## 🍄 介绍词（中文）

> 一片会悄悄长在桌面上的小蘑菇森林。
> 它不会吵你，也不会挡住你，只是在屏幕角落慢慢冒出彩色小蘑菇，陪你工作、发呆、写代码。
> 每一朵蘑菇都像一个安静的小朋友：轻轻出现，乖乖待着，把忙碌的电脑变成一点点温柔的森林。
> 安全提醒：请勿食用任何来源不明或无法识别的蘑菇；请在正规渠道购买野生菌；如果进食蘑菇后出现任何不适，请立即就医，以免耽搁病情。

## 📁 文件结构

```text
TinyMushroomForest/
├── main.py
├── mushroom.py
├── whispers.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 📴 退出

按 `ESC`，或在系统托盘图标菜单中选择 `Exit`。

## License

MIT

---

<a id="english"></a>

# 🍄 Tiny Mushroom Forest

Tiny Mushroom Forest is a tiny mushroom woodland that quietly moves into your desktop — a lightweight desktop toy, cozy mini game, and little piece of everyday life aesthetics. It is transparent and gentle, like a layer of morning mist. Every few seconds, colorful little mushrooms shyly appear across your screen — sometimes a single one, sometimes a small, gently staggered cluster — as if whispering: you worked hard today; here is a little bit of cute. Over time the forest slowly fills in and can cover the whole screen.

> **Safety warning / 安全警示**  
> Do not eat any mushroom from an unknown source or any mushroom you cannot confidently identify. Please buy wild mushrooms only through reputable channels. If you feel unwell after eating mushrooms, seek medical attention immediately to avoid delaying care.  
> 请勿食用任何来源不明或无法识别的蘑菇。请在正规渠道购买野生菌。如果进食蘑菇后出现任何不适，请立即就医，以免耽搁病情。

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

Created with LingTai.

Mushrooms keep appearing and the forest gradually grows denser; once it reaches its capacity, the oldest friends softly step aside for new ones. Their silhouettes are inspired by real fungi — button-style rounded caps, chanterelle, oyster, shiitake, enoki, porcini, inky cap, morel, and more. Every mushroom is drawn live with `QPainter`, with no image assets required. Search-friendly words: desktop aesthetics, cozy game, desktop toy, mushroom game, generative art, screen overlay.

> Plant a small, non-intrusive forest on your busy desktop.

## ✨ Features

- Python 3.11+ / PySide6
- Desktop aesthetics / desktop toy / cozy mini game
- Transparent, frameless, always-on-top overlay
- Mushrooms appear slowly — sometimes one at a time, sometimes in a small, gently staggered cluster scattered naturally around a center
- The forest can gradually fill the whole screen; once it hits its capacity, the oldest mushroom is reaped first to keep performance reasonable
- Several real-mushroom-inspired morphology variants: button-style rounded cap (plain, without white spots), chanterelle (funnel), oyster (side shelf), shiitake (low brown convex), enoki (slender cluster knob), porcini (stout broad cap), inky cap (tall bell), morel (pitted honeycomb cone)
- Random red, orange, yellow, green, blue, purple, and pink caps
- Soft, semi-transparent watercolor / hand-drawn mushroom strokes
- Bottom-to-top growth animation in 2 seconds (10% → 100%)
- Click a mushroom to dissolve it into a burst of rising bubbles 🫧
- As the bubbles rise, a short comforting nutrition-themed whisper appears in **black, bold, cursive script, fully opaque** (e.g. “A glass of water is a quiet kindness.”) and stays visible for **at least 3 seconds** before gently easing away
  - Whispers are inspired by mainstream, everyday nutrition basics (water, fiber, whole grains, protein, colorful plants, and a balanced plate). They are gentle notes only — no medical, disease, detox, or weight-loss claims.
- Press `ESC` to exit, or use the system tray menu
- Tray menu includes `Grow one mushroom`
- Fully drawn in code; no image files needed

## 🚀 Run

```bash
git clone https://github.com/9s5bz2jvd2-lang/tiny-mushroom-forest.git
cd tiny-mushroom-forest
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

On Windows, use `.venv\\Scripts\\activate` instead of the `source` command.

## 🍄 Introduction copy (English)

> A tiny mushroom forest that quietly grows on your desktop.
> It does not interrupt you or cover your work — it simply lets colorful little mushrooms appear in the corners of your screen, keeping you company while you work, think, or code.
> Each mushroom feels like a shy little friend: softly arriving, calmly staying, and turning a busy computer into a gentler place.
> Safety warning: do not eat any mushroom from an unknown source or any mushroom you cannot confidently identify; buy wild mushrooms only through reputable channels; if you feel unwell after eating mushrooms, seek medical attention immediately to avoid delaying care.

## 📴 Exit

Press `ESC`, or choose `Exit` from the system tray menu.

## License

MIT

<!-- Maintainer update: Runyuan Wang (9s5bz2jvd2-lang). -->

---

> **禁止抄袭商用，违者等同盗法，因果自负**
> **Plagiarism and commercial use prohibited. Violators shall be deemed as infringers of law and shall bear all consequences.**
>
> 公益开源项目，禁止商用 | Public welfare open-source project, commercial use prohibited
> License: CC BY-NC 4.0
