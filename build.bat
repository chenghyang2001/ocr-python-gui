@echo off
chcp 65001 >nul
echo ========================================
echo   OCR 文字辨識工具 - 打包腳本
echo ========================================
echo.

:: 啟用虛擬環境
call venv\Scripts\activate.bat

:: 清理舊的打包檔案
if exist "dist" (
    echo [1/3] 清理舊的打包檔案...
    rmdir /s /q dist
)
if exist "build" (
    rmdir /s /q build
)

:: 執行 PyInstaller 打包
echo [2/3] 正在打包為執行檔...
pyinstaller ^
    --name "OCR文字辨識工具" ^
    --windowed ^
    --onefile ^
    --clean ^
    --noconfirm ^
    main.py

if %errorlevel% neq 0 (
    echo.
    echo [錯誤] 打包失敗
    pause
    exit /b 1
)

:: 驗證執行檔
echo.
echo [3/3] 驗證打包結果...
if exist "dist\OCR文字辨識工具.exe" (
    echo.
    echo ========================================
    echo   打包成功！
    echo   執行檔位置: dist\OCR文字辨識工具.exe
    for %%A in ("dist\OCR文字辨識工具.exe") do echo   檔案大小: %%~zA bytes
    echo ========================================
) else (
    echo [錯誤] 找不到執行檔
    pause
    exit /b 1
)

echo.
pause
