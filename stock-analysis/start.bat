@echo off
echo ======================================================================
echo Stock Analysis Skill - 快速启动
echo ======================================================================
echo.
echo 请选择操作:
echo   1. 实时行情分析
echo   2. 股票推荐
echo   3. 早盘报告
echo   4. 完整分析
echo   5. 退出
echo.
set /p choice=请输入选项 (1-5):

if "%choice%"=="1" (
    echo.
    echo 正在运行实时行情分析...
    python %USERPROFILE%\.openclaw\skills\stock-analysis\scripts\quick_analysis.py
) else if "%choice%"=="2" (
    echo.
    echo 正在生成股票推荐...
    python %USERPROFILE%\.openclaw\skills\stock-analysis\scripts\stock_recommend.py
) else if "%choice%"=="3" (
    echo.
    echo 正在生成早盘报告...
    python %USERPROFILE%\.openclaw\skills\stock-analysis\scripts\morning_report.py
) else if "%choice%"=="4" (
    echo.
    echo 正在运行完整分析...
    python %USERPROFILE%\.openclaw\skills\stock-analysis\scripts\final_analysis.py
) else if "%choice%"=="5" (
    echo.
    echo 退出...
    exit
) else (
    echo.
    echo 无效选项，请重新运行
)

echo.
pause
