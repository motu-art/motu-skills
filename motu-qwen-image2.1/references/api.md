# image_qwen_image_2_1_t2i — Motu Workflow API

Qwen Image 2.1 文生图。Base URL `https://api.motu.art`，鉴权
`Authorization: Bearer $MOTU_KEY`（从仓库 `.envrc` 读，勿硬编码）。

异步模式：提交拿 `workflow_request_id` → 轮询状态直到 `completed` / `failed`
→ `result[]` 里取 OSS 签名 URL 下载。典型生成 ~30 秒；网关拥堵时排队可达
10 分钟，脚本默认 timeout 900 秒。

## 1. 提交

`POST https://api.motu.art/workflows/image_qwen_image_2_1_t2i`

| 参数 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| prompt | string | 是 | 见下方官方默认示例 | 英文散文 prompt，≤ 6000 字符 |
| width | number | 否 | 1024 | 512–2048，8 的倍数 |
| height | number | 否 | 1024 | 512–2048 |
| seed | number | 否 | 0 | 0–10000000000000000；同 seed + 同 prompt 复现同族结果 |
| batch_size | number | 否 | 1 | 1–4；同一 prompt 的多个备选 |
| priority | string | 否 | "default" | `"urgent"` 优先处理 |

响应 `202`: `{"status":"queued","workflow_request_id":"<uuid>"}`；
`400` 参数缺失/非法；`401` 未带 key；`403` key 无效；`404` workflow 不存在。
网关偶发 `504`（nginx 超时）——稍等重试即可，不会重复计费请求。

## 2. 轮询

```
GET https://api.motu.art/workflow/status?workflow_request_id={id}
```

⚠️ 文档里写的路径形式 `GET /workflows/status/{id}` 实际返回
`500 {"message":"Failed to retrieve API cost"}`（网关已知问题，两个
workflow 皆如此）——**一律用上面的 query 参数形式**。

响应：

```json
{
  "workflow_request_id": "<uuid>",
  "status": "queued | processing | completed | failed",
  "result": [{ "url": "https://.../1?OSSAccessKeyId=...", "width": 1024, "height": 1536, "file_size": 1864948 }]
}
```

`result` 仅在 `completed` 时出现；数组长度 = batch_size。URL 是阿里云 OSS
签名链接，**14 天后过期**，且不带扩展名（内容是 PNG）——拿到就下载保存为
`.png`。

## 分辨率规则（实测）

输出**严格等于请求的 width×height**，没有放大机制（区别于 z-image 的 2×）：

| 请求 | 输出 |
|---|---|
| 1024×1024 | 1024×1024 |
| 1024×1536 | 1024×1536 |

要 2K 细节就直接请求 2048 级画布（如 2048×2048、1536×2048），单边范围
512–2048。

## 与兄弟 skill 的分工

| 需求 | 用 |
|---|---|
| 画面里有中文/英文文字（海报标题、包装、招牌、UI 文案） | **本 skill**（Qwen 2.1 文字渲染最强，实测中文标题+副行全对） |
| 2K 高清、最快速度、无文字画面 | motu-z-image（~15s，2× 放大） |
| 拉丁文字为主的品牌/海报字体设计 | motu-ideogram4 |

## 官方默认示例（风格样板）

官方默认 prompt 是一整段英文叙事散文——这就是本 skill 所有模板的格式基准：

```text
Greyscale fashion editorial portrait of an avant-garde woman tilted upwards in profile, captured with striking high-contrast chiaroscuro lighting. She wears oversized, thick-rimmed circular black sunglasses with matte dark lenses, concealing her upward gaze. Her attire merges high couture with tactical abstraction: a high-necked structural dress tailored from heavyweight fabric featuring a disrupted optical camouflage pattern—interlocking oversized polka dots, pixelated stippling, and organic contour blotches in stark monochrome that mimic military disruptive patterns in a refined runway style. Around her shoulders, asymmetric pleated webbing and tailored cargo straps are integrated seamlessly into the garment's architecture. In her gloved hand, she clutches a structured matte-leather geometric handbag accented with subtle tactical buckles, utility stitching, and dark brushed-metal hardware. Her skin texture is rendered with hyper-detailed clarity, sculpted by intense, razor-sharp studio key light and deep graphite shadows. The striking background is a vivid mixed-media graphic collage, composed of flat vibrant lime green planes, stark black and white overlapping circles, segmented semi-circles with bold zebra striping, dense micro-halftone dot matrices, and vector topographic contour lines. The clash between monochromatic disruptive camo elements on her clothing and the saturated, retro-futuristic pop-art backdrop creates an intense visual dissonance, emphasizing sharp silhouettes, paper cut-out edges, dynamic compositional balance, and clean graphic novel textures. Absolutely no text, no typography, no letters, no words, no numbers, no logos, no watermark, no captions, pure imagery only.
```
