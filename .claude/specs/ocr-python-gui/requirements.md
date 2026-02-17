# Requirements Document

## Introduction

OCR Python GUI 是一個桌面應用程式，讓使用者可以載入圖片，透過 OCR（光學字元辨識）技術將圖片中的文字擷取出來，並提供一鍵複製到剪貼簿的功能。本專案使用 Python 開發，搭配 tkinter GUI 框架提供直覺的使用者介面。OCR 引擎採用 Tesseract（透過 pytesseract 套件），並使用 Python 虛擬環境 (venv) 管理相依套件。

## Alignment with Product Vision

本專案旨在提供一個簡單、實用的工具，幫助使用者快速從圖片中提取文字內容，減少手動輸入的時間與錯誤。適合需要從截圖、照片或掃描文件中提取文字的日常使用情境。核心流程為三步驟：選圖 → 辨識 → 複製。

## Requirements

### REQ-001：圖片載入

**User Story:** 身為一個使用者，我想要能夠選擇並載入一張圖片，以便從圖片中提取文字而不需要手動重新輸入。

#### Acceptance Criteria

1. WHEN 使用者點擊「選擇圖片」按鈕 THEN 系統 SHALL 開啟檔案選擇對話框，允許選擇圖片檔案
2. IF 使用者選擇了有效的圖片檔案（支援 PNG、JPG、JPEG、BMP、TIFF 格式）THEN 系統 SHALL 將圖片顯示在預覽區域中
3. IF 使用者選擇了不支援的檔案格式 THEN 系統 SHALL 顯示錯誤提示訊息
4. WHEN 圖片載入成功 THEN 系統 SHALL 自動調整圖片大小以適應預覽區域，同時保持原始比例

### REQ-002：OCR 文字辨識

**User Story:** 身為一個使用者，我想要能夠對載入的圖片執行 OCR 辨識，以便將圖片中的文字轉為可編輯、可複製的文字，節省手動抄寫的時間。

#### Acceptance Criteria

1. WHEN 圖片載入成功後，使用者點擊「開始辨識」按鈕 THEN 系統 SHALL 執行 OCR 辨識
2. WHEN OCR 辨識正在執行時 THEN 系統 SHALL 顯示處理中的狀態提示（例如「辨識中...」），且 GUI 不得凍結
3. IF OCR 辨識完成且成功 THEN 系統 SHALL 在文字區域中顯示辨識出的完整文字
4. IF OCR 辨識失敗或無法辨識任何文字 THEN 系統 SHALL 顯示適當的提示訊息（例如「未偵測到文字」或具體錯誤原因）
5. WHEN 圖片包含繁體中文或英文文字 THEN 系統 SHALL 正確辨識並顯示對應字元

### REQ-003：複製到剪貼簿

**User Story:** 身為一個使用者，我想要能夠一鍵將 OCR 辨識出的文字複製到剪貼簿，以便直接貼上到其他應用程式中使用。

#### Acceptance Criteria

1. WHEN OCR 辨識完成且文字區域有內容 THEN 系統 SHALL 啟用「複製到剪貼簿」按鈕
2. WHEN 使用者點擊「複製到剪貼簿」按鈕 THEN 系統 SHALL 將文字區域中的所有文字複製到系統剪貼簿
3. WHEN 複製成功 THEN 系統 SHALL 顯示「已複製！」的成功提示
4. IF 文字區域為空 THEN 系統 SHALL 停用「複製到剪貼簿」按鈕

## Non-Functional Requirements

### Performance
- OCR 辨識應在 10 秒內完成一般大小的圖片（小於 5MB）
- GUI 在 OCR 處理期間 SHALL 保持回應，UI 執行緒延遲不超過 100ms（使用背景執行緒處理 OCR）

### Security
- 應用程式僅在本機處理圖片，不上傳任何資料到外部伺服器
- 不儲存使用者的圖片或辨識結果

### Reliability
- 系統 SHALL 能正確處理解析度範圍 100x100 至 10000x10000 像素的圖片
- WHEN Tesseract OCR 引擎未安裝或初始化失敗時，系統 SHALL 顯示包含失敗原因與安裝說明連結的錯誤訊息
- WHEN 載入的圖片檔案損壞或無法讀取時，系統 SHALL 顯示明確的錯誤訊息

### Usability
- 主要操作流程不超過 3 個步驟（選圖 → 辨識 → 複製）
- 視窗大小應可調整，且版面配置隨之自適應
- 介面文字使用繁體中文

### Compatibility
- 支援 Python 3.9 以上版本
- 支援 Windows 10/11 作業系統
- 需要安裝 Tesseract OCR 引擎（需另行安裝）

### Constraints（開發環境）
- 專案 SHALL 使用 Python 虛擬環境 (venv) 管理相依套件
- 專案 SHALL 提供 requirements.txt 列出所有相依套件
- README SHALL 包含完整的環境設定步驟說明（建立 venv、安裝套件、安裝 Tesseract）
