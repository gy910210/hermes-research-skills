# Publish Guide

## 首版发布建议

建议 tag：`v0.1.0-zh`

## GitHub 发布步骤

```bash
git add .
git commit -m "feat: initial Chinese release of Hermes research skills"
git push origin main
git tag v0.1.0-zh
git push origin v0.1.0-zh
```

如果本机安装了 Hermes skills 发布链路，可继续尝试：

```bash
hermes skills publish skills/research-orchestrator-zh --to github --repo gy910210/hermes-research-skills
```

也可以先只把 GitHub 仓库作为 tap 源分发。
