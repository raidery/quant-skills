# quant-skills

Quantitative finance skills for Claude Code - 为 Claude Code 提供量化金融数据查询能力。

## 📋 项目简介

本项目为 Claude Code 提供 A 股市场数据查询功能，通过 [pywencai](https://github.com/zsrl/pywencai) 库实现自然语言查询同花顺问财数据。

## 🚀 快速开始

### 环境要求

- **Python 3.6+**
- **Node.js v16+** （pywencai 内部执行 JS 代码需要）
- **pywencai 库**：`pip install pywencai`

### 验证环境

```bash
python wencai/scripts/check_environment.py
```

### 获取 Cookie

所有查询都需要问财 Cookie：

1. 访问 https://www.iwencai.com/ 并登录
2. 打开浏览器开发者工具（F12）
3. 切换到 Network 标签
4. 刷新页面，找到任意请求
5. 复制请求头中的 Cookie 字段值

### 配置 Cookie

**方式 1：环境变量（推荐）**
```bash
export WENCAI_COOKIE="your_cookie_here"
```

**方式 2：配置文件**
```bash
mkdir -p ~/.wencai
cat > ~/.wencai/config.json << 'EOF'
{
  "cookie": "your_cookie_here"
}
EOF
```

**方式 3：代码中传入**
```python
result = pywencai.get(query='涨停股', cookie='your_cookie_here')
```

## 📦 项目结构

```
quant-skills/
├── wencai/                          # 生产版 Skill（直接使用 pywencai）
│   ├── SKILL.md                     # Skill 文档（英文为主）
│   ├── README.md                    # 使用说明
│   ├── scripts/
│   │   └── check_environment.py     # 环境检查脚本
│   └── references/
│       ├── api_reference.md         # API 完整参数文档
│       └── query_examples.md        # 查询示例大全
│
├── pywencai/                        # 开发版 Skill（封装版本）
│   ├── TEST_GUIDE.md                # 测试指南
│   ├── test_comprehensive.py        # 综合测试脚本
│   └── wencai/
│       ├── SKILL.md                 # Skill 文档（中文为主）
│       ├── scripts/
│       │   └── query_wencai.py      # 封装的查询脚本
│       └── references/
│           └── query_types.md       # 查询类型示例
│
├── CLAUDE.md                        # Claude Code 项目指南
├── .gitignore                       # Git 忽略规则
└── README.md                        # 本文件
```

## 🔧 两个版本说明

### wencai/ - 生产版本

**特点：**
- 直接使用 `pywencai.get()` API
- 适合熟悉 pywencai 的用户
- 文档以英文为主，面向国际用户
- 包含完整的 API 参考和查询示例

**使用示例：**
```python
import pywencai

result = pywencai.get(
    query='市盈率小于20且ROE大于15%',
    cookie='your_cookie_here',
    sort_key='涨跌幅',
    sort_order='desc'
)
print(result)
```

### pywencai/ - 开发版本

**特点：**
- 封装了 `query_wencai()` 函数
- 自动处理列名清洗和数据精简
- 返回 Markdown 格式表格
- 文档以中文为主
- 包含测试脚本和指南

**使用示例：**
```python
from pywencai.wencai.scripts.query_wencai import query_wencai

# 简单查询
result = query_wencai("今日涨停股")
print(result)

# 高级查询
result = query_wencai(
    query="ROE大于20%的股票",
    sort_key="ROE",
    sort_order="desc",
    max_rows=20
)
print(result)
```

## 💡 使用示例

### 基础查询

```python
# 涨停股
pywencai.get(query='今日涨停股', cookie=cookie)

# 高 ROE 股票
pywencai.get(query='ROE大于20%', cookie=cookie)

# 板块查询
pywencai.get(query='新能源汽车板块', cookie=cookie)
```

### 技术指标查询

```python
# MACD 金叉
pywencai.get(query='MACD金叉', cookie=cookie)

# 均线突破
pywencai.get(query='突破60日均线', cookie=cookie)
```

### 多条件组合查询

```python
query = """
涨幅大于1%，大单金额大于5000万，10日内ma10金叉ma60，
月macd大于0，流通市值大于50亿，收盘价大于ma10
""".replace("\n", "").strip()

result = pywencai.get(
    query=query,
    cookie=cookie,
    loop=True,      # 获取所有页
    perpage=100,    # 每页100条
    log=True        # 显示日志
)
```

### 排序和分页

```python
# 按涨幅排序
pywencai.get(
    query='科技股',
    sort_key='涨跌幅',
    sort_order='desc',
    cookie=cookie
)

# 获取多页数据
pywencai.get(
    query='A股',
    loop=3,         # 获取前3页
    perpage=100,    # 每页100条
    cookie=cookie
)
```

### 其他资产类型

```python
# 指数
pywencai.get(query='上证指数', query_type='zhishu', cookie=cookie)

# 基金
pywencai.get(query='科技类基金', query_type='fund', cookie=cookie)

# 可转债
pywencai.get(query='可转债', query_type='conbond', cookie=cookie)
```

## 🧪 测试

### 运行环境检查

```bash
python wencai/scripts/check_environment.py
```

### 运行测试脚本

```bash
# 设置 Cookie
export WENCAI_COOKIE="your_cookie_here"

# 运行封装版本测试
python pywencai/wencai/scripts/query_wencai.py

# 运行综合测试
python pywencai/test_comprehensive.py
```

## ⚠️ 注意事项

1. **Cookie 有效期**：Cookie 会过期，需要定期更新
2. **低频使用**：建议低频调用，避免被问财服务屏蔽
3. **Node.js 依赖**：pywencai 内部执行 JS 代码，必须安装 Node.js v16+
4. **数据延迟**：问财数据可能有延迟，非实时数据
5. **查询限制**：每页最多返回 100 条数据（问财限制）

## 📚 文档

- **API 参考**：[wencai/references/api_reference.md](wencai/references/api_reference.md)
- **查询示例**：[wencai/references/query_examples.md](wencai/references/query_examples.md)
- **测试指南**：[pywencai/TEST_GUIDE.md](pywencai/TEST_GUIDE.md)
- **Claude 指南**：[CLAUDE.md](CLAUDE.md)

## 🔗 相关链接

- [pywencai GitHub](https://github.com/zsrl/pywencai)
- [同花顺问财](https://www.iwencai.com/)
- [Claude Code](https://claude.ai/code)

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
