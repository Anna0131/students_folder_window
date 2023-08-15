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
import from_file_display_window


# 使用者上傳資料夾
# 選擇申請/非申請模式
# 選擇學生

nb = None
student_buttons = None
mode = None

def open_folder():
    global base_folder, nb, mode,current_student_folder
    #base_folder = r"C:\code_practice\json_student\json_student\Final-Scoring Assistance System\000001"
    base_folder = filedialog.askdirectory()  # 讓使用者選擇資料夾
    if base_folder:
        tk.messagebox.showinfo("操作說明", f"請先點選模式，再點選學生。\n(您選擇的資料夾是：{base_folder}) ")
        global nb, mode
        if nb:
            nb.destroy()
        nb = ttk.Notebook(root)


        # 放所有學生資料夾的完整路徑
        student_folder = [
            os.path.join(base_folder, folder)
            for folder in os.listdir(base_folder)
            if os.path.isdir(os.path.join(base_folder, folder))
        ]
        
        # 模式選擇清單
        mode_selection_frame = ttk.Frame(root)
        mode_selection_frame.pack(side=tk.TOP)
        # 選擇 "申請模式" 或 "非申請模式"
        def apply_mode():
            global mode
            mode = "申請模式"
             # 設定選中模式按鈕的樣式
            style.configure("Selected.TButton", background="blue")
            apply_mode_button.configure(style="Selected.TButton")
            not_apply_mode_button.configure(style="TButton")
            update_display_with_mode(mode)

        def not_apply_mode():
            global mode
            mode = "非申請模式"
            # 設定選中模式按鈕的樣式
            style.configure("Selected.TButton", background="blue")
            apply_mode_button.configure(style="TButton")
            not_apply_mode_button.configure(style="Selected.TButton")
            update_display_with_mode(mode)
        
        current_student_folder = None  # 用來儲存當前學生資料夾
        def update_display_with_mode(choose_mode):
            global current_student_folder
            if current_student_folder:
                display_student_data(current_student_folder, choose_mode)
        

        apply_mode_button = ttk.Button(
            mode_selection_frame, text="申請模式", command=apply_mode
        )
        apply_mode_button.pack(side=tk.LEFT, padx=5, pady=5) 
        not_apply_mode_button = ttk.Button(
           mode_selection_frame, text="非申請模式", command=not_apply_mode
        )
        not_apply_mode_button.pack(side=tk.LEFT, padx=5, pady=5)

        if mode == "申請模式" or mode == "非申請模式":
            # 初始畫面顯示第一個學生的資料夾內容
            display_student_data(student_folder[0], mode) 

        # 創建用於顯示學生人數的 Label
        student_count_label = tk.Label(root, text=f"學生人數：{len(student_folder)}", font=("Helvetica", 12))
        student_count_label.place(relx=1, rely=0, anchor="ne")  # 顯示在右上角

        # 計算按鈕的寬度
        button_width = 0
        for folder in student_folder:
            button_width=max(button_width,len(os.path.basename(folder)))

        student_buttons_frame = ttk.Frame(root)
        student_buttons_frame.pack(side=tk.RIGHT, fill="y")
        

        student_buttons_canvas = tk.Canvas(student_buttons_frame, width=button_width*7.5)
        student_buttons_canvas.pack(side=tk.LEFT, fill="y")

        student_buttons_scrollbar = ttk.Scrollbar(student_buttons_frame, orient=tk.VERTICAL, command=student_buttons_canvas.yview)
        student_buttons_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        student_buttons_canvas.config(yscrollcommand=student_buttons_scrollbar.set)
        
        student_buttons = ttk.Frame(student_buttons_canvas)
        student_buttons_canvas.create_window((0, 0), window=student_buttons, anchor="nw")


        for folder in student_folder:
            student_name = os.path.basename(folder)
            ttk.Button(
                student_buttons,
                text=student_name,
                command=lambda f=folder: display_student_data(f, mode),
                width=button_width
            ).pack(side=tk.TOP)

        student_buttons.update_idletasks()  # Update canvas to compute proper scroll region
        # 調整 canvas 的 scroll region 以顯示完整內容
        student_buttons_canvas.config(scrollregion=student_buttons_canvas.bbox("all"))


def display_student_data(folder, choose_mode):
    global nb,current_student_folder 
    if nb:
        # 刪除現有的 notebook 頁面，方便切換顯示不同的子視窗
        nb.destroy()
    nb = ttk.Notebook(root)
    current_student_folder = folder  # 更新當前學生資料夾
    # 創建分頁
    page_basic_info = ttk.Frame(nb)
    page_course_records = ttk.Frame(nb)
    page_course_learning_outcomes = ttk.Frame(nb)
    page_multidimensional_performance = ttk.Frame(nb)
    page_multidimensional_performance_summary = ttk.Frame(nb)
    page_learning_process_self_description = ttk.Frame(nb)
    page_other_pdf = ttk.Frame(nb)
    
    nb.add(page_basic_info, text="基本資料")
    nb.add(page_course_records, text="修課紀錄")
    nb.add(page_course_learning_outcomes, text="課程學習成果")
    nb.add(page_multidimensional_performance, text="多元表現")
    nb.add(page_multidimensional_performance_summary, text="多元表現綜整心得.pdf")
    nb.add(page_learning_process_self_description, text="學習歷程自述.pdf")
    nb.add(page_other_pdf, text="其他.pdf")

    # 設定分頁的順序
    nb.tab(page_basic_info, state="normal")
    nb.tab(page_course_records, state="normal")
    nb.tab(page_course_learning_outcomes, state="normal")
    nb.tab(page_multidimensional_performance, state="normal")
    nb.tab(page_multidimensional_performance_summary, state="normal")
    nb.tab(page_learning_process_self_description, state="normal")
    nb.tab(page_other_pdf, state="normal")
    
    # 學生資料夾的所有檔案
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        from_file_display_window.display_file(filename, nb, filepath, choose_mode,page_basic_info,page_course_records,page_course_learning_outcomes,page_multidimensional_performance,page_multidimensional_performance_summary,page_learning_process_self_description,page_other_pdf)
    
    nb.pack(side=tk.LEFT, fill="both", expand=True)

root = tk.Tk()
style = ttk.Style()

style.configure("Grey.TLabel", background="light grey")  # 背景顏色為淺灰色
root.title("評分輔助系統")
root.geometry("1200x550")

open_folder()

root.mainloop()
