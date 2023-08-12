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
# 課程學習成果
# 申請/非申請模式

# 每一筆資料的成果類別代碼 
def display_course_performance(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)   
    for record in data:   
        if "成果類別代碼" in record:
            result_code = record["成果類別代碼"]

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
                            command=lambda filepath=filepath: Audio_video_scrolling.show_file(filepath),
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
                            command=lambda filepath=filepath: Audio_video_scrolling.show_file(filepath),
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
                                    command=lambda filepath=filepath: Audio_video_scrolling.show_file(
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
                            command=lambda filepath=filepath: Audio_video_scrolling.show_file(filepath),
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