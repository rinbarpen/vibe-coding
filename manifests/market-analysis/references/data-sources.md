# A 股数据源参考

## AkShare (推荐)

| 属性 | 说明 |
|------|------|
| 官网 | https://akshare.akfamily.xyz/ |
| 安装 | `pip install akshare` |
| Token | 无需 |
| 特点 | 数据全面、更新及时、完全免费 |
| 覆盖 | A股日/分钟/实时、指数、基金、期货、宏观经济 |
| 代理 | 国内环境无需代理 |

**主要接口**:
```python
import akshare as ak

# A股日线（前复权）
df = ak.stock_zh_a_hist(symbol="600519", period="daily",
                        start_date="20240101", end_date="20241231",
                        adjust="qfq")

# 实时行情
df = ak.stock_zh_a_spot_em()

# 指数行情
df = ak.stock_zh_index_daily(symbol="sh000001")

# 龙虎榜
df = ak.stock_sse_summary()
```

## Tushare Pro

| 属性 | 说明 |
|------|------|
| 官网 | https://tushare.pro/ |
| 安装 | `pip install tushare` |
| Token | 需要注册获取（免费用户有积分限制） |
| 特点 | 数据规范、接口稳定，高级数据需付费 |
| 覆盖 | A股日/分钟、财务数据、基本面、公告 |

## 其他数据源

| 数据源 | 特点 |
|--------|------|
| **Yahoo Finance** (`yfinance`) | 全球市场，A 股需 `ticker.SS` 格式，国内访问受限 |
| **东方财富** (EastMoney) | 通过 AkShare 间接获取，数据质量高 |
| **新浪财经** (Sina Finance) | 实时行情数据，通过 API 获取 |