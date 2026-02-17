# OCR 文字辨識桌面工具

一款使用 Python 開發的 OCR 文字辨識桌面應用程式，可從圖片中提取文字內容。透過直覺的圖形介面，使用者能輕鬆載入圖片、執行文字辨識，並將結果複製到剪貼簿。

## 功能特色

- **圖片載入** - 支援 PNG、JPG、JPEG、BMP、TIFF 等常見圖片格式
- **OCR 文字辨識** - 支援繁體中文與英文的文字辨識
- **一鍵複製** - 辨識結果可一鍵複製到系統剪貼簿
- **圖片預覽** - 載入圖片後自動顯示縮圖預覽
- **背景處理** - OCR 辨識於背景執行緒進行，介面不會凍結
- **本機處理** - 所有 OCR 處理皆在本機完成，無需網路連線

## 前置需求

### Python

- Python 3.9 或以上版本
- 下載安裝：https://www.python.org/downloads/

### Tesseract OCR 引擎

本工具需要安裝 Tesseract OCR 引擎才能執行文字辨識。

#### Windows 安裝步驟

1. 前往 [Tesseract OCR 下載頁面](https://github.com/UB-Mannheim/tesseract/wiki) 下載安裝程式
2. 執行安裝程式，安裝過程中請勾選 **「Additional language data」** 中的 **「Chinese Traditional」（chi_tra）**，以支援繁體中文辨識
3. 安裝完成後，將 Tesseract 安裝路徑加入系統 PATH 環境變數（預設路徑為 `C:\Program Files\Tesseract-OCR`）

> **設定 PATH 環境變數方法：**
> 1. 開啟「系統內容」→「進階系統設定」→「環境變數」
> 2. 在「系統變數」中找到 `Path`，點選「編輯」
> 3. 新增 Tesseract 安裝路徑（例如 `C:\Program Files\Tesseract-OCR`）
> 4. 儲存後重新開啟命令提示字元

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
3. **複製到剪貼簿** - 辨識完成後，點選「複製到剪貼簿」按鈕將結果複製

## 專案結構

```
ocr-python-gui/
├── main.py            # 應用程式進入點
├── gui.py             # GUI 介面模組（tkinter）
├── ocr_engine.py      # OCR 引擎模組（pytesseract）
├── requirements.txt   # Python 相依套件清單
├── .gitignore         # Git 忽略規則
└── README.md          # 專案說明文件
```

## 技術棧

- **GUI 框架**：[tkinter](https://docs.python.org/3/library/tkinter.html)（Python 標準庫）
- **OCR 引擎**：[pytesseract](https://github.com/madmaze/pytesseract)（Tesseract OCR 的 Python 綁定）
- **圖片處理**：[Pillow](https://pillow.readthedocs.io/)（PIL 的維護分支）
