import os  # 匯入操作系統功能的模組
import json  # 匯入處理 JSON 檔案的模組
import tkinter as tk  # 匯入 Tkinter 模組，用來建立 GUI 程式
from tkinter import ttk  # 匯入 ttk 模組，提供了一些增強的 GUI 元件
from tkinter import filedialog  # 匯入 filedialog 模組，提供選擇檔案的對話框功能
import webbrowser  # 匯入 webbrowser 模組，用來開啟瀏覽器
import fitz  # 匯入 fitz 模組，用來讀取 PDF 檔案
from tkinter.scrolledtext import ScrolledText
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from tkinter import *
from tkinter import messagebox
from tkvideo import tkvideo
# 目前最新進度多個學生

nb = None
student_buttons = None
# 選擇資料夾，將該資料夾下的檔案顯示在 ttk.Notebook 中
def open_folder():
    global base_folder, student_buttons_frame, nb
    base_folder = r"C:\code_practice\json_student\json_student\000001"

    if base_folder:
        if nb:
            nb.destroy()
        nb = ttk.Notebook(root)

        student_buttons_frame = ttk.Frame(root)  # 學生切換清單

        # 放所有學生資料夾的完整路徑
        student_folder = [os.path.join(base_folder, folder) for folder in os.listdir(base_folder) if
                          os.path.isdir(os.path.join(base_folder, folder))]

        # 初始化顯示第一個學生的資料夾內容
        display_student_data(student_folder[0]) 

        student_buttons = ttk.Frame(student_buttons_frame)
        student_buttons.pack(side=tk.LEFT)

        for folder in student_folder:
            student_name = os.path.basename(folder)  # 獲取學生資料夾的名稱
            ttk.Button(student_buttons, text=student_name, command=lambda f=folder: display_student_data(f)).pack(
                side=tk.TOP)

        # 將學生切換清單 Frame 和 notebook 放入主視窗中
        student_buttons_frame.pack(side=tk.RIGHT, fill="y")
        nb.pack(side=tk.LEFT, fill="both", expand=True)  # 將 nb 放置在 student_buttons_frame 的左側

def display_student_data(folder):
    global nb
    if nb:
        # 刪除現有的 notebook 頁面
        nb.destroy()

    nb = ttk.Notebook(root)

    # 遍歷學生資料夾下的所有檔案
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        display_file(filename, nb, filepath)

    # 將 notebook 放入主視窗中
    nb.pack(side=tk.LEFT, fill="both", expand=True)  # 將 nb 放置在 student_buttons_frame 的左側



# 顯示指定類型的文件內容
def display_file(filename, nb, filepath): 
    # filename = 要顯示的文件名
    # nb = 顯示 JSON 文件內容的 ttk.Notebook 對象 ，可以將多個頁面添加到nb中
    if filename.endswith(".json") and "修課紀錄" in filename: # 如果文件名以 ".json" 結尾      
        page = ttk.Frame(nb) # 創建新的 Frame
        tree = ttk.Treeview(page, columns=("學年度", "學期", "課程類別", "科目名稱", "學分數", "學業成績", "推估相對表現"))
        nb.add(page, text=((os.path.basename(filename)).split("_")[-1]).split(".json")[0]) # 將Frame 添加到Notebook 
        create_json_table(filepath,tree)

    

    elif filename.endswith(".json") and "LIST" not in filename: # 如果文件名以 ".json" 結尾      
        page = ttk.Frame(nb) # 創建新的Frame 
        nb.add(page, text=((os.path.basename(filename)).split("_")[-1]).split(".json")[0]) # 將 Frame 添加到 Notebook   
        main = setCanvas(page)  
        display_json(filepath, main ) # 顯示 JSON 內容

    
    elif filepath.endswith(".pdf") :
        if "多元表現綜整心得" or "其他" or "學習歷程自述" in filename:
            page = ttk.Frame(nb) # 創建新的Frame
            nb.add(page, text=((os.path.basename(filename)).split("_")[-1]).split(".json")[0]) # 將Frame 添加到Notebook
            main = setCanvas(page)
            display_else_pdf(filepath, main, 0)
                              
def display_else_pdf(filename, page,row):
    ttk.Label(page, text=filename).grid(column=0, row=row, sticky="W")
    button = tk.Button(page, text="顯示檔案", command=lambda : show_file(filename))
    button.grid(column=1, row=row, sticky="W")                               
    row+=1                    
  
def create_json_table(filename,tree):
    def calculate_relative_performance(score, distribution, total_count, lose_num):       
        interval_min = None  # 分數區間的最小值
        interval_max = None  # 分數區間的最大值
        range_num = 0 #區間總人數

        for key, value in distribution.items():
            min, max = key.split("_")
            min = int(min.replace("組距", ""))
            max = int(max.replace("的人數", ""))

            if min > score:           
                lose_num += value   

            if min <= score <= max:             
                interval_min = min
                interval_max = max            
                range_num = value

        relative_performance = (((1 - (score - interval_min) / (interval_max - interval_min)) * range_num + lose_num )/ total_count) * 100
        return str(round(relative_performance, 1)) + "%"

    # 讀取JSON檔案
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 取得修課紀錄資料
    records = data[list(data.keys())[1]]
    
    # 創建表格
    # tree = ttk.Treeview(root, columns=("學年度", "學期", "課程類別", "科目名稱", "學分數", "學業成績", "推估相對表現"))
    
    # 設置表格欄位名稱並置中對齊
    for column in tree["columns"]:
        tree.heading(column, text=column, anchor="center")
        tree.column(column, anchor="center", stretch=True, width=90)
        tree.heading(column, command=lambda col=column: sort_treeview(tree, col, False))  # 添加點擊事件

    # 設置第 0 欄的寬度為 0
    tree.column("#0", width=0)


    # 插入資料
    for record in records:
        score = int(record["學業成績"]["分數"])
        # 分數分布資料
        distribution = record["本科目分數級距分布"]
        # 班級總人數
        total_count = int(record["母體人數"])
        row = [
            record["實際修課學年度"],
            record["實際修課學期"],
            record["課程類別"],
            record["科目名稱"],
            int(record["學分數"]),
            score,
            calculate_relative_performance(score, distribution, total_count, 0)
        ]
        tree.insert("", "end", values=row)
    # 設置Treeview的大小和位置
    tree.pack(fill="both", expand=True)

def sort_treeview(tree, col, reverse):
    def convert_to_float_with_percent(value):
        # 移除百分比符號並轉換為浮點數
        try:
            return float(value.replace("%", ""))
        except ValueError:
            return 0.0  # 轉換失敗時，返回 0.0

    # 取得所有行的資料，並使用自定義排序函數進行排序
    data = [(convert_to_float_with_percent(tree.set(child, col)), child) for child in tree.get_children('')]
    data.sort(key=lambda x: x[0], reverse=reverse)

    for index, item in enumerate(data):
        tree.move(item[1], '', index)  # 重新排列 tree 中的行

    # 更改欄位標題的點擊事件，切換排序順序
    tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))


# filename = 檔案名稱 / page = 顯示的頁面（一個 Tkinter Frame）
#List=dict / 多元表現=dict / 修課紀錄=dict / 基本資料=dict / 課程學習成果=list
def display_json(filename, page): # 顯示 JSON 檔案的內容
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f) # 將 JSON 格式的數據轉換為 Python 對象，ex字典、列表   
    row = 0  
    if type(data)==dict:      
        for key, value in data.items(): # 字典每一項鍵值對          
            key_label = ttk.Label(page, text=key, style="Grey.TLabel") #列出標題
            key_label.grid(column=0, row=row, sticky="w")
            row+=1   
            if isinstance(value, dict): # 如果value是字典
                ttk.Label(page, text=key+": ").grid(column=0, row=row, sticky="W") # 則使用 ttk.Label 顯示鍵和值，使用 grid 函數定位元件。
                for k, v in value.items():
                    ttk.Label(page, text=k+": ").grid(column=1, row=row, sticky="W")
                    ttk.Label(page, text=v, wraplength=1000, anchor="w", justify="left").grid(column=2, row=row, sticky="W")
                    row += 1
            elif isinstance(value, list): # 如果value是list
                for dictionary in value: #該list中的各個dictionary 
                    ttk.Label(page, text="\n").grid(column=0, row=row, sticky="W")      
                    for kk, vv in dictionary.items(): # 走遍該字典每一項鍵值對
                        if kk in ["證明文件連結", "影音檔案連結", "外部影音連結"]:    
                            filepath = os.path.join(os.path.dirname(filename), vv)
                            
                            ttk.Label(page, text=kk).grid(column=0, row=row, sticky="W")
                            if os.path.isfile(filepath):
                                # 創建按鈕
                                #print(filepath)
                                button = tk.Button(page, text="顯示檔案", command=lambda filepath=filepath: show_file(filepath))
                                button.grid(column=1, row=row, sticky="W")                               
                            else:
                                ttk.Label(page, text="無").grid(column=1, row=row, sticky="W")
                            row+=1                        
                        elif isinstance(vv, dict)==False:  # 如果值不是一個字典，則只顯示鍵和值
                            ttk.Label(page, text=kk+": ").grid(column=0, row=row, sticky="W")
                            ttk.Label(page, text=vv, wraplength=1000, anchor="w", justify="left").grid(column=1, row=row, sticky="W")                       
                            row += 1         
            else:  # 如果值不是一個字典，則只顯示鍵和值
                ttk.Label(page, text=key+": ").grid(column=0, row=row, sticky="W")
                ttk.Label(page, text=value, wraplength=1000, anchor="w", justify="left").grid(column=1, row=row, sticky="W")
                row += 1 
         
        
    elif type(data)==list: 
        for dictionary in data: #列表中的各個dictionary
            #print(type(dictionary))         
            for kk, vv in dictionary.items(): # 該字典每一項鍵值對
                if kk in ["課程學習成果文件檔案連結", "課程學習成果影音檔案連結", "外部影音連結"]:    
                    filepath = os.path.join(os.path.dirname(filename), vv)
                    
                    ttk.Label(page, text=kk).grid(column=0, row=row, sticky="W")
                    if os.path.isfile(filepath):
                        # 創建按鈕

                        button = tk.Button(page, text="顯示檔案", command=lambda filepath=filepath: show_file(filepath))
                        button.grid(column=1, row=row, sticky="W")                               
                    else:
                        ttk.Label(page, text="無").grid(column=1, row=row, sticky="W")
                    row+=1 

                elif isinstance(vv, dict): # 如果值是一個字典
                    ttk.Label(page, text=kk+": ").grid(column=0, row=row, sticky="W") # 則使用 ttk.Label 顯示鍵和值，使用 grid 函數定位元件。
                    for k, v in vv.items():
                        ttk.Label(page, text=k+": ").grid(column=1, row=row, sticky="W")
                        ttk.Label(page, text=v, wraplength=1000, anchor="w", justify="left").grid(column=2, row=row, sticky="W")
                        row += 1
                else:  # 如果值不是一個字典，則只顯示鍵和值
                    ttk.Label(page, text=kk+": ").grid(column=0, row=row, sticky="W")
                    ttk.Label(page, text=vv, wraplength=1000, anchor="w", justify="left").grid(column=1, row=row, sticky="W")
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
        
def setCanvas(page) :
    # 設定 Canvas
    # Create canvas inside main frame
    my_canvas = tk.Canvas(page)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Create ScrollBar inside main frame
    my_scrollbar = ttk.Scrollbar(page, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    # Creating internal frame for the buttons
    main = tk.Frame(my_canvas)
    main.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
    my_canvas.create_window((0,0), window=main, anchor="nw")
    return main


root = tk.Tk()
style = ttk.Style()
# 背景顏色為淺灰色
style.configure("Grey.TLabel", background="light grey")
root.title("評分輔助系統")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

open_folder()#直接讓使用者上傳資料夾

root.mainloop()
