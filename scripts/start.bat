@echo off
chcp 65001 >nul
echo ========================================
echo    人工智能社交媒体营销分析系统
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

:: 检查虚拟环境是否存在
if not exist "venv\Scripts\activate.bat" (
    echo [信息] 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
)

:: 激活虚拟环境
echo [信息] 激活虚拟环境...
call venv\Scripts\activate.bat

:: 检查依赖是否安装
if not exist "venv\Lib\site-packages\PyQt6" (
    echo [信息] 安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
)

:: 启动应用
echo [信息] 启动应用程序...
python main.py

:: 如果程序异常退出，暂停显示错误信息
if errorlevel 1 (
    echo.
    echo [错误] 程序异常退出，请检查错误信息
    pause
)

:: 退出虚拟环境
deactivate 