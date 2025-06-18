@echo off
chcp 65001 >nul
echo ========================================
echo        清理临时文件和缓存
echo ========================================
echo.

:: 清理Python缓存文件
echo [信息] 清理Python缓存文件...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
for /r . %%f in (*.pyc) do @if exist "%%f" del "%%f"

:: 清理临时文件
echo [信息] 清理临时文件...
if exist "temp\*" del /q "temp\*"
if exist "logs\*.log" del /q "logs\*.log"

:: 清理matplotlib缓存
echo [信息] 清理matplotlib缓存...
if exist "%USERPROFILE%\.matplotlib\*" del /q "%USERPROFILE%\.matplotlib\*"

:: 清理IDE缓存
echo [信息] 清理IDE缓存...
if exist ".idea\*" rd /s /q ".idea"
if exist ".vscode\*" rd /s /q ".vscode"

echo.
echo [完成] 清理完成！
echo.
pause 