# Qwen Image 2.1 提示词编写指南

来源：motu 平台 `image_qwen_image_2_1_t2i` 工作流的官方默认示例 prompt（最权威的
风格样板）。它是一段**英文叙事散文**（natural-language prose）——完整句子、自然
段落，而不是 z-image 那种逗号字段组。本 skill 所有模板（`references/templates/`）
都已按散文格式写好，写 prompt 时优先模仿它们的结构。

## 核心原则

1. **先定义「画什么」，再定义「怎么画」，最后定义「不要画什么」。** 内容覆盖
   固定顺序：目标 → 主体 → 身份特征 → 动作/状态 → 环境 → 空间关系 → 构图 →
   视觉层级 → 风格 → 材质 → 光线 → 色彩 → 镜头 → 文字 → 一致性 → 负面约束。
   散文里相邻字段合并成句，不必一项一句。
2. **写事实关系，不写抽象评价。** 模型理解「a walnut conference table for eight
   in the center, floor-to-ceiling windows on the left, morning light entering
   from the left」，不理解「高级、震撼、未来感」。形容词只做调味，不做主菜。
3. **用完整英文句子，不用逗号碎片。** 每句话陈述一个可画的事实；句内可用冒号、
   破折号、分号展开细节（官方示例即如此）。
4. **用英文写正文。** 需要渲染在画面上的中文文字，用引号原样保留在句中。

❌ `一个非常高级、漂亮、震撼、未来感、科技感的办公室。`

✓ `A modern AI company office in open layout. A walnut conference table for
eight stands at the center with dark metal legs, floor-to-ceiling glass wall
on the left lets natural light enter from the left, and a large horizontal
display mounted on the light gray wall on the right shows a muted data
visualization. …`

## 散文格式与折叠规则

官方示例的形态：**一整段（或两三段）流畅英文**，5–9 句，按固定内容顺序推进，
以一句负面约束收尾。把模板的填充清单折叠成散文的规则：

- **相邻同域字段合并成一句。**「身份 + 服装 + 材质」写成一句：`She wears a
  high-necked structural dress tailored from heavyweight fabric featuring …`。
- **一个从句回答一个问题。** 光线一句（源 + 方向 + 性质 + 效果），背景一句
  （层次 + 元素），风格收效一句。
- **顺序即权重。** 越靠前的内容越被严格遵守；负面约束永远最后一句。
- **禁止 `key: value` 属性写法**（那是 z-image 的格式）；写成自然介词短语：
  `light from a large window on the left at 45 degrees, soft and even`。

### 散文骨架（通用）

```text
[A sentence of what this image is: medium + subject + scene].
[Subject identity and characteristics: age/gender/build/temperament, or category/material/structure].
[Subject action or state, attire and details: fabrics, textures, accessories layered expansion].
[Environment and background: foreground/midground/background or background element list].
[Spatial relationships and composition: subject position, framing, visual hierarchy, negative space].
[Lighting: source + direction + nature + effect on the subject].
[Lens and perspective: focal length, depth of field, camera position].
[Style and color: visual language, palette, overall mood and effect].
[On-image text (if any): quoted + position + font style].  ← can be merged into composition
[Absolute negatives: Absolutely no …, pure imagery only].
```

## 写法规则

- **画面文字**：放进双引号并写明位置与字体气质：
  `Large headline text "秋日茶集" in elegant serif Chinese calligraphy at the
  top center`。中文/英文文字渲染是本 workflow 的强项（实测中文标题 + 副行全对），
  但**保持简短**——一个主标题 + 一行副文案最稳，长段落正文仍易出错字。
- **负面约束没有独立字段**。标准收尾句（无文字画面用）：
  `Absolutely no text, no typography, no letters, no words, no numbers, no
  logos, no watermark, no captions, pure imagery only.`
  画面有指定文字时改写为排除其余：`Absolutely no other text, no watermark,
  no people.`
- 全文 ≤ 6000 字符；散文通常 600–1500 字符已足够，**写满事实比写满字符重要**。
- 种子复现：同 `seed` + 同 prompt → 同族结果。迭代时锁 seed 只改 prompt，能看清
  改动效果；要多样性就换 seed。

## 八维度自检（提交前必过）

任何 prompt 提交前，逐项确认已回答：

| 维度 | 要回答的问题 | 散文里落在哪 |
|---|---|---|
| Subject | 画什么？ | 第 1 句总述 |
| Identity | 它长什么样？（不可变特征） | 主体身份/特征句 |
| Action | 它在做什么/什么状态？ | 动作/状态句 |
| Environment | 在哪里？什么时间天气？ | 环境背景句 |
| Composition | 怎么摆？什么画幅景别？ | 空间构图句 + 请求的 width/height |
| Lighting | 光从哪里来？什么性质？ | 光线句 |
| Style | 什么视觉语言/媒介？ | 风格调色句 |
| Constraint | 什么绝对不能出现？ | 最后的 Absolutely no… 句 |

八项都有明确答案、画幅与用途匹配（竖屏海报 → portrait、横幅头图 → landscape/
banner、方图社媒 → square）、画面文字在引号内、负面收尾句在场 —— 才提交。

## 单图工作流：意图 → 模板 → 填充 → 自审 → 自动提交

1. **判意图。** 从用户需求识别生成意图（人物？产品？海报？场景？…），拿不准时
   按 `references/templates/index.md` 的路由表匹配；一个需求混合多个意图
   （「一套 3 张：产品图 + 场景图 + 海报」）就拆成多个单图任务。
2. **选模板。** 读对应的 `references/templates/<intent>.md`，拿到该意图的填充
   清单、散文骨架和示例；具体词条（光线/相机/风格/色彩/材质）从
   `references/vocabulary.md` 取，折叠进句子。
3. **填充。** 把用户给的信息填进骨架；模板要求的字段用户没说的，按模板默认值或
   合理设计补全 —— **宁可补全，不可留空**（留空 = 模型自由发挥 = 漂移）。清单是
   给 skill 的设计指引，**不是向用户提问的问卷**。
4. **自审。** 先跑机械 lint：`python3 scripts/prompt_check.py --prompt-file p.txt`
   （报错 → 修复 → 重审），再过八维度自检 + 画幅匹配 + 文字引号。逐句读一遍
   prompt：每句话是否都能在画面上落实？
5. **自动提交。** 审查通过即用脚本提交并等待下载——**不向用户确认**；完成后在
   报告里给出本张的本地文件路径、实际分辨率与所用完整 prompt（含设计假设）。

多图需求（套图、系列、一个需求的多个意图）**逐张走完 1–5**，每张独立设计、独立
自审、过审即提交 —— 不要复制一个 prompt 改两个字批量提交，也不要攒一批等用户
确认。角色/产品需要跨图一致时，按 `references/templates/series.md` 的 MASTER
锁定法先写固定描述块（自行设计，不请求确认），再逐张只改场景/动作/景别。

## batch_size 与逐张的区别

- `batch_size: 2–4`：**同一个 prompt** 的多个备选（同描述、不同随机种子方向）。
  适合「这个再给我 3 张挑一张」。
- 逐张操作：**每张有自己的定制 prompt**。适合内容不同的多图需求 —— 这是默认
  工作流，也是结果最大程度符合意图的关键。

尺寸 preset 表见 [SKILL.md](../SKILL.md) 参数一节。
