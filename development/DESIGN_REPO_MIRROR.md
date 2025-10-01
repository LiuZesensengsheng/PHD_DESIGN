# 设计仓库镜像（Design-only Repo Mirror）

目标：只共享 `docs/` 与 `docs/development/` 等设计文件到“设计专用私有仓库”，不暴露源码。

设计仓库地址（SSH）：`git@github.com:LiuZesensengsheng/PHD_DESIGN.git`

## 一次性初始化（Owner 执行）
1) 在 GitHub 新建私有仓库（已建：`PHD_DESIGN`）。
2) 在本机生成部署密钥（Windows PowerShell）：
```powershell
ssh-keygen -t ed25519 -C "design-mirror" -f "$env:USERPROFILE\.ssh\design_mirror_proj"
```
> 提示输入口令时，直接两次回车留空。
3) 将 `design_mirror_proj.pub` 内容添加到设计仓 Deploy keys（Write 权限）。
4) 将 `design_mirror_proj` 私钥内容，添加到主仓 Secrets：`DESIGN_MIRROR_SSH_KEY`。
5) 主仓的 GitHub Actions 已配置于 `.github/workflows/publish-design.yml`。

## 手动首次导出（可选）
在主仓根目录执行：
```powershell
git remote add design-origin git@github.com:LiuZesensengsheng/PHD_DESIGN.git;
git subtree split --prefix=docs -b design-publish;
git push -u design-origin design-publish:main
```
> 若使用 Actions，首次也可由工作流完成。

## 日常使用
- 当 `docs/**` 有变更并合入 `main` 后，Actions 会自动分割并推送到设计仓 `main`。
- 协作者仅被邀请到设计仓；主仓不添加外部协作者。

## 常见问题
- 历史保留：`git subtree split` 会将 `docs/` 的相关历史保留到目标分支。
- 只读站点：可在设计仓启用 GitHub Pages（配合 MkDocs）给更大圈子只读浏览。
- 安全：不要把主仓加入外协；设计仓保持私有，开启分支保护与 PR 审核。
