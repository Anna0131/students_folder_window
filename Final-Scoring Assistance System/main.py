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
    base_folder = r"C:\code_practice\json_student\json_student\000001"
    #base_folder = filedialog.askdirectory()  # 讓使用者選擇資料夾
    if base_folder:
        #tk.messagebox.showinfo("操作說明", f"請先點選模式，再點選學生。\n(您選擇的資料夾是：{base_folder}) ")
        global nb, mode
        if nb:
            nb.destroy()
        nb = ttk.Notebook(root)

        student_buttons_frame = ttk.Frame(root)  # 放學生切換清單和模式選擇清單的 frame
        # 放所有學生資料夾的完整路徑
        student_folder = [
            os.path.join(base_folder, folder)
            for folder in os.listdir(base_folder)
            if os.path.isdir(os.path.join(base_folder, folder))
        ]
        # 模式選擇清單
        mode_selection_window = ttk.Frame(student_buttons_frame)
        mode_selection_window.pack(side=tk.TOP)
        # 學生切換清單
        student_buttons = ttk.Frame(student_buttons_frame)
        student_buttons.pack(side=tk.BOTTOM)   

        # 將學生切換清單 Frame 和 notebook 放入主視窗中
        student_buttons_frame.pack(side=tk.RIGHT, fill="y")
        nb.pack(
            side=tk.LEFT, fill="both", expand=True
        )  #  nb 放 student_buttons_frame 的左邊

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
            mode_selection_window, text="申請模式", command=apply_mode
        )
        apply_mode_button.pack(pady=5)
        not_apply_mode_button = ttk.Button(
            mode_selection_window, text="非申請模式", command=not_apply_mode
        )
        not_apply_mode_button.pack(pady=5)

        if mode == "申請模式" or mode == "非申請模式":
            # 初始畫面顯示第一個學生的資料夾內容
            display_student_data(student_folder[0], mode) 
        for folder in student_folder:
            student_name = os.path.basename(folder)  # 學生資料夾的名稱
            ttk.Button(
                student_buttons,
                text=student_name,
                command=lambda f=folder: display_student_data(f, mode),
            ).pack(side=tk.TOP)

def display_student_data(folder, choose_mode):
    global nb,current_student_folder 
    if nb:
        # 刪除現有的 notebook 頁面，方便切換顯示不同的子視窗
        nb.destroy()
    nb = ttk.Notebook(root)
    current_student_folder = folder  # 更新當前學生資料夾
    # 學生資料夾的所有檔案
    for filename in os.listdir(folder):
        
        filepath = os.path.join(folder, filename)
        from_file_display_window.display_file(filename, nb, filepath, choose_mode)

    nb.pack(side=tk.LEFT, fill="both", expand=True)

root = tk.Tk()
style = ttk.Style()

style.configure("Grey.TLabel", background="light grey")  # 背景顏色為淺灰色
root.title("評分輔助系統")
root.geometry("1200x550")

open_folder()

root.mainloop()
