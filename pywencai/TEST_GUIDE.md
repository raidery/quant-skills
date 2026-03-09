# Wencai Skill - 测试说明

## 已完成的工作

✅ Skill 结构已初始化
✅ 核心脚本 query_wencai.py 已实现
✅ SKILL.md 文档已编写
✅ 查询示例参考文档已创建
✅ Skill 验证通过
✅ Skill 已打包：wencai.skill (6.8K)

## 文件结构

```
wencai/
├── SKILL.md                      # Skill 使用说明
├── scripts/
│   └── query_wencai.py          # 核心查询脚本
├── references/
│   └── query_types.md           # 查询示例参考
└── wencai.skill                 # 打包后的 Skill 文件
```

## 测试前准备

在测试之前，你需要提供一个有效的问财 cookie。

### 获取 Cookie 的方法：

1. 访问 https://www.iwencai.com/
2. 登录后打开浏览器开发者工具（F12）
3. 切换到 Network 标签
4. 刷新页面，找到任意请求
5. 复制请求头中的 Cookie 字段值

### 配置 Cookie（三种方式任选一种）：

**方式 1: 环境变量（推荐用于测试）**
```bash
export WENCAI_COOKIE="your_cookie_here"
```

**方式 2: 配置文件**
```bash
mkdir -p ~/.wencai
cat > ~/.wencai/config.json << 'EOF'
{
  "cookie": "your_cookie_here"
}
EOF
```

**方式 3: 直接在代码中传入**
```python
result = query_wencai("涨停股", cookie="your_cookie_here")
```

## 测试步骤

### 1. 基本功能测试

```bash
cd /home/admin/bench/claude-code/wencai/wencai
export WENCAI_COOKIE="your_cookie_here"
python scripts/query_wencai.py
```

预期输出：退市股票的 Markdown 表格

### 2. 自定义查询测试

创建测试脚本：

```python
from scripts.query_wencai import query_wencai

# 测试 1: 基本查询
print("测试 1: 查询涨停股")
result = query_wencai("今日涨停股", max_rows=10)
print(result)
print("\n" + "="*60 + "\n")

# 测试 2: 条件查询
print("测试 2: 查询高ROE股票")
result = query_wencai("ROE大于20%的股票", sort_key="ROE", sort_order="desc", max_rows=10)
print(result)
print("\n" + "="*60 + "\n")

# 测试 3: 概念股查询
print("测试 3: 查询机器人概念股")
result = query_wencai("机器人概念股", max_rows=10)
print(result)
```

### 3. 异常处理测试

```python
from scripts.query_wencai import query_wencai

# 测试空结果
result = query_wencai("不存在的查询条件xyz123")
print(result)  # 应该返回: "当前未搜索到符合条件的标的"

# 测试无 cookie（需要先 unset WENCAI_COOKIE）
# result = query_wencai("涨停股")
# 应该返回: "配置错误：未找到 cookie..."
```

## 安装 Skill

将打包好的 wencai.skill 文件安装到 Claude Code：

```bash
# 复制到 Claude Code 的 skills 目录
cp /home/admin/bench/claude-code/wencai/wencai/wencai.skill ~/.claude/skills/
```

或者使用 Claude Code 的安装命令（如果支持）。

## 使用 Skill

安装后，在 Claude Code 中可以直接使用自然语言查询：

```
查询今日涨停股
问财：ROE大于20%的股票
帮我找机器人概念的龙头股
```

Claude 会自动识别并调用 wencai Skill 进行查询。

## 注意事项

1. **Cookie 有效期**：Cookie 可能会过期，需要定期更新
2. **低频使用**：建议低频调用，避免被问财屏蔽
3. **Node.js 依赖**：确保已安装 Node.js v16+（当前环境：v24.3.0 ✓）
4. **数据延迟**：问财数据可能有延迟，非实时数据

## 故障排查

### 问题 1: "未找到 cookie"
- 检查环境变量是否设置：`echo $WENCAI_COOKIE`
- 检查配置文件是否存在：`cat ~/.wencai/config.json`

### 问题 2: "查询超时"
- 网络连接问题，稍后重试
- 检查问财网站是否可访问

### 问题 3: "当前未搜索到符合条件的标的"
- 查询条件可能不正确
- 尝试简化查询条件
- 参考 references/query_types.md 中的示例

## 下一步

1. 提供有效的 cookie 进行测试
2. 验证各项功能是否正常
3. 根据测试结果进行调整和优化
