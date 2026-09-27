# 套图 / 系列图 — series

**何时用**：一个角色/产品/场景的 N 张图、系列插画、组图、多角度展示。这是多图
需求的**一致性策略层**，叠加在具体意图模板之上：先用别的模板定内容，用本模板
锁一致性。Z-Image 用逗号字段组当 MASTER 块；Qwen 散文格式的对应物是**整句
原样复制**的固定描述句组。

## MASTER 固定块（一次写好，逐张原样复制）

用完整英文句子写死跨图一致的部分，每张 prompt 原样复制这一段：

```text
The subject is [identity: name or role, age, gender/species, ethnicity where relevant].
[Locked appearance: face shape, defining features, hairstyle and color, skin or material, build].
[Locked outfit: each piece with color and material].
[Locked prop: the signature item].
[Locked style: medium and style anchors, word for word identical across the set].
[Locked palette: primary, secondary, accent].
These details remain identical in every image of the set.
```

## 每张只写的变量句

```text
In this scene, [action: observable behavior], [expression], in [scene: place and time],
[shot size and camera angle], [light: source, direction, quality].
```

（构图/灯光可随场景变；风格句与负面句保持逐字一致。）

## 工作流（逐张 = 逐张设计、逐张校验、逐张提交）

1. **先写 MASTER 块**并请用户确认（这是套图的「选角」环节，改一次成本 = 重出
   全套）。
2. **列分镜清单**：每张一行 —— 编号、意图模板、场景/动作/景别一句话。混合意图
   （产品图 + 场景图 + 海报）每张标各自模板。
3. **逐张组装 prompt**：MASTER 块（原样复制）+ 变量句 + 该意图模板的光线/构图/
   负面句 → 过八维度自检 → 提交（输出命名为 look_01.png、look_02.png …）。
4. 某张不满意 → 只重做该张（同 seed 微调 prompt 或换 seed），其余不动。

## 要点

- MASTER 块里**只放必须跨图一致**的属性；会变化的（动作、场景、光线）绝不进块。
- 统一全组的画幅（全 portrait 或全 square）与风格句、负面句 —— 拼在一起才像
  一套。
- 场景变化写「路径」不写「突变」：`walking from sunlight into shade`，不写
  `suddenly in darkness`。
- 4 张以上的组，每张文件名编号（look_01 …），报告更好读。

## 示例

MASTER 块（角色套图）：

```text
The subject is a young street photographer, a woman in her mid-twenties, East Asian.
She has an oval face with soft features, straight black hair cut just below the shoulders with a small silver star hairpin on the left, light olive skin, and a slim relaxed build.
She wears an oversized dusty-pink knit cardigan over a white tee, wide dark denim trousers and cream canvas sneakers, with a small canvas tote on her shoulder.
A compact film camera hangs from a strap around her neck.
Warm editorial lifestyle photography with gentle film grain and soft contrast.
The palette holds dusty pink, cream and washed denim blue.
These details remain identical in every image of the set.
```

SCENE 01（晨间咖啡店，中景）追加变量句：

```text
In this scene, she sits by a large window in a morning cafe, holding the camera up to her eye with both hands with a focused calm expression, in a sunlit specialty coffee shop at eight in the morning, medium shot at eye level, soft morning window light from camera left.
```

SCENE 02（黄昏街道，全景）追加变量句：

```text
In this scene, she walks down a quiet tree-lined street at dusk, the camera resting against her chest and a relaxed smile looking off-frame, on a residential street at golden hour, wide shot at eye level, warm low sunset backlight from camera right.
```
