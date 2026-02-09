# 防幻觉引用工作流 (Citation Workflow)

**核心原则**: 永远不要凭记忆编写 BibTeX。AI 生成的引用错误率极高。

## 验证流程 (MANDATORY)

1. **搜索 (Search)**: 使用 Exa MCP 或 Web Search 查找论文。
2. **验证 (Verify)**: 在 Semantic Scholar 或 arXiv 上确认论文标题、作者和年份。
3. **获取 BibTeX (Fetch)**: 通过 DOI 或 arXiv ID 获取原始 BibTeX 数据。
4. **标记 (Mark)**: 
   - 验证成功：直接使用。
   - 验证失败：标记为 `[CITATION NEEDED]` 或 `\cite{PLACEHOLDER_author2024_verify}`。

## 推荐工具

### 1. Exa MCP (学术搜索)
```bash
# 示例查询
"Find papers on RLHF for language models published after 2023"
```

### 2. Semantic Scholar API
用于验证论文 ID 和获取元数据。

### 3. DOI to BibTeX
```python
import requests

def doi_to_bibtex(doi: str) -> str:
    response = requests.get(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"}
    )
    return response.text
```

## 失败处理
如果你无法通过程序验证引用，必须告知用户：
> "我无法验证以下引用，已将其标记为占位符，请手动核实：
> - [Author et al., 2024] 关于 X 的论述"
