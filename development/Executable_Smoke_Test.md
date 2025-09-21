# 可执行包自测（Executable Smoke Test）方案

> 目的：在“不进入源码环境”的前提下，对打包产物（dist/ 内的 exe）进行自动化冒烟测试，覆盖“能启动 → 进入关键场景 → 出现关键 UI/日志标记 → 无崩溃”的最小闭环。人工测试只做体验验收。

## 一、测试范围与目标
- 启动可靠性：双击与命令行均可启动；窗口化默认（F11 切换全屏）。
- 资源可用性：字体/贴图/主题/JSON 等关键资源可被找到；无 FileNotFoundError。
- 关键流程：MAIN_MENU → LOADING → CAMPAIGN → COMBAT → 奖励 → 返回 的日志检查点出现。
- 崩溃监控：dist/<name>/bundled_crash.log 不产生，或为空（含完整 traceback 以便定位）。

## 二、运行环境与输入通道
- 环境变量（无需改包体）：
  - FORCE_WINDOWED=1|0：窗口/全屏（打包默认 1）。
  - LOG_LEVEL=INFO|DEBUG（可扩展，当前日志已基本可用）。
  - AUTOTEST_SCRIPT=tests/runtime_scenarios/<xxx>.json（可扩展，用于自动注入 UI 事件）。
  - RNG_SEED=<int>：固定随机性（可扩展）。
- 外置配置/资源（直接改 dist/ 即生效）：theme.json、logging_config.json、assets/、data/。
- 启动脚本：建议在 dist 下提供 run_with_env.cmd（见附录）。

## 三、冒烟测试：一键命令（PowerShell）
> Windows 场景；按要求用分号 ; 连接多条命令。

```powershell
# 1) 构建 one-folder 产物（含资源）
python scripts\build_windows.py --clean --name "smoke_dev";

# 2) 运行并采集日志（不阻塞 UI）
& ".\dist\smoke_dev\smoke_dev.exe" *>&1 | Tee-Object ".\dist\smoke_run.log";

# 3) 判定：无崩溃日志、出现关键检查点
if (Test-Path ".\dist\smoke_dev\bundled_crash.log") { throw "Crash log exists" };
Select-String -Path ".\dist\smoke_run.log" -Pattern "Changed state to: MAIN_MENU" | Out-Null;
Select-String -Path ".\dist\smoke_run.log" -Pattern "Changed state to: LOADING" | Out-Null;
Select-String -Path ".\dist\smoke_run.log" -Pattern "Changed state to: CAMPAIGN" | Out-Null;
```

说明：
- 初次运行若黑屏，可按 F11 在全屏/窗口间切换；日志仍会输出到 smoke_run.log。
- 关键资源缺失会在 bundled_crash.log 中体现（含完整 traceback）。

## 四、（可选）自动试玩脚本 AUTOTEST_SCRIPT
> 需要更“像人”的自动化时启用，默认可不需要。脚本描述一段“输入事件 + 断言”。

脚本格式（JSON 草案）：
```json
{
  "seed": 12345,
  "steps": [
    { "type": "wait", "ms": 1000 },
    { "type": "click", "x": 960, "y": 540 },
    { "type": "key", "key": "SPACE" },
    { "type": "drag", "from": [1200, 900], "to": [1200, 300] },
    { "type": "assert_log", "contains": "Opening reward modal" }
  ],
  "success_mark": "CHECKPOINT_OK"
}
```
执行方式：
```powershell
$env:AUTOTEST_SCRIPT = "tests\runtime_scenarios\basic_reward.json"; 
& ".\dist\smoke_dev\smoke_dev.exe" *>&1 | Tee-Object ".\dist\smoke_run.log";
Select-String -Path ".\dist\smoke_run.log" -Pattern "CHECKPOINT_OK" | Out-Null;
```

实现思路：
- 在游戏主循环中（仅测试模式）读取 AUTOTEST_SCRIPT，按顺序注入 pygame 事件（UIManager 前置处理）。
- 每个步骤执行后可 sleep 指定毫秒，或等待指定日志标记。
- 脚本最后输出 CHECKPOINT_OK，供 CI/脚本断言。

## 五、CI 集成建议（本地也可一键跑）
1) 代码质量：ruff、mypy、pytest -q（含无头集成测试）。
2) 构建：python scripts/build_windows.py --clean --name CI。
3) 冒烟：如第三章。失败则输出 smoke_run.log 与 bundled_crash.log 作为工件。

## 六、常见问题与排错
- 黑屏但不崩溃：
  - 按 F11 切换全屏/窗口；确保 FORCE_WINDOWED=1。
  - 检查 theme.json 与字体路径是否存在；必要时替换为系统字体。
- FileNotFoundError：
  - 将缺失的文件/目录补入 scripts/build_windows.py 的 --add-data 列表；或统一改为 get_resource_path() 加载。
- 双击崩溃看不到信息：
  - 查看 dist/<name>/bundled_crash.log（含完整 traceback）。

## 七、附录：run_with_env.cmd（建议随包分发）
```cmd
@echo off
set FORCE_WINDOWED=1
set LOG_LEVEL=INFO
REM set AUTOTEST_SCRIPT=tests\runtime_scenarios\basic_reward.json
"%~dp0smoke_dev.exe" 1> "%~dp0run.log" 2>&1
pause
```

---
维护：本文件针对 Windows/PowerShell 场景编写。若迁移到 Linux/Mac，请用 shell 语法替换示例命令，并将 `;` 改为 `&&` 或分行。
