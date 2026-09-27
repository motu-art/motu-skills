# 书籍 / 专辑封面 — bookcover

**何时用**：书封、专辑封面、播客封面、课程封面、报告封面。文字是交付物的
一半（书名/作者/专辑名）——Z-Image 可渲染**短**引号文字（拉丁字母最稳，
中文短标题可用；长中文文案建议转 motu-qwen-image2-1）。商业活动海报用
[poster.md](poster.md)，纯图形 Logo 用 [logo.md](logo.md)。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 品类 | 书（小说/科技/悬疑/儿童）/ 专辑 / 播客 / 课程 |
| 标题 | **逐字**（引号）+ 位置 + 字体气质 |
| 副文字 | 作者名/专辑人名/期号——逐字 + 位置 |
| 类型气质 | 文学/科技/悬疑/温暖/复古——决定视觉与字体 |
| 视觉隐喻 | 一个承载主题的意象（悬疑=剪影+雾；科技=几何光） |
| 构图 | 文字区预留（上 1/3 或中央）；主体避开文字区 |
| 色彩 | 主色/辅色 + 类型化配色（悬疑深蓝黑、儿童明快） |
| 字体气质 | serif 文学 / 无衬线现代 / 手写温暖 / 粗黑标题感 |
| 禁止 | 乱码、错字、额外文字、重复文字、水印 |

## Z-Image 骨架

```text
title: [书名], A book cover design for a [品类] title, designed around [视觉隐喻].,
[4-6 氛围词: hushed, ominous, literary, elegant …],
[主视觉: minimalist white lighthouse on a dark rocky point, single beam cutting a diagonal through fog, lower two thirds],
[文字: headline text "[EXACT TITLE]" across the upper third in elegant high-contrast serif with wide letter spacing, subline text "[EXACT AUTHOR]" beneath it in smaller type],
[背景处理: deep graded midnight blue dissolving to charcoal, fine paper-grain texture],
[配色: midnight blue, fog gray, warm beam-gold accent],
[构图: title band upper third, visual kept clear of the type, print-ready margins],
book cover design, confident art direction, professional typography, clean hierarchy,
[调色: deep blues, contrast: medium, saturation: low-moderate],
[调子词: hushed, ominous],
no other text, no misspelling, no garbled characters, no repeated words, no watermark
```

## 填写要点

- 封面文字极简：主标题 + 一个署名是甜点位；腰封文案/简介文字不要进生图
  （留给排版工具）。
- 中文标题 ≤ 6 字且逐字引号；长中文或中英混排 → 转 motu-qwen-image2-1。
- 字体气质按品类锁：文学 serif、科技几何无衬线、儿童圆润手写——写成英文
  描述（`elegant high-contrast serif`）。
- 视觉避开文字区显式写（`kept clear of the top third reserved for the title`），
  否则主体顶到标题。

## 示例（完整可直接提交）

```text
title: The Lighthouse in Fog, A book cover design for a literary mystery novel, designed around a lighthouse beam swept by fog., hushed, ominous, literary, elegant, restrained, minimalist white lighthouse on a dark rocky point seen from the sea, its single beam cutting a diagonal through layered fog, occupying the lower two thirds, headline text "THE LIGHTHOUSE" across the upper third in elegant high-contrast serif with wide letter spacing, subline text "a novel by E. Winters" beneath it in smaller spaced type, deep graded midnight blue dissolving to charcoal at the edges with fine paper-grain texture, midnight blue, fog gray, warm beam-gold accent, title band in upper third, visual kept clear of the type, print-ready margins, book cover design, confident art direction, professional typography, clean hierarchy, deep blues, contrast: medium, saturation: low-moderate, hushed, ominous, no other text, no misspelling, no garbled characters, no repeated words, no watermark
```
