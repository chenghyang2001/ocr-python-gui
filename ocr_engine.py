"""OCR 引擎模組

封裝所有 OCR 相關的處理邏輯，包含圖片載入、驗證與文字辨識。
使用 pytesseract 作為 Tesseract OCR 的 Python 綁定，
使用 Pillow (PIL) 處理圖片載入與格式驗證。
"""

from PIL import Image
import pytesseract
import os


class OCREngine:
    """OCR 引擎類別

    提供圖片載入、驗證與 OCR 文字辨識功能。
    初始化時自動檢查 Tesseract 是否已安裝且可用。
    """

    SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

    def __init__(self) -> None:
        """初始化 OCR 引擎，自動偵測 Tesseract 路徑並檢查是否可用

        先嘗試在常見安裝路徑中尋找 Tesseract 執行檔，
        找到後設定 pytesseract.tesseract_cmd，
        再透過 pytesseract.get_tesseract_version() 檢測是否可正常運作。
        """
        self._auto_detect_tesseract()
        try:
            pytesseract.get_tesseract_version()
            self._available: bool = True
        except Exception:
            self._available: bool = False

    @staticmethod
    def _auto_detect_tesseract() -> None:
        """自動偵測 Tesseract 執行檔路徑並設定 pytesseract.tesseract_cmd

        依序檢查：
        1. 系統 PATH 中是否已可直接呼叫
        2. Windows 常見安裝路徑
        3. 環境變數 TESSERACT_PATH
        """
        import shutil
        import platform

        # 若 PATH 中已可找到，直接返回
        if shutil.which('tesseract'):
            return

        # Windows 常見安裝路徑
        if platform.system() == 'Windows':
            common_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                os.path.expandvars(r'%LOCALAPPDATA%\Tesseract-OCR\tesseract.exe'),
                os.path.expandvars(r'%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe'),
            ]
            for path in common_paths:
                if os.path.isfile(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    return

        # 檢查環境變數 TESSERACT_PATH
        env_path = os.environ.get('TESSERACT_PATH')
        if env_path and os.path.isfile(env_path):
            pytesseract.pytesseract.tesseract_cmd = env_path

    def is_available(self) -> bool:
        """檢查 Tesseract 是否已安裝且可用

        Returns:
            bool: True 表示 Tesseract 可用，False 表示不可用
        """
        return self._available

    def load_image(self, file_path: str) -> Image.Image:
        """載入並驗證圖片檔案，回傳 PIL Image 物件

        先驗證檔案副檔名是否為支援的格式，再使用 Pillow 開啟並驗證
        圖片完整性，最後重新開啟以取得可用的 Image 物件。

        Args:
            file_path: 圖片檔案的路徑

        Returns:
            Image.Image: 已驗證且可用的 PIL Image 物件

        Raises:
            ValueError: 檔案格式不支援（副檔名不在 SUPPORTED_FORMATS 中）
            FileNotFoundError: 檔案不存在
            IOError: 圖片檔案損壞或無法讀取
        """
        # 驗證檔案副檔名是否在支援的格式中（不分大小寫）
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"不支援的檔案格式：{ext}")

        try:
            # 使用 Image.open 載入並呼叫 verify() 驗證圖片完整性
            img = Image.open(file_path)
            img.verify()

            # verify() 後 Image 物件不可再使用，需重新開啟
            img = Image.open(file_path)
            return img
        except FileNotFoundError:
            raise
        except Exception as e:
            raise IOError(f"無法載入圖片：{e}")

    def perform_ocr(self, image: Image.Image, lang: str = 'chi_tra+eng') -> str:
        """對圖片執行 OCR 辨識，回傳辨識出的文字

        使用 pytesseract 呼叫 Tesseract OCR 引擎，對給定的 PIL Image
        物件進行文字辨識。預設語言設定為繁體中文加英文。

        Args:
            image: 已載入的 PIL Image 物件
            lang: Tesseract 語言參數，預設為 'chi_tra+eng'（繁體中文+英文）

        Returns:
            str: 辨識出的文字（已去除前後空白），若未偵測到文字則回傳空字串

        Raises:
            RuntimeError: OCR 辨識過程中發生錯誤
        """
        try:
            result = pytesseract.image_to_string(image, lang=lang)
            return result.strip()
        except pytesseract.TesseractError as e:
            raise RuntimeError(f"OCR 辨識失敗：{e}")
