#!/bin/bash

echo "======================================================================"
echo "Stock Analysis Skill - 快速启动"
echo "======================================================================"
echo
echo "请选择操作:"
echo "  1. 实时行情分析"
echo "  2. 股票推荐"
echo "  3. 早盘报告"
echo "  4. 完整分析"
echo "  5. 退出"
echo

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo
        echo "正在运行实时行情分析..."
        python "$HOME/.openclaw/skills/stock-analysis/scripts/quick_analysis.py"
        ;;
    2)
        echo
        echo "正在生成股票推荐..."
        python "$HOME/.openclaw/skills/stock-analysis/scripts/stock_recommend.py"
        ;;
    3)
        echo
        echo "正在生成早盘报告..."
        python "$HOME/.openclaw/skills/stock-analysis/scripts/morning_report.py"
        ;;
    4)
        echo
        echo "正在运行完整分析..."
        python "$HOME/.openclaw/skills/stock-analysis/scripts/final_analysis.py"
        ;;
    5)
        echo
        echo "退出..."
        exit 0
        ;;
    *)
        echo
        echo "无效选项，请重新运行"
        exit 1
        ;;
esac

echo
echo "执行完成。"