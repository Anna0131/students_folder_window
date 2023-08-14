import tkinter as tk
from tkinter import ttk
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
def display_student_data(folder, mode):
    print(f"Displaying data for student in folder: {folder} with mode: {mode}")

root = tk.Tk()
base_folder = r"C:\code_practice\json_student\json_student\Final-Scoring Assistance System\000001"
student_folder = [
            os.path.join(base_folder, folder)
            for folder in os.listdir(base_folder)
            if os.path.isdir(os.path.join(base_folder, folder))
        ]
student_folder = ["Student 1", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3", "Student 2", "Student 3"]

student_buttons_frame = ttk.Frame(root)
student_buttons_frame.pack(side=tk.RIGHT, fill="y")

student_buttons_canvas = tk.Canvas(student_buttons_frame)
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
    ).pack(side=tk.TOP)

student_buttons.update_idletasks()  # Update canvas to compute proper scroll region

student_buttons_canvas.config(scrollregion=student_buttons_canvas.bbox("all"))

def on_mousewheel(event):
    student_buttons_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

root.bind("<MouseWheel>", on_mousewheel)  # 綁定滾輪事件

root.mainloop()
