#!/usr/bin/env python3
"""
Wencai Skill 综合测试
"""

import sys
sys.path.insert(0, '/home/admin/bench/claude-code/wencai/wencai/scripts')

from query_wencai import query_wencai

print("=" * 80)
print("Wencai Skill 综合测试")
print("=" * 80)

# 测试 1: 涨停股查询
print("\n【测试 1】查询今日涨停股")
print("-" * 80)
result = query_wencai("今日涨停股", max_rows=5)
print(result)

# 测试 2: 条件筛选查询
print("\n\n【测试 2】查询 ROE 大于 20% 的股票")
print("-" * 80)
result = query_wencai("ROE大于20%的股票", sort_key="ROE", sort_order="desc", max_rows=5)
print(result)

# 测试 3: 概念股查询
print("\n\n【测试 3】查询机器人概念股")
print("-" * 80)
result = query_wencai("机器人概念股", max_rows=5)
print(result)

# 测试 4: 空结果测试
print("\n\n【测试 4】测试空结果处理")
print("-" * 80)
result = query_wencai("不存在的查询条件xyz123abc", max_rows=5)
print(result)

print("\n" + "=" * 80)
print("测试完成！")
print("=" * 80)
