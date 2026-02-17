"""GUI 模組

建構 tkinter GUI 介面，處理使用者互動與流程控制。
使用 pack 佈局搭配 expand=True, fill=BOTH，使視窗可調整大小且版面自適應。
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import threading
from ocr_engine import OCREngine


class OCRApp:
    """OCR 文字辨識工具 GUI 應用程式

    提供圖片載入、OCR 文字辨識與剪貼簿複製功能的圖形介面。
    使用 pack 佈局，圖片預覽與文字區域設定 expand=True, fill=BOTH，
    使視窗大小可調整且版面隨之自適應。
    """

    def __init__(self, root: tk.Tk) -> None:
        """初始化 GUI 元件與 OCREngine

        建立所有 widget（按鈕、圖片預覽 Label、Text + Scrollbar、狀態列），
        設定視窗標題與最小尺寸，並檢查 OCREngine 是否可用。

        Args:
            root: tkinter 主視窗物件
        """
        # 視窗設定
        self.root = root
        self.root.title("OCR 文字辨識工具")
        self.root.minsize(600, 500)

        # 狀態變數
        self.current_image = None
        self.preview_photo = None
        self.is_processing = False

        # === 頂部按鈕 Frame ===
        btn_frame = tk.Frame(root)
        btn_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.select_btn = tk.Button(
            btn_frame, text="選擇圖片", command=self.select_image
        )
        self.select_btn.pack(side=tk.LEFT, padx=5)

        self.ocr_btn = tk.Button(
            btn_frame, text="開始辨識", command=self.start_ocr, state=tk.DISABLED
        )
        self.ocr_btn.pack(side=tk.LEFT, padx=5)

        # === 圖片預覽區域 ===
        self.preview_label = tk.Label(root, text="請選擇圖片", bg="#f0f0f0")
        self.preview_label.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # === 辨識結果標籤 ===
        result_label = tk.Label(root, text="辨識結果：", anchor=tk.W)
        result_label.pack(side=tk.TOP, fill=tk.X, padx=5)

        # === 文字區域 Frame（Text + Scrollbar）===
        text_frame = tk.Frame(root)
        text_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(text_frame, wrap=tk.WORD)
        self.text_area.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # 連結 Text 與 Scrollbar
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

        # === 底部 Frame ===
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.copy_btn = tk.Button(
            bottom_frame,
            text="複製到剪貼簿",
            command=self.copy_to_clipboard,
            state=tk.DISABLED,
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(bottom_frame, text="就緒")
        self.status_label.pack(side=tk.RIGHT, padx=5)

        # === 初始化 OCREngine ===
        self.engine = OCREngine()
        if not self.engine.is_available():
            self._update_status("警告：未偵測到 Tesseract OCR 引擎")

    def _update_status(self, message: str) -> None:
        """更新狀態列 Label 的文字

        Args:
            message: 要顯示在狀態列的訊息文字
        """
        self.status_label.config(text=message)

    def select_image(self) -> None:
        """開啟檔案選擇對話框，載入並預覽圖片

        透過 filedialog 讓使用者選擇圖片檔案，使用 OCREngine 載入圖片，
        並在預覽區域顯示縮圖。載入成功後啟用 OCR 按鈕。

        支援格式：PNG、JPG、JPEG、BMP、TIFF
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("圖片檔案", "*.png *.jpg *.jpeg *.bmp *.tiff"), ("所有檔案", "*.*")]
        )
        if not file_path:
            return

        try:
            image = self.engine.load_image(file_path)
        except ValueError:
            messagebox.showerror("錯誤", "不支援的檔案格式")
            return
        except (FileNotFoundError, IOError):
            messagebox.showerror("錯誤", "無法載入圖片")
            return

        self.current_image = image
        self._resize_preview_image(image)
        self.ocr_btn.config(state=tk.NORMAL)
        self._update_status("圖片已載入")

    def _resize_preview_image(self, image: Image.Image, max_width: int = 550, max_height: int = 300) -> None:
        """將圖片縮放至預覽尺寸並更新預覽 Label

        使用 thumbnail 方法等比例縮放圖片，確保不超過最大寬高限制，
        並保持對 PhotoImage 的參考以避免垃圾回收。

        Args:
            image: 要預覽的 PIL Image 物件
            max_width: 預覽區域最大寬度（預設 550 像素）
            max_height: 預覽區域最大高度（預設 300 像素）
        """
        preview = image.copy()
        preview.thumbnail((max_width, max_height), Image.LANCZOS)
        self.preview_photo = ImageTk.PhotoImage(preview)
        self.preview_label.config(image=self.preview_photo, text="")

    def start_ocr(self) -> None:
        """啟動背景執行緒執行 OCR 辨識

        檢查 OCR 引擎是否可用，若可用則停用按鈕、清空文字區域，
        並啟動背景執行緒執行辨識，避免阻塞 GUI 主執行緒。
        """
        if not self.engine.is_available():
            messagebox.showerror(
                "錯誤",
                "未偵測到 Tesseract OCR 引擎。\n\n請至以下網址下載安裝：\nhttps://github.com/UB-Mannheim/tesseract/wiki",
            )
            return

        self.is_processing = True
        self.select_btn.config(state=tk.DISABLED)
        self.ocr_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.text_area.delete("1.0", tk.END)
        self._update_status("辨識中...")
        threading.Thread(target=self._run_ocr_thread, daemon=True).start()

    def _run_ocr_thread(self) -> None:
        """在背景執行緒中執行 OCR 辨識

        呼叫 OCREngine.perform_ocr 進行文字辨識，完成後透過
        self.root.after 將結果回傳至主執行緒更新 GUI，
        確保不會在背景執行緒中直接操作 tkinter 元件。
        """
        try:
            result = self.engine.perform_ocr(self.current_image)
            self.root.after(0, self._on_ocr_complete, result)
        except Exception as e:
            self.root.after(0, self._on_ocr_error, str(e))

    def copy_to_clipboard(self) -> None:
        """將文字區域內容複製到系統剪貼簿（待後續任務實作）"""
        pass
