# 书籍 / 专辑封面 — bookcover

**何时用**：书封、专辑封面、播客封面、课程封面、报告封面。**文字是交付物的
一半**（书名/作者/专辑名逐字渲染）——Qwen 中英文文字渲染的主场之一。商业活动
海报用 [poster.md](poster.md)，纯图形 Logo 用 [logo.md](logo.md)。

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

## Qwen 散文骨架

```text
[Task statement]. A [book / album / podcast] cover for a [genre] title, designed around [visual metaphor].
[Main visual: subject, rendering, where it sits], kept clear of the [top third / center band] reserved for the title.
The title text "[EXACT TITLE]" sits [position] in [font style], with "[EXACT AUTHOR / ARTIST NAME]" in smaller type [position]. All text is spelled exactly as written, cleanly typeset with strong hierarchy and no extra words.
[Background treatment: texture, gradient, scene depth].
The palette holds [colors] matching the [genre] register, the mood [adjective].
Professional cover design with confident art direction and print-ready composition.
Absolutely no other text, no misspelling, no garbled characters, no repeated words, no watermark.
```

## 填写要点

- 封面文字极简：主标题 + 一个署名是甜点位；腰封文案/简介文字不要进生图
  （留给排版工具）。
- 字体气质按品类锁：文学 serif、科技几何无衬线、儿童圆润手写——写成英文
  描述（`an elegant high-contrast serif`）。
- 视觉避开文字区显式写（`kept clear of the top third reserved for the title`），
  否则主体顶到标题。
- 竖版封面用 portrait preset；播客/专辑可用 square。

## 示例（完整可直接提交）

```text
A book cover for a literary mystery novel, designed around the metaphor of a lighthouse beam swept by fog. The main visual is a minimalist white lighthouse on a dark rocky point seen from the sea, its single beam cutting a diagonal through layered fog, the lighthouse kept in the lower two thirds clear of the title band. The title text "雾中灯塔" sits across the upper third in an elegant high-contrast serif with wide letter spacing, with "林晚 著" in smaller type beneath it. All text is spelled exactly as written, cleanly typeset with strong hierarchy and no extra words. The background is a deep graded midnight blue dissolving to charcoal at the edges, with fine paper-grain texture. The palette holds midnight blue, fog gray and one warm beam-gold accent, the mood hushed and ominous. Professional cover design with confident art direction and print-ready composition. Absolutely no other text, no misspelling, no garbled characters, no repeated words, no watermark.
```
