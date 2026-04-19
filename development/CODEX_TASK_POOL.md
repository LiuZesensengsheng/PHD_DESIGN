# Codex 浠诲姟姹?

## 鐢ㄩ€?

杩欎唤鏂囨。鍙褰曚竴绫讳簨鎯咃細

- 鍝簺浠诲姟閫傚悎 Codex 鐙珛杩炵画鎵ц鍑犲皬鏃?
- 杩欎簺浠诲姟闇€瑕佷粈涔堣緭鍏?
- 浜у嚭鏄粈涔?
- 鍝簺浠诲姟宸茬粡鍙互鐩存帴鍋氾紝鍝簺杩橀渶瑕佸厛缁х画瀹?
- 宸插畬鎴愮殑澶у潡浠诲姟鍙繚鐣欑儹鍖虹储寮曪紝璇︾粏璁板綍绉诲姩鍒?`docs/development/task_pool_archive/`

杩欎唤鏂囨。涓嶆槸锛?

- 鏃ユ姤
- 鏋舵瀯鍘熷垯鏂囨。
- 鍐崇瓥鏃ュ織

## 浣跨敤鏂瑰紡

姣忔閫夋嫨浠诲姟鏃讹紝鍏堢‘璁?4 浠朵簨锛?

1. 浠诲姟鏄惁浠嶇鍚堝綋鍓嶄紭鍏堢骇
2. 杈撳叆鏂囨。鎴栨暟鎹槸鍚﹀凡缁忓瓨鍦?
3. 瀹屾垚鏍囧噯鏄惁瓒冲娓呮
4. 鏄惁閫傚悎浣庣洃鐫ｈ繛缁墽琛?

## 浠诲姟閫夋嫨瑙勫垯

浼樺厛浜ょ粰 Codex 鐨勪换鍔★細

- 杈撳叆鏂囦欢鏄庣‘
- 杈撳嚭鏂囦欢鏄庣‘
- 娴嬭瘯鏍囧噯鏄庣‘
- 涓嶄緷璧栭珮棰戜汉宸ュ缇庡垽鏂?
- 涓嶄緷璧栧疄鏃惰瘯鐜╂墜鎰?

鏆傛椂涓嶈浜ょ粰 Codex 闀挎椂闂寸嫭绔嬫帹杩涚殑浠诲姟锛?

- 绾瑙夋墦纾?
- 鏈€缁堝墽鎯呰姘斿畾绋?
- 楂樹富瑙傛€х殑 UX 璋冩暣
- 鏈€鍚庨樁娈电殑绾墜鎰熷钩琛?

## 褰撳墠娲昏穬浠诲姟

- 褰撳墠鎺ㄨ崘鎵ц鏂瑰紡锛?
  - 鍏堝仛 `combat orchestration v1`锛屾殏涓嶇 UI 鑺傜偣鍖?
  - 涓茶鎺ㄨ繘锛屼笉骞惰寮€澶氭潯 combat 涓昏矾寰勯噸鏋?
  - 鍏佽鐭湡杩佺Щ绐楀彛锛屼絾涓嶆帴鍙楅暱鏈熷弻杞?
  - `2026-03-16` 鍒ゅ畾鏇存柊锛歚combat orchestration v1` 宸插彲瑙嗕负瀹屾垚锛屽悗缁浆鍏ユ洿灏忓垏鐗囩殑 chore / card-play / planner / policy 鏀跺彛
  - v1 涔嬪悗鐨勫墿浣?fallback 闈㈤粯璁ゅ彧鍖呮嫭鏉′欢鍨嬨€佸睘鎬ф潵婧愬瀷鍜屽叾浠栧皬浼楀鏉傛晥鏋?

### P1. Narrative Pipeline V1

- 鐩爣锛?
  - 涓哄彊浜嬩簨浠跺缓绔嬩竴鏉℃竻鏅扮殑 `draft -> normalized source -> build -> runtime -> acceptance` 绠＄嚎
  - 缁熶竴褰撳墠 narrative/questline 涓婚摼涓?legacy campaign-event 璺嚎锛岄伩鍏嶇户缁弻鐪熺浉澧為暱
  - 璁╃瓥鍒掍笌 Codex 鍙互鍦ㄤ笉纰?runtime 缁嗚妭鐨勫墠鎻愪笅绋冲畾鎵╁啓 narrative 鍐呭
- Current execution rules:
  - follow `docs/development/NARRATIVE_PIPELINE_V1.md`
  - use `docs/development/NARRATIVE_PIPELINE_TASK_TABLE_V1.md` as the rollout order
  - treat `data/questlines/*.json` as the active runtime path during migration
  - do not add new growth to `contexts/campaign/infrastructure/events/*.json`
  - do not retire legacy narrative runtime files until:
    - migration inventory exists
    - normalized source schema exists
    - source -> runtime build parity is proven on the active tutorial path
  - prefer serial rollout, not multiple competing narrative architecture branches
- Main inputs:
  - `docs/development/NARRATIVE_PIPELINE_V1.md`
  - `docs/development/NARRATIVE_PIPELINE_TASK_TABLE_V1.md`
  - `docs/development/DATA_PIPELINE_GUARDRAILS_V1.md`
  - `contexts/shared/quest_loader.py`
  - `contexts/shared/quest_runtime.py`
  - `contexts/narrative/application/service.py`
  - `contexts/event/state.py`
  - `data/questlines/`
  - `data/events_drafts/`
  - `data/events_src/`
- 棰勬湡杈撳嚭锛?
  - 涓€濂?normalized narrative source schema
  - draft/source/build tooling for narrative content
  - tutorial narrative path migrated onto the new source/build model
  - narrative scenario acceptance tests covering the active tutorial event/combat/reward path
  - a clear legacy retirement plan for the old campaign event route
- 杈圭晫锛?
  - 涓嶉噸鍐?`EventState` 灞曠ず灞?
  - 涓嶆妸 narrative pipeline 鎵╂垚閫氱敤鑴氭湰 VM
  - 涓嶆妸 combat event bus 涓?narrative event pipeline 娣蜂负涓€璋?
  - 涓嶅湪 schema 灏氭湭绋冲畾鍓嶄竴鍙ｆ皵杩佸畬鎵€鏈?legacy narrative content
  - 涓嶈 runtime 鐩存帴璇?draft 鏂囦欢
- 褰撳墠闃舵鍒ゆ柇锛?
  - `Phase 0` 鍙互瑙嗕负宸插噯澶囧畬鎴?
  - 榛樿涓嬩竴姝ユ槸 `Phase 1 + Phase 2`
  - 鍦?tutorial path 鏋勫缓绛変环 build 涔嬪墠锛屼笉搴斿垹闄ゅ叏閮?legacy narrative 鍐呭

### P1. Campaign Simplification V1

- 鐩爣锛?
  - 鍦ㄤ笉閲嶅紑鏁磋疆 UI 閲嶅啓銆佸叏閲?DDD 鎺ㄨ繘鎴栬妭鐐规爲杩佺Щ鐨勫墠鎻愪笅锛屽畬鎴愪竴杞?campaign 渚х殑 targeted simplification
  - 璁╁綋鍓?mixed-mode campaign 鏋舵瀯鏇村鏄撹銆佹洿瀹夊叏鎵╁睍锛屼篃鏇翠究浜?Codex 闀挎椂闂磋繛缁崗浣?
- Current execution rules:
  - follow `docs/development/CAMPAIGN_SIMPLIFICATION_PLAN_V1.md` serially
  - `2026-04-05`: `Phase 0` landed
  - `2026-04-05`: `Phase 1` landed: removed residual thesis / meeting compat wrappers and old headless meeting paths
  - `2026-04-05`: `Phase 2` landed: moved `CampaignState` service wiring into a dedicated service bundle while keeping stable host attrs/seams
  - `2026-04-05`: `Phase 3` landed: split `MeetingService` into focused selection / shop / event-flow helpers while keeping the stable service surface
  - `2026-04-05`: `Phase 4` landed: split campaign mouse input into dedicated intent resolution + dispatch helpers while preserving click priority and state seams
  - `2026-04-05`: the mainline simplification pass is effectively complete through `Phase 4`
  - `Phase 5` is now a triggered backlog slice, not an automatic next step
  - only start `Phase 5` when near-term roadmap work directly touches DDL / fusion / compaction rules or shared board invariants
  - do not mix this with a large UI rewrite, full DDD push, or full node migration work
- Main inputs:
  - `docs/development/CAMPAIGN_SIMPLIFICATION_PLAN_V1.md`
  - `docs/development/UI_ARCHITECTURE_V1.md`
  - `docs/development/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
  - `docs/development/CAMPAIGN_HOTSPOT_DEFER_LIST_V1.md`
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/meeting_service.py`
  - `contexts/campaign/services/campaign_mouse_event_service.py`
  - `contexts/campaign/services/track_block_service.py`
  - `contexts/campaign/services/thesis_meta_service.py`
- 棰勬湡杈撳嚭锛?
  - 绠€鍖栬鍒掋€佺儹鐐规枃妗ｅ拰浠诲姟绯荤粺鐘舵€佷繚鎸佸悓姝?
  - focused guardrail tests + `scripts/run_repo_smoke_baseline.py` 淇濇姢鍏抽敭 seams
  - 涓€杞互鍒犳棫璺緞銆佹敹绱?host seams銆佹媶楂?ROI 鐑偣涓轰富鐨?campaign targeted refactor
- 杈圭晫锛?
  - 涓嶅仛 whole-campaign facade
  - 涓嶅仛 full `CampaignView` rewrite
  - 涓嶅仛 repository-everywhere
  - 涓嶅仛 purity-driven `Track` aggregate promotion
  - 涓嶆妸 runtime UI 婕旇繘鎵╂垚鍙︿竴杞叏灞€鏋舵瀯閲嶅啓
- 褰撳墠闃舵鍒ゆ柇锛?
  - `Phase 0` 鍒?`Phase 4` 宸插畬鎴愬苟鍙涓哄綋鍓嶄富绾挎敹鍙?
  - `Phase 5` 鍙繚鐣欎负 triggered backlog锛屼笉鍐嶈涓鸿嚜鍔ㄤ笅涓€姝?
  - 鍙湁杩戞湡寰呭仛鐩存帴瑙﹀強 DDL / fusion / compaction 鎴?shared board invariants 鏃舵墠鍚姩

### P1. Campaign Self Refactor V1

- Goal:
  - run one campaign-only refactor pass focused on shell ownership, thesis
    write-path convergence, and task-area internal rule clarity
  - improve stability, DDD readiness, and AI safety without reopening `view`,
    visual runtime, or shared architecture
- Current execution rules:
  - follow `docs/development/CAMPAIGN_SELF_REFACTOR_PLAN_V1.md` serially
  - `2026-04-18`: `Phase 0` landed: scope freeze, task entry, daily-log
    handoff, and baseline validation pack
  - `2026-04-18`: `Phase 1` landed: grouped service surfaces now install on
    `CampaignState` while preserving legacy service aliases and stable
    `request_*` seams
  - `2026-04-18`: `Phase 2` landed: thesis atomic checkpoint/restore and
    session tier/publication writes now route through explicit campaign thesis
    seams instead of being duplicated across multiple thesis services
  - `2026-04-18`: `Phase 3` landed: `TrackBlockService` now keeps the same
    stable public surface while its overlap, DDL snake, fusion, and layout
    rules are split into smaller internal rule units
  - `2026-04-18`: `Phase 4` landed: campaign self-refactor guardrails/docs are
    refreshed and this task is now downgraded to closed reference memory
  - do not mix this task with a `CampaignView` rewrite, visual-runtime
    extraction, shared-utils pass, or full node migration work
  - stop and re-scope if progress requires broad edits under
    `contexts/campaign/view.py`, `contexts/campaign/rendering/`,
    `contexts/campaign/ui_runtime/`, or `contexts/shared/`
- Main inputs:
  - `docs/development/CAMPAIGN_SELF_REFACTOR_PLAN_V1.md`
  - `docs/development/CAMPAIGN_SIMPLIFICATION_PLAN_V1.md`
  - `docs/development/CAMPAIGN_AGGREGATE_CANDIDATE_REVIEW_V1.md`
  - `docs/development/AGGREGATE_INVARIANT_TESTS_V1.md`
  - `docs/development/CAMPAIGN_SERVICE_DEPENDENCY_HOTSPOTS_V1.md`
  - `contexts/campaign/state.py`
  - `contexts/campaign/services/campaign_state_service_bundle.py`
  - `contexts/campaign/services/thesis_write_path_service.py`
  - `contexts/campaign/services/thesis_meta_service.py`
  - `contexts/campaign/services/thesis_submission_flow_service.py`
  - `contexts/campaign/services/thesis_round_service.py`
  - `contexts/campaign/services/thesis_slice.py`
  - `contexts/campaign/services/track_block_service.py`
  - `contexts/campaign/domain/thesis_runtime_state.py`
  - `contexts/campaign/domain/session_store.py`
- Expected outputs:
  - a thinner `CampaignState` shell with stable external seams preserved
  - clearer thesis main write paths and stronger track-local isolation
  - `TrackBlockService` kept as the stable task-area facade but with smaller
    internal rule units
  - updated campaign guardrails/docs for the new phase
- Boundaries:
  - do not treat this as a whole-campaign aggregate promotion
  - do not start visual-runtime / node / rendering refactors here
  - do not widen this into repository-everywhere or shared cleanup
  - do not reopen stable request seams without a concrete trigger
- Current phase judgment:
  - `Phase 0` landed
  - `Phase 1` landed
  - `Phase 2` landed
  - `Phase 3` landed
  - `Phase 4` landed
  - mainline complete: keep this task as closed reference memory, not as the
    default next active move
  - if a change requires broad `view` or `shared` edits, pause and split a
    separate task

### P1. Combat Action Contracts + Queue Skeleton V1

- 鐩爣锛?
  - 寤虹珛鏈€灏?`CombatAction`銆乣ResolutionContext`銆乣ActionQueue`銆乣ActionExecutor`
  - 鍏堟妸鈥滃姩浣滆涔夆€濆拰鈥滈『搴忔墽琛屽叆鍙ｂ€濈珛璧锋潵锛岃€屼笉鏄竴娆℃€ц縼瀹屾墍鏈?effect
- 涓昏杈撳叆锛?
  - `contexts/combat/domain/services/play_card_transaction.py`
  - `contexts/combat/domain/effects/executor.py`
  - `contexts/combat/mvc/model.py`
  - `contexts/combat/domain/chore_host.py`
- 棰勬湡杈撳嚭锛?
  - 涓€鐗堟渶灏忓姩浣滃悎鍚屼笌闃熷垪楠ㄦ灦
  - 涓€缁?focused tests锛岃鐩?`push_front` / `push_back` / `drain`
  - 涓€浠界畝鐭鏄庯紝绾﹀畾鍚庣画鏂板鏉傛満鍒朵紭鍏堣蛋鏂扮紪鎺掑彛
- 杈圭晫锛?
  - 涓嶅垏 UI
  - 涓嶅叏閲忚縼绉诲崱鐗屾晥鏋?
  - 涓嶉『鎵嬮噸鍐?`CombatModel`
- 瀹屾垚鏍囧噯锛?
  - 闃熷垪楠ㄦ灦鍙嫭绔嬫祴璇?
  - 鑷冲皯鍑犵被鍩虹鍔ㄤ綔鍙€氳繃鎵ц鍣ㄧǔ瀹氳惤鐘舵€?
  - 鍚庣画浠诲姟鍙互鍦ㄨ繖濂楅鏋朵笂缁х画涓茶鎺ㄨ繘

### P1. Chore Resolution Orchestration Cutover V1

- 鐩爣锛?
  - 鍏堟妸 `CombatChoreHost` 鐨?resolution actions 骞跺叆缁熶竴鍔ㄤ綔闃熷垪
  - 娑堥櫎 `CombatModel._apply_chore_resolution_actions()` 閲岀殑澶у垎鏀В閲婂櫒
- 涓昏杈撳叆锛?
  - `contexts/combat/domain/chore_host.py`
  - `contexts/combat/mvc/model.py`
  - `contexts/combat/mvc/factory.py`
- 棰勬湡杈撳嚭锛?
  - `ChoreResolutionOrchestrator`
  - `CombatChoreResolutionAction -> CombatAction` 鐨勬槧灏勫眰
  - 浠诲姟瀹夸富鍊掕鏃?/ 鍙戝竷鍚庣画浠诲姟 / 鍙樿韩 / 鏁屼汉 buff 鐨?focused tests
- 杈圭晫锛?
  - 涓嶆墿鍐欐柊鐨?task host 鎶借薄杩愬姩
  - 涓嶆妸 card play 涓昏矾寰勪竴璧峰ぇ鏀?
- 瀹屾垚鏍囧噯锛?
  - chore resolution 涓昏矾寰勫垏鍒版柊闃熷垪
  - 鏃?`_apply_chore_resolution_actions()` 涓昏В閲婇€昏緫鍒犻櫎鎴栭檷涓鸿杽閫傞厤灞?
  - 浠诲姟閾惧紡鍙戝竷鍜屽€掕鏃跺洖褰掍笉閫€鍖?

### P1. Card Play Orchestrator Entry Cutover V1

- 鐩爣锛?
  - 涓哄嚭鐗屽缓绔嬫樉寮忕紪鎺掑叆鍙ｏ紝鍑忓皯鈥渀CardPlayed` 浜嬩欢 + `CombatModel` 璁㈤槄鈥濇壙鎷呬富娴佺▼鐨勭▼搴?
- 涓昏杈撳叆锛?
  - `contexts/combat/domain/player.py`
  - `contexts/combat/domain/services/play_card_transaction.py`
  - `contexts/combat/mvc/model.py`
- 棰勬湡杈撳嚭锛?
  - `CardPlayOrchestrator`
  - 鏄庣‘鐨勫嚭鐗岀紪鎺掑叆鍙ｄ笌鍚庡鐞?checkpoint
  - 涓€浠界畝鐭鏄庯紝璁板綍 `CardPlayed` 鍦ㄨ縼绉绘湡鍐呮槸閫氱煡杩樻槸涓诲叆鍙?
- 杈圭晫锛?
  - 涓嶈姹傛闃舵鎶婃墍鏈?effect 閮芥敼鎴?action
  - 淇濈暀浜嬪姟灞傛牎楠?/ 鎵ｈ垂 / 鍥炴粴閫昏緫
- 瀹屾垚鏍囧噯锛?
  - 鍑虹墝涓昏矾寰勬湁鍗曚竴缂栨帓鍏ュ彛
  - 鍗＄墝鍚庡鐞嗛『搴忔瘮褰撳墠鏇存樉寮?
  - 涓嶅啀缁х画鍚戞棫 `CombatModel` 鐩存墽琛岃矾寰勫爢鏂板鏉傞€昏緫

### P1. High-Frequency Effect Planner V1

- 鐩爣锛?
  - 鍏堟妸楂橀銆佷綆椋庨櫓鍗＄墝鏁堟灉鏀规垚鈥滃厛瑙勫垝鍔ㄤ綔锛屽啀椤哄簭鎵ц鈥?
- 涓昏杈撳叆锛?
  - `contexts/combat/domain/effects/executor.py`
  - `contexts/combat/domain/effects/impl/core.py`
  - 楂橀鎴樻枟鍥炲綊娴嬭瘯
- 棰勬湡杈撳嚭锛?
  - 涓€鐗堟渶灏?`EffectPlanner`
  - 鑷冲皯 4 绫婚珮棰戞晥鏋?action 鍖栵細
    - 鍗曚綋浼ゅ
    - 鏍兼尅
    - 鎶界墝
    - 涓?buff / debuff
- 杈圭晫锛?
  - 涓嶄竴娆℃€ц縼 60 绫?effect
  - pile / pointer / 寮洪殢鏈哄鏉傜墝鍏堜笉姹備竴杞仛瀹?
- 瀹屾垚鏍囧噯锛?
  - 楂橀鏁堟灉閫氳繃 queue 绋冲畾缁撶畻
  - 缁撶畻椤哄簭銆佽繛閿?follow-up 鍜屽悗缁墿灞曠偣鏇存樉寮?
  - 鏃ф墽琛屽櫒鍙繚鐣欐湁闄愬吋瀹圭敤閫旓紝涓嶅啀鎵╂柊閫昏緫

### P1. Combat Post-Resolution Policies V1

- 鐩爣锛?
  - 鎶婃竻鐞嗘浜℃晫浜恒€佸崱鐗屽幓鍚戙€佸紓鑹插悗澶勭悊銆佹垬鏂楃粨鏉熸鏌ユ敹鎴愮粺涓€ checkpoint
- 涓昏杈撳叆锛?
  - `contexts/combat/mvc/model.py`
  - `contexts/combat/domain/services/pile_service.py`
  - `contexts/combat/domain/services/ideal_policy.py`
- 棰勬湡杈撳嚭锛?
  - 涓€缁?post-resolution policy/helper
  - focused regression tests锛屼繚鎶?card route / prune / combat end 椤哄簭
- 杈圭晫锛?
  - 涓嶅仛 UI 渚у姩鐢荤紪鎺?
  - 涓嶉『鎵嬫敼 render state 鍗忚
- 瀹屾垚鏍囧噯锛?
  - 鍑虹墝涓庝换鍔″姩浣滅粨绠楀悗鐨勬敹灏捐矾寰勬洿缁熶竴
  - 椤哄簭閿欒涓嶅啀渚濊禆闅愬紡璋冪敤閾惧厹浣?

### P2. Turn Flow Orchestration V1

- 鐩爣锛?
  - 鏄惧紡鏁寸悊 enemy turn start / end銆乼ask tick銆乼urn checkpoint 鐨勬祦绋嬬偣
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 鍏堟妸 chore resolution 鍜?card play 涓ゆ潯鏈€璐典富璺緞鍒囩ǔ
  - 杩欎竴鍧楅€傚悎鍦ㄥ墠鍑犳绋冲畾鍚庣户缁敹鍙?

## 宸插綊妗ｅ畬鎴愪换鍔★紙鐑尯鍙繚鐣欑储寮曪級

- `Campaign UI Handoff Orchestration`
  - 宸插湪 `2026-03-17` 鏀跺彛锛屽畬鏁村瓙浠诲姟銆佷富瑕佷骇鍑轰笌閲嶅紑鏉′欢瑙?`docs/development/task_pool_archive/2026-03_2026-04_completed.md`
- `Combat Queue Full Cutover` 涓?`Combat Queue Residual Closure`
  - phase-2 涓?residual 鏀跺熬鍧囧凡褰掓。锛宎ctive `red/white` fallback 杈圭晫宸插湪 `2026-03-31` 鏀跺彛鍒?`0`
- `Campaign Aggregate / Orchestration Closure`
  - thesis銆乼ask-area銆丏DD follow-up 鐨勬湰杞敹鍙ｅ凡褰掓。
- `Combat Analysis Capability Iteration V1`
  - 褰撳墠杞凡鍦?`2026-04-05` 瀹屾垚锛涗笅涓€杞簲閲嶆柊鎷嗕换鍔★紝涓嶅啀鎶?V1 checklist 闀挎湡鐣欏湪鐑尯

## 寰呭畾 / 闇€瑕佹洿澶氬墠缃潯浠?

### P2. 涓夌绮捐嫳鍓嶇疆鏈哄埗璇勪及

- 鐩爣锛?
  - 鐩樻竻鈥滃井淇?/ QQ / 閭鈥濅笁绔簿鑻遍渶瑕佺殑鏈€灏忓涓昏兘鍔?
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 澶嶆潅搴﹂珮浜?DDL 绮捐嫳
  - 渚濊禆鏇撮噸鐨勭簿鑻变笓灞炶鍒?

### P2. 鏁屼汉鏁板€煎熀绾?v1

- 鐩爣锛?
  - 缁欐櫘閫氭晫 / 绮捐嫳 / boss 寤虹涓€鐗堟暟鍊兼洸绾?
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - TA 涓婚鏈哄埗杩樺湪缁х画钀藉湴
  - 鐜板湪鍏堝仛鏁板€间細浜х敓鍋囩簿纭?

### P2. 绾㈢櫧鍗＄浜岃疆璋冩暟

- 鐩爣锛?
  - 鍙慨棣栬疆骞宠　鍚庢毚闇茬殑闂鍗?
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 闇€瑕佹洿澶氳瘯鐜╁弽棣?

### P2. Headless 骞宠　妫€鏌?

- 鐩爣锛?
  - 寤虹珛杞婚噺鐨勬棤 UI 骞宠　浣撴
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 鏈哄埗寤鸿浼樺厛绾ф洿楂?

### P2. Combat Chore Host V2锛堝湪 chore resolution cutover 鍚庡啀缁х画锛?

- 鐩爣锛?
  - 鍦ㄧ幇鏈?shared chore host銆侀摼寮?`publish_chore`銆丏DL 鍘嬪姏琛ㄨ揪宸茬粡鍙窇鐨勫熀纭€涓婏紝鎶婄悙浜嬪涓绘矇娣€鎴愭洿绋冲畾鐨勬垬鏂椾腑灞傝兘鍔?
- 褰撳墠宸茶惤鍦板熀绾匡細
  - `CombatChoreHost` 宸叉寕鍒?`CombatState`
  - 鐐瑰悕涓婚鍏变韩瀹夸富銆侀摼寮忓悗缁换鍔°€丏DL 涓€鍥炲悎鍊掕鏃朵笌澶辫触鍒嗘。琛ㄨ揪宸插瓨鍦?
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 褰撳墠鏇撮珮 ROI 鐨勫垏鍙ｆ槸鍏堟妸 resolution path 骞跺叆缁熶竴缂栨帓灞?
  - 鑻ヨ繃鏃╃户缁墿瀹夸富鎶借薄锛屽鏄撳湪涓昏矾寰勫皻鏈垏绋冲墠褰㈡垚鏂扮殑鍙岃建

### P2. Encounter Contract Expansion

- 鐩爣锛?
  - 鎵?encounter / enemy / task-chain 鐨勫唴瀹?contract銆佸瓧娈电害鏉熷拰寮曠敤鏍￠獙
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 褰撳墠鍏堟妸娲昏穬 TA 涓荤嚎鍋氱ǔ
  - 闇€瑕佸湪鐜版湁杩愯閾句笂纭畾鏈€甯歌鐨勫潖鏁版嵁褰㈡€?

### P2. Balance Report Script V1

- 鐩爣锛?
  - 寤虹珛杞婚噺鏁板€间綋妫€鑴氭湰锛屽厛鍋氬紓甯稿彂鐜帮紝涓嶅仛澶嶆潅骞宠　 AI
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 鏁屼汉涓庝换鍔℃満鍒朵粛鍦ㄧ户缁惤鍦?
  - 鐜板湪鍋氭繁骞宠　瀹规槗浜х敓鍋囩簿纭?

### P2. Resource Guardrail Convergence V1

- 鐩爣锛?
  - 鍦ㄧ幇鏈?`scripts/check_resource_contracts.py` 涓?`scripts/check_asset_manifest_consistency.py` 楠ㄦ灦涔嬩笂锛岄€愭鏀舵暃璧勬簮鍏ュ彛涓庢竻鍗曟紓绉?
  - 璁╄祫婧愰棶棰樺敖閲忓湪 repo guard / smoke baseline 闃舵鏆撮湶锛岃€屼笉鏄湪杩愯鏈熸垨鎵撳寘鏈熸墠鍙戠幇
- 褰撳墠宸茶惤鍦板熀绾匡細
  - `repo-guards` 宸插寘鍚?resource contract 涓?asset manifest consistency 妫€鏌?
  - manifest / enum 婕傜Щ宸蹭慨澶?
  - 褰撳墠浠嶆湁涓€鎵?`assets/` 纭紪鐮佽矾寰勫憡璀︼紝涓昏闆嗕腑鍦?campaign / combat / deck / loading / main_menu / shared ui
- 涓昏杈撳叆锛?
  - `scripts/check_resource_contracts.py`
  - `scripts/check_asset_manifest_consistency.py`
  - `scripts/run_repo_smoke_baseline.py`
  - `contexts/shared/infrastructure/assets/`
  - 褰撳墠鍛婅鏂囦欢娓呭崟
- 棰勬湡杈撳嚭锛?
  - 涓€浠芥寜浼樺厛绾у垎缁勭殑璧勬簮鍏ュ彛杩佺Щ娓呭崟
  - 绗竴鎵归珮浠峰€艰繍琛屾椂璺緞浠庣‖缂栫爜 `assets/` 鏀跺彛鍒扮粺涓€璧勬簮鍏ュ彛
  - 鏇村皬鐨?allowlist / 鏇村皯鐨?warning 鏁伴噺
  - 鏉′欢鎴愮啛鏃讹紝鎶婇儴鍒?warning 鍗囩骇涓?hard-fail contract
- 杈圭晫锛?
  - 涓嶅仛涓€娆℃€р€滃叏浠撳簱缁熶竴璧勬簮绯荤粺閲嶅啓鈥?
  - 涓嶄负浜嗚祫婧愭不鐞嗛噸寮€鏁磋疆 UI / rendering 閲嶆瀯
  - 涓嶅湪褰撳墠涓荤嚎浼樺厛绾т箣鍓嶆姠鍗?combat / campaign 涓昏矾寰勫伐浣?
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 璧勬簮 guardrail 楠ㄦ灦宸茬粡钀藉湴锛岀煭鏈熼闄╁凡浠庘€滀笉鍙鈥濋檷鍒扳€滃彲瑙佲€?
  - 鍓╀綑闂涓昏鏄伐绋嬪€烘敹鏁涳紝涓嶆槸闃绘柇褰撳墠杩戞湡涓荤嚎鐨?P0
  - 鏇撮€傚悎鎸夋ā鍧楅『鎵嬫敹鍙ｏ紝鑰屼笉鏄珛鍒诲紑涓€鏉￠噸鍨嬫不鐞嗘敮绾?

### P2. Combat Analysis 涓嬩竴杞媶鍒?

- 褰撳墠鐘舵€侊紙`2026-04-05`锛夛細
  - `Combat Analysis Capability Iteration V1` 宸插畬鎴愬苟褰掓。
  - 涓嬩竴杞笉娌跨敤鏃?checklist锛岀瓑鏍锋湰缂哄彛鍜屾牎鍑嗙洰鏍囨洿娓呮鍚庡啀閲嶆柊鎷嗕换鍔?
- 褰撳墠涓嬩竴杞鍒欙細
  - 淇濇寔 `source facts -> reviewed annotation -> projection`
  - 涓嶇洿鎺ヤ粠鍗＄墝鏂囨湰璺冲叡浜涔?
  - 鍙湁鍚屼竴绉嶅け璐ユā寮忓湪澶氫釜瑙掕壊閲嶅鍑虹幇鏃讹紝鎵嶄笂鍗囦负鍏变韩璇箟
- 褰撳墠寤鸿椤哄簭锛?
  1. 鍏堢ǔ core benchmark
  2. 鍐嶆寜瑙掕壊閫愪釜绋宠緟鍔╁眰
  3. 鍏堟墿楠岃瘉闆嗭紝鍐嶆墿妯″瀷琛ㄩ潰
  4. 杈呭姪灞傜ǔ瀹氬悗锛屽啀缁х画 `enemy pressure -> matchup -> recommendation`
- 褰撳墠榛樿瑙傚療鍏ュ彛锛?
  - 鍏堝埛 `combat_analysis_portfolio_report` 鐪嬬粍鍚堢骇鏁版嵁鐞嗚В锛屽啀鍐冲畾涓嬩竴杞琛ュ摢涓€灞?
- 涓嬩竴杞€欓€夋柟鍚戯細
  - 鎵?STS 姝ｈ礋鏍锋湰涓?near-neighbor
  - 缁х画鍋氶仐鐗?/ 鏃跺簭 / 鐘舵€佽〃杈炬牎鍑?
  - 缁х画鎵╂晫浜?pressure 鎶ュ憡鍙鍖?
  - 缁х画瑙傚療鍊煎緱鍏变韩鍖栫殑鏃跺簭璇箟锛?
    - `hold / retain / cross-turn value`
    - `delayed resolution / delayed payoff`
    - `conditional trigger window`
    - `threshold burst window`
  - 淇濇寔瑙掕壊绉佹湁澶嶆潅搴︾暀鍦?`projection_gap`锛屼笉瑕佽繃鏃╂薄鏌撳叡浜眰
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 鍏堣瀵熸湰杞?benchmark / snapshot / HTML 鎶ュ憡鏄惁绋冲畾
  - 涓嬩竴杞渶濂藉熀浜庢柊澧炲け璐ユ牱鏈噸鏂板畾涔変富鏀荤偣

### P3. 鍐呭鎺ュ叆宸ヤ綔娴?

- 鐩爣锛?
  - 鏂囨。鍖栨柊鍗＄墝 / 鏂版晫浜?/ 鏂扮壒璐ㄦ帴鍏ユ祦绋?
- 褰撳墠涓嶄紭鍏堢殑鍘熷洜锛?
  - 褰撳墠鏇撮渶瑕佸厛鎶?TA 绾垮拰鏁版嵁閾剧户缁仛绋?

## 鏈€杩戝畬鎴?

- `Combat Analysis Capability Iteration V1`
  - 褰撳墠杞畬鎴愬苟宸插綊妗?
- `Combat Queue Full Cutover` / `Combat Queue Residual Closure`
  - active `red/white` fallback 杈圭晫宸插湪 `2026-03-31` 鏀跺彛鍒?`0`
- `Campaign UI Handoff Orchestration`
  - 浜ゆ帴閾惧凡瀹屾垚骞跺凡褰掓。
- `Campaign Aggregate / Orchestration Closure`
  - thesis / task-area / DDD follow-up 鐨勬湰杞敹鍙ｅ凡瀹屾垚骞跺綊妗?
- 鏇存棭瀹屾垚椤癸細
  - 瑙?`docs/development/task_pool_archive/2026-03_2026-04_completed.md`
  - 浠ュ強鏈€杩戝懆鎶ャ€佹棩鎶ヤ笌涓撻」鏂囨。

## 閫€鍑鸿鍒?

褰撳嚭鐜颁互涓嬩换涓€鎯呭喌鏃讹紝浠诲姟搴旇浠庢椿璺冨尯绉昏蛋锛?

- 宸茬粡瀹炵幇
- 琚柊鐨勮璁″喅绛栭樆濉?
- 涓嶅啀閫傚悎褰撳墠鐢熶骇闃舵
- 闇€瑕佹寔缁珮棰戜汉宸ヤ富瑙傚弽棣?
