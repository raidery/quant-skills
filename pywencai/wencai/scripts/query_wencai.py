#!/usr/bin/env python3
"""
Wencai Query Script - 问财查询脚本

通过 pywencai 库使用自然语言查询 A 股市场数据
"""

import os
import json
import logging
import re
from pathlib import Path
from typing import Optional, Union

import pandas as pd
import pywencai

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def get_cookie(cookie_param: Optional[str] = None) -> str:
    """
    按优先级获取 cookie：
    1. 函数参数 cookie_param
    2. 环境变量 WENCAI_COOKIE
    3. 配置文件 ~/.wencai/config.json

    Args:
        cookie_param: 可选的 cookie 参数

    Returns:
        str: Cookie 字符串

    Raises:
        ValueError: 未找到 cookie
    """
    # 优先级 1: 函数参数
    if cookie_param:
        logging.info("使用参数传入的 cookie")
        return cookie_param

    # 优先级 2: 环境变量
    env_cookie = os.getenv('WENCAI_COOKIE')
    if env_cookie:
        logging.info("使用环境变量 WENCAI_COOKIE")
        return env_cookie

    # 优先级 3: 配置文件
    config_path = Path.home() / '.wencai' / 'config.json'
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                config_cookie = config.get('cookie')
                if config_cookie:
                    logging.info(f"使用配置文件 {config_path}")
                    return config_cookie
        except Exception as e:
            logging.warning(f"读取配置文件失败: {e}")

    raise ValueError("未找到 cookie，请通过参数、环境变量或配置文件提供")


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    清洗列名，去除日期前缀

    示例：
        '20260309[最新涨跌幅]' -> '涨跌幅'
        '退市@退市日期' -> '退市日期'
        '股票代码' -> '股票代码'（保持不变）

    Args:
        df: 原始 DataFrame

    Returns:
        pd.DataFrame: 列名已清洗的 DataFrame
    """
    new_columns = []
    for col in df.columns:
        # 匹配模式：[内容]
        match = re.search(r'\[(.*?)\]', col)
        if match:
            new_columns.append(match.group(1))
        else:
            # 去除可能的日期前缀（8位数字）
            cleaned = re.sub(r'^\d{8}', '', col)
            # 去除 @ 符号后的内容前缀
            if '@' in cleaned:
                cleaned = cleaned.split('@')[-1]
            new_columns.append(cleaned)

    df.columns = new_columns
    return df


def select_key_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    智能选择关键列，优先保留：
    - 代码、名称
    - 价格相关（现价、涨跌幅、涨跌额）
    - 成交量、成交额
    - 市值、市盈率
    - 板块、行业
    - 其他重要指标

    Args:
        df: 原始 DataFrame

    Returns:
        pd.DataFrame: 只包含关键列的 DataFrame
    """
    priority_keywords = [
        '代码', 'code', '股票代码',
        '名称', 'name', '股票名称', '股票简称',
        '现价', '最新价', '收盘价', 'price',
        '涨跌幅', '涨幅', '跌幅', 'change',
        '涨跌', '涨跌额',
        '成交量', 'volume',
        '成交额', 'amount',
        '市值', '总市值', '流通市值',
        '市盈率', 'pe',
        '板块', '所属板块', '行业', '概念',
        'roe', '净资产收益率',
        '退市', '日期'
    ]

    # 保留匹配关键词的列
    selected_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword.lower() in col_lower for keyword in priority_keywords):
            selected_cols.append(col)

    # 如果没有匹配到，返回前10列
    if not selected_cols:
        selected_cols = df.columns[:10].tolist()

    # 如果匹配的列太多，限制在前15列
    if len(selected_cols) > 15:
        selected_cols = selected_cols[:15]

    return df[selected_cols]


def extract_main_dataframe(result: dict) -> pd.DataFrame:
    """
    从字典类型的返回结果中提取主要的 DataFrame

    Args:
        result: pywencai.get() 返回的字典

    Returns:
        pd.DataFrame: 提取的主要数据表

    Raises:
        ValueError: 无法从字典中提取 DataFrame
    """
    # 遍历字典，找到第一个 DataFrame
    for key, value in result.items():
        if isinstance(value, pd.DataFrame) and not value.empty:
            logging.info(f"从字典中提取 DataFrame: {key}")
            return value

    raise ValueError("无法从返回结果中提取有效的 DataFrame")


def query_wencai(
    query: str,
    query_type: str = 'stock',
    max_rows: int = 15,
    loop: Union[bool, int] = False,
    cookie: Optional[str] = None,
    sort_key: Optional[str] = None,
    sort_order: str = 'desc',
    perpage: int = 100,
    log: bool = True
) -> str:
    """
    查询问财数据并返回 Markdown 表格

    Args:
        query: 自然语言查询语句
        query_type: 查询类型（stock/zhishu/fund/conbond等）
        max_rows: 限制返回的行数
        loop: 是否循环分页（False/True/数字）
        cookie: 可选的 cookie 参数
        sort_key: 排序字段
        sort_order: 排序方式（asc/desc）
        perpage: 每页数据条数
        log: 是否打印日志

    Returns:
        str: Markdown 格式的表格字符串
    """
    try:
        # 步骤 1: 获取 cookie
        actual_cookie = get_cookie(cookie)

        # 步骤 2: 记录查询日志
        logging.info(f"查询问财：{query}, 类型：{query_type}")

        # 步骤 3: 调用 pywencai.get()
        result = pywencai.get(
            query=query,
            query_type=query_type,
            cookie=actual_cookie,
            sort_key=sort_key,
            sort_order=sort_order,
            perpage=perpage,
            loop=loop,
            log=log,
            retry=10
        )

        # 步骤 4: 识别返回类型
        if result is None:
            return "当前未搜索到符合条件的标的"

        if isinstance(result, dict):
            # 详情类查询，提取主要 DataFrame
            df = extract_main_dataframe(result)
        elif isinstance(result, pd.DataFrame):
            # 列表类查询，直接是 DataFrame
            df = result
        else:
            return f"未知的返回类型: {type(result)}"

        # 检查 DataFrame 是否为空
        if df.empty:
            return "当前未搜索到符合条件的标的"

        # 步骤 5: 清洗列名
        df = clean_column_names(df)

        # 步骤 6: 精简列（保留关键列）
        df = select_key_columns(df)

        # 步骤 7: 限制行数
        df = df.head(max_rows)

        # 步骤 8: 转换为 Markdown 表格
        markdown_table = df.to_markdown(index=False)

        logging.info(f"查询成功，返回 {len(df)} 行数据")
        return markdown_table

    except ValueError as e:
        # Cookie 相关错误
        error_msg = str(e)
        logging.error(f"配置错误: {error_msg}")
        return f"配置错误：{error_msg}"

    except Exception as e:
        # 其他错误
        error_msg = str(e)
        logging.error(f"查询失败：{query}, 错误：{error_msg}")

        # 判断错误类型
        if 'timeout' in error_msg.lower():
            return "查询超时，请稍后重试"
        elif 'connection' in error_msg.lower() or 'network' in error_msg.lower():
            return f"网络请求失败：{error_msg}"
        else:
            return f"查询失败：{error_msg}"


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("Wencai Query Script - 测试")
    print("=" * 60)

    # 测试查询
    test_query = "退市股票"
    print(f"\n测试查询: {test_query}\n")

    try:
        result = query_wencai(
            query=test_query,
            max_rows=10,
            log=True
        )
        print(result)
    except Exception as e:
        print(f"测试失败: {e}")

    print("\n" + "=" * 60)
