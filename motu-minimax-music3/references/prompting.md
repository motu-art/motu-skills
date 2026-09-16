# MiniMax Music 3 — caption 与歌词编写指南

来源：motu 平台 `audio_minimax_music_3` 工作流的官方默认 caption（最权威的风格样板）
+ 音乐生成通用实践。

## 核心原则

1. **用英文写 caption**。官方样板是英文；英文对曲风、乐器、编曲词汇的覆盖更好。
2. **caption 写"制作简报"，不是关键词堆砌**。模型接受 6000 字符，结构化的简报
   （全局风格 → 声音palette → 人声说明 → 分段编曲）显著优于 "epic cinematic music"。
3. **器乐要显式封锁人声**。单独一句："Fully instrumental with no vocals, spoken
   words, chants, or vocal samples." 不写这句话可能出哼唱/和声。
4. **歌词与时长匹配**。一行歌词约 3–5 秒；180 秒的流行歌约 40 行。
   `max_duration` 是上限不是目标——编曲写够了才会真的生成那么长。

## 推荐 caption 结构（与官方样板一致）

```
### Global Metadata     曲风家族、情绪氛围、速度感受、情绪走向、画面感
### Vocal Details       器乐：完全封口；歌曲：人声性别/音域/唱法
### Arrangement         Intro → Main Theme → Development → Bright Section → Outro，
                       每段写清主奏乐器、伴奏织体、能量走向
```

## 词汇速查

- **速度**：60 bpm (downtempo/sleepy) · 75–90 bpm (lo-fi/R&B) · 100–120 bpm (pop) ·
  120–128 bpm (house) · 140+ bpm (drum & bass)
- **情绪**：warm, lighthearted, melancholic, hopeful, epic, tense, playful, nostalgic
- **织体**：sparse, open space between notes, layered, dense, minimal, lush
- **常见坑**：要"安静背景乐"就写 "no melody peaks, sits under dialogue"；
  要避免 AI 味电音就写 "acoustic instruments only, no synthetic pads"

## 官方样板 caption（儿童夏日器乐，逐字）

```
Lighthearted children's instrumental music with a warm, cheerful summer atmosphere.
The style blends gentle children's easy-listening, acoustic pop, and playful soundtrack
elements. Keep the tempo relaxed to moderately upbeat, with a soft, steady pulse that
feels lively without becoming energetic or rushed. The emotional progression should move
from peaceful curiosity into bright, carefree happiness, evoking a sunny summer afternoon
beneath the shade of leafy trees, distant cicadas, and a soft breeze passing through
the branches.

The sonic palette should remain clean, airy, warm, and natural. Piano, small wooden
xylophone, and delicate wind chimes form the core instrumentation. Avoid heavy drums,
aggressive percussion, dense electronic textures, dramatic orchestral elements, or
strong bass. Maintain plenty of open space between notes, with a simple and memorable
melody suitable for children.

### Vocal Details

Fully instrumental with no vocals, spoken words, chants, or vocal samples.

### Arrangement

**Intro:** Begin quietly with sparse wind-chime notes and a few soft piano tones,
creating the feeling of sunlight filtering through tree leaves. Leave generous space
between phrases.

**Main Theme:** Introduce the wooden xylophone with a simple, cheerful melody. The piano
provides light chordal support underneath, while subtle wind-chime accents appear at the
ends of selected phrases. Establish a gentle, relaxed rhythmic motion.

**Development:** Allow the piano to briefly take over the main melody while the xylophone
responds with short playful phrases. Gradually enrich the harmony without making the
arrangement dense. Maintain a breezy, effortless summer character throughout.

**Bright Section:** Bring the xylophone melody forward again with slightly more rhythmic
movement and brighter piano accompaniment. This should be the happiest point of the piece,
suggesting children enjoying a peaceful summer day outdoors while leaves move gently in
the wind.

**Outro:** Gradually simplify the arrangement. Let the xylophone disappear first, followed
by increasingly sparse piano notes. Finish with a few delicate wind-chime tones fading
naturally into silence, leaving a calm, warm, and innocent summer feeling.
```

## 歌词写法

- 用段落标记，独占一行：`[Intro]` `[Verse 1]` `[Pre-Chorus]` `[Chorus]` `[Verse 2]`
  `[Bridge]` `[Final Chorus]` `[Outro]`。
- 副歌重复就写重复——模型会按标记演绎，不会自动补副歌。
- 和声/哼鸣直接写成 `(ooh)` `(ahh)` 括号衬词。
- 语言：中英文歌词均可；caption 仍建议英文。
- 例：

```
[Verse 1]
City lights are fading slow
Coffee going cold, nowhere to go

[Chorus]
So we drive, we drive, till the morning comes
Windows down, humming half-forgotten songs
```

## 常见需求的写法速查

- **视频 BGM**：写 "sits under dialogue, no melody peaks, consistent energy"，时长对齐视频。
- **产品/品牌 jingle**：10–15 秒，一段hook + 品牌 logo 定音；歌词短、可记。
- **播客片头**：15–30 秒，"modern, clean, upbeat corporate, subtle synth arps"。
- **游戏/紧张氛围**：低频脉冲 + 单音 motif + "tense, building"，避免旋律化。
- **Lo-fi 学习背景**：75 bpm、"vinyl crackle"、"soft electric piano"、"no vocals"。
