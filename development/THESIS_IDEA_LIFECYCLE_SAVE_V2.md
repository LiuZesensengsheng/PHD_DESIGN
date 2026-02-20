# 论文线 Idea 触发-接受流程与新存档方案（V3，覆盖旧 V2）

## 1. 背景与目标

旧版方案把 Idea 阶段拆成了“来源选择 + 收敛选择”两段。  
该表达不符合当前策划：来源是**游戏内触发入口**，不是玩家交互选择。

本版按最新口径重写：

1. 游戏过程中有 3 种入口触发 Idea。
2. 系统随机生成一个 `IdeaQualityLevel`。
3. 玩家只决定是否接受该 Idea。
4. 接受后立刻开启一条新的论文线。
5. 允许同时拥有多条论文线并行推进。

本方案继续采用开发期策略：**不做旧存档兼容**。

## 2. 设计边界

本方案覆盖：

1. Idea 触发与 Offer（提案）生命周期。
2. Idea 到论文线创建的接口与落盘结构。
3. 多论文线并行下的状态隔离要求。

本方案不覆盖：

1. 论文 Boss 战具体战斗机制。
2. 审稿阶段数值平衡。
3. 旧存档迁移器。
4. 星图高频交互玩法（EA 口径为仅在论文发表时做完整星图展示）。

## 3. 核心共识（定版）

1. `IdeaTriggerSource` 表示触发来源，不是 UI 选项。
2. `IdeaQualityLevel` 由系统随机决定，不由玩家手动选。
3. 玩家交互只有一件事：`accept` 或 `reject` 当前 Offer。
4. 不存在“收敛状态”与“二次策略选择”。

## 4. 枚举定义（定版）

### 4.1 `IdeaTriggerSource`

1. `ADVISOR_TRIGGERED`
2. `SELF_TRIGGERED`
3. `OPPORTUNITY_TRIGGERED`

### 4.2 `IdeaQualityLevel`

1. `LOW`
2. `MID`
3. `HIGH`

### 4.3 `IdeaOfferStatus`

1. `OFFERED`
2. `ACCEPTED`
3. `REJECTED`
4. `EXPIRED`

### 4.4 枚举中文对照（防理解偏差）

以下中文是展示语义，不是代码枚举值本身。

#### `IdeaTriggerSource`

1. `ADVISOR_TRIGGERED` -> `导师触发`
2. `SELF_TRIGGERED` -> `自主触发`
3. `OPPORTUNITY_TRIGGERED` -> `机会触发`

#### `IdeaQualityLevel`

1. `LOW` -> `低档题目`
2. `MID` -> `中档题目`
3. `HIGH` -> `高档题目`

#### `IdeaOfferStatus`

1. `OFFERED` -> `待决定`
2. `ACCEPTED` -> `已接受`
3. `REJECTED` -> `已拒绝`
4. `EXPIRED` -> `已过期`

## 5. 领域对象

### 5.1 `IdeaOffer`（聚合根）

1. `offerId: int`
2. `triggerSource: IdeaTriggerSource`
3. `qualityLevel: IdeaQualityLevel`
4. `status: IdeaOfferStatus`
5. `createdTurn: int`
6. `expireTurn: int | null`
7. `acceptedTrackIndex: int | null`
8. `seed: int | null`（可选，用于可回放随机）

### 5.2 `ThesisTrackMeta`（与 Offer 关联字段）

1. `trackIndex: int`
2. `originOfferId: int`
3. `originSource: IdeaTriggerSource`
4. `originQuality: IdeaQualityLevel`

## 6. 业务流程（单段式）

### 6.1 触发与生成

1. 游戏内事件命中某入口时，调用 `emitIdeaOffer(source)`。
2. 服务基于 `source` 随机生成 `qualityLevel`。
3. 写入一条 `IdeaOffer(status=OFFERED)`。
4. UI 展示该 Offer，等待玩家处理。

### 6.2 玩家决策

1. 玩家接受：`acceptIdeaOffer(offerId)`。
2. 玩家拒绝：`rejectIdeaOffer(offerId)`。
3. 若超时未处理：`expireIdeaOffer(offerId)`。

### 6.3 接受后的效果

1. 分配新论文线 `trackIndex`。
2. 以 `qualityLevel` 调用论文蓝图服务创建该线。
3. 将 Offer 标记为 `ACCEPTED` 并回填 `acceptedTrackIndex`。
4. 持久化 `ThesisTrackMeta`，用于后续追溯。

## 7. 随机质量规则（先简化）

可先用配置权重，后续再调参。建议初始值：

1. `ADVISOR_TRIGGERED`: `LOW=50%`, `MID=40%`, `HIGH=10%`
2. `SELF_TRIGGERED`: `LOW=25%`, `MID=50%`, `HIGH=25%`
3. `OPPORTUNITY_TRIGGERED`: `LOW=35%`, `MID=40%`, `HIGH=25%`

约束：

1. 权重和必须为 `100`。
2. 权重读取失败时回退统一分布 `33/34/33` 并打日志。

## 8. 状态机规则

### 8.1 合法流转

1. `OFFERED -> ACCEPTED`
2. `OFFERED -> REJECTED`
3. `OFFERED -> EXPIRED`

### 8.2 非法流转（全部拒绝）

1. `ACCEPTED -> *`
2. `REJECTED -> *`
3. `EXPIRED -> *`

### 8.3 处理要求

1. 非法流转返回错误码或异常。
2. 非法流转不落盘。
3. 记录日志（`offerId`、当前状态、目标操作）。

## 9. 新存档结构（V3）

在 `persistent` 新增：

```json
{
  "_thesis_idea_offers": {
    "version": 1,
    "next_offer_id": 104,
    "offers": {
      "101": {
        "offer_id": 101,
        "trigger_source": "SELF_TRIGGERED",
        "quality_level": "HIGH",
        "status": "ACCEPTED",
        "created_turn": 7,
        "expire_turn": 10,
        "accepted_track_index": 2,
        "seed": 318721
      },
      "102": {
        "offer_id": 102,
        "trigger_source": "ADVISOR_TRIGGERED",
        "quality_level": "LOW",
        "status": "OFFERED",
        "created_turn": 8,
        "expire_turn": 11,
        "accepted_track_index": null,
        "seed": 318913
      }
    }
  },
  "_thesis_track_meta": {
    "2": {
      "track_index": 2,
      "origin_offer_id": 101,
      "origin_source": "SELF_TRIGGERED",
      "origin_quality": "HIGH"
    }
  }
}
```

说明：

1. `offers` 以 `offer_id` 字符串为键。
2. 每条论文线仅记录 1 个 `origin_offer_id`。
3. 同时存在多条论文线时，`_thesis_track_meta` 按 `track_index` 隔离。

## 10. 开发期不兼容策略

本阶段采用“新存档优先”，不实现旧档迁移。

执行规则：

1. 发现旧字段（如 `_thesis_idea_lifecycle`）时不迁移。
2. 发现结构非法时重置：
3. `_thesis_idea_offers = {version:1,next_offer_id:1,offers:{}}`
4. `_thesis_track_meta = {}`
5. 记录日志：`THESIS_IDEA_SAVE_V3_RESET`。

## 11. 服务接口契约（建议）

1. `emitIdeaOffer(source: IdeaTriggerSource, currentTurn: int): IdeaOffer`
2. `listOpenIdeaOffers(currentTurn: int): list[IdeaOffer]`
3. `acceptIdeaOffer(offerId: int, currentTurn: int): list[int]`
4. `rejectIdeaOffer(offerId: int, currentTurn: int): IdeaOffer`
5. `expireIdeaOffers(currentTurn: int): list[int]`
6. `getIdeaOffer(offerId: int): IdeaOffer | null`

契约规则：

1. `acceptIdeaOffer` 成功后必须返回创建的 block id 列表。
2. 蓝图调用参数 `idea_quality` 直接映射为 `low/mid/high`。
3. 同一 `offerId` 只能被处理一次。

## 12. 与现有代码的最小接入点

1. 触发端：论文线相关入口事件调用 `emitIdeaOffer`。
2. 接受端：在接受动作中调用现有论文蓝图服务。
3. 蓝图端：保持蓝图服务职责不变，仅消费 `idea_quality`。
4. 存档端：将 Offer 与 TrackMeta 写入 `persistent`。

## 13. 校验与测试建议

### 13.1 状态机测试

1. `OFFERED -> ACCEPTED` 成功。
2. `OFFERED -> REJECTED` 成功。
3. `ACCEPTED -> REJECTED` 被拒绝。

### 13.2 随机与落盘测试

1. 不同 `source` 命中不同权重分布。
2. 序列化/反序列化后 Offer 字段一致。
3. 非法存档触发重置并产生日志。

### 13.3 多论文线并行测试

1. 连续接受多个 Offer，可创建多个 `track_index`。
2. 各线 `origin_offer_id` 不串线。
3. 某一线推进失败不影响其他线状态。

## 14. 明确删除的旧概念

以下内容从方案中移除：

1. `IdeaConvergenceMode`
2. `IDEA_CONVERGENCE_PENDING`
3. “来源选择”交互步骤
4. “二次策略选择”交互步骤

## 15. 立意来源与流程定版（本轮讨论结论）

### 15.1 来源分类（保留三类）

1. 导师给题（`ADVISOR_TRIGGERED`）
2. 自主发现（`SELF_TRIGGERED`）
3. 事件赠送/机会触发（`OPPORTUNITY_TRIGGERED`）

### 15.2 系统层统一规则

1. 三类来源最终都产出同一种 `IdeaOffer`。
2. 三类来源共用同一状态机与同一落盘结构。
3. 玩家对任意来源的交互统一为：`accept` 或 `reject`。
4. 一旦 `accept`，立即创建论文线并锁定该线甘特图蓝图。

### 15.3 表现层差异（仅叙事包装不同）

1. 导师给题：直接揭示立意，节奏最快。
2. 自主发现：允许一个短剧情步骤后再揭示立意（最多一步，不扩展为长流程）。
3. 事件赠送：突发出现，强调戏剧性与随机感。

### 15.4 方案取舍（已定）

1. 采用“方案1”作为主流程：直接给立意 Offer，玩家选择做或不做。
2. “方案2（先给灵感再抽奖揭示）”不作为主循环，仅可用于低频特殊事件。
3. 立意阶段不新增独立资源条（例如 `idea准备度`），避免污染卡牌主循环。

### 15.5 甘特图硬约束（已定）

1. 立意质量决定论文线规模（长度/节点数/奖励密度）。
2. 该规模在 `accept` 时一次性确定并锁定。
3. 后续不再通过“立意环节”二次改写该线规模。

## 16. 论文题目池（科研味，立意文案候选）

### 16.1 导师给题（`ADVISOR_TRIGGERED`）

1. 基于多中心回顾数据的术后并发症风险预测模型比较研究
2. 面向低资源实验室的细胞图像分割流程标准化与复现评估
3. 不同超参数搜索策略在小样本场景下的泛化误差分析
4. 面向中文医学摘要的术语规范化与信息抽取联合框架
5. 基于公开数据集的跨设备域偏移校正方法及临床可用性验证

### 16.2 自主发现（`SELF_TRIGGERED`）

1. 从失败实验中学习：负结果驱动的模型修正与收益边界分析
2. 面向长尾标签分布的课程学习策略在文本分类中的有效性研究
3. 将因果图先验引入时序预测：在噪声环境下的稳健性评估
4. 基于主动学习的人机协同标注流程对标注成本的影响研究
5. “小模型+高质量数据”是否优于“大模型+低质量数据”的实证比较

### 16.3 机会触发（`OPPORTUNITY_TRIGGERED`）

1. 新发布开放数据集上的快速复现实验与基线重建报告
2. 跨校合作项目中的多模态特征对齐与缺失模态补全研究
3. 面向突发公共议题的实时文本立场检测与漂移追踪方法
4. 利用工业界匿名日志进行异常检测的可迁移性验证
5. 限时算力条件下轻量模型蒸馏方案的性能-成本折中分析

### 16.4 题目风格约束（供后续批量生成使用）

1. 每个题目必须同时包含：`对象` + `方法` + `评估语境`。
2. 避免纯口号型题目（如“XX研究综述”），优先“可做可测”的题目。
3. 题目长度建议 18~32 字（中文），保持“像真论文题目”的密度。
4. 可在 UI 上显示“短标题”，但落盘保留完整标题。

---

该文档为论文线 Idea 阶段 V3 技术基线。  
结论口径：**来源是触发上下文，随机质量由系统给出，玩家只做接/不接，并支持多论文线并行。**
