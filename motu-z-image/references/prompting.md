# Z-Image Turbo 提示词编写指南

来源：motu 平台 `z_image_turbo_2k` 工作流的官方默认示例 prompt（最权威的风格
样板）。它是一个**结构化逗号分组**格式，本 skill 的所有模板
（`references/templates/`）都已按该格式写好 —— 写 prompt 时优先模仿它们的结构。

## 核心原则

1. **先定义「画什么」，再定义「怎么画」，最后定义「不要画什么」。**
   固定顺序：任务目标 → 主体 → 主体特征 → 动作/状态 → 场景 → 构图 → 空间关系 →
   视觉风格 → 材质细节 → 光线 → 色彩 → 镜头 → 画质 → 文字 → 一致性 → 负面约束。
2. **写事实关系，不写抽象评价。** 模型理解「左侧落地窗、中央 8 人长桌、自然光从
   左侧进入」，不理解「高级、震撼、未来感」。形容词只做调味，不做主菜。
3. **约束越明确越好，而不是越长越好。** 每个从句回答一个具体问题；删掉任何不
   改变画面的话。
4. **用英文写正文。** 官方示例全是英文；镜头、材质、灯光词汇的英文覆盖更好。
   需要渲染的中文文字仍然用引号原样保留。

❌ `一个非常高级、漂亮、震撼、未来感、科技感的办公室。`

✓ `title: Modern AI Office, A modern AI company office in open layout., focused, calm,
professional, …, central 8-person long table, floor-to-ceiling glass wall on the left,
light gray wall with a large horizontal display on the right, dark walnut tabletop,
black metal legs, natural light entering from the left, …`

## Z-Image 结构化提示词格式

官方示例 prompt 的形态：**一整段、逗号分隔的「字段组」序列**，每组是一个语义单元
（一个名词短语或 `key: value` 属性），按固定的大致顺序推进。它不是 JSON，也不需要
换行 —— 就是一串按序排列的逗号短语。`title:` 是唯一显式命名的字段，永远在最前。

### 字段组顺序（骨架）

| # | 字段组 | 写什么 | 示例（人像） |
|---|---|---|---|
| 1 | `title:` | 3–6 词短标题，概括整张图 | `title: Minimal Luxury Beauty Portrait` |
| 2 | 一句话总述 | 这是一张什么图（媒介 + 主体 + 场景） | `A modern luxury beauty portrait featuring clean makeup, soft lighting, and a natural studio setting.` |
| 3 | 氛围关键词 | 4–6 个风格/情绪词 | `airy, bright, elegant, modern luxury, beauty editorial` |
| 4 | 环境 | 地点 + 空间特征 | `natural light studio with large windows` |
| 5 | 道具/背景元素 | 环境里的具体物件，逐个列 | `neutral light gray backdrop …, minimalist stool, small vase with white flowers` |
| 6 | 环境氛围 | 2–4 个场景气质词 | `clean, bright, and luxurious` |
| 7 | 配色 | 2–3 主色 + 1 强调色 | `soft white, light gray, red accent (lip color)` |
| 8 | 主体身份 | 是什么/是谁：类别、性别年龄、族裔、体态、气质 | `human, female, age range: 20-25, East Asian, refined features, slim, elegant` |
| 9+ | 主体细节组（按模板展开） | 人物：姿势 → 脸型五官 → 表情视线 → 唇/胡须等细部 → 发型发色 → 妆容皮肤 → 服装配饰。产品：结构清单 → 状态 → 摆放。场景：前景 → 中景 → 背景 → 天气 | `seated on stool, slightly turned to camera …` |
| 10 | 相机 | 画幅、焦段、镜头类型、光圈、ISO、快门、白平衡 | `full_frame, 85mm, prime, f/2.0, ISO 100, shutter speed: 1/160, white balance: 5500` |
| 11 | 景别/构图 | 景别、画幅方向、机位高度、主体位置、对焦点 | `close-up portrait, vertical, eye-level, subject centered with slight headroom, eyes (nearest eye sharp)` |
| 12 | 景深 | 深浅 + 背景处理 | `shallow, softly blurred background` |
| 13 | 主光 | 灯光名称 + 光源 + 柔光方式 + `position:` + `intensity:` | `Soft Window Light, natural window light, sheer white curtain as diffusion, position: camera left, 45 degrees, intensity: soft and even` |
| 14 | 辅光/轮廓光 | 补光设备 + `ratio:` + 位置 + 作用 | `white bounce card, ratio: 1:2 (gentle shadows), position: camera right, subtle hair glow for separation` |
| 15 | 光线氛围 | 2–3 个光感词 | `bright and airy, soft, diffused` |
| 16 | 整体风格 | 一句风格定位 | `clean luxury editorial` |
| 17 | 调色 | 色温倾向 + `contrast:` + 过渡 + `saturation:` + 关键色调 | `neutral with slight warm bias, contrast: medium, soft transitions, saturation: moderate, natural skin tones with bold red lips` |
| 18 | 调色氛围 | 2 个调子词 | `clean and bright, soft and lifted` |
| 19 | 叙事收尾句 | 一句话点出画面讲述的感受/故事 | `She embodies modern elegance and confidence, with a timeless beauty that draws you in.` |
| 20 | 情绪关键词 | 2 个短语收束 | `luxury and poise, captivated by her refined beauty` |

非人物模板沿用同一条脊柱（title → 总述 → 关键词 → 环境 → 道具 → 配色 → 主体与
细节 → 相机 → 构图 → 景深 → 灯光 → 风格 → 调色 → 叙事句 → 情绪词），只是第 8/9
组换成该领域的主体细节组。每个模板文件里都已给出对应的骨架和完整示例。

### 写法规则

- 逗号是组分隔符；组内并列用逗号连写也可以，但**一个组只干一件事**。
- 属性写成 `key: value`（`position: camera left`、`age range: 20-25`、`ratio: 1:2`）。
- 有画面文字时，文字放进双引号并写明位置与字体气质：
  `headline text "AUTUMN SALE" across the top in bold condensed sans-serif`。屏幕文字
  保持简短（一个标题、3–5 个词），长文案容易出错字。
- 负面约束没有独立字段 —— 用肯定句排除：`empty background with no people, no text,
  no watermark`，放在靠近结尾处。
- 全文 ≤ 6000 字符；`title:` 之后正常大小写，属性值小写开头即可。
- 种子复现：同 `seed` + 同 prompt → 同族结果。迭代时锁 seed 只改 prompt，能看清
  改动效果；要多样性就换 seed。

## 八维度自检（提交前必过）

任何 prompt 提交前，逐项确认已回答：

| 维度 | 要回答的问题 | 对应字段组 |
|---|---|---|
| Subject | 画什么？ | 总述 + 主体身份 |
| Identity | 它长什么样？（不可变特征） | 主体细节组 |
| Action | 它在做什么/什么状态？ | 姿势/状态组 |
| Environment | 在哪里？什么时间天气？ | 环境 + 道具 |
| Composition | 怎么摆？什么画幅景别？ | 构图 + 景深 |
| Lighting | 光从哪里来？什么性质？ | 主光 + 辅光 |
| Style | 什么视觉语言/媒介？ | 关键词 + 风格 + 调色 |
| Constraint | 什么绝对不能出现？ | 负面约束 |

八项都有明确答案、画幅与用途匹配（竖屏海报 → portrait、横幅头图 → banner/
landscape、方图社媒 → square）、画面文字在引号内 —— 才提交。

## 单图工作流：意图 → 模板 → 填充 → 自审 → 自动提交

1. **判意图。** 从用户需求识别生成意图（人物？产品？海报？场景？…），拿不准时
   按 `references/templates/index.md` 的路由表匹配；一个需求混合多个意图
   （「一套 3 张：产品图 + 场景图 + 海报」）就拆成多个单图任务。
2. **选模板。** 读对应的 `references/templates/<intent>.md`，拿到该意图的填充清单、
   骨架和示例；具体词条（光线/相机/风格/色彩/材质）从 `references/vocabulary.md`
   取。
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
