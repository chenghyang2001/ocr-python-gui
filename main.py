import tkinter as tk
from gui import OCRApp


def main() -> None:
    """建立 Tk root 視窗，實例化 OCRApp，進入主迴圈"""
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
