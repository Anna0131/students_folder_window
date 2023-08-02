import json
import tkinter as tk
from tkinter import ttk
#修課紀錄table + 推估相對表現
filename = r"C:\Users\annnn\OneDrive\桌面\json_student\01686463\01686463_修課紀錄.json"

def calculate_relative_performance(score, distribution, total_count, lose_num):
    """
    計算推估相對表現
    score: 學生的分數
    distribution: 班級分數分布的組距字典資料
    total_count: 班級總人數
    lose_num: 分數小於等於學生分數的人數(輸過區間總人數)
    return: 推估相對表現
    """ 
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

# 創建tkinter視窗
root = tk.Tk()
root.title("JSON Table")

# 創建表格
tree = ttk.Treeview(root, columns=("學年度", "學期", "課程類別", "科目名稱", "學分數", "學業成績", "推估相對表現"))
# 設置表格欄位名稱並置中對齊
for column in tree["columns"]:
    tree.heading(column, text=column, anchor="center")
    tree.column(column, anchor="center")
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

# 啟動視窗
root.mainloop()

"""
def create_json_table(filename):
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
    tree = ttk.Treeview(root, columns=("學年度", "學期", "課程類別", "科目名稱", "學分數", "學業成績", "推估相對表現"))
    # 設置表格欄位名稱並置中對齊
    for column in tree["columns"]:
        tree.heading(column, text=column, anchor="center")
        tree.column(column, anchor="center")
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
"""