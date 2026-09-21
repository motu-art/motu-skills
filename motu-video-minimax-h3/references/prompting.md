# MiniMax Hailuo 视频 Prompt 编写指南

来源：官方文档 <https://platform.minimaxi.com/docs/guides/video-prompt> 的思路 + motu 平台
五个工作流（t2v / i2v / ia2v / r2v / ra2v）的官方示例 prompt。后者是最权威的风格样板，
写 prompt 时优先模仿它们的结构。「五步导演法」（见下）提炼自官方 H3 提示词技能说明的
社区教程（模式选择 → 三字段结构 → 六要素镜头 → 一致性约束 → 声音分层），已映射到
motu 的五个工作流。

## 核心原则

1. **用英文写**。官方示例全是英文；英文 prompt 对镜头、材质、音频词汇的覆盖更好。
2. **写成拍摄方案（treatment），不是一句话描述**。模型能接受很长的 prompt（6000 字符，
   ra2v 8000），结构化、分镜头的描述显著优于一句话。
3. **时间轴与 duration 对齐**。分镜时间码必须覆盖且不超过你设置的 `duration`。
   5 秒放 2–3 个镜头，10 秒放 4–5 个；别在 5 秒里塞 8 个镜头。
4. **显式排除不想要的内容**。官方示例都以负面约束收尾
   （"No text, subtitles, logos or watermarks …"）。
5. **按五步导演法层层递进设计，每句话都要有明确职责**。prompt 不是越长越好；
   出片公式：**选对模式 → 锁定角色 → 拆解动作 → 设计镜头 → 分离声音**。
   给模型一句愿望，它只能自由发挥；给它一份可执行的导演方案，它才稳定出片。

## 五步导演法：层层递进的方案设计流程

H3 是一个集合导演、摄影、演员、录音和配乐于一体的 AI 剧组。写 prompt 就是给这份
剧组下可执行的拍摄方案 —— 按下面五步依次推进，不要跳步。

### 第一步：先选任务模式，别一上来就写提示词

判断公式：**没有素材 → 文生视频；有起点 → 首帧；有起点和终点 → 首尾帧；
只有结果 → 尾帧；需要同时参考角色、动作、风格或声音 → 多模态参考。**

映射到 motu 的五个工作流：

| 你手里有什么 | 模式 | motu 工作流 | prompt 的重点 |
|---|---|---|---|
| 只有文字 | 文生视频 | t2v | 自由度高，但人物/服装/场景最容易漂移；适合概念短片、创意测试、空镜氛围镜头 |
| 一张开场图 | 首帧图生视频 | i2v | 不是重新描写图片，而是：哪些视觉信息必须保持不变 + 接下来发生什么动作（人物转身/抬头/行走、海报动态化、产品展示、漫剧角色开口） |
| 开头 + 结尾两张图 | 首尾帧生视频 | r2v | 最重要的不是描述两张图，而是把「中间怎么变化」拆成连续动作（站立→拔剑、晴天→暴雨、盒子打开、便服→战甲） |
| 只有结尾图 | 尾帧生视频 | **ra2v（只传 `--image-end`）** | 反推动作路径，让最终构图精确落到参考图。例：尾帧是碎在地上的茶杯 → 手碰到杯沿→杯子倾斜→滑落桌面→撞击地面→碎片停止移动 |
| 图 / 视频 / 音频组合参考 | 多模态参考生成 | ra2v（组合图+音频）；口播用 ia2v | 角色图锁人物形象、动作视频约束表演、音频参考控制声音、场景图维持世界观、品牌素材保商品细节 |

### 第二步：把提示词拆成三个「剧组部门」

官方结构化格式包含三个核心字段：

| 字段 | 剧组角色 | 要写的内容 |
|---|---|---|
| `integrated_multimodal_description` | 导演 + 摄影指导的镜头脚本（主体） | 画面风格、景别与构图、人物身份、人物动作、镜头运动、对白或旁白、镜头切换时间、画面内可见文字、必须保持一致的内容；负面约束放在末尾 |
| `overall_soundscape` | 录音师的现场声音清单 | 风雨雷、脚步/呼吸/衣料摩擦、开门/拔剑/碰撞/碎裂、街道车厢市场等环境底噪、笑声喘息等非语言人声；**对白不要在这里重复**；1–4 句 |
| `non_diegetic_music` | 只有观众听得见、画中人物听不见的配乐 | 乐器、速度、节奏、音量动态变化、结束方式；**不要只写「悲伤的/紧张的/史诗感音乐」**——模型需要的是乐器与动态，不是抽象情绪；不需要配乐时写 `N/A`；1–3 句 |

✗ `non_diegetic_music: 悲伤的音乐。`
✓ `non_diegetic_music: 缓慢而稀疏的古琴音符，低音弦乐逐渐加入，人物拔剑时音量短暂增强，结尾迅速减弱。`

下面的「推荐结构」是同样内容的散文形态（官方示例 1–3 用的就是它），两种形态等价，
三字段格式是显式版本，推荐默认使用。

### 第三步：每个镜头都写清六件事

公式：**风格＋景别＋主体＋动作＋镜头运动＋声音**

- ✗ 「古装女孩在雨中抬头，唯美电影感」
- ✓ 「电影感真人画面，中景。身穿红色古装的年轻女子站在雨夜客栈门口，右手握住伞柄，
  缓慢抬头看向屋檐。镜头以较小幅度缓慢推进到她的脸部。雨水敲击瓦片，远处传来低沉雷声。」

字数没多多少，可执行程度完全不同。

**一个镜头只安排一种主要运镜**。推镜、摇镜、环绕、跟拍、变焦堆在句末会互相冲突；
运镜不是装饰，而是叙事 —— 按叙事目的选：

| 运镜 | 叙事目的 |
|---|---|
| 缓慢推进 push in (slowly) | 强调表情或关键物品 |
| 向后拉远 pull back / dolly out | 展示人物与环境关系 |
| 左右摇摄 pan / tilt | 揭示画面外的新信息 |
| 横向平移 truck / lateral tracking | 陪伴人物移动 |
| 跟随拍摄 follow shot | 表现奔跑、追逐或行走 |
| 环绕拍摄 orbit / arc shot | 强化人物登场或力量感 |
| 固定镜头 static / locked-off | 突出表演和构图稳定性 |

运镜写成自然动作句（"the camera pushes in with small amplitude at slow speed"），
不堆砌关键词。

### 第四步：写「一致性约束」，把动作拆小

图生视频最常见的翻车：五官漂移、发型改变、服装变色、配饰消失、左右手交换道具、
场景布局突变。两层防御，缺一不可：

1. **prompt 开头主动声明不变量**（只有这句还不够）：

   > Preserve the young woman's facial features, hairstyle, costume style and color,
   > props and accessories, body proportions, standing position, scene layout, and the
   > direction of lighting shown in `<Picture 1>`.

2. **复杂动作拆成连续、可观察的小动作**：
   - ✗ 「女主转身拔剑，与敌人战斗」
   - ✓ 视线移向画面右侧 → 左手按住剑鞘 → 右手握住剑柄 → 身体缓慢转向右后方 →
     剑刃逐渐拔出 → 动作结束时脸部朝向镜头

   动作越复杂，越应该减少同镜头的其它并发要求（大幅移动、说话、运镜、场景变化
   不要同时发生），必要时拆成多个镜头。

   同理，**写变化路径，不写结果**：「她突然变成凤凰」✗ →
   「火光从手臂向肩部扩散，衣袖逐渐转化为羽毛，双臂展开，羽翼完全成形」✓。

### 第五步：对白、声音和音乐必须分层

- **说话人稳定编号**：同一角色跨镜头始终用 S1、S2……；首次出现时交代年龄范围、
  性别、音高、音色、语速、口音或情绪状态：

  > The young woman (S1), calm, low and slightly breathy voice, says at a measured pace:
  > `<d>[Chinese] 终于找到你了。</d>`

- **对白格式 `<d>[语言] 对白原文</d>`**，只写在 `integrated_multimodal_description`
  里，绝不重复进 `overall_soundscape`。
- **画外旁白必须声明嘴唇不动**："S1 says in voice-over … the person's lips remain
  closed throughout the shot." —— 否则模型可能把旁白当成现场对白，让角色动嘴。
- **配乐避让台词**：有对白的镜头写 "the music decreases in volume during the dialogue
  and gently rises after her final word"，比只写「紧张配乐」层次清楚得多。
- **人物边跑边说长对白是大忌**：口型 + 大幅动作 + 运镜并发会显著增加崩坏概率；
  长对白拆镜头，或改成画外旁白。

## 推荐结构（与官方示例一致；三字段的散文等价形态）

```
[Style & look]      一句话定调：介质风格、镜头、光线、色调、质感
[Scene overview]    1–2 句话讲清整个片段发生什么
[Shot list]         [0s-2.5s] Shot 1: … / [2.5s-5s] Shot 2: …（或 SHOT 1: / CUT 2:）
[Camera]            整体运镜与剪辑规则（hard cuts / no dissolves / slight frame jitter …）
[Audio]             环境声、配乐、重音点、收尾
[Negative]          No text/subtitles/logos/watermarks；按需排除 cartoon、CG 感等
```

## 运镜词汇

推镜 push in / dolly in · 拉镜 pull out / dolly out · 摇镜 pan / tilt ·
移镜 truck / tracking shot · 跟镜 follow shot · 环绕 orbit / arc shot ·
升降 crane / pedestal up-down · 甩镜 whip pan · 手持 handheld ·
固定 static / locked-off · 主观 POV · 特写 close-up / extreme macro ·
低角度 low-angle · 俯拍 top-down / overhead · 剪影逆光 silhouette, backlight

组合示例："the camera executes a slow, deliberate push-in to reveal the intricate circuitry"。
每种运镜的叙事目的见第三步的运镜表；一个镜头只选**一种**主要运镜，写成自然动作句。

## 引用输入（i2v / ia2v / r2v / ra2v 关键技巧）

- i2v：用 **`<Picture 1>`** 指代输入图。官方 i2v 示例开头就写
  "The transparent gaming mouse from <Picture 1> in its original scene…"，
  并用 "The scene opens opens exactly on image 1" 把首帧钉死在输入图上。
- ia2v：**`<Picture 1>`** 是人物肖像（也是视频首帧与构图锚点），**`<Audio 1>`** 是唯一的
  语音来源——口型、节奏、情绪全部由音频驱动，音频会被 1:1 原样拷贝为成片音轨。
- r2v：首帧 **`<Picture 1>`**，尾帧 **`<Picture 2>`**。官方示例用
  "Use <Picture 2> and <Picture 1> as reference frames"，再用 CUT 1 / CUT 2 /
  TRANSITION 描述从首帧到尾帧的过渡过程（重点写「中间怎么变化」的连续动作路径）。
- ra2v：同 r2v，另有 **`<Audio 1>`** 可引用（"and <Audio 1> exactly as it is"）。
  **只有尾帧**时也用 ra2v（只传 `--image-end`）：prompt 反推合理前情，把动作路径
  一步步引到尾帧，并写明最终构图精确落到 `<Picture 2>`。
- 首帧锚定句式（三字段格式常用开头，把 0 秒钉死在输入图上）：
  "For the target video, at 0.00 seconds into the target video, `<Picture 1>`
  (from [Shot 1]) is fully referenced."

## 官方示例 1 — i2v（产品片，默认 prompt）

```
Editorial tech product film. The transparent gaming mouse from <Picture 1> in its original
scene: a pitch-black studio void with a dark, subtle reflective surface, lit by dramatic
duotone vibrant blue and warm neon orange rim lighting. Deep soft shadow falloff into pure
black. Monochromatic dark palette with electric blue and amber accents. Material motif:
glowing internal metallic micro-components and glossy acrylic refractions. The environment
is constant throughout.
SHOT 1: The scene opens exactly on image 1, the mouse resting confidently on the dark
surface, the blue and orange lights slowly pulse brighter, refracting deeply through the
transparent acrylic shell as the camera executes a slow, deliberate push-in to reveal the
intricate circuitry.
SHOT 2: Cut to an extreme macro profile of the ridged scroll wheel and layered internal
micro-components; the camera glides slowly along the side as a sharp beam of warm orange
light sweeps across the metallic textures, contrasting perfectly against the deep blue
ambient glow.
SHOT 3: Cut to a low-angle beauty shot: the mouse levitates weightlessly a few centimeters
above the dark reflective surface, rotating in a slow, precise orbit; the duotone lighting
flares gently along the glassy transparent edges before fading slowly into a sleek silhouette.
Audio: deep pulsing sub-bass room tone, sharp tactile mechanical clicks, a sweeping glassy
whoosh on cuts, and a rising electronic swell that resolves to near-silence on the final fade.
```

## 官方示例 2 — t2v（动作片预告）

```
Realistic live-action cinematic look, action movie trailer: practical film photography
style, a post-rain dusk metropolis, anamorphic lens, shallow depth of field, film grain,
city volumetric fog, flying-car traffic between the towers, restrained grading for a
premium feel, powerful natural movement.
Scene overview: at dusk on a cluster of skyscrapers, the protagonist is being chased,
sprinting and leaping across rooftops, jumping from one building's roof to the next with
pursuers closing in behind. This is the escape sequence of an action movie trailer: every
leap is life-or-death, thrilling and fluid.
Storyboard (each shot a separate scene, rapid cuts, all landing on the musical beats):
[0s-1.5s] Shot 1: high side angle: the protagonist sprinting at the roof edge, pursuers
appearing in the rooftop doorway behind him, wind catching his coat.
[1s-2.5s] Shot 2: the protagonist leaps across the gap between buildings, body stretching
mid-air, towers and flying-car light trails behind him, a slight slow-motion feel.
[2.5s-4s] Shot 3: he lands, rolls and rises, low-angle shot, tower shadows and fog behind
him, he keeps running.
[4s-5s] Shot 4: freeze: the instant he hits the edge of the next roof and launches into
the jump, silhouette, holding.
Camera: each shot its own angle, cuts clean and hard, no dissolves, a slight frame jitter
on the jumps.
Audio: wind, rapid footsteps, city ambience, low score underneath, an accent hit on each
leap, the score bursting at 4s, closing the last 1s.
No text, subtitles, logos or watermarks of any kind, no animation or cartoon rendering,
no overly-CG look, keep the live-action texture.
```

## 官方示例 3 — r2v / ra2v（美漫风格过场）

```
Bold comic-book ink style, heavy linework, red and blue-black palette, night city.
Use <Picture 2> and <Picture 1> as reference frames and <Audio 1> exactly as it is.
CUT 1: top-down view of the little boy superhero on the rooftop — red cape fluttering in
the wind, hands planted on his hips, freckles and a cocky grin as he looks straight up
into the camera. The camera slowly descends toward him as he delivers his line — as he
speaks, comic-book graphic overlay text word by word in sync with his voice: "GET READY TO"
- "MEET" — "YOUR" — "MAKER" — huge jagged comic lettering, white with heavy black outlines
and red drop shadows, tilted at scrappy angles, until the three words hang stacked in the
air above him between his face and the lens.
TRANSITION: a violent WHIP PAN off the rooftop that SMEARS the floating words away with
it, motion-streaked —
CUT 2: low hero angle on the colossal black mech-kaiju towering over the skyline as it
rears back and unleashes a GIANT terrifying ROAR — jaws wide with fangs, red eyes and
chest-core flaring blinding bright, blue lightning arcing off its head, the roar's
shockwave rippling dust and rattling windows down the buildings, comic-style speed-lines
and ink splatter bursting from the impact of the sound. It leans INTO the camera as the
roar peaks. Hold on the roar.
```

（`<Audio 1>` 只有 ra2v 有对应的音频输入参数；r2v 照抄时去掉。）

## 官方示例 4 — ia2v（数字人口播，默认 prompt，结构化规格）

ia2v 的默认 prompt 不是散文而是**结构化规格**：subject_definitions → summary →
retention_analysis → detailed_description → overall_soundscape → non_diegetic_music。
需要定制口播场景时照抄这个骨架再改。核心条款（翻译摘要）：

- **subject_definitions**：`<Subject 1>` 是 `<Picture 1>` 中唯一出现的人（含五官、发型、
  妆容、服装、比例、姿势与构图位置）；`<Picture 1>` 是视频首帧与全片构图锚点（背景、
  道具、光线、色彩、景深全部以此为准）；`<Audio 1>` 是唯一权威的语音、时间与演绎来源。
- **summary**：[关键帧补全 + 音频复用] 一镜到底、固定机位的 talking-head，只有
  `<Subject 1>` 一人；从 `<Picture 1>` 精确起始；`<Audio 1>` 全量 1:1 拷贝为唯一成片音轨。
- **retention_analysis**：人物身份/五官/皮肤/发型/服装/比例 fully_preserved；首帧构图
  fully_preserved；音频 fully_copy（不得重生成、裁剪、变速、变调、降噪、混音或叠加）。
- **detailed_description**：机位三脚架锁定（无推拉摇移、无变焦、无焦点呼吸）；口型、
  音素、下颌动作、停顿、重音、呼吸全部由音频驱动；静音段嘴自然闭合；动作仅限说话
  相关的细微运动 + 眨眼 + 轻微头部微动。
- **overall_soundscape**：只保留 `<Audio 1>`，不加任何环境声、配乐、音效。
- **non_diegetic_music**：N/A，不生成音乐。

英文原文见平台文档 `video_minimax_h3_ia2v` 的默认 prompt（约 4000 字符），需要逐字版
可直接不带 prompt 提交——不发送 prompt 时平台自动套用该规格。

## 实战范例 — 雨夜客栈女主登场（首帧 i2v，三字段完整版）

素材：首帧图是一名红衣古装女子站在雨夜客栈门外，手持黑伞，腰间佩剑。视频 8 秒，
她抬头看向二楼，然后说「终于找到你了」。

```
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1])
is fully referenced.
integrated_multimodal_description: [Shot 1] Cinematic live-action, medium shot. Preserve
the young woman's facial features, hairstyle, red historical costume, black umbrella,
sword, body proportions, standing position, the inn entrance, and the direction of the
rainy-night lighting shown in <Picture 1>. The camera pushes in with small amplitude at
slow speed as she gradually raises her gaze toward the illuminated window on the second
floor. Her left hand continues holding the umbrella while her right hand slowly rests on
the sword hilt. The young woman with a calm, low and slightly breathy voice (S1) says at
a measured pace: <d>[Chinese] 终于找到你了。</d> Her appearance and costume remain
unchanged throughout the shot.
overall_soundscape: Steady rain strikes the umbrella and roof tiles. Water runs along
the stone pavement, accompanied by distant thunder, a faint wooden sign creak, and
subtle fabric movement as she raises her arm.
non_diegetic_music: Sparse guqin notes at a slow tempo, joined by sustained low strings.
The music decreases in volume during the dialogue and gently rises after her final word.
```

这段 prompt 做了六件事，也是自查清单：① 锁定参考图与视频起点（锚定句）；② 声明
人物、服装、道具、场景、光线不变；③ 把「抬头并按剑」拆成连续动作；④ 全程只用一种
主运镜（小幅缓推）；⑤ 单独描述对白与说话人声音特征（S1 + `<d>` 格式）；⑥ 雨声、
动作音、配乐三层分开，配乐避让对白。

## 六个高频翻车点（提交前自查）

1. **一句话塞进太多事**：15 秒内安排五个场景、三个人物、打斗、对白和复杂运镜，
   大概率顾此失彼。先把一个关键动作拍稳，再考虑加镜头。
2. **镜头切换没有时间点**：多镜头 prompt 必须写明第几秒切换，且时间严格递增、
   覆盖 `duration`。
3. **只写结果，不写动作路径**：「她突然变成凤凰」→ 写成火光扩散、衣袖化羽的
   渐变过程；首尾帧/尾帧模式尤其如此。
4. **人物边跑边说长对白**：跑步、转身、表情、口型、运镜同时发生会显著增加难度；
   拆镜头或改画外旁白（并注明嘴唇保持闭合）。
5. **把对白写进环境音**：对白只放在主体描述字段；`overall_soundscape` 只负责
   雨声、脚步、碰撞等声音，不重复对白。
6. **运镜关键词堆砌**：推镜、摇镜、环绕、跟拍、变焦全塞进一句会互相冲突；
   一镜一种主运镜，写成自然动作句。

## 长片分镜：每个镜头一份独立 prompt

单次生成的 `duration` 上限是 15 秒。按「分镜拆解 → 逐镜生成 → 合并」的策略做长片时
（流程见 SKILL.md「Long-form strategy」），prompt 这样写：

- **一镜一 prompt**：每个镜头单独提交一次生成，prompt 的时间轴 `[0s-Ns]` 只覆盖
  该镜头自己的 `duration`，绝不写整部片子的总时间轴。
- **风格句与负面约束逐镜复用**：每个 prompt 用同一句 style & look 开头、同一组
  负面约束收尾（人物、场景、色调的描述也原样复用），合并后才像一个整体。
- **连贯转场**：把上一镜的尾帧（API 结果里的 `cover_url`）作为下一镜的 `--image`
  （i2v）或 `--image-start`（r2v/ra2v），prompt 写 "The scene opens exactly on
  <Picture 1>, continuing directly from the previous shot"；这种链式镜头必须按顺序生成。
- **硬切**：各镜独立生成即可，prompt 里照常写 "Cut to …"；各镜可并行提交。
- **音频**：每镜自带的生成音频会在合并时拼成整条音轨；若整片要配一条独立音乐，
  在各镜 prompt 里只写环境声/音效，合并后再用 ffmpeg 铺背景乐。

## 常见需求的写法速查

- **产品展示**：棚拍虚空 + 双色轮廓光 + push-in / macro / levitate 三镜头 + 机械音效。
- **人物动起来**（i2v 人像）：写明 "the person from <Picture 1>"，动作要小而具体
  （转头、微笑、发丝飘动），幅度越大越容易崩。
- **数字人口播**（ia2v）：人像 + 语音音频；prompt 默认即可；`duration` ≥ 音频时长；
  aspect 用 3:4 / 9:16 等竖向比例。
- **电影感**：anamorphic lens、shallow depth of field、film grain、volumetric fog、
  restrained grading + 分镜表 + 配乐描述。
- **动漫/插画**：先定风格（comic-book ink / anime cel shading / watercolor），负面约束里
  就不要再排除 cartoon rendering。
- **首尾帧过渡**（r2v）：先分别描述首帧画面和尾帧画面（各自锚定 <Picture 1>/<Picture 2>），
  再用 TRANSITION 写明过渡方式（whip pan / morph / match cut / 运镜穿越）。
- **画面跟声音走**（ra2v）：把 <Audio 1> 的节奏写进分镜（"an accent hit on each leap，
  the score bursting at 4s"），让剪辑点落在音频重音上。
- **有对白的剧情**（AI 漫剧）：S1/S2 稳定编号 + 首现交代声音特征；对白用
  `<d>[语言] 原文</d>` 且只写在主体描述字段；配乐写避让（对白时降、对白后升）；
  参考图先声明一致性约束再拆动作（见第四步）。
- **画外旁白**：写明 "says in voice-over" 且画面人物嘴唇保持闭合，避免模型
  错误地给角色对口型。
- **变身 / 渐变效果**：写变化路径不写结果（火光从手臂向肩部扩散→衣袖转化为
  羽毛→双臂展开→羽翼成形），配合首尾帧模式效果最稳。

## 万能提示词模板（五步流程的可执行版）

不想每次从头设计时，按此模板直接产出完整 prompt（即本指南五步导演法的固化形式）：

> 你是一名 MiniMax H3 视频提示词导演。请根据我的需求，先判断应使用：1. 文生视频；
> 2. 首帧图生视频；3. 首尾帧生视频；4. 尾帧生视频；5. 多模态参考生成。然后输出完整的
> 英文视频提示词，必须包含：
>
> `integrated_multimodal_description`：沿时间线描述画面风格、景别、人物身份、外观
> 一致性、连续动作、镜头运动、镜头切换、对白、旁白和画面文字。
> `overall_soundscape`：使用 1–4 句话描述环境音、动作音和非语言人声，不要重复对白。
> `non_diegetic_music`：使用 1–3 句话描述背景音乐的乐器、速度、节奏、音量变化和
> 结束方式；不需要配乐时写 N/A。
>
> 执行规则：
> - 第一个镜头先确定风格、景别、主体和初始构图。
> - 后续镜头标注切换时间，时间严格递增。
> - 每个镜头只安排一种主要镜头运动，写成自然动作句，不堆砌关键词。
> - 参考图模式必须锁定人物、服装、道具、位置、场景和光线的一致性。
> - 复杂动作拆成连续、可观察的小动作。
> - 说话人使用稳定编号 S1、S2；对白使用 `<d>[语言] 对白原文</d>` 格式。
> - 旁白必须注明画面人物嘴唇保持闭合。
> - 首尾帧模式重点描述中间变化路径；尾帧模式必须反推合理前情，并让最终构图
>   精确落到参考图。
> - 直接输出可复制的完整提示词，不要解释。
>
> 我的视频需求：【人物、场景、动作、时长、比例、对白、参考素材、希望的风格】
