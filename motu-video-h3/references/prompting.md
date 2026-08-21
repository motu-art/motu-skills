# MiniMax Hailuo 视频 Prompt 编写指南

来源：官方文档 <https://platform.minimaxi.com/docs/guides/video-prompt> 的思路 + motu 平台
三个工作流（t2v / i2v / r2v）的官方示例 prompt。后者是最权威的风格样板，写 prompt 时
优先模仿它们的结构。

## 核心原则

1. **用英文写**。三个官方示例全是英文；英文 prompt 对镜头、材质、音频词汇的覆盖更好。
2. **写成拍摄方案（treatment），不是一句话描述**。模型能接受很长的 prompt（6000 字符），
   结构化、分镜头的描述显著优于一句话。
3. **时间轴与 duration 对齐**。分镜时间码必须覆盖且不超过你设置的 `duration`。
   5 秒放 2–3 个镜头，10 秒放 4–5 个；别在 5 秒里塞 8 个镜头。
4. **显式排除不想要的内容**。官方示例都以负面约束收尾
   （"No text, subtitles, logos or watermarks …"）。

## 推荐结构（与官方示例一致）

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

## 引用输入图片（i2v / r2v 关键技巧）

- i2v：用 **`<Picture 1>`** 指代输入图。官方 i2v 示例开头就写
  "The transparent gaming mouse from <Picture 1> in its original scene…"，
  并用 "The scene opens exactly on image 1" 把首帧钉死在输入图上。
- r2v：首帧 **`<Picture 1>`**，尾帧 **`<Picture 2>`**。官方 r2v 示例用
  "Use <Picture 2> and <Picture 1> as reference frames"，再用 CUT 1 / CUT 2 /
  TRANSITION 描述从首帧到尾帧的过渡过程。

## 官方示例 1 — i2v（产品片，默认 prompt）

```
Editorial tech product film. The transparent gaming mouse from <Picture 1> in its original
scene: a pitch-black studio void with a dark, subtle reflective surface, lit by dramatic
duotone vibrant blue and warm neon orange rim lighting. Deep soft shadow falloff into pure
black. Monochromatic dark palette with electric blue and amber accents. Material motif:
glowing internal metallic micro-components and glossy acrylic reflections. The environment
is constant throughout. SHOT 1: The scene opens exactly on image 1, the mouse resting
confidently on the dark surface, the blue and orange lights slowly pulse brighter,
refracting deeply through the transparent acrylic shell as the camera executes a slow,
deliberate push-in to reveal the intricate circuitry. SHOT 2: Cut to an extreme macro
profile of the shaped scroll wheel and layered internal micro-mechanisms, the camera glides
slowly along the side as a sharp beam of warm orange light sweeps across the metallic
textures, contrasting perfectly against the deep blue ambient glow. SHOT 3: Cut to a
low-angle beauty shot: the mouse levitates weightlessly a few centimeters above the dark
reflective surface, rotating in a slow, precise unit, the duotone lighting flares gently
along the glassy transparent edges before fading slowly into a sleek, static, branded hero
silhouette. Audio: deep pulsating sub-bass room tone, sharp tactile mechanical clicks, a
sweeping glassy whoosh on cuts, and a rising electronic swell that resolves to
near-silence on the final frame.
```

## 官方示例 2 — t2v（动作片预告）

```
Realistic live-action cinematic look, action movie trailer; practical film photography
style, a post-rain dusk metropolis, anamorphic lens, shallow depth of field, film grain,
city volumetric fog, flying-car traffic between the towers, restrained grading for a
premium feel, powerful natural moments.
Scene overview: at dusk on a cluster of skyscrapers, the protagonist is being chased,
sprinting and leaping across rooftops, jumping from one building's roof to the next with
pursuers closing in behind. This is the escape sequence of an action movie trailer: every
leap is life-or-death, thrilling and fluid.
Storyboard (each shot a separate scene, rapid cuts, all landing on the musical beats):
[0s-2.5s] Shot 1: high side angle: the protagonist sprinting at the roof edge, pursuers
appearing in the rooftop doorway behind him, wind catching his coat.
[2.5s-5s] Shot 2: the protagonist leaps across the gap between buildings, body stretching
mid-air, towers and flying-car light trails behind him, a slight slow-motion feel.
[5s-7s] Shot 3: he lands, rolls and rises, low-angle shot, tower shadows and fog behind
him, he keeps running.
[7s-9s] Shot 4: freeze: the instant he hits the edge of the next roof and launches into
the jump, silhouette, backlight, hold.
Camera: each shot its own angle, cuts clean and hard, no dissolves, a slight frame jitter
on the jumps.
Audio: wind, rapid footsteps, city ambience, low score underneath, an accent hit on each
leap, the score bursting at 4s, closing the last 1s.
No text, subtitles, logos or watermarks of any kind, no animation or cartoon rendering,
no overly-CG look, keep the live-action texture.
```

## 官方示例 3 — r2v（美漫风格过场）

```
Bold comic-book ink style, heavy linework, red and blue-black palette, night city.
Use <Picture 2> and <Picture 1> as reference frames and <Audio 1> exactly as it is.
CUT 1: top-down view of the little boy superhero on the rooftop — red cape fluttering in
the wind, hands spread on his hips, freckles and a cocky grin as he looks straight up into
the camera. The camera slowly descends toward him as he delivers his line — as he speaks,
comic-book graphic overlay text is styled in sync with his voice: "GET READY TO" — "MEET!"
— "YOUR" — "MAKER" — huge jagged comic lettering, white with heavy black outlines and red
drop shadows, placed at strong angles, until the three words hang stacked in the air above
him between his face and the lens. TRANSITION: a violent WHIP PAN off the rooftop into
CUT 2, the feeling words with it in motion-streaked … CUT 2: low hero angle on the
colossal black mech kaiju towering over the skyline as it rears back and unleashes a GIANT
terrifying ROAR — jaws wide with fangs, red eyes and chest core flaring blinding bright,
blue lightning arcing off its head, the roar's shockwave rippling dust and rattling
windows down the building edges while debris is sent scattering, bursting from the impact
of the sound. It leans INTO the camera as the roar peaks. Hold on the roar.
```

（注：r2v 示例中出现 `<Audio 1>`，但当前 API 参数表里没有音频输入参数——照抄时去掉即可。）

## 常见需求的写法速查

- **产品展示**：棚拍虚空 + 双色轮廓光 + push-in / macro / levitate 三镜头 + 机械音效。
- **人物动起来**（i2v 人像）：写明 "the person from <Picture 1>"，动作要小而具体
  （转头、微笑、发丝飘动），幅度越大越容易崩。
- **电影感**：anamorphic lens、shallow depth of field、film grain、volumetric fog、
  restrained grading + 分镜表 + 配乐描述。
- **动漫/插画**：先定风格（comic-book ink / anime cel shading / watercolor），负面约束里
  就不要再排除 cartoon rendering。
- **首尾帧过渡**（r2v）：先分别描述首帧画面和尾帧画面（各自锚定 <Picture 1>/<Picture 2>），
  再用 TRANSITION 写明过渡方式（whip pan / morph / match cut / 运镜穿越）。
