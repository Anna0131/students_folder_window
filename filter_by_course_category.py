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

# 目前最新進度多個學生，課程類別功能

nb = None
student_buttons = None
mode = None


def open_folder():
    global base_folder, nb, mode
    # base_folder = r"C:\code_practice\json_student\json_student\000001"
    base_folder = filedialog.askdirectory()  # 讓使用者選擇資料夾
    if base_folder:
        tk.messagebox.showinfo("操作說明", f"請先點選模式，再點選學生。\n(您選擇的資料夾是：{base_folder}) ")
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

        def not_apply_mode():
            global mode
            mode = "非申請模式"

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
    global nb
    if nb:
        # 刪除現有的 notebook 頁面，方便切換顯示不同的子視窗
        nb.destroy()
    nb = ttk.Notebook(root)

    # 學生資料夾的所有檔案
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        display_file(filename, nb, filepath, choose_mode)

    nb.pack(side=tk.LEFT, fill="both", expand=True)


# 依據檔案類型 顯示該學生所有檔案
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
        create_json_table(filepath, tree)

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
                main = setCanvas(page)  # 加入捲軸
                display_json_mode_one(filepath, main)  # 顯示 JSON 內容

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
                main_top = setCanvas(top_frame)
                main_bottom = setCanvas(bottom_frame)
                display_json_mode_two(filepath, main_top, main_bottom)  # 顯示 JSON 內容
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
            main = setCanvas(page)
            display_json_mode_one(filepath, main)  # 顯示 JSON 內容

    elif filepath.endswith(".pdf"):
        if "多元表現綜整心得" or "其他" or "學習歷程自述" in filename:
            page = ttk.Frame(nb)
            nb.add(
                page,
                text=((os.path.basename(filename)).split("_")[-1]).split(".json")[0],
            )  # 將Frame 添加到Notebook
            main = setCanvas(page)
            display_else_pdf(filepath, main, 0)  # 顯示圖片


# 每一筆資料的成果類別代碼
def display_course_performance(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    for record in data:
        if "成果類別代碼" in record:
            result_code = record["成果類別代碼"]





# 修課紀錄頁面
def create_json_table(filename, tree):
    # 讀取JSON檔案
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 取得"修課紀錄"資料
    records = data[list(data.keys())[1]]

    # 相對表現函式
    def calculate_relative_performance(score, distribution, total_count, lose_num):
        interval_min = None  # 分數區間的最小值
        interval_max = None  # 分數區間的最大值
        range_num = 0  # 區間總人數

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

        relative_performance = (
            (
                (1 - (score - interval_min) / (interval_max - interval_min)) * range_num
                + lose_num
            )
            / total_count
        ) * 100
        return str(round(relative_performance, 1)) + "%"

    # 課程領域
    domains = [
        "語文領域",
        "數學領域",
        "社會領域",
        "自然科學領域",
        "藝術領域",
        "綜合活動領域",
        "科技領域",
        "健康與體育領域",
        "全民國防教育",
    ]

    # 課程類別
    others_domains = ["校訂必修及選修", "專業及實習科目(技高)、專精科目(綜高)"]

    # 從課程代碼得到課程領域名稱
    def get_domain(record):
        domain_code = record["課程代碼"][19:21]
        domain_mapping = {
            "01": "語文領域",
            "02": "數學領域",
            "03": "社會領域",
            "04": "自然科學領域",
            "05": "藝術領域",
            "06": "綜合活動領域",
            "07": "科技領域",
            "08": "健康與體育領域",
            "09": "全民國防教育",
        }
        return domain_mapping.get(domain_code, "未知領域")

    # 表格欄位名稱、置中對齊
    for column in tree["columns"]:
        tree.heading(column, text=column, anchor="center")
        tree.column(column, anchor="center", stretch=True, width=90)
        tree.heading(
            column, command=lambda col=column: sort_treeview(tree, col, False)
        )  # 排序功能(點擊)

    # 第0欄寬度=0
    tree.column("#0", width=0)

    # 新增一個下拉選單"八大領域一般課程"
    domain_filter_frame = ttk.Frame(tree)  # 新的 Frame 作為下拉選單的容器
    domain_filter_frame.pack(side=tk.BOTTOM, fill=tk.X)  # 該 Frame 在 tree 中的位置

    domain_label = ttk.Label(
        domain_filter_frame, text="八大領域一般課程"
    )  
    domain_label.pack(anchor="w", side=tk.LEFT)

    # 下拉選單顯示八大領域一般課程的所有選項
    domain_filter = ttk.Combobox(
        domain_filter_frame, values=domains
    )  # 下拉選單的選項為 domains 列表
    domain_filter.pack(anchor="w", side=tk.LEFT)

    # 新增下拉選單 "其他多元特色及專業課程"
    other_courses_frame = ttk.Frame(domain_filter_frame)
    other_courses_frame.pack(side=tk.RIGHT, fill=tk.X)

    other_courses_label = ttk.Label(domain_filter_frame, text="其他多元特色及專業課程")
    other_courses_label.pack(anchor="w", side=tk.LEFT)

    other_courses_filter = ttk.Combobox(domain_filter_frame, values=others_domains)
    other_courses_filter.pack(anchor="w", side=tk.LEFT)

    # 根據選擇的領域 篩選符合條件的課程資料並顯示在頁面
    def on_domain_select(event):
        selected_value = domain_filter.get()
        filter_courses_by_domain(records, tree, domain_filter, selected_value, 1)
    domain_filter.bind(
        "<<ComboboxSelected>>", on_domain_select
    )  
    # 當使用者選擇其他多元特色及專業課程下拉選單
    def on_other_courses_select(event):
        other_selected_value = other_courses_filter.get()
        filter_courses_by_domain(
            records, tree, other_courses_filter, other_selected_value, 2
        )
    other_courses_filter.bind("<<ComboboxSelected>>", on_other_courses_select)

    # 表格欄位 = "學年度", "學期", "課程類別", "科目名稱", "學分數", "學業成績", "推估相對表現"
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
            calculate_relative_performance(score, distribution, total_count, 0),
        ]
        tree.insert("", "end", values=row)
    tree.pack(fill="both", expand=True)

    def filter_courses_by_domain(records, tree, filter, selected_domain, num):
        if num == 1:  # "八大領域一般課程" 下拉選單
            # 篩選符合選擇的課程
            selected_courses = [
                record
                for record in records
                if get_domain(record) == selected_domain
                and (record["課程代碼"][16] == "1" or record["課程代碼"][16] == "3")
                and record["課程代碼"][-5] == "1"  # 課程類別為部定必修、選修-加深加廣選修  # 科目屬性：一般科目
            ]

        elif num == 2:  # "其他多元特色及專業課程" 下拉選單
            if selected_domain == "校訂必修及選修":
                selected_courses = [  # 篩選符合選擇的課程
                    # 校訂必修及選修=課程類別為校訂必修、校訂選修、選修-多元選修，且科目屬性為一般科目
                    record
                    for record in records
                    if (
                        (record["課程代碼"][16] == "2")
                        or (record["課程代碼"][16] == "5")
                        or (record["課程代碼"][16] == "7")
                    )
                    and (record["課程代碼"][-5] == "1")
                ]
            elif selected_domain == "專業及實習科目(技高)、專精科目(綜高)":
                # 專業及實習科目(技高)、專精科目(綜高)=課程類別為部定必修、校訂必修、校訂選修、基礎訓練、職前訓練、寒暑假課程、返校課程、職業技能訓練，且科目屬性為 專業科目、實習科目、專精科目、專精科目(核心科目)
                selected_courses = [
                    record
                    for record in records
                    # 篩選符合選擇的課程
                    if (  
                        (record["課程代碼"][16] == "1")
                        or (record["課程代碼"][16] == "2")
                        or (record["課程代碼"][16] == "7")
                        or (record["課程代碼"][16] == "B")
                        or (record["課程代碼"][16] == "C")
                        or (record["課程代碼"][16] == "D")
                        or (record["課程代碼"][16] == "E")
                        or (record["課程代碼"][16] == "F")
                    )
                    and (
                        (record["課程代碼"][-5] == "2")
                        or (record["課程代碼"][-5] == "3")
                        or (record["課程代碼"][-5] == "4")
                        or (record["課程代碼"][-5] == "5")
                    )
                ]

        # 清除舊資料並顯示新的資料
        tree.delete(*tree.get_children())
        # 遍歷篩選後的課程並顯示在tree
        for record in selected_courses:
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
                calculate_relative_performance(score, distribution, total_count, 0),
            ]
            tree.insert("", "end", values=row)


def sort_treeview(tree, col, reverse):
    def convert_to_float_with_percent(value):
        # 移除百分比符號並轉換為浮點數
        try:
            return float(value.replace("%", ""))
        except ValueError:
            return 0.0

    # 取得所有行的資料並排序
    data = [
        (convert_to_float_with_percent(tree.set(child, col)), child)
        for child in tree.get_children("")
    ]
    data.sort(key=lambda x: x[0], reverse=reverse)

    for index, item in enumerate(data):
        tree.move(item[1], "", index)  # 重新排列 tree 中的行

    # 更改欄位標題的點擊事件，切換排序順序
    tree.heading(col, command=lambda: sort_treeview(tree, col, not reverse))


def display_json_mode_two(filename, main_top, main_bottom):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    row = 0

    for dictionary in data:
        category_code = dictionary["成果類別代碼"]
        if category_code == "1":
            for kk, vv in dictionary.items():  # 該字典每一項鍵值對
                if kk in ["課程學習成果文件檔案連結", "課程學習成果影音檔案連結", "外部影音連結"]:
                    filepath = os.path.join(os.path.dirname(filename), vv)
                    ttk.Label(main_top, text=kk).grid(column=0, row=row, sticky="W")
                    if os.path.isfile(filepath):
                        button = tk.Button(
                            main_top,
                            text="顯示檔案",
                            command=lambda filepath=filepath: show_file(filepath),
                        )
                        button.grid(column=1, row=row, sticky="W")
                    else:
                        ttk.Label(main_top, text="無").grid(
                            column=1, row=row, sticky="W"
                        )
                    row += 1

                elif isinstance(vv, dict):  # 如果值是一個字典
                    ttk.Label(main_top, text=kk + ": ").grid(
                        column=0, row=row, sticky="W"
                    )
                    for k, v in vv.items():
                        ttk.Label(main_top, text=k + ": ").grid(
                            column=1, row=row, sticky="W"
                        )
                        ttk.Label(
                            main_top,
                            text=v,
                            wraplength=1000,
                            anchor="w",
                            justify="left",
                        ).grid(column=2, row=row, sticky="W")
                        row += 1
                else:  # 如果值不是一個字典，則只顯示鍵和值
                    ttk.Label(main_top, text=kk + ": ").grid(
                        column=0, row=row, sticky="W"
                    )
                    ttk.Label(
                        main_top, text=vv, wraplength=1000, anchor="w", justify="left"
                    ).grid(column=1, row=row, sticky="W")
                    row += 1
        elif category_code == "2":
            for kk, vv in dictionary.items():  # 該字典每一項鍵值對
                if kk in ["課程學習成果文件檔案連結", "課程學習成果影音檔案連結", "外部影音連結"]:
                    filepath = os.path.join(os.path.dirname(filename), vv)
                    ttk.Label(main_bottom, text=kk).grid(column=0, row=row, sticky="W")
                    if os.path.isfile(filepath):
                        button = tk.Button(
                            main_bottom,
                            text="顯示檔案",
                            command=lambda filepath=filepath: show_file(filepath),
                        )
                        button.grid(column=1, row=row, sticky="W")
                    else:
                        ttk.Label(main_bottom, text="無").grid(
                            column=1, row=row, sticky="W"
                        )
                    row += 1

                elif isinstance(vv, dict):  # 如果值是一個字典
                    ttk.Label(main_bottom, text=kk + ": ").grid(
                        column=0, row=row, sticky="W"
                    )
                    for k, v in vv.items():
                        ttk.Label(main_bottom, text=k + ": ").grid(
                            column=1, row=row, sticky="W"
                        )
                        ttk.Label(
                            main_bottom,
                            text=v,
                            wraplength=1000,
                            anchor="w",
                            justify="left",
                        ).grid(column=2, row=row, sticky="W")
                        row += 1
                else:  # 如果值不是一個字典，則只顯示鍵和值
                    ttk.Label(main_bottom, text=kk + ": ").grid(
                        column=0, row=row, sticky="W"
                    )
                    ttk.Label(
                        main_bottom,
                        text=vv,
                        wraplength=1000,
                        anchor="w",
                        justify="left",
                    ).grid(column=1, row=row, sticky="W")
                    row += 1


def display_json_mode_one(filename, page):  # 顯示 JSON 檔案的內容
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    row = 0
    # 多元表現=dict / 修課紀錄=dict / 基本資料=dict
    if type(data) == dict:
        for key, value in data.items():  # 字典每一項鍵值對
            key_label = ttk.Label(page, text=key, style="Grey.TLabel")  # 列出標題
            key_label.grid(column=0, row=row, sticky="w")
            row += 1
            if isinstance(value, dict):  # 如果value是字典
                ttk.Label(page, text=key + ": ").grid(
                    column=0, row=row, sticky="W"
                )  # 則使用 ttk.Label 顯示鍵和值，使用 grid 函數定位元件。
                for k, v in value.items():
                    ttk.Label(page, text=k + ": ").grid(column=1, row=row, sticky="W")
                    ttk.Label(
                        page, text=v, wraplength=1000, anchor="w", justify="left"
                    ).grid(column=2, row=row, sticky="W")
                    row += 1
            elif isinstance(value, list):  # 如果value是list
                for dictionary in value:  # 該list中的各個dictionary
                    ttk.Label(page, text="\n").grid(column=0, row=row, sticky="W")
                    for kk, vv in dictionary.items():  # 走遍該字典每一項鍵值對
                        if kk in ["證明文件連結", "影音檔案連結", "外部影音連結"]:
                            filepath = os.path.join(os.path.dirname(filename), vv)

                            ttk.Label(page, text=kk).grid(column=0, row=row, sticky="W")
                            if os.path.isfile(filepath):
                                button = tk.Button(
                                    page,
                                    text="顯示檔案",
                                    command=lambda filepath=filepath: show_file(
                                        filepath
                                    ),
                                )
                                button.grid(column=1, row=row, sticky="W")
                            else:
                                ttk.Label(page, text="無").grid(
                                    column=1, row=row, sticky="W"
                                )
                            row += 1
                        elif isinstance(vv, dict) == False:  # 如果值不是一個字典，則只顯示鍵和值
                            ttk.Label(page, text=kk + ": ").grid(
                                column=0, row=row, sticky="W"
                            )
                            ttk.Label(
                                page,
                                text=vv,
                                wraplength=1000,
                                anchor="w",
                                justify="left",
                            ).grid(column=1, row=row, sticky="W")
                            row += 1
            else:  # 如果值不是一個字典，則只顯示鍵和值
                ttk.Label(page, text=key + ": ").grid(column=0, row=row, sticky="W")
                ttk.Label(
                    page, text=value, wraplength=1000, anchor="w", justify="left"
                ).grid(column=1, row=row, sticky="W")
                row += 1

    # 課程學習成果=list
    elif type(data) == list:
        for dictionary in data:  # 列表中的各個dictionary
            for kk, vv in dictionary.items():  # 該字典每一項鍵值對
                if kk in ["課程學習成果文件檔案連結", "課程學習成果影音檔案連結", "外部影音連結"]:
                    filepath = os.path.join(os.path.dirname(filename), vv)
                    ttk.Label(page, text=kk).grid(column=0, row=row, sticky="W")
                    if os.path.isfile(filepath):
                        button = tk.Button(
                            page,
                            text="顯示檔案",
                            command=lambda filepath=filepath: show_file(filepath),
                        )
                        button.grid(column=1, row=row, sticky="W")
                    else:
                        ttk.Label(page, text="無").grid(column=1, row=row, sticky="W")
                    row += 1

                elif isinstance(vv, dict):  # 如果值是一個字典
                    ttk.Label(page, text=kk + ": ").grid(column=0, row=row, sticky="W")
                    for k, v in vv.items():
                        ttk.Label(page, text=k + ": ").grid(
                            column=1, row=row, sticky="W"
                        )
                        ttk.Label(
                            page, text=v, wraplength=1000, anchor="w", justify="left"
                        ).grid(column=2, row=row, sticky="W")
                        row += 1
                else:  # 如果值不是一個字典，則只顯示鍵和值
                    ttk.Label(page, text=kk + ": ").grid(column=0, row=row, sticky="W")
                    ttk.Label(
                        page, text=vv, wraplength=1000, anchor="w", justify="left"
                    ).grid(column=1, row=row, sticky="W")
                    row += 1

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

    # 水平捲軸放在下面
    h_scrollbar = ttk.Scrollbar(page, orient=tk.HORIZONTAL, command=my_canvas.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    my_canvas.configure(xscrollcommand=h_scrollbar.set)

    # 放置內容的內部 frame
    main = tk.Frame(my_canvas)
    # 當 main 的大小變化時，重新設定畫布的捲動區域，實現捲動效果
    main.bind(
        "<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all"))
    )
    # 創建一個可捲動的視窗，並將 main 放置在視窗中
    my_canvas.create_window((0, 0), window=main, anchor="nw")  # 左上角 (anchor="nw")

    return main


root = tk.Tk()
style = ttk.Style()
style.configure("Grey.TLabel", background="light grey")  # 背景顏色為淺灰色
root.title("評分輔助系統")
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.geometry("1200x550")

open_folder()

root.mainloop()
