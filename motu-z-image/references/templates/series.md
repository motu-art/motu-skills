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

1. **先写 MASTER 块**并请用户确认（这是套图的「选角」环节，改一次成本 = 重出全套）。
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

## 示例

MASTER 块（角色套图）：

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

SCENE 01（晨间咖啡店，中景）追加：

```text
title: Film Girl Look 01, …, seated by a large window in a morning cafe, holding the camera up to her eye with both hands, focused calm expression, medium shot, vertical, eye-level, soft morning window light from camera left, …
```

SCENE 02（黄昏街道，全景）追加：

```text
title: Film Girl Look 02, …, walking down a quiet tree-lined street at dusk, camera resting against her chest, relaxed smile looking off-frame, wide shot, vertical, eye-level, warm low sunset backlight from behind camera right, …
```
