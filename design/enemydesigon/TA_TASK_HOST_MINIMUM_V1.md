# TA 第三批前置机制评估：迟到学生 / 代到学生的最小琐事宿主 v1

## 目标

这份文档只回答一个问题：

**为了实现“迟到学生 -> 代到学生”这一组点名主题敌人，战斗系统最小需要补什么样的琐事宿主？**

术语说明：

- 本文在 TA 线设计语义上，把玩家不断被迫处理的 `task` 统一称为“琐事”。
- 当前工程代码已经以 `chore` / `chore_host` / `publish_chore` 为主；文中出现 `task` / `task_host` / `publish_task` 时应视为兼容别名。

这轮不追求完整 TA 琐事系统，也不追求“一次支持所有主题”。
目标是给第三批敌人实现提供一个**足够小、但不走回头路**的中层方案。

## 结论先说

实现迟到学生 / 代到学生，**不需要先做完整的 TA 全局琐事系统**。

最小可行方案是：

1. 在 combat runtime 里新增一个**战斗内琐事宿主**，只支持少量琐事对象
2. 第一版只支持**共享倒计时 + 单条琐事发布 + 失败回调**
3. 迟到学生本身不直接内建倒计时逻辑，而是：
   - 进入战斗时由 encounter 或 enemy passive 发布一件琐事
   - 琐事倒计时结束后，通过失败回调把迟到学生转换成代到学生

一句话：

**先做“战斗内 deadline 琐事宿主”，不要先做完整 TA 琐事系统。**

## 为什么现在不能直接做

当前战斗系统已经支持：

- 敌人 intent / passive
- 多敌人战斗
- `progress` / `insight` / `flee_next` 这类敌人状态条件
- 主运行链的 `species.json + skills.json + encounter`

但当前还没有：

- 战斗内琐事对象宿主
- 共享倒计时
- 琐事完成/失败事件
- 失败后替换敌人的正式入口

所以“迟到学生”的真正前置不是数值，而是：

**一个能在战斗里挂 deadline 琐事并触发失败结果的最小宿主。**

## 最小琐事宿主应该承载什么

### 1. 琐事实例

最小琐事实例建议至少有这些字段：

- `task_id`
- `title`
- `kind`
- `target_enemy_id`
- `countdown`
- `max_countdown`
- `on_success`
- `on_failure`
- `completed`
- `failed`

说明：

- `kind` 第一版其实只需要一种：
  - `eliminate_target_before_deadline`
- `target_enemy_id` 用来绑定迟到学生
- `on_failure` 不直接写复杂脚本，只保存一个结构化结果，例如：
  - `transform_enemy`
  - `spawn_enemy`
  - `apply_enemy_buff`

### 2. 琐事宿主状态

最小琐事宿主建议作为 combat runtime object，挂在 `CombatState` 上。

建议字段：

- `tasks`
- `max_slots`
- `shared_countdown`
- `shared_max_countdown`
- `enabled`

但为了最小化，本轮推荐：

- `max_slots = 1`

原因：

- 迟到学生 / 代到学生只需要验证 deadline 琐事这条链
- 不值得一上来就把“最多 3 个琐事”完整做完
- 接口可以先按未来能扩到 3 的形式设计，但运行上先只支持 1

### 3. 最小行为

琐事宿主第一版只需要支持 4 个动作：

1. `publish_task(task)`
2. `complete_task(task_id)`
3. `tick_countdown()`
4. `collect_resolution_actions()`

说明：

- `publish_task`：在迟到学生登场或某个 trigger 满足时发布琐事
- `complete_task`：当目标敌人死亡或被视为处理完时完成琐事
- `tick_countdown`：按固定时机把共享倒计时 -1
- `collect_resolution_actions`：把成功/失败要触发的动作交给上层执行，不由琐事宿主直接改敌人列表

## 最小琐事宿主不应该承载什么

为了避免第一版过重，这些东西本轮明确不做：

- 最多 3 个琐事同时存在的完整规则
- 完整的主题琐事池抽取
- 任意琐事完成后重置到 3 的全局通用规则
- 复杂琐事条件（打出几张牌、同色/异色统计）
- DDL 压缩规则
- 三端复活规则
- UI 演出层

也就是说：

**第一版只做“deadline 目标击杀/处理琐事”。**

## 推荐挂载位置

### 推荐

新增类似：

- `contexts/combat/domain/task_host.py`

并在：

- `contexts/combat/domain/state.py`

里给 `CombatState` 增加：

- `task_host: Optional[CombatTaskHost] = None`

### 为什么不建议挂在 Enemy 上

因为“迟到学生琐事”本质上不是敌人私有状态，而是：

- 战斗内公共压力对象
- 以后要被 UI、倒计时、失败惩罚、多个敌人共享引用

所以它更像 combat runtime 子系统，而不是单敌人 passive。

## 推荐时序

### 最小时序

第一版推荐这样跑：

1. 遭遇开始
   - 发布一件绑定迟到学生的琐事
   - 倒计时设为 3

2. 每个敌方回合开始
   - `task_host.tick_countdown()`

3. 如果迟到学生在倒计时前被击破/处理
   - `complete_task(task_id)`
   - 本次不触发失败分支

4. 如果倒计时归零且琐事未完成
   - 琐事宿主产出一个 resolution action：
     - `transform_enemy(late_student -> proxy_student)`

5. 上层 orchestrator 应用这个 action

### 为什么推荐“敌方回合开始”计时

因为这样最稳定：

- 玩家每轮有完整窗口处理琐事
- 时机容易和敌人战斗节奏对齐
- 不需要新建额外 phase

## 迟到学生 / 代到学生的最小落地表达

### 迟到学生

第一版不必让它拥有复杂技能树。

最小表达可以是：

- 遭遇开始时对应一个“某人的空桌子”琐事
- 本体只有很轻的骚扰意图
- 核心压力来自倒计时

失败后：

- 转换成代到学生

### 代到学生

第一版可以不依赖琐事宿主继续存活，只作为失败结果怪存在。

最小表达：

- 从迟到学生失败转换而来
- 提供稳定但烦人的低压多段伤害或全体支持
- 不再继续生成 deadline 琐事

这样能把“迟到 -> 代到”的戏剧性先做出来，而不用一次做完整点名系统。

## 附带需要的最小辅助机制

除了琐事宿主本体，还需要两个很薄的配套点：

### A. 敌人替换/变换入口

需要一个最小 action 应用能力，例如：

- 删除一个敌人
- 在相同索引位置生成另一个 species

这不一定要做通用大系统，但至少要让：

- `迟到学生 -> 代到学生`

这条链能跑。

### B. 琐事完成判定入口

第一版只要支持：

- 目标敌人死亡时，相关 task 自动完成

不需要更复杂的条件解析器。

## 推荐实现顺序

### 第一步

新增最小 `CombatTaskHost`

只支持：

- 单琐事
- 倒计时
- 目标敌人绑定
- 成功/失败 resolution action

### 第二步

在 `CombatState` 挂上 `task_host`

并在战斗 turn 时机里加：

- `tick_countdown()`

### 第三步

补一个最小 enemy transform 应用点

支持：

- 迟到学生失败时替换为代到学生

### 第四步

把迟到学生 / 代到学生接入 TA CSV 敌人链

## 不建议的错误做法

1. 一上来就做完整 3 槽琐事系统
2. 把琐事倒计时逻辑硬写进迟到学生 enemy flags
3. 让琐事宿主直接修改敌人列表
4. 顺手把 DDL 和三端一起做了

这些都会把第三批前置机制从“小中层”做成“大系统”。

## 当前建议

如果下一步要真正开始实现第三批点名主题敌人，推荐顺序是：

1. 先做 `CombatTaskHost` 最小版
2. 只服务 `迟到学生 / 代到学生`
3. 验证“deadline -> failure -> enemy transform”这条链
4. 之后再决定是否扩成 TA 通用琐事系统

## 最终判断

**迟到学生 / 代到学生的最小前置，不是完整 TA 琐事系统，而是一个只支持 deadline 目标琐事的战斗内琐事宿主。**

这是当前最小、最稳、也最不容易返工的切法。
