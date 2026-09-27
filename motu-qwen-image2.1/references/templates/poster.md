# 海报 / 广告设计 — poster

**何时用**：品牌海报、产品广告、活动视觉、宣传页。**画面文字是核心交付物**——
这正是 Qwen 2.1 的最强项（中英文标题、副文案实测全对），文字多的海报优先用
本 skill 而不是 z-image。纯拉丁字体字形设计仍可考虑 motu-ideogram4。

这是最容易因 prompt 不严谨而失败的类型：文字必须**逐字引用 + 写明位置与字体
气质**，并显式排除额外文字。

## 填充清单

| 字段 | 设计要点 |
|---|---|
| 任务 | 什么品牌/产品的什么海报 |
| 核心主体 | 产品/人物（第一视觉） |
| 视觉主题 | 未来科技/高级奢华/自然/年轻/专业 |
| 构图 | 中心/对角线/三分法；主体位置；留白比例给文字（~30%） |
| 视觉层级 | 第一视觉→第二视觉→第三视觉 |
| 文字 | 主标题/副标题/按钮文案——**逐字**，引号 |
| 排版 | 标题在哪、副标题在哪、按钮在哪；字体气质 |
| 背景 | 具体背景元素 |
| 色彩 | 主色/辅色/强调色 |
| 禁止 | 乱码、错误拼写、额外文字、重复文字、Logo 变形、元素拥挤 |

## Qwen 散文骨架

```text
[Task statement]. A commercial poster for [brand/product], built around [visual theme].
[Core subject: what it is, where it sits in the frame, how large].
The background is [specific background], kept quiet so the subject leads.
[Visual hierarchy: the eye goes first to ..., then ..., then ...].
Large headline text "[EXACT TEXT]" [position] in [font style], with smaller subline text "[EXACT TEXT]" [position] in [font style], and [a button / badge reading "[EXACT TEXT]"] [position]. The text must be spelled exactly as written, in [modern, clean, premium] typography with clear hierarchy, no extra words added.
About thirty percent of the frame is reserved as clean negative space for the type.
[Palette: primary, secondary, accent], [mood] in feel.
Premium advertising design with strong art direction, professional typography and clean layout.
Absolutely no other text, no misspelling, no garbled characters, no repeated words, no distorted logo, no cluttered elements, no watermark.
```

## 填写要点

- 文字三保险：逐字引号 + 位置 + 字体气质，负面再排一次 `no other text`。
  中文文字是本 workflow 的强项，但**保持简短**——主标题 + 一行副文案最稳，
  长段落正文仍易错字。
- 主题词（高级/年轻）要落到可画的字体与配色事实上：高级 = serif 大字标 +
  米白大留白；年轻 = 粗黑体 + 高饱和撞色。
- 留白比例显式写（`about thirty percent clean negative space`），不写这句
  文字常挤到主体。
- 品牌真实 Logo 画不准——写「badge 形状 + 品牌名文字」比写「我的 Logo」可靠。

## 示例（完整可直接提交，实测通过）

```text
A commercial poster for a Chinese tea shop, built around warm minimalist naturalness. A stoneware teacup with green tea sits on a light wooden table in the lower half of the frame, soft morning light from the left, blurred tea leaves in the background. The eye goes first to the headline, then to the teacup, then to the gentle depth of leaves behind. Large headline text "秋日茶集" in elegant serif Chinese calligraphy at the top center, with smaller subline text "手作 · 限定 · 每日鲜泡" beneath it in thin spaced sans-serif. The text must be spelled exactly as written, in premium editorial typography with clear hierarchy, no extra words added. Generous negative space surrounds the type. The palette is warm beige and deep green, quiet and inviting in feel. Premium advertising design with strong art direction, professional typography and clean layout. Absolutely no other text, no misspelling, no garbled characters, no repeated words, no distorted logo, no cluttered elements, no watermark, no people.
```

此示例为实测 prompt（1024×1536 输出）：主标题四字与副行九字（含间隔号）全部
正确，宋体衬线气质到位。
