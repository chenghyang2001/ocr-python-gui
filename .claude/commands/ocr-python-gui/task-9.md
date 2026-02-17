# ocr-python-gui - Task 9

Execute task 9 for the ocr-python-gui specification.

## Task Description
建立 main.py 應用程式進入點

## Code Reuse
**Leverage existing code**: gui.py

## Requirements Reference
**Requirements**: Usability NFR

## Usage
```
/Task:9-ocr-python-gui
```

## Instructions

Execute with @spec-task-executor agent the following task: "建立 main.py 應用程式進入點"

```
Use the @spec-task-executor agent to implement task 9: "建立 main.py 應用程式進入點" for the ocr-python-gui specification and include all the below context.

# Steering Context
## Steering Documents Context

No steering documents found or all are empty.

# Specification Context
## Specification Context (Pre-loaded): ocr-python-gui

### Requirements
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

---

### Design
# Design Document

## Overview

OCR Python GUI 是一個基於 tkinter 的桌面應用程式，提供圖片載入、OCR 文字辨識與剪貼簿複製功能。採用 MVC-like 架構，將 GUI 展示層、OCR 處理邏輯與應用程式控制流程分離，確保可維護性與可測試性。

## Steering Document Alignment

### Technical Standards
- 使用 Python 標準庫 tkinter 作為 GUI 框架，無需額外安裝 GUI 套件
- 使用 pytesseract 作為 Tesseract OCR 的 Python 綁定
- 使用 Pillow (PIL) 處理圖片載入與縮放
- 使用 threading 模組實現非阻塞 OCR 處理

### Project Structure
```
ocr-python-gui/
├── main.py              # 應用程式進入點
├── ocr_engine.py        # OCR 處理邏輯
├── gui.py               # tkinter GUI 介面
├── requirements.txt     # Python 相依套件
├── README.md            # 專案說明與安裝指引
└── .gitignore           # Git 忽略規則
```

## Code Reuse Analysis

### Existing Components to Leverage
- **tkinter**：Python 內建 GUI 框架，無需額外安裝
- **tkinter.filedialog**：檔案選擇對話框
- **tkinter.messagebox**：錯誤與提示訊息

### Integration Points
- **Tesseract OCR**：透過 pytesseract 呼叫系統安裝的 Tesseract 引擎
- **System Clipboard**：透過 tkinter 內建的 clipboard 方法操作剪貼簿
- **PIL/Pillow**：圖片載入、格式驗證與縮放

## Architecture

```mermaid
graph TD
    A[main.py<br/>應用程式進入點] --> B[gui.py<br/>OCRApp 類別]
    B --> C[tkinter 視窗<br/>圖片預覽 / 文字區域 / 按鈕]
    B --> D[ocr_engine.py<br/>OCREngine 類別]
    D --> E[pytesseract<br/>Tesseract 綁定]
    D --> F[Pillow<br/>圖片處理]
    B --> G[threading<br/>背景執行緒]
    G --> D
    B --> H[tkinter clipboard<br/>剪貼簿操作]
```

### 使用者操作流程

```mermaid
sequenceDiagram
    participant U as 使用者
    participant G as GUI (OCRApp)
    participant T as 背景執行緒
    participant O as OCREngine

    U->>G: 點擊「選擇圖片」
    G->>G: 開啟 filedialog
    U->>G: 選擇圖片檔案
    G->>O: load_image(path)
    O-->>G: 回傳 PIL Image
    G->>G: 顯示圖片預覽

    U->>G: 點擊「開始辨識」
    G->>G: 顯示「辨識中...」狀態
    G->>T: 啟動背景執行緒
    T->>O: perform_ocr(image)
    O->>O: pytesseract.image_to_string()
    O-->>T: 回傳辨識文字
    T-->>G: callback 更新 GUI
    G->>G: 顯示辨識結果，啟用複製按鈕

    U->>G: 點擊「複製到剪貼簿」
    G->>H: clipboard_clear + clipboard_append
    G->>G: 顯示「已複製！」提示
```

## Components and Interfaces

### Component 1：OCREngine（ocr_engine.py）
- **Purpose：** 封裝所有 OCR 相關的處理邏輯，包含圖片載入、驗證與文字辨識
- **Interfaces：**
  ```python
  class OCREngine:
      SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

      def __init__(self) -> None:
          """初始化 OCR 引擎，檢查 Tesseract 是否可用"""

      def is_available(self) -> bool:
          """檢查 Tesseract 是否已安裝且可用"""

      def load_image(self, file_path: str) -> Image:
          """載入並驗證圖片檔案，回傳 PIL Image 物件
          Raises: ValueError（不支援的格式）, FileNotFoundError, IOError（檔案損壞）"""

      def perform_ocr(self, image: Image, lang: str = 'chi_tra+eng') -> str:
          """對圖片執行 OCR 辨識，回傳辨識出的文字
          Raises: RuntimeError（OCR 失敗）"""
  ```
- **Dependencies：** pytesseract, Pillow
- **Reuses：** 無（新建模組）

### Component 2：OCRApp（gui.py）
- **Purpose：** 建構 tkinter GUI 介面，處理使用者互動與流程控制
- **佈局策略：** 使用 `pack` 佈局搭配 `expand=True, fill=BOTH`，使視窗可調整大小且版面自適應
- **Interfaces：**
  ```python
  class OCRApp:
      def __init__(self, root: tk.Tk) -> None:
          """初始化 GUI 元件與 OCREngine
          - 設定視窗標題、最小尺寸
          - 建立所有 widget（按鈕、圖片預覽 Label、Text + Scrollbar、狀態列）
          - 使用 pack 佈局，圖片預覽與文字區域設定 expand=True, fill=BOTH
          - 檢查 OCREngine.is_available()，若不可用則在狀態列顯示警告"""

      def select_image(self) -> None:
          """開啟檔案選擇對話框，載入並預覽圖片
          - filedialog.askopenfilename 設定 filetypes 過濾器：
            [("圖片檔案", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("所有檔案", "*.*")]
          - 呼叫 OCREngine.load_image() 載入圖片
          - 呼叫 _resize_preview_image() 縮放後顯示預覽"""

      def _resize_preview_image(self, image: Image, max_width: int, max_height: int) -> ImageTk.PhotoImage:
          """將圖片縮放至預覽區域大小，保持原始比例
          - 使用 Image.thumbnail((max_width, max_height), Image.LANCZOS)
          - 轉換為 ImageTk.PhotoImage 供 tkinter Label 顯示
          - 注意：OCR 辨識使用原始圖片，此方法僅用於預覽顯示"""

      def start_ocr(self) -> None:
          """啟動背景執行緒執行 OCR 辨識
          - 先檢查 OCREngine.is_available()，若不可用則彈出安裝說明對話框
          - 設定 is_processing = True
          - 停用「選擇圖片」和「開始辨識」按鈕，防止重複操作
          - 顯示「辨識中...」狀態
          - 啟動 threading.Thread(target=_run_ocr_thread)"""

      def _run_ocr_thread(self) -> None:
          """背景執行緒中執行 OCR
          - 呼叫 OCREngine.perform_ocr(self.current_image)
          - 使用 self.root.after(0, self._on_ocr_complete, result) 回到主執行緒更新 GUI
          - 不直接操作任何 tkinter widget（tkinter 非執行緒安全）"""

      def _on_ocr_complete(self, result: str) -> None:
          """OCR 完成後在主執行緒中更新 GUI
          - 將辨識結果顯示在 Text widget 中
          - 若結果非空：啟用「複製到剪貼簿」按鈕
          - 若結果為空：顯示「未偵測到文字」
          - 重新啟用「選擇圖片」和「開始辨識」按鈕
          - 設定 is_processing = False"""

      def copy_to_clipboard(self) -> None:
          """將文字區域內容複製到系統剪貼簿
          - root.clipboard_clear() + root.clipboard_append(text)
          - 顯示「已複製！」成功提示"""

      def _update_status(self, message: str) -> None:
          """更新狀態列 Label 的文字"""
  ```
- **Dependencies：** tkinter, OCREngine, threading
- **Reuses：** tkinter 內建的 filedialog、messagebox、clipboard 方法；Pillow 的 ImageTk

### Component 3：main.py（應用程式進入點）
- **Purpose：** 建立 tkinter 主視窗，啟動應用程式
- **Interfaces：**
  ```python
  def main() -> None:
      """建立 Tk root 視窗，實例化 OCRApp，進入主迴圈"""
  ```
- **Dependencies：** tkinter, gui.OCRApp

## Data Models

### GUI 佈局結構
```
+------------------------------------------+
|           OCR 文字辨識工具                  |
+------------------------------------------+
|  [選擇圖片]  [開始辨識]                     |
+------------------------------------------+
|                                          |
|          圖片預覽區域                       |
|        (tkinter Label                    |
|         + PhotoImage)                    |
|                                          |
+------------------------------------------+
|  辨識結果：                                |
|  +--------------------------------------+|
|  |                                      ||
|  |     文字顯示區域                       ||
|  |   (tkinter Text widget,             ||
|  |    可捲動, 可選取)                     ||
|  |                                      ||
|  +--------------------------------------+|
+------------------------------------------+
|  [複製到剪貼簿]          狀態列：就緒        |
+------------------------------------------+
```

### 狀態管理
```
應用程式狀態（以 OCRApp 實例變數表示）：
- current_image: Optional[PIL.Image]  # 當前載入的原始圖片（OCR 使用原始解析度）
- preview_photo: Optional[ImageTk.PhotoImage]  # 縮放後的預覽圖片（避免被 GC 回收）
- ocr_result: str                     # OCR 辨識結果文字
- is_processing: bool                 # 是否正在執行 OCR（控制按鈕停用/啟用）
```

### 大圖片處理策略
- 預覽顯示：使用 `Image.thumbnail()` 縮放至預覽區域大小，僅用於顯示
- OCR 辨識：使用原始解析度圖片，確保辨識準確度
- 記憶體管理：同一時間只保留一張原始圖片與一張預覽圖片，載入新圖片時釋放前一張

## Error Handling

### Error Scenarios
1. **Tesseract 未安裝**
   - **Handling：** OCREngine.__init__() 中檢測，設定 is_available = False
   - **User Impact：** 啟動時在狀態列顯示警告訊息，點擊辨識時彈出對話框顯示安裝說明與連結（Windows: https://github.com/UB-Mannheim/tesseract/wiki ）

2. **不支援的圖片格式**
   - **Handling：** filedialog 設定過濾器限制可選格式；OCREngine.load_image() 二次驗證
   - **User Impact：** 顯示 messagebox 錯誤提示「不支援的檔案格式」

3. **圖片檔案損壞或無法讀取**
   - **Handling：** Pillow Image.open() 的例外被 OCREngine.load_image() 捕獲
   - **User Impact：** 顯示 messagebox 錯誤提示「無法載入圖片」

4. **OCR 辨識失敗**
   - **Handling：** pytesseract 例外被 perform_ocr() 捕獲
   - **User Impact：** 文字區域顯示錯誤訊息，狀態列更新為「辨識失敗」

5. **OCR 結果為空**
   - **Handling：** perform_ocr() 回傳空字串時特別處理
   - **User Impact：** 文字區域顯示「未偵測到文字」，複製按鈕維持停用

## Testing Strategy

### Unit Testing
- 測試 OCREngine.load_image() 對各種圖片格式的載入行為（REQ-001 AC-2）
- 測試 OCREngine.load_image() 對不支援格式的錯誤處理（REQ-001 AC-3）
- 測試 OCREngine.load_image() 對損壞檔案的錯誤處理（Reliability NFR）
- 測試 OCREngine.perform_ocr() 的文字辨識結果（REQ-002 AC-3）
- 測試 OCREngine.is_available() 的 Tesseract 檢測邏輯（Reliability NFR）

### Integration Testing
- 測試完整流程：載入圖片 → OCR 辨識 → 取得結果（REQ-001 + REQ-002）
- 測試背景執行緒的 OCR 處理與 root.after() 回調機制（REQ-002 AC-2）

### End-to-End Testing
- 手動測試：選擇圖片 → 點擊辨識 → 確認文字 → 複製到剪貼簿 → 在其他應用貼上驗證（REQ-001 ~ REQ-003）
- 測試不同大小、解析度的圖片（Reliability NFR）
- 測試繁體中文與英文混合的圖片（REQ-002 AC-5）

**Note**: Specification documents have been pre-loaded. Do not use get-content to fetch them again.

## Task Details
- Task ID: 9
- Description: 建立 main.py 應用程式進入點
- Leverage: gui.py
- Requirements: Usability NFR

## Instructions
- Implement ONLY task 9: "建立 main.py 應用程式進入點"
- Follow all project conventions and leverage existing code
- Mark the task as complete using: claude-code-spec-workflow get-tasks ocr-python-gui 9 --mode complete
- Provide a completion summary
```

## Task Completion
When the task is complete, mark it as done:
```bash
claude-code-spec-workflow get-tasks ocr-python-gui 9 --mode complete
```

## Next Steps
After task completion, you can:
- Execute the next task using /ocr-python-gui-task-[next-id]
- Check overall progress with /spec-status ocr-python-gui
