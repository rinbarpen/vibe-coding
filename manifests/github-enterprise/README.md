# GitHub Enterprise Development Manifest

面向 GitHub 企业级项目开发治理的独立 manifest 包。

## 适用场景

需要一个完整的 GitHub 项目治理基础设施的项目：
- 分支策略和命名规范
- PR 标题强制和大小审查
- CI/CD 自动化和质量控制
- Release 和 tag 管理
- Issue 分类和路由
- 安全扫描和依赖管理
- 文档站点和 README 规范

## 文件清单

详见 CLAUDE.md 中的完整目录树和各文件说明。

## 使用方式

```bash
# 将 manifest 初始化到目标项目
./scripts/init-enterprise.sh /path/to/your/project
```

初始化后：
1. 编辑 `.github/CODEOWNERS` 填入真实的 owner 和 team
2. 编辑 `.github/SECURITY.md` 填入 security contact 信息
3. 在 GitHub Web UI 中配置 branch protection rules
4. 根据需要调整 workflows 中的语言版本矩阵

## 依赖

- GitHub 仓库
- GitHub Actions 已启用
- 需要配置的 secrets：`GITHUB_TOKEN`（默认可用），`CODECOV_TOKEN`（如需覆盖率报告）
