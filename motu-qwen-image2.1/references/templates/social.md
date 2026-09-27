# 社交媒体配图 — social

**何时用**：Instagram/小红书/公众号封面/Facebook/LinkedIn 配图、活动宣传图、
campaign 视觉。核心：**平台画幅 + 核心信息一眼懂**。文字较多时本 skill 的中文
渲染优势明显。

## 填充清单

| 字段 | 必答 |
|---|---|
| 平台 | Instagram（方图 1:1）/ 小红书（竖图 3:4）/ 封面横图 —— 决定画幅 |
| 内容主题 | 发什么内容 |
| 核心信息 | 用户看图后应立即理解的一句话 |
| 主体 | 什么主体、在画面什么位置 |
| 文字 | 主标题/副标题——逐字引号 + 位置 + 字体 |
| 风格 | 年轻/专业/高级/生活方式 |
| 视觉层级 | 主体 → 标题 → 辅助信息 → 品牌 |
| 背景 | 具体背景 |
| 禁止 | 额外文字、乱码、水印、元素拥挤 |

## Qwen 散文骨架

```text
[Platform + statement]. A [square / vertical] social media cover image about [topic], designed so the viewer instantly understands [core message].
[Subject: what it is, where it sits, rendered in what style].
[Background: specific environment or color field].
Bold headline text "[EXACT TEXT]" [position] in [font style], with smaller subline text "[EXACT TEXT]" [position], spelled exactly as written with clear hierarchy and no extra words.
[Visual hierarchy: subject first, headline second, supporting detail third].
[Palette and mood], [young / professional / premium / lifestyle] in style.
Social media campaign quality with commercial art direction and strong visual hierarchy.
Absolutely no other text, no misspelling, no garbled characters, no watermark, no cluttered elements.
```

## 填写要点

- 先定画幅再写 prompt：方图（square 1024/2048）/ 竖图 3:4（portrait）/ 横幅
  （banner），平台画幅错了内容再好也白费。
- 「一眼懂」= 主体大 + 标题短：中文主标题 ≤ 8 字最佳，副行一句话。
- 小红书风格高频元素：大字标题压在高对比主体上、手写体点缀、明亮撞色——
  把这些写成具体事实（字体气质 + 色名）。
- 品牌 Logo 位置留给后期叠加时，负面排掉所有 text。

## 示例（完整可直接提交）

```text
A vertical social media cover image for a Xiaohongshu post about autumn desk setups, designed so the viewer instantly understands a cozy seasonal workspace. A warm wooden desk fills the lower two thirds of the frame with a ceramic mug of hot tea sending up faint steam, an open notebook, a small amber reading lamp glowing, and a sprig of dried maple leaves laid beside the cup, rendered in bright lifestyle photography. The background is a soft warm-beige wall with gentle window light and shadow. Bold headline text "秋日书桌改造" across the upper fifth of the frame in friendly rounded Chinese sans-serif, with smaller subline text "5 个好物点亮秋天" beneath it in thin spaced type, spelled exactly as written with clear hierarchy and no extra words. The eye lands on the glowing lamp first, then the headline, then the steaming mug. The palette holds warm beige, amber and soft white, cozy and inviting, lifestyle style. Social media campaign quality with commercial art direction and strong visual hierarchy. Absolutely no other text, no misspelling, no garbled characters, no watermark, no cluttered elements, no people.
```
