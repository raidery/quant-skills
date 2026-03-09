---
name: wencai
description: Query Chinese A-share stock market data using natural language through pywencai library (同花顺问财). Use when user needs to (1) Query A-share stock data with keywords like 问财, wencai, 股票查询, (2) Search stocks by conditions like 涨停股, 龙头股, 高ROE, (3) Query financial metrics like 市盈率, 净利润, 营收, (4) Query technical indicators like MACD, KDJ, 均线, (5) Analyze sector/industry information like 板块, 概念股. Triggers on 问财, wencai, A股, 股票查询, or any Chinese stock market queries.
---

# Wencai (问财) - A股市场数据查询

## Overview

通过 pywencai 库使用自然语言查询 A 股市场数据，包括实时行情、财务指标、技术面数据和板块信息。

## Quick Start

基本查询示例：

```python
from scripts.query_wencai import query_wencai

# 查询涨停股
result = query_wencai("今日涨停股")
print(result)

# 查询高ROE股票，按ROE降序排列
result = query_wencai(
    query="ROE大于20%的股票",
    sort_key="ROE",
    sort_order="desc",
    max_rows=20
)
print(result)
```

## Cookie 配置

pywencai 需要 cookie 才能使用。支持三种配置方式（按优先级）：

### 方式 1: 函数参数（优先级最高）
```python
result = query_wencai("涨停股", cookie="your_cookie_here")
```

### 方式 2: 环境变量
```bash
export WENCAI_COOKIE="your_cookie_here"
```

### 方式 3: 配置文件
创建 `~/.wencai/config.json`：
```json
{
  "cookie": "your_cookie_here"
}
```

**获取 cookie 方法：**
1. 访问 https://www.iwencai.com/
2. 登录后打开浏览器开发者工具（F12）
3. 切换到 Network 标签
4. 刷新页面，找到任意请求
5. 复制请求头中的 Cookie 字段值

## Query Workflow

1. **准备查询** - 用自然语言描述查询条件
2. **调用函数** - 使用 `query_wencai()` 执行查询
3. **数据处理** - 自动清洗列名、精简列、限制行数
4. **返回结果** - 获得 Markdown 表格格式的结果

## Parameters

### query (必填)
自然语言查询语句，例如：
- "今日涨停股"
- "市盈率小于20且ROE大于15%的股票"
- "机器人概念股"
- "退市股票"

### query_type (可选，默认 'stock')
查询类型：
- `stock` - 股票（默认）
- `zhishu` - 指数
- `fund` - 基金
- `conbond` - 可转债

### max_rows (可选，默认 15)
限制返回的行数，节省 context 空间

### loop (可选，默认 False)
是否循环获取多页数据：
- `False` - 只返回第一页
- `True` - 返回所有页
- `数字` - 返回指定页数

### sort_key (可选)
排序字段，值为返回结果的列名，例如 "涨跌幅"、"ROE"

### sort_order (可选，默认 'desc')
排序方式：
- `desc` - 降序
- `asc` - 升序

### cookie (可选)
Cookie 参数，优先级最高

## Data Processing

### 列名清洗
自动去除日期前缀：
- `20260309[最新涨跌幅]` → `涨跌幅`
- `退市@退市日期` → `退市日期`

### 关键列提取
智能保留重要列：
- 基础信息：代码、名称
- 价格数据：现价、涨跌幅、涨跌额
- 交易数据：成交量、成交额
- 估值指标：市值、市盈率
- 分类信息：板块、行业、概念

### 行数限制
通过 `max_rows` 参数控制返回行数，默认 15 行

## Error Handling

### 空结果
```
当前未搜索到符合条件的标的
```

### 网络错误
```
查询超时，请稍后重试
网络请求失败：[错误详情]
```

### Cookie 错误
```
未找到 cookie，请通过参数、环境变量或配置文件提供
```

### 其他错误
所有错误都会被捕获并返回友好提示，同时记录到日志

## Advanced Usage

### 复杂查询
```python
# 查询符合多个条件的股票
result = query_wencai(
    query="市盈率小于30且市净率小于3且ROE大于10%的股票",
    sort_key="ROE",
    sort_order="desc",
    max_rows=30
)
```

### 分页查询
```python
# 获取前3页数据
result = query_wencai(
    query="涨停股",
    loop=3,
    max_rows=50
)
```

### 指数查询
```python
# 查询指数
result = query_wencai(
    query="上证指数",
    query_type="zhishu"
)
```

## Query Examples

详细查询示例请参考 [references/query_types.md](references/query_types.md)

## Notes

1. **低频使用** - 建议低频调用，避免被问财屏蔽
2. **Cookie 有效期** - Cookie 可能过期，需要定期更新
3. **Node.js 依赖** - pywencai 需要 Node.js v16+ 环境
4. **数据延迟** - 问财数据可能有延迟，非实时数据
