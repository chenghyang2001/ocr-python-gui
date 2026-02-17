@echo off
chcp 65001 >nul
echo ========================================
echo   OCR 文字辨識工具 - 啟動腳本
echo ========================================
echo.

:: 檢查 Python 是否已安裝
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 Python，請先安裝 Python 3.9 以上版本
    echo 下載連結: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 檢查 Tesseract 是否已安裝
tesseract --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 找不到 Tesseract OCR 引擎
    echo 請先安裝: https://github.com/UB-Mannheim/tesseract/wiki
    echo 安裝後請將路徑加入系統 PATH 環境變數
    echo.
)

:: 建立虛擬環境（若不存在）
if not exist "venv" (
    echo [1/3] 建立 Python 虛擬環境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [錯誤] 建立虛擬環境失敗
        pause
        exit /b 1
    )
) else (
    echo [1/3] 虛擬環境已存在，跳過建立
)

:: 啟用虛擬環境並安裝套件
echo [2/3] 安裝相依套件...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

:: 啟動應用程式
echo [3/3] 啟動 OCR 文字辨識工具...
echo.
python main.py

pause
