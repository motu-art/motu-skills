# UI / App 界面生图 — ui

**何时用**：Web/App/Desktop 界面概念稿、设计探索、落地页视觉。要求布局层级
+ 间距系统一致。**注意**：这是概念图，不是可交付前端代码；真实 UI 用设计工具
+ 代码实现，本模板出的是「视觉方向稿」。

## 填充清单

| 字段 | 必答 |
|---|---|
| 任务 | Web / App / Desktop 的什么界面 |
| 产品 | 产品名称与定位 |
| 页面 | Dashboard / Chat / Editor / Settings |
| 目标用户 | 谁在用、关心什么 |
| 核心功能 | 2–3 个，决定界面内容 |
| 布局 | sidebar + content / 顶部导航 / 卡片流；左中右各放什么 |
| 设计语言 | minimal / modern / professional / AI-native / clean / 信息密度 |
| 视觉 | 背景/卡片/边框/圆角/阴影的取值 |
| 交互元素 | 按钮/输入框/导航的样子 |
| 文字 | 界面文案**逐字引用**（Qwen 强项，含中文）；克制数量 |
| 禁止 | 不可用的装饰组件、重复按钮、乱码 |

## Qwen 散文骨架

```text
[Task statement]. A clean UI concept design of a [page] screen for [product], a [positioning] tool for [target users].
The layout follows [sidebar + content / top navigation + card grid], with [left region], [center region], and [right region].
The header shows the product name "[EXACT NAME]" with [navigation items], and the main content presents [core function 1] and [core function 2].
UI text is rendered exactly as written: label "[EXACT TEXT]", button "[EXACT TEXT]", title "[EXACT TEXT]", in clear hierarchy with consistent spacing.
The visual system uses [background color] backgrounds, [card treatment], [border], [corner radius] and [shadow depth], every element aligned to a consistent grid.
Minimal, modern, professional, AI-native design language with clean high-information-density layout.
Absolutely no unusable decorative components, no duplicated buttons, no garbled text, no misspelling, no watermark.
```

## 填写要点

- UI 文案逐字引用且**数量克制**：一个产品名 + 3–6 个标签/按钮文案。全英文
  界面最稳；中文界面是本 skill 强项但每块文字都要引号点名。
- 布局句写三区各放什么（`a slim icon sidebar on the left, a conversation thread
  in the center, a context panel on the right`）——布局是 UI 稿的第一读物。
- 设计令牌取值化（`8-pixel corner radius, 1px borders at 8% opacity`）让「干净」
  可执行。
- 交付真实产品 → 此稿只做方向；结构精确的界面用 HTML/CSS 实现，素材图另出。

## 示例（完整可直接提交）

```text
A clean UI concept design of an analytics dashboard screen for "星析 DataLens", a data insight tool for growth teams. The layout follows a sidebar plus content structure, with a slim dark icon sidebar on the left, a wide content area in the center holding a KPI row and two charts, and a slim filter panel on the right. The header shows the product name "星析 DataLens" with navigation items, and the main content presents trend lines and a channel breakdown table. UI text is rendered exactly as written: label "本周活跃用户", button "新建看板", title "增长总览", in clear hierarchy with consistent spacing. The visual system uses a very dark slate background, slightly lighter cards with 1px borders at low opacity, an 8-pixel corner radius and soft shallow shadows, every element aligned to a consistent grid. Minimal, modern, professional, AI-native design language with clean high-information-density layout. Absolutely no unusable decorative components, no duplicated buttons, no garbled text, no misspelling, no watermark.
```
