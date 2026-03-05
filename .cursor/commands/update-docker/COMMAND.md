---
description: 自动更新 Docker 配置，确保 Dockerfile、docker-compose.yml 与项目依赖和入口保持一致。
globs: ["Dockerfile", "docker-compose*.yml", "*.dockerfile"]
---

# Update Docker Command

此规则定义了 `/update-docker` 命令，用于保持 Docker 配置与项目状态同步。

## 命令定义

### `/update-docker`

**目的**: 根据项目当前的依赖、入口、环境变量等，更新 `Dockerfile`、`docker-compose.yml` 等 Docker 配置。

**使用方式**: 在对话框中输入 `/update-docker`。

**执行逻辑**:
1. **分析项目**: 扫描 `pyproject.toml`、`package.json`、`requirements.txt` 等获取依赖和入口。
2. **检查现有配置**: 读取 `Dockerfile`、`docker-compose*.yml` 等。
3. **执行更新**: 运行 `python3 .cursor/commands/update-docker/update_docker.py`。
4. **同步**: 确保镜像构建命令、端口映射、卷挂载与项目实际状态一致。

**示例**:
- `/update-docker`
