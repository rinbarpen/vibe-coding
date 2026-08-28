# AutoFigure + OmniRoute + SAM3（4090）设计规格

## 目标

让当前工作区的 AutoFigure-Edit 支持以下运行组合：

- SAM3 使用 4090 主机的本地 GPU 后端；
- 文本推理和 SVG 重建通过 OmniRoute 的 OpenAI 兼容接口；
- 默认模型为 `gpt-5.6-luna`，推理强度为 `high`；
- API Key、主机地址和权重路径通过环境变量或命令行传入，不写入版本库。

## 架构与数据流

```text
method text / PDF
        |
        v
AutoFigure-Edit
  |-- step 1: image generation (configurable provider)
  |-- step 2: local SAM3 on 4090 -> masks / icon crops
  |-- step 3-4: OmniRoute /v1 -> text + multimodal SVG reconstruction
  `-- outputs -> PNG + editable SVG + intermediate artifacts
```

OmniRoute 的默认地址使用 `http://127.0.0.1:20128/v1`，同时保留
`OMNIROUTE_BASE_URL` 覆盖项，适配远程 OmniRoute 主机。模型和推理强度分别由
`OMNIROUTE_MODEL` 与 `OMNIROUTE_REASONING_EFFORT` 控制。

## 配置接口

新增 CLI 参数：

- `--reasoning_effort {minimal,low,medium,high,xhigh}`
- `--omniroute`：使用 OmniRoute 预设

新增环境变量：

- `OMNIROUTE_BASE_URL`，默认 `http://127.0.0.1:20128/v1`
- `OMNIROUTE_MODEL`，默认 `gpt-5.6-luna`
- `OMNIROUTE_REASONING_EFFORT`，默认 `high`
- `OMNIROUTE_API_KEY`，不提供默认值
- `SAM3_REPO`、`SAM3_CHECKPOINT`、`SAM3_DEVICE`，用于 4090 本地部署

OmniRoute 请求仅在 provider 为 `openai_response` 或 `custom` 时启用
`reasoning.effort`。对于不接受该字段的兼容路由，提供显式关闭值并保留原有调用路径。

## 4090 部署

添加可重复执行的部署脚本，完成：

1. 检查 NVIDIA 驱动、CUDA 可见设备和显存；
2. 创建 Python 3.12+ 虚拟环境；
3. 安装 PyTorch/CUDA 依赖及 SAM3；
4. 写出不含密钥的 `.env.sam3-4090.example`；
5. 用 `--sam_backend local` 启动 AutoFigure-Edit；
6. 运行导入、编译和本地 SAM3 加载检查。

当前 Codex 沙箱未暴露 NVIDIA 设备，因此 4090 的 GPU 加载检查在目标机器上执行；本地静态检查和配置检查在当前工作区完成。

## 错误处理与回滚

- OmniRoute 不可达：保留原始 provider 参数，命令立即报告连接错误；
- SAM3 权重缺失：启动前报告路径，不自动下载受限权重；
- 模型拒绝 `reasoning` 字段：通过显式关闭参数回到兼容请求格式；
- 回滚：删除新增脚本和配置入口，恢复 `autofigure2.py` 的原始 provider 默认值；源码目录和已生成 outputs 不删除。

## 验证标准

- 单元测试覆盖 OmniRoute 默认值、CLI 参数和 reasoning payload；
- `py_compile` 通过；
- `/healthz` 返回 `{"status":"ok"}`；
- 4090 目标机上 `torch.cuda.is_available()` 为真且 SAM3 device 为 `cuda:0`；
- 真实生成测试输出 `figure.png`、`final.svg`，且 SVG 可被编辑器打开。

