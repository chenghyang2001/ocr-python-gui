# OCR 文字辨識桌面工具

一款使用 Python 開發的 OCR 文字辨識桌面應用程式，可從圖片中提取文字內容。透過直覺的圖形介面，使用者能輕鬆載入圖片、執行文字辨識，並將結果複製到剪貼簿。

## 功能特色

- **圖片載入** - 支援 PNG、JPG、JPEG、BMP、TIFF 等常見圖片格式
- **OCR 文字辨識** - 支援繁體中文與英文的文字辨識
- **一鍵複製** - 辨識結果可一鍵複製到系統剪貼簿
- **圖片預覽** - 載入圖片後自動顯示縮圖預覽
- **背景處理** - OCR 辨識於背景執行緒進行，介面不會凍結
- **本機處理** - 所有 OCR 處理皆在本機完成，無需網路連線

## 快速開始（Windows）

只需雙擊 `run.bat`，腳本會自動完成以下步驟：
1. 檢查 Python 與 Tesseract 是否已安裝
2. 建立虛擬環境（首次執行）
3. 安裝相依套件
4. 啟動應用程式

```
run.bat
```

## 前置需求

### Python

- Python 3.9 或以上版本
- 下載安裝：https://www.python.org/downloads/

### Tesseract OCR 引擎

本工具需要安裝 Tesseract OCR 引擎才能執行文字辨識。

#### Windows 安裝步驟

**方式一：使用 winget 安裝（推薦）**

```bash
winget install UB-Mannheim.TesseractOCR
```

安裝完成後，手動下載中文語言包：
- 繁體中文：從 [tessdata/chi_tra.traineddata](https://github.com/tesseract-ocr/tessdata/raw/main/chi_tra.traineddata) 下載
- 簡體中文：從 [tessdata/chi_sim.traineddata](https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata) 下載

將下載的 `.traineddata` 檔案放入 `C:\Program Files\Tesseract-OCR\tessdata\` 目錄。

**方式二：手動安裝**

1. 前往 [Tesseract OCR 下載頁面](https://github.com/UB-Mannheim/tesseract/wiki) 下載安裝程式
2. 執行安裝程式，安裝過程中請勾選 **「Additional language data」** 中的 **「Chinese Traditional」（chi_tra）**，以支援繁體中文辨識

**設定 PATH 環境變數（選擇性）：**

本工具支援自動偵測 Tesseract 安裝路徑（包含 `C:\Program Files\Tesseract-OCR` 等常見位置），通常不需手動設定 PATH。若自動偵測失敗，可手動設定：

1. 開啟「系統內容」→「進階系統設定」→「環境變數」
2. 在「使用者變數」中找到 `Path`，點選「編輯」
3. 新增 Tesseract 安裝路徑（例如 `C:\Program Files\Tesseract-OCR`）
4. 儲存後重新開啟命令提示字元

也可設定環境變數 `TESSERACT_PATH` 指向 `tesseract.exe` 的完整路徑。

#### macOS 安裝步驟

```bash
brew install tesseract
brew install tesseract-lang   # 安裝額外語言包（含繁體中文）
```

#### Linux (Ubuntu/Debian) 安裝步驟

```bash
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-chi-tra   # 安裝繁體中文語言包
```

#### 驗證安裝

安裝完成後，開啟終端機或命令提示字元，輸入以下指令確認安裝成功：

```bash
tesseract --version
tesseract --list-langs   # 確認已安裝的語言包
```

## 環境設定

1. 建立 Python 虛擬環境：

```bash
python -m venv venv
```

2. 啟用虛擬環境：

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. 安裝相依套件：

```bash
pip install -r requirements.txt
```

## 使用方式

確認虛擬環境已啟用後，執行以下指令啟動應用程式：

```bash
python main.py
```

## 操作說明

1. **選擇圖片** - 點選「選擇圖片」按鈕，從檔案瀏覽器中選擇要辨識的圖片
2. **開始辨識** - 圖片載入後，點選「開始辨識」按鈕執行 OCR 文字辨識
3. **複製到剪貼簿** - 辨識完成後，點選「複製到剪貼簿」按鈕將結果複製到系統剪貼簿

## 打包為執行檔

可使用 `build.bat` 將應用程式打包為獨立的 `.exe` 執行檔：

```
build.bat
```

或手動執行：

```bash
pip install pyinstaller
pyinstaller --name "OCR文字辨識工具" --windowed --onefile --clean --noconfirm main.py
```

打包完成後，執行檔位於 `dist\OCR文字辨識工具.exe`。

> **注意**：打包後的執行檔仍需要目標電腦已安裝 Tesseract OCR 引擎。

## 專案結構

```
ocr-python-gui/
├── main.py            # 應用程式進入點
├── gui.py             # GUI 介面模組（tkinter）
├── ocr_engine.py      # OCR 引擎模組（pytesseract）
├── requirements.txt   # Python 相依套件清單
├── run.bat            # 一鍵啟動腳本（Windows）
├── build.bat          # 打包為執行檔腳本（Windows）
├── .gitignore         # Git 忽略規則
└── README.md          # 專案說明文件
```

## 技術棧

- **GUI 框架**：[tkinter](https://docs.python.org/3/library/tkinter.html)（Python 標準庫）
- **OCR 引擎**：[pytesseract](https://github.com/madmaze/pytesseract)（Tesseract OCR 的 Python 綁定）
- **圖片處理**：[Pillow](https://pillow.readthedocs.io/)（PIL 的維護分支）
- **打包工具**：[PyInstaller](https://pyinstaller.org/)（可選，用於產生 .exe 執行檔）

## 更新紀錄

| 版本 | 日期 | 變更內容 |
|------|------|----------|
| v1.4 | 2026-02-18 05:07 | 新增 `build.bat` 打包腳本，支援 PyInstaller 打包為 `.exe` 執行檔 |
| v1.3 | 2026-02-18 04:57 | 將「複製到剪貼簿」按鈕移至頂部工具列，改善介面佈局 |
| v1.2 | 2026-02-18 04:50 | 新增 Tesseract 路徑自動偵測功能，支援 Windows 常見安裝路徑與 `TESSERACT_PATH` 環境變數 |
| v1.1 | 2026-02-18 04:10 | 實作剪貼簿複製功能，更新 README 文件 |
| v1.0 | 2026-02-18 04:02 | 完成 OCR 辨識結果處理與錯誤回調機制 |
| v0.9 | 2026-02-18 03:59 | 實作背景執行緒 OCR 處理，避免 GUI 凍結 |
| v0.8 | 2026-02-18 03:55 | 實作圖片選擇與預覽功能 |
| v0.7 | 2026-02-18 03:51 | 完成 OCRApp GUI 框架建置 |
| v0.6 | 2026-02-18 03:48 | 新增 OCREngine 的 `perform_ocr` 方法，支援繁體中文+英文辨識 |
| v0.5 | 2026-02-18 03:44 | 建立 OCREngine 類別，實作圖片載入與格式驗證 |
| v0.4 | 2026-02-18 03:32 | 完成基礎任務架構 |
| v0.3 | 2026-02-18 03:21 | 強化核心模組錯誤處理 |
| v0.2 | 2026-02-18 03:10 | 重構專案結構，增強基礎功能 |
| v0.1 | 2026-02-18 03:00 | 初始專案建立，基礎架構與功能實作 |
