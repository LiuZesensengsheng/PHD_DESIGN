# 论文线·任务线管理服务（DDD＋数据驱动方案） MVP

> 目标：以领域驱动设计（DDD）方式管理甘特任务线，严禁直接篡改列表；通过“蓝图→实例”的数据驱动机制，保证可见性、可回放、可扩展。

---

## 1. 边界与原则（Bounded Context & Principles）
- 边界上下文：Campaign Scheduling（战役排程/甘特）
- 设计原则：
  - 单一写入口：任何轨道/块的新增、合并、休眠、归档，均通过服务提交事务；视图与状态机只读快照。
  - 蓝图→实例：立题后一次性 Commit 蓝图并激活；提前接收仅改变触发性（休眠），不改几何。
  - 不变量守护：Pinned 节点不可合并/删除；每行尾块为 DDL；融合只加强度与时长；工作量守恒。
  - 数据驱动：蓝图、层级梯子、判词脚本、台词/期刊/综述，均来自外部 JSON/CSV。

---

## 2. 领域模型（Domain Model）
- Aggregate Root：Track（任务线/论文线）
  - id: string
  - ideaTier: 'S'|'A'|'B'|'C'（由 Idea 决定）
  - lanes: Lane[]（行/轨）
  - state: 'Planned'|'Active'|'Dormant'|'Completed'|'Rejected'|'Archived'
  - tier: 'T0'|'T1'|'T2'|'T3'|'T4'（投稿层级）
  - blueprintVersion: number
  - history: DomainEvent[]
- Lane（实体）：
  - index: number（逻辑索引，逻辑上不压缩；渲染可紧凑显示）
  - blocks: Block[]
- Block（值对象）：
  - id, blockType: 'event'|'combat'|'ddl'|'rest'
  - trackIndex, startTurn, duration, trackSpan（默认1）
  - pinned: boolean（写作×导师、每轮审稿DDL）
  - tags: string[]（如 'FUSED'）

---

## 3. 生命周期（Lifecycle）
- Planned：立题前/蓝图已生成未激活
- Active：蓝图已实例化并自动推进（autoadvance）
- Dormant：提前接收导致的后续等待/DDL变为“休眠占位”（显示不触发）
- Completed：发表闭环
- Rejected：本轮拒稿，等待降级与重投
- Archived：彻底收尾（仅保留快照）

流转（关键）：
IdeaChosen → BuildBlueprint → CommitBlueprint → Active  
Verdict: Accept → Completed | Minor/Major → Battle→Submit→Active | Reject → DemoteTier→Repost→Active  
PublishingDone → Completed → Archived（可延迟）

---

## 4. 数据驱动（Schemas, CSV/JSON）

### 4.1 蓝图（Blueprint JSON）
```json
{
  "track_id": "paper_main",
  "idea_tier": "A",
  "tier_cap": "T1",
  "default_target_tier": "T2",
  "round_budget": 2,
  "lanes": [
    {
      "index": 0,
      "blocks": [
        {"id":"w1","block_type":"event","track_index":0,"start_turn":0,"duration":1,"pinned":false,"tags":["workload"]},
        {"id":"w2","block_type":"event","track_index":0,"start_turn":2,"duration":1,"pinned":false,"tags":["workload"]},
        {"id":"boss_write","block_type":"combat","track_index":0,"start_turn":4,"duration":1,"pinned":true,"tags":["writing_boss"]},
        {"id":"post0","block_type":"event","track_index":0,"start_turn":5,"duration":0,"pinned":true,"tags":["post"]},
        {"id":"wait0","block_type":"event","track_index":0,"start_turn":5,"duration":2,"pinned":false,"tags":["waiting"]},
        {"id":"ddl0","block_type":"ddl","track_index":0,"start_turn":7,"duration":1,"pinned":true,"tags":["review_judgment"]}
      ]
    }
  ]
}
```

### 4.2 层级梯子（Tier Ladder JSON）
```json
{
  "start_from": "T0",
  "demote_order": ["T0","T1","T2","T3","T4"],
  "t4_policy": {"battle": false, "auto_accept": true},
  "verdict_rules": {
    "T0": {"minor_weight": 0.3, "major_weight": 0.5, "reject_weight": 0.2},
    "T3": {"minor_weight": 0.6, "major_weight": 0.2, "reject_weight": 0.2}
  }
}
```

### 4.3 判词剧场（Reviewer Verdict Script JSON）
```json
{
  "templates": [
    {"role":"format","result":"MINOR","text":"图2分辨率肉眼不可见，建议放大到肉眼可见。"},
    {"role":"method","result":"MAJOR","text":"请把方法写到结果那么长，再把结果写到附录那么远。"},
    {"role":"angel","result":"ACCEPT","text":"写得太棒了，建议直接通过。"}
  ],
  "editor": [
    {"result":"MAJOR","text":"综合意见：大修。我们将继续耐心等你，直到你也开始等我们。"}
  ]
}
```

### 4.4 Idea 档映射（Idea Catalog JSON）
```json
{
  "tiers": {
    "S": {"workload_blocks": 4, "tier_cap": "T0", "round_budget": 3, "default_target_tier":"T1"},
    "A": {"workload_blocks": 3, "tier_cap": "T1", "round_budget": 2, "default_target_tier":"T2"},
    "B": {"workload_blocks": 2, "tier_cap": "T2", "round_budget": 2, "default_target_tier":"T3"},
    "C": {"workload_blocks": 1, "tier_cap": "T3", "round_budget": 1, "default_target_tier":"T4"}
  }
}
```

---

## 5. 服务接口（Application/Domain Services）

### 5.1 TrackService（唯一写入口）
- build_blueprint(idea_meta) → TrackBlueprint
- commit_blueprint(track_id, blueprint) → version
- activate_track(track_id, version) → Active
- add_lane(track_id, lane_spec) → version
- add_blocks(track_id, blocks[]) → version
- mark_pinned(track_id, block_ids[]) → version
- set_dormant(track_id, block_ids[]) → version（提前接收后标记未来等待/DDL为休眠）
- apply_verdict(track_id, verdict) → {accept|min|maj|reject}（调用降级/重投/生成返修战等）
- demote_tier(track_id) → version
- archive(track_id) → Archived
- snapshot(track_id) / restore(snapshot)
- validate(plan) → violations[]（重叠、Pinned 安全、DDL 末尾、层级策略）

### 5.2 Repositories
- TrackRepository：load/save aggregate 快照（或事件溯源）
- BlueprintRepository：加载蓝图 JSON
- PolicyRepository：层级梯子/判词脚本/Idea 档等 JSON

---

## 6. 只读暴露与违规禁改（防止 append）
- ReadOnlyBlocks：对外提供 `__len__/__iter__/__getitem__`；所有写操作（append/extend/insert/remove/pop/clear/__setitem__/__delitem__）均 `raise RuntimeError("Blocks are read-only. Use TrackService")`。
- CampaignState.blocks 替换为 property，返回 ReadOnlyBlocks 视图；任何直接写入一律报错。
- 单测：直接 append 抛错；通过 TrackService.add_blocks 成功。

---

## 7. 不变量与校验（Invariants & Validation）
- Pinned 不可合并/删除/改型；校验失败拒绝提交。
- 每行尾块为 DDL，提交前自动矫正 `_ensure_last_block_is_ddl_per_track()`。
- 融合只加强度与时长；`duration = a.duration + b.duration`；`block_type` 取优先级（combat > event > rest）；DDL 优先。
- 几何固定：Commit 后起点/时长/行索引固定；提前接收仅将未来等待/DDL转 Dormant，不重排几何。
- 工作量守恒：合并不减少总 duration。

---

## 8. 领域事件（Domain Events）
- TrackBlueprintCommitted(track_id, version)
- TrackActivated(track_id)
- DDLArrived(track_id, ddl_id)
- ReviewerVerdict(track_id, verdict, tier)
- TrackDemoted(track_id, from_tier, to_tier)
- TrackCompleted(track_id)
- TrackArchived(track_id)

状态机/演出订阅以上事件决定“进战/审判席/返修提交/重投”。

---

## 9. 渲染与状态机集成（Integration）
- 视图只读：`draw_layers(blocks_snapshot, current_turn, ...)` 不变。
- 状态机只发意图：例如 IdeaChosen → service.build+commit+activate；审判席结果 → service.apply_verdict；拒稿 → service.demote_tier → repost。
- 不直接操作列表；任何试图调用 `state.blocks.append()` 立刻报错。

---

## 10. 可扩展性（Extensibility）
- 新线种类：通过新增蓝图 JSON + 注册策略即可；服务不需要分支代码。
- 新层级/期刊策略：修改 Tier Ladder JSON 即得。
- 新演出/台词：复制 Writer/Editor/Journal/Review CSV/JSON；不改域模型。
- 支持事件溯源：可选将 DomainEvent 持久化，实现回放/调试。

---

## 11. MVP 最小落地（不写代码也能推进的清单）
- 文档：本规范＋蓝图/梯子/判词/Idea 档 4 份 JSON 草案
- 只读容器：ReadOnlyBlocks 设计与注释（禁止 append）
- TrackService 方法契约（doc-only）与不变量清单
- 集成流程图：IdeaChosen→Commit/Activate→DDL→Verdict→流转

---

## 12. 这是否足够 DDD、可扩展且数据驱动？
- DDD：以 Track 为聚合根，Lane/Block 为组成；通过服务与仓储协调，使用领域事件对外表达状态变化，保护不变量，满足 DDD 基本要求。
- 可扩展：新增线/层级/规则/台词，均通过配置 JSON/CSV 扩展，无需改代码逻辑；判词、梯子、Idea 档、蓝图分离，方便调参。
- 数据驱动：蓝图、梯子、判词脚本、Idea 映射与文案池均外置；运行时加载生成实例；演出与 UI 仅消费数据，不绑定实现细节。

---

## 13. 备注与实现建议
- 先将现有 `CampaignState` 写入路径切换到 TrackService；把 `blocks` 改为只读视图。
- 复用现有 `_normalize_no_overlap/_resolve_fusion/_ensure_last_block_is_ddl_per_track` 作为服务内部校验/矫正步骤。
- 不做“删除行导致 index 压缩”；保留逻辑 index，渲染层可紧凑显示，避免回放失真。


