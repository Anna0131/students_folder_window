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
# 修課紀錄

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
        "全部",
        "語文領域",
        "數學領域",
        "社會領域",
        "自然科學領域",
        "藝術領域",
        "綜合活動領域",
        "科技領域",
        "健康與體育領域",
        "全民國防教育",
        "校訂必修及選修", "專業及實習科目(技高)、專精科目(綜高)"
    ]

    # 課程類別
    #others_domains = ["校訂必修及選修", "專業及實習科目(技高)、專精科目(綜高)"]

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
        domain_filter_frame, text="篩選課程"
    )  
    domain_label.pack(anchor="w", side=tk.LEFT)

    # 下拉選單顯示八大領域一般課程的所有選項
    domain_filter = ttk.Combobox(
        domain_filter_frame, values=domains
    )  # 下拉選單的選項為 domains 列表
    domain_filter.pack(anchor="w", side=tk.LEFT)

    # 新增下拉選單 "其他多元特色及專業課程"
    """
    other_courses_frame = ttk.Frame(domain_filter_frame)
    other_courses_frame.pack(side=tk.RIGHT, fill=tk.X)

    other_courses_label = ttk.Label(domain_filter_frame, text="其他多元特色及專業課程")
    other_courses_label.pack(anchor="w", side=tk.LEFT)

    other_courses_filter = ttk.Combobox(domain_filter_frame, values=others_domains)
    other_courses_filter.pack(anchor="w", side=tk.LEFT)

    """
    
    # 根據選擇的領域 篩選符合條件的課程資料並顯示在頁面
    def on_domain_select(event):
        selected_value = domain_filter.get()
        if (selected_value == "校訂必修及選修" or 
            selected_value == "專業及實習科目(技高)" or 
            selected_value == "專精科目(綜高)"):     
            filter_courses_by_domain(records, tree, domain_filter, selected_value, 2)
        elif (selected_value=="全部"):
            filter_courses_by_domain(records, tree, domain_filter, selected_value, 0)
        else:
            filter_courses_by_domain(records, tree, domain_filter, selected_value, 1)
    domain_filter.bind(
        "<<ComboboxSelected>>", on_domain_select
    )  
    # 當使用者選擇其他多元特色及專業課程下拉選單
    """
    def on_other_courses_select(event):
        other_selected_value = other_courses_filter.get()
        filter_courses_by_domain(
            records, tree, other_courses_filter, other_selected_value, 2
        )
    other_courses_filter.bind("<<ComboboxSelected>>", on_other_courses_select)
    """
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
        elif num==0: # 全部課程
            selected_courses = list(records)
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

    # 重設所有欄位標題，刪除箭頭符號
    for col_id in tree["columns"]:
        tree.heading(col_id, text=col_id)

    # 在點擊的欄位上顯示箭頭
    arrow = " ↓" if reverse else " ↑"
    tree.heading(col, text=col + arrow, command=lambda: sort_treeview(tree, col, not reverse))
