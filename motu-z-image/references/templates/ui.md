# UI / App 界面设计稿 — ui

**何时用**：Web/App/Desktop 界面视觉稿、设计方向探索、落地页视觉概念。
注意：生图产出的是**视觉方向**，不是可交互、像素级的 UI 实现 —— 真实界面仍要
前端实现；结构/数据必须精确的界面看 [infographic.md](infographic.md) 的建议。

## 填充清单

| 字段 | 必答 |
|---|---|
| 任务 | Web / App / Desktop 哪种 |
| 产品与页面 | 名称 + Dashboard/Chat/Editor/Settings |
| 目标用户 | 谁 |
| 核心功能 | 2–3 个 |
| 布局 | sidebar + content / top nav / card layout；左中右各是什么 |
| 设计语言 | minimal / modern / professional / AI-native / clean / 高信息密度 |
| 视觉 | 背景/卡片/边框/圆角/阴影的具体样式 |
| 排版 | 标题明显、正文易读、层级清晰、间距统一 |
| 交互元素 | 按钮/输入框/导航的具体样式 |
| 禁止 | 无功能装饰组件、重复按钮、乱码 |

## Z-Image 骨架

```text
title: [产品][页面] UI, A clean [web/app] ui design for [产品] [页面].,
minimal, modern, professional, ai-native, clean,
[画布环境: presented straight-on on a neutral light background],
[配色: 背景色, 卡片色, 强调色],
[布局组: left sidebar navigation, central content area, right auxiliary panel],
[内容组: sidebar with icon-and-label nav items, central dashboard with stat cards and a line chart, right panel with activity list],
[设计语言组: high information density with generous whitespace, consistent 8px spacing grid],
[视觉组: soft white card surfaces, hairline borders, 12px corner radius, subtle layered shadows],
[排版组: clear typographic hierarchy, prominent page title, readable body text],
[交互组: one primary accent button, outlined secondary buttons, clean search input],
straight-on screen view, full interface visible, centered,
flat crisp interface rendering, Even Diffused Lighting, no harsh reflections on screen, intensity: uniform,
none, flat render only,
clean, precise, modern,
product ui design, professional interface design,
[调色: 轻或深色模式, contrast: clear, saturation: restrained],
[调子词],
[叙事句],
[情绪词],
consistent spacing and hierarchy, no duplicated buttons, no broken components,
no garbled placeholder text, no decorative non-functional elements, no watermark
```

## 填写要点

- 布局三区（左/中/右）各一句说清放什么 —— 这是 UI 稿成败的核心字段。
- `straight-on screen view` + `full interface visible` 保证界面完整不透视变形。
- 生图界面里的「文字」必然是假字：声明 `no garbled placeholder text` 能减轻，
  不能根除；真实 UI 用前端实现。
- 深浅模式显式选一个写进调色组。

## 示例（完整可直接提交）

```text
title: Analytics Dashboard UI, A clean web ui design for a saas analytics dashboard., minimal, modern, professional, ai-native, clean, presented straight-on on a neutral light gray background, soft off-white canvas, white card surfaces, vivid indigo accent, left sidebar navigation, central content area, right auxiliary panel, sidebar with icon-and-label nav items and a workspace switcher at top, central dashboard with four stat cards above a large line chart and a data table below, right panel with a scrollable activity feed and filter chips, high information density with generous whitespace, consistent 8px spacing grid, soft white card surfaces, hairline borders, 12px corner radius, subtle layered shadows, clear typographic hierarchy, prominent page title, readable body text, one primary indigo button, outlined secondary buttons, clean search input in the top bar, straight-on screen view, full interface visible, centered, flat crisp interface rendering, Even Diffused Lighting, no harsh reflections on screen, intensity: uniform, none, flat render only, clean, precise, modern, product ui design, professional interface design, light mode, contrast: clear, saturation: restrained with vivid accent, calm and organized, quietly confident, Every metric finds its place without noise., clarity and control, effortless overview, consistent spacing and hierarchy, no duplicated buttons, no broken components, no garbled placeholder text, no decorative non-functional elements, no watermark
```
