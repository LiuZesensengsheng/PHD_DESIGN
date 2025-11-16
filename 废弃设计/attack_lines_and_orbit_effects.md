### 行星环绕与飞剑光线效果 - 技术纪要

本文记录当前两个原型的核心技术实现、调参入口，以及问题与解决方案清单。

- 相关文件
  - `linshi/card_orbit_min.py`：环绕“灯带”+中心贴图+局部法线起伏的最小延迟光照原型
  - `linshi/attack_lines_min.py`：中心贴图+飞剑光线（线段）+线即光源+背景底图

---

### 渲染管线（两者通用）
1) 几何通道 G-Pass（离屏FBO）：
   - 输出 `g_albedo`（RGBA）、`g_normal`（RGB）和深度纹理（depth attachment）。
   - 透明像素直接丢弃，避免错误受光与遮挡。
   - 背景作为全屏四边形绘制到最远层（深度≈-1），采用小的圆角半径避免SDF门槛导致 alpha≈0。
2) 光照合成 Light-Pass（全屏）：
   - 读取 `g_albedo`、`g_normal`、必要时读取 `g_depth` 做遮挡判断。
   - 可配置主光（Key Light）。
   - 其他光源（环绕灯、飞剑线采样点）逐像素叠加，按法线余弦项与距离衰减。
3) 特效叠加（Additive）：
   - 轨迹/线段独立通道以加法混合绘制；其片元使用 `g_depth` 做遮挡裁剪。

---

### 技术手段与要点
- 延迟光照（Deferred Shading）：
  - 先存几何，再单独做全屏光照，便于统一遮挡与多光源叠加。
  - 深度比较以统一的映射：`depth_ndc = (-u_depth + 1.0) * 0.5`，范围 [0..1]。

- 背景底图：
  - 在 G-Pass 以全屏四边形绘制，`gp_depth≈-0.98`，`gp_radius` 给一个小正值（例如 8.0），确保 alpha=1。否则 SDF 的 0 边界可能导致整体透明。

- 环绕“灯带”（Orbit 最小版）：
  - 环绕体不可见但写深度，用作遮挡；光源跟随其位置移动。
  - 中心贴图使用“伪圆柱法线”+带状小幅时间扰动（仅法线变化，位置不动）实现局部起伏高光。

- 飞剑光线（Attack-Lines 最小版）：
  - 屏幕空间横向线段（矩形）+软边厚度，前后分层（前景/后景在深度上区分）。
  - “线即光源”：每条线取若干采样点（默认3）作为点光传给 Light-Pass，颜色使用青色；并使用 `u_ll_depth` 与 `g_depth` 做遮挡。

- 调参入口（部分）：
  - Orbit：`CENTER_SIZE`、环绕半径/速度、法线扰动强度、主光强度与半径等。
  - Attack-Lines：`NUM_LINES`、`LINE_*`（速度/长度/厚度/透明度）、`FRONT_RATIO`、`KEY_LIGHT_*`、线光每条采样点数量与半径/强度等。

- 性能策略：
  - 复用 VAO/FBO/Program；
  - 控制线光采样密度（3→5）与半径/强度；
  - 必要时可将 Light-Pass 降分辨率再上采样。

- 调试工具：
  - Attack-Lines: 运行时按键切换：`0` 正常光照、`1` 直接显示 `g_albedo` RGB、`2` 显示 `g_albedo` Alpha。

---

### 常见问题与解决办法（问题 → 解决）
- 看不到背景：
  - 原因：背景 SDF 圆角半径为 0，`smoothstep(0,1,-dist)` 在边界会给近 0 的 alpha，被整体当作透明；或背景深度设为 -1.0 某些驱动不写入。
  - 解决：将 `gp_radius` 设为小正值（如 8.0）确保 alpha=1；将背景深度改为 `-0.98` 并开启深度写入。

- `KeyError: 'g_depth'`：
  - 原因：Light-Pass 着色器里未声明 `g_depth` 却在 CPU 侧绑定；或我们移除后又在代码引用。
  - 解决：一致化——若需要遮挡（线光），在 shader 中声明并绑定；否则移除 CPU 绑定。

- 飞剑线不可见：
  - 原因：未给线片元 shader 绑定 `g_depth`；或线的 `u_depth` 取值错误；或加法混合但 alpha≈0。
  - 解决：在绘线前 `g_depth.use(2)`；前景设 `u_depth≈+0.6`，后景 `≈-0.6`，中心 `0.0`；线段 alpha 与厚度适当调高。

- Uniform 读取报错 `TypeError: 'Uniform' object cannot be interpreted as an integer`：
  - 原因：错误地将 `Program` 当 dict 使用 `get()`；返回的是 Uniform 对象，不能当作大小。
  - 解决：不使用 `get()`；统一直接赋值 `program['name'].value = ...`；数组类 uniform 先构造完整列表并填充到固定上限。

- 调试视图 `NameError: debug_prog is not defined`：
  - 原因：未在 `run()` 初始化阶段创建 debug program/VAO。
  - 解决：在程序初始化时创建 `debug_prog` 与 `debug_vao`，并在按键分支中渲染。

---

### 运行方式
- 环绕最小版：
  - `python linshi/card_orbit_min.py`
- 飞剑最小版：
  - `python linshi/attack_lines_min.py`
  - 运行时按 `0/1/2` 切换视图用于定位。

---

### 后续建议
- Light-Pass 半分辨率渲染+上采样，进一步降本。
- 线光采样自适应：按线长动态增加光样本密度；近处更密，远处更疏。
- 环绕与飞剑两种特效的统一材质系统（可共享颜色/亮度主题与遮挡规则）。
