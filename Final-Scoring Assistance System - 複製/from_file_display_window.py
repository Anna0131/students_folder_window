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

def display_file(filename, nb, filepath, choose_mode ,page_basic_info,page_course_records,page_course_learning_outcomes,page_multidimensional_performance,page_multidimensional_performance_summary,page_learning_process_self_description,page_other_pdf):
    
    # 修課紀錄頁面
    if filename.endswith(".json") and "修課紀錄" in filename:  # filename = 要顯示的文件名
        tree = ttk.Treeview(
            page_course_records, columns=("學年度", "學期", "課程類別", "科目名稱", "學分數", "學業成績", "推估相對表現")
        )

        Course_Record.create_json_table(filepath, tree)

    elif filename.endswith(".json") and "LIST" not in filename:
        # 課程學習成果頁面
        if "課程學習成果" in filename:
            if choose_mode == "申請模式":   
                main = Audio_video_scrolling.setCanvas(page_course_learning_outcomes)  # 加入捲軸
                Course_Learning_Outcomes.display_json_mode_one(filepath, main)  # 顯示 JSON 內容

            elif choose_mode == "非申請模式":
                # 設置上下兩個 Frame
                paned_window = tk.PanedWindow(page_course_learning_outcomes, orient=tk.VERTICAL)
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
                page_course_learning_outcomes.grid_rowconfigure(0, weight=1)
                page_course_learning_outcomes.grid_columnconfigure(0, weight=1)
                top_frame.grid_rowconfigure(0, weight=1)
                top_frame.grid_columnconfigure(0, weight=1)
                bottom_frame.grid_rowconfigure(0, weight=1)
                bottom_frame.grid_columnconfigure(0, weight=1)
        # 基本資料、多元表現頁面
        else:
            if "基本資料"  in filename:
                main = Audio_video_scrolling.setCanvas(page_basic_info)
                Course_Learning_Outcomes.display_json_mode_one(filepath, main)  # 顯示 JSON 內容
            elif "多元表現" in filename:
                main = Audio_video_scrolling.setCanvas(page_multidimensional_performance)
                Course_Learning_Outcomes.display_json_mode_one(filepath, main)  # 顯示 JSON 內容

    elif filepath.endswith(".pdf"):
        if "多元表現綜整心得"  in filename: # 將Frame 添加到Notebook
            main = Audio_video_scrolling.setCanvas(page_multidimensional_performance_summary)
            Audio_video_scrolling.display_else_pdf(filepath, main, 0)  # 顯示圖片
        elif  "其他" in filename:
            main = Audio_video_scrolling.setCanvas(page_other_pdf)
            Audio_video_scrolling.display_else_pdf(filepath, main, 0)  # 顯示圖

        elif  "學習歷程自述" in filename:
            main = Audio_video_scrolling.setCanvas(page_learning_process_self_description)
            Audio_video_scrolling.display_else_pdf(filepath, main, 0)  # 顯示圖