# 套图 / 系列图 — series

**何时用**：一个角色/产品/场景的 N 张图、系列插画、组图、表情包雏形、多角度
展示。这是多图需求的**一致性策略层**，叠加在具体意图模板之上：先用别的模板定
内容，用本模板锁一致性。

## MASTER 固定块（一次写好，逐张原样复制）

```text
[主体固定外观]
identity: [角色/产品名], [年龄感/类别], [脸型/形态], [发型发色/结构],
[肤色/材质], [体态/比例], …

[固定服装/部件]
outfit: [逐件，颜色材质], …
[固定道具] props: [标志性物品]
[固定风格] style: [媒介与风格锚点，逐字不变]
[固定配色] palette: [主/辅/强调色]
```

这些属性在**所有图**中保持一致 —— 每张 prompt 里此块一字不改，只改下面的变量组。

## 每张只写的变量组

```text
SCENE 0N
[动作]：正在做什么（可观察）
[表情]：什么情绪（角色类）
[场景]：在哪里、什么时间
[景别/镜头]：远中近、机位
[光线]：光源方向与性质（可随场景变，风格基调不变）
```

## 工作流（逐张 = 逐张设计、逐张校验、逐张提交）

1. **自行设计 MASTER 块**（套图的「选角」环节，改一次成本 = 重出全套）——不请求用户确认，按需求最合理解读直接锁定，并在最终报告里展示 MASTER 块内容与设计依据，便于用户事后调整重出。
2. **列分镜清单**：每张一行 —— 编号、意图模板、场景/动作/景别一句话。混合意图
   （产品图 + 场景图 + 海报）每张标各自模板。
3. **逐张组装 prompt**：MASTER 块（原样复制）+ 变量组 + 该意图模板的相机/灯光/
   负面组 → 过八维度自检 → 提交（输出命名为 look_01.png、look_02.png …）。
4. 某张不满意 → 只重做该张（同 seed 微调 prompt 或换 seed），其余不动。

## 要点

- MASTER 块里**只放必须跨图一致**的属性；会变化的（姿势、场景、光线）绝不进块。
- 统一全组的画幅（全 portrait 或全 square）与风格句、负面组 —— 拼在一起才像一套。
- 变量组里的场景变化写「路径」不写「突变」：`walking from sunlight into shade`，
  不写 `suddenly in darkness`。
- 4 张以上的组，考虑给每张编号进 title（`Panel 01` / `Look 02`），报告页更好读。

## 示例素材：MASTER 块 + 变量组

MASTER 块（角色套图，逐张原样复制）：

```text
character, female, age range: 24-28, East Asian, oval face, soft features,
shoulder-length black hair with blunt bangs, small silver star hairpin on the left,
light olive skin, slim build,
outfit: oversized dusty-pink knit cardigan over a white tee, wide dark denim trousers,
cream canvas sneakers, small canvas tote,
props: film camera hanging on the neck,
style: warm editorial lifestyle photography, film grain, gentle contrast,
palette: dusty pink, cream, washed denim blue
```

SCENE 01（晨间咖啡店，中景）变量组：seated by a large window, holding the camera
up to her eye with both hands, focused calm expression, medium shot, soft morning
window light from camera left。

SCENE 02（黄昏街道，全景）变量组：walking down a quiet tree-lined street, camera
resting against her chest, relaxed smile looking off-frame, wide shot, warm low
sunset backlight from behind camera right。

## 示例（完整可直接提交）

MASTER 块 + 变量组 + portrait 模板的相机/灯光/调色/负面组，组装完成的整条
prompt（两条间 MASTER 部分一字不改）：

SCENE 01 组装完成：

```text
title: Film Girl Look 01, A warm editorial lifestyle photograph of a young street photographer in a morning cafe., airy, calm, cinematic, sunlit specialty coffee shop with a large storefront window, wooden table with a ceramic latte cup and an open notebook, cream and dusty pink tones, human, female, age range: 24-28, East Asian, oval face, soft features, shoulder-length black hair with blunt bangs, small silver star hairpin on the left, light olive skin, slim build, outfit: oversized dusty-pink knit cardigan over a white tee, wide dark denim trousers, cream canvas sneakers, small canvas tote, props: film camera hanging on the neck, seated by the window facing camera left, holding the camera up to her eye with both hands, focused calm expression, medium shot, vertical, eye-level, subject centered with gentle headroom, full_frame, 50mm, prime, f/2.0, ISO 400, shutter speed: 1/125, white balance: 5200, shallow, softly blurred cafe background, Soft Window Light, morning sun through the pane, sheer white curtain as diffusion, position: camera left, 45 degrees, intensity: soft and even, white bounce card, ratio: 1:2, position: camera right, subtle separation on the hair, warm editorial lifestyle photography, film grain, gentle contrast, neutral with slight warm bias, contrast: medium, soft transitions, saturation: moderate, dusty pink, cream, washed denim blue, She loses herself in the frame while the city wakes outside., quiet focus and morning calm, no extra fingers, no deformed hands, no watermark, no text
```

SCENE 02 组装完成：

```text
title: Film Girl Look 02, A warm editorial lifestyle photograph of the same street photographer walking home at dusk., calm, warm, cinematic, quiet tree-lined residential street with parked bicycles and glowing shop windows, warm orange and denim blue tones, human, female, age range: 24-28, East Asian, oval face, soft features, shoulder-length black hair with blunt bangs, small silver star hairpin on the left, light olive skin, slim build, outfit: oversized dusty-pink knit cardigan over a white tee, wide dark denim trousers, cream canvas sneakers, small canvas tote, props: film camera hanging on the neck, walking down the sidewalk, camera resting against her chest, relaxed smile looking off-frame, wide shot, vertical, eye-level, subject on the right third with the street leading left, full_frame, 35mm, prime, f/2.8, ISO 200, shutter speed: 1/250, white balance: 4800, moderate, gentle falloff into evening, Golden Hour Backlight, low sun behind camera right, natural haze softening the rim, position: behind, 30 degrees, intensity: warm and low, silver reflector, ratio: 1:3, position: camera left, lifting her face out of shadow, warm editorial lifestyle photography, film grain, gentle contrast, neutral with strong warm bias, contrast: medium, saturation: moderate, dusty pink, cream, washed denim blue, She drifts home unhurried as the streetlights come on., dusk ease and quiet warmth, no extra fingers, no deformed hands, no watermark, no text
```
