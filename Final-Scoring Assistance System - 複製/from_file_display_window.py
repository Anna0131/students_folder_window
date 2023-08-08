import os  # 匯入操作系統功能的模組
import json  # 匯入處理 JSON 檔案的模組
import tkinter as tk  # 匯入 Tkinter 模組，用來建立 GUI 程式
from tkinter import ttk  # 匯入 ttk 模組，提供了一些增強的 GUI 元件
from tkinter import filedialog  # 匯入 filedialog 模組，提供選擇檔案的對話框功能
import webbrowser  # 匯入 webbrowser 模組，用來開啟瀏覽器
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from tkinter import *
from tkinter import messagebox
import Audio_video_scrolling
import Course_Learning_Outcomes
import Course_Record
# 依據學生資料夾內的檔案類型
# 顯示該學生所有檔案

def display_file(filename, nb, filepath, choose_mode):
    # 修課紀錄頁面
    if filename.endswith(".json") and "修課紀錄" in filename:  # filename = 要顯示的文件名
        page = ttk.Frame(nb)  # 創建新的 Frame
        tree = ttk.Treeview(
            page, columns=("學年度", "學期", "課程類別", "科目名稱", "學分數", "學業成績", "推估相對表現")
        )
        nb.add(
            page, text=((os.path.basename(filename)).split("_")[-1]).split(".json")[0]
        )  # 將 Frame (page) 添加到 Notebook (nb)
        Course_Record.create_json_table(filepath, tree)

    elif filename.endswith(".json") and "LIST" not in filename:
        # 課程學習成果頁面
        if "課程學習成果" in filename:
            if choose_mode == "申請模式":
                page = ttk.Frame(nb)
                nb.add(
                    page,
                    text=((os.path.basename(filename)).split("_")[-1]).split(".json")[
                        0
                    ],
                )
                main = Audio_video_scrolling.setCanvas(page)  # 加入捲軸
                Course_Learning_Outcomes.display_json_mode_one(filepath, main)  # 顯示 JSON 內容

            elif choose_mode == "非申請模式":
                page = ttk.Frame(nb)
                nb.add(
                    page,
                    text=((os.path.basename(filename)).split("_")[-1]).split(".json")[
                        0
                    ],
                )
                # 設置上下兩個 Frame
                paned_window = tk.PanedWindow(page, orient=tk.VERTICAL)
                paned_window.grid(row=0, column=0, sticky="nsew")
                top_frame = tk.Frame(paned_window)
                bottom_frame = tk.Frame(paned_window)
                paned_window.add(top_frame)
                paned_window.add(bottom_frame)
                ttk.Label(top_frame, text="專題實作及實習科目學習成果").pack(pady=10)
                ttk.Label(bottom_frame, text="其他課程學習成果").pack(pady=10)
                main_top = Audio_video_scrolling.setCanvas(top_frame)
                main_bottom = Audio_video_scrolling.setCanvas(bottom_frame)
                Course_Learning_Outcomes.display_json_mode_two(filepath, main_top, main_bottom)  # 顯示 JSON 內容
                # Frame 和 page 的行列，讓內容自動填滿佈局
                page.grid_rowconfigure(0, weight=1)
                page.grid_columnconfigure(0, weight=1)
                top_frame.grid_rowconfigure(0, weight=1)
                top_frame.grid_columnconfigure(0, weight=1)
                bottom_frame.grid_rowconfigure(0, weight=1)
                bottom_frame.grid_columnconfigure(0, weight=1)
        # 基本資料、多元表現頁面
        else:
            page = ttk.Frame(nb)
            nb.add(
                page,
                text=((os.path.basename(filename)).split("_")[-1]).split(".json")[0],
            )
            main = Audio_video_scrolling.setCanvas(page)
            Course_Learning_Outcomes.display_json_mode_one(filepath, main)  # 顯示 JSON 內容

    elif filepath.endswith(".pdf"):
        if "多元表現綜整心得" or "其他" or "學習歷程自述" in filename:
            page = ttk.Frame(nb)
            nb.add(
                page,
                text=((os.path.basename(filename)).split("_")[-1]).split(".json")[0],
            )  # 將Frame 添加到Notebook
            main = Audio_video_scrolling.setCanvas(page)
            Audio_video_scrolling.display_else_pdf(filepath, main, 0)  # 顯示圖片