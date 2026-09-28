# 意图路由表 — 按用户需求找模板

拿到生成需求后先判意图，再读对应模板文件。一个需求混合多个意图
（「一套 3 张：产品图 + 场景图 + 海报」）就拆成多个单图任务，逐张套用各自模板。

**画面里要有中文/英文文字的需求（海报、招牌、UI 文案、带字主图）优先路由到
本 skill**——文字渲染是 Qwen Image 2.1 的最强项（实测中文标题+副行全对）；
无文字、求速度求 2K 的画面交给 motu-z-image。

| 用户在要什么（示例关键词） | 模板文件 | 一句话 |
|---|---|---|
| 角色/IP/吉祥物/游戏角色/卡通形象/3D 形象 | [character.md](character.md) | 全身角色设计稿，剪影识别度优先 |
| 真人肖像/职业照/头像/商务人像/ID 照 | [portrait.md](portrait.md) | 真实皮肤质感 + 影棚布光 |
| 人物在某个场景里做事（最通用的出图需求） | [people-scene.md](people-scene.md) | 人物 + 环境组合，视觉分层 |
| 产品摄影/工业品/消费电子/包装 | [product.md](product.md) | 结构准确 + 商业影棚光 |
| 电商主图/白底图/详情页首图 | [ecommerce.md](ecommerce.md) | 白底 70–85% 占比，平台合规 |
| 食品/美食/菜谱/餐厅菜单图 | [food.md](food.md) | 食欲感特写，窗光 |
| 汽车/零部件/工业机械/五金 | [automotive.md](automotive.md) | 精密金属质感，硬轮廓光 |
| 珠宝/首饰/香水/口红/美妆小件特写 | [jewelry.md](jewelry.md) | 微距 + 反射控制，高级光泽 |
| 时尚/lookbook/服装大片/造型街拍 | [fashion.md](fashion.md) | 服装是主角，硬闪或大柔光 |
| 动物/宠物/猫狗/野生动物 | [animal.md](animal.md) | 眼睛锐利 + 解剖正确 |
| 自然风光/山川/海岸/星空/壁纸 | [landscape.md](landscape.md) | 摄影真实感，时刻+三层+光向 |
| 场景/环境概念图/游戏场景/电影场景/世界观 | [scene.md](scene.md) | 前中背景纵深 + 大气透视 |
| 建筑/室内设计/空间/家装效果 | [architecture.md](architecture.md) | 透视垂直，材质分区 |
| 海报/广告设计/宣传页/活动视觉（**含画面文字**） | [poster.md](poster.md) | 视觉层级 + 逐字文字 + 留白 |
| 书封/专辑封面/播客封面/课程封面（含标题署名） | [bookcover.md](bookcover.md) | 类型气质 + 视觉隐喻 + 逐字标题 |
| 网站/落地页 hero 图/SaaS 宣传视觉 | [hero-image.md](hero-image.md) | 大留白给标题，主体偏侧 |
| 样机/T恤印花/包装盒/海报上墙/屏幕界面落地 | [mockup.md](mockup.md) | 贴图随载体变形，无悬浮感 |
| 社交媒体配图/公众号封面/小红书图 | [social.md](social.md) | 平台画幅 + 核心信息一眼懂 |
| Logo/品牌视觉/icon/标志 | [logo.md](logo.md) | 几何极简，小尺寸可用 |
| UI/App 界面/网页设计概念稿 | [ui.md](ui.md) | 布局层级 + 间距系统 |
| 信息图/流程图/步骤图 | [infographic.md](infographic.md) | 结构优先，文字精确 |
| 漫画/分镜/故事板/连环画 | [comic.md](comic.md) | 多格一致角色 + 景别变化 |
| 插画/编辑配图/书籍插图/概念艺术 | [illustration.md](illustration.md) | 隐喻叙事 + 媒介纹理手感 |
| 套图/系列图/一个角色多张/一组图 | [series.md](series.md) | MASTER 锁定 + 逐张生成 |

都不像？用 [people-scene.md](people-scene.md)（有人）或 [scene.md](scene.md)
（无人）作为起点，它们是最通用的骨架。

所有模板的散文格式、内容顺序、自检清单见
[../prompting.md](../prompting.md)。
