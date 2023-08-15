import os  # 匯入操作系統功能的模組
import json  # 匯入處理 JSON 檔案的模組
import tkinter as tk  # 匯入 Tkinter 模組，用來建立 GUI 程式
from tkinter import ttk  # 匯入 ttk 模組，提供了一些增強的 GUI 元件
import webbrowser  # 匯入 webbrowser 模組，用來開啟瀏覽器
from tkinter.scrolledtext import ScrolledText

from tkinter import *
from tkinter import filedialog  # 匯入 filedialog 模組，提供選擇檔案的對話框功能
from PIL import Image, ImageTk
from tkinter import messagebox

# 圖片、影片顯示功能
# 捲軸功能

# 顯示 PDF 檔案和名稱
def display_else_pdf(filename, page, row):
    ttk.Label(page, text=filename).grid(column=0, row=row, sticky="W")
    button = tk.Button(page, text="顯示檔案", command=lambda: show_file(filename))
    button.grid(column=1, row=row, sticky="W")
    row += 1
def show_file(filepath):
    if filepath.endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
        # 打開圖片並顯示
        image = Image.open(filepath)
        image.show()
    elif filepath.endswith((".mp4", ".avi", ".mkv", ".mov")):
        # 開啟影片
        webbrowser.open_new_tab(filepath)
    else:
        # 其他類型的檔案使用預設瀏覽器開啟
        webbrowser.open_new_tab(filepath)


# 建立可捲動的 frame
def setCanvas(page):
    my_canvas = tk.Canvas(page)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)  # 填滿整個 frame，且可隨視窗大小自動擴展
    
    # 垂直捲軸放在右邊
    v_scrollbar = ttk.Scrollbar(page, orient=tk.VERTICAL, command=my_canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    my_canvas.configure(yscrollcommand=v_scrollbar.set)
 
    
    # 放置內容的內部 frame
    main = tk.Frame(my_canvas)
    #("main height:", main.winfo_reqheight())  # 印出 main 的預計高度
    # 創建一個可捲動的視窗，並將 main 放置在視窗中
    my_canvas.create_window((0, 0), window=main, anchor="nw")  # 左上角 (anchor="nw")
    # 當 main 的大小變化時，重新設定畫布的捲動區域，實現捲動效果
    def configure_canvas(event):
        my_canvas.configure(scrollregion=my_canvas.bbox("all"))
    main.bind("<Configure>", configure_canvas)
    
    # 綁定滑鼠滾輪事件，實現垂直捲動
    def on_mousewheel(event):
        my_canvas.yview_scroll(-1 * int(event.delta / 120), "units")      
    my_canvas.bind("<MouseWheel>", on_mousewheel)


    return main
