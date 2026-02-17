# Implementation Plan

## Task Overview
依據設計文件，將實作拆分為 10 個原子任務，從底層 OCR 引擎開始，逐步建構 GUI 介面，最後完成專案配置與文件。每個任務觸及 1-2 個檔案，可在 15-30 分鐘內完成。

## Steering Document Compliance
- 專案結構遵循設計文件中定義的平坦式檔案結構（main.py / gui.py / ocr_engine.py）
- 使用 Python 標準庫 tkinter + pytesseract + Pillow 技術棧
- 所有介面文字使用繁體中文
- 所有 OCR 處理在本機完成，無網路呼叫（Security NFR）

## Atomic Task Requirements
**每個任務必須符合以下標準：**
- **File Scope**: 觸及 1-3 個相關檔案
- **Time Boxing**: 15-30 分鐘內可完成
- **Single Purpose**: 一個可測試的成果
- **Specific Files**: 明確指定要建立/修改的檔案
- **Agent-Friendly**: 清楚的輸入/輸出，最小化上下文切換

## Task Format Guidelines
- 使用 checkbox 格式：`- [ ] Task number. Task description`
- **指定檔案**：永遠包含要建立/修改的確切檔案路徑
- **包含實作細節**：以子項目列出
- 使用 `_Requirements: X.Y_` 格式引用需求
- 使用 `_Leverage: path/to/file_` 格式引用可重用的既有程式碼
- 僅限程式撰寫任務（不包含部署、使用者測試等）

## Good vs Bad Task Examples
❌ **Bad（太廣泛）**：
- "實作 OCR 系統"（影響多個檔案，多個目的）
- "建立 GUI 介面"（範圍模糊，未指定檔案）

✅ **Good（原子化）**：
- "建立 OCREngine 類別核心結構於 ocr_engine.py"
- "實作 OCRApp 的圖片選擇與預覽功能於 gui.py"

## Tasks

- [x] 1. 建立 .gitignore 與 requirements.txt
  - Files: `.gitignore`, `requirements.txt`
  - 建立 `.gitignore`，包含：`venv/`, `__pycache__/`, `*.pyc`, `.idea/`, `.vscode/`, `*.egg-info/`
  - 建立 `requirements.txt`，列出相依套件：`pytesseract`, `Pillow`
  - Purpose: 建立專案基礎配置檔案
  - _Requirements: Constraints NFR_

- [x] 2. 建立 OCREngine 類別核心結構於 ocr_engine.py
  - File: `ocr_engine.py`
  - 匯入：`from PIL import Image`、`import pytesseract`
  - 建立 `OCREngine` 類別
  - 定義 `SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')` 常數
  - 實作 `__init__()`：使用 try/except 呼叫 `pytesseract.get_tesseract_version()` 檢查 Tesseract 是否可用，設定 `self._available: bool`
  - 實作 `is_available() -> bool`：回傳 `self._available`
  - 實作 `load_image(file_path: str) -> Image.Image`：
    - 驗證檔案副檔名是否在 SUPPORTED_FORMATS 中（不分大小寫），否則 raise ValueError
    - 使用 `Image.open(file_path)` 載入並呼叫 `.verify()` 驗證完整性
    - 驗證後重新 `Image.open()` 取得可用的 Image 物件（verify 後 Image 不可用）
    - 捕獲 FileNotFoundError 直接 raise，捕獲其他 PIL 例外轉為 IOError
  - Purpose: 建立 OCR 引擎的圖片載入與驗證功能
  - _Requirements: REQ-001 AC-2, REQ-001 AC-3, Reliability NFR_

- [x] 3. 實作 OCREngine 的 OCR 辨識方法於 ocr_engine.py
  - File: `ocr_engine.py`（延續 task 2）
  - 實作 `perform_ocr(image: Image.Image, lang: str = 'chi_tra+eng') -> str`：
    - 呼叫 `pytesseract.image_to_string(image, lang=lang)`
    - 對結果做 `strip()` 處理
    - 捕獲 `pytesseract.TesseractError` 並轉為 `RuntimeError`
  - Purpose: 完成 OCR 引擎的文字辨識功能
  - _Leverage: ocr_engine.py_
  - _Requirements: REQ-002 AC-3, REQ-002 AC-4, REQ-002 AC-5_

- [x] 4. 建立 OCRApp GUI 基礎框架於 gui.py
  - File: `gui.py`
  - 匯入：`import tkinter as tk`, `from tkinter import filedialog, messagebox`, `from PIL import ImageTk, Image`, `import threading`, `from ocr_engine import OCREngine`
  - 建立 `OCRApp` 類別
  - 實作 `__init__(root: tk.Tk)`：
    - 設定視窗標題「OCR 文字辨識工具」、最小尺寸 `root.minsize(600, 500)`
    - 初始化狀態變數：`self.current_image = None`, `self.preview_photo = None`, `self.is_processing = False`
    - 建立頂部按鈕 Frame：「選擇圖片」按鈕、「開始辨識」按鈕（`state=tk.DISABLED`）
    - 建立圖片預覽 Label（`pack(expand=True, fill=tk.BOTH)`）
    - 建立「辨識結果：」標籤
    - 建立文字區域 Frame：Text widget + Scrollbar（`pack(expand=True, fill=tk.BOTH)`）
    - 建立底部 Frame：「複製到剪貼簿」按鈕（`state=tk.DISABLED`）、狀態列 Label
    - 初始化 `self.engine = OCREngine()`，若 `not engine.is_available()` 則更新狀態列顯示警告
  - 實作 `_update_status(message: str)`：設定狀態列 Label 的 text
  - Purpose: 建立完整的 GUI 佈局，所有 widget 就位
  - _Leverage: ocr_engine.py_
  - _Requirements: REQ-001 AC-1, REQ-003 AC-4, Usability NFR_

- [x] 5. 實作 OCRApp 的圖片選擇與預覽功能於 gui.py
  - File: `gui.py`（延續 task 4）
  - 實作 `select_image()`：
    - 呼叫 `filedialog.askopenfilename(filetypes=[("圖片檔案", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("所有檔案", "*.*")])`
    - 若使用者取消選擇則直接 return
    - 使用 try/except 呼叫 `self.engine.load_image(path)`
    - 捕獲 ValueError 顯示 `messagebox.showerror("錯誤", "不支援的檔案格式")`
    - 捕獲 IOError 顯示 `messagebox.showerror("錯誤", "無法載入圖片")`
    - 成功後儲存 `self.current_image = image`
    - 呼叫 `_resize_preview_image()` 更新預覽
    - 啟用「開始辨識」按鈕：`self.ocr_btn.config(state=tk.NORMAL)`
    - 更新狀態列
  - 實作 `_resize_preview_image(image: Image.Image, max_width: int = 550, max_height: int = 300) -> None`：
    - `preview = image.copy()`
    - `preview.thumbnail((max_width, max_height), Image.LANCZOS)`
    - `self.preview_photo = ImageTk.PhotoImage(preview)`（保留參考避免 GC）
    - 更新預覽 Label 的 image
  - Purpose: 完成圖片選擇、載入與預覽顯示流程
  - _Leverage: gui.py, ocr_engine.py_
  - _Requirements: REQ-001 AC-1, REQ-001 AC-2, REQ-001 AC-3, REQ-001 AC-4_

- [x] 6. 實作 OCRApp 的 OCR 啟動與背景執行緒於 gui.py
  - File: `gui.py`（延續 task 5）
  - 實作 `start_ocr()`：
    - 檢查 `self.engine.is_available()`，不可用時彈出 `messagebox.showerror` 含安裝說明與連結 `https://github.com/UB-Mannheim/tesseract/wiki`
    - 設定 `self.is_processing = True`
    - 停用三個按鈕：選擇圖片、開始辨識、複製到剪貼簿
    - 清空 Text widget：`self.text_area.delete("1.0", tk.END)`
    - 更新狀態列「辨識中...」
    - 啟動 `threading.Thread(target=self._run_ocr_thread, daemon=True).start()`
  - 實作 `_run_ocr_thread()`：
    - try: `result = self.engine.perform_ocr(self.current_image)`
    - 成功：`self.root.after(0, self._on_ocr_complete, result)`
    - except: `self.root.after(0, self._on_ocr_error, str(e))`
  - Purpose: 完成 OCR 啟動流程與背景執行緒，確保 GUI 不凍結
  - _Leverage: gui.py_
  - _Requirements: REQ-002 AC-1, REQ-002 AC-2, Performance NFR_

- [x] 7. 實作 OCRApp 的 OCR 結果處理與錯誤回調於 gui.py
  - File: `gui.py`（延續 task 6）
  - 實作 `_on_ocr_complete(result: str)`：
    - 清空 Text widget 後插入結果
    - 若 `result` 非空：啟用「複製到剪貼簿」按鈕，更新狀態列「辨識完成」
    - 若 `result` 為空：插入「未偵測到文字」，複製按鈕維持停用
    - 重新啟用「選擇圖片」、「開始辨識」按鈕
    - 設定 `self.is_processing = False`
  - 實作 `_on_ocr_error(error_msg: str)`：
    - 清空 Text widget 後插入錯誤訊息
    - 重新啟用「選擇圖片」、「開始辨識」按鈕
    - 複製按鈕維持停用
    - 更新狀態列「辨識失敗」
    - 設定 `self.is_processing = False`
  - Purpose: 完成 OCR 結果與錯誤的 GUI 更新（主執行緒回調）
  - _Leverage: gui.py_
  - _Requirements: REQ-002 AC-3, REQ-002 AC-4, REQ-003 AC-1, REQ-003 AC-4_

- [x] 8. 實作 OCRApp 的剪貼簿複製功能於 gui.py
  - File: `gui.py`（延續 task 7）
  - 實作 `copy_to_clipboard()`：
    - 取得 Text widget 文字：`text = self.text_area.get("1.0", tk.END).strip()`
    - 若 text 為空則直接 return
    - `self.root.clipboard_clear()`
    - `self.root.clipboard_append(text)`
    - 更新狀態列「已複製！」
  - Purpose: 完成剪貼簿複製功能
  - _Leverage: gui.py_
  - _Requirements: REQ-003 AC-2, REQ-003 AC-3_

- [x] 9. 建立 main.py 應用程式進入點
  - File: `main.py`
  - 匯入：`import tkinter as tk`, `from gui import OCRApp`
  - 建立 `main()` 函式：
    - `root = tk.Tk()`
    - `app = OCRApp(root)`
    - `root.mainloop()`
  - 加入 `if __name__ == '__main__': main()`
  - Purpose: 建立應用程式進入點，使程式可透過 `python main.py` 啟動
  - _Leverage: gui.py_
  - _Requirements: Usability NFR_

- [x] 10. 撰寫 README.md 含完整環境設定與使用說明
  - File: `README.md`
  - 撰寫以下內容（繁體中文）：
    - 專案簡介：OCR 文字辨識桌面工具
    - 功能特色：圖片載入、OCR 辨識（繁中/英文）、一鍵複製
    - 前置需求：
      - Python 3.9+
      - Tesseract OCR 安裝步驟（含 Windows 安裝連結 https://github.com/UB-Mannheim/tesseract/wiki）
      - 繁體中文語言包（chi_tra）設定說明
    - 環境設定步驟：
      - `python -m venv venv`
      - `venv\Scripts\activate`（Windows）
      - `pip install -r requirements.txt`
    - 使用方式：`python main.py`
    - 操作說明：選擇圖片 → 開始辨識 → 複製到剪貼簿
  - Purpose: 提供完整的專案文件，讓使用者能順利設定與使用
  - _Requirements: Constraints NFR, Compatibility NFR_
