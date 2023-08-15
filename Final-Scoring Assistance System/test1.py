import tkinter as tk
from tkinter import ttk

def setCanvas(page):
    my_canvas = tk.Canvas(page)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # 垂直捲軸放在右邊
    v_scrollbar = ttk.Scrollbar(page, orient=tk.VERTICAL, command=my_canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    my_canvas.configure(yscrollcommand=v_scrollbar.set)

    # 放置內容的內部 frame
    main = tk.Frame(my_canvas)
    my_canvas.create_window((0, 0), window=main, anchor="nw")

    # 綁定滑鼠滾輪事件，實現垂直捲動
    def on_mousewheel(event):
        my_canvas.yview_scroll(-1 * int(event.delta / 120), "units")
    my_canvas.bind("<MouseWheel>", on_mousewheel)

    # 當 main 的大小變化時，重新設定畫布的捲動區域，實現捲動效果
    def configure_canvas(event):
        my_canvas.configure(scrollregion=my_canvas.bbox("all"))
    main.bind("<Configure>", configure_canvas)

    return main

# 建立主視窗
root = tk.Tk()

# 建立 Notebook
nb = ttk.Notebook(root)
nb.pack(fill="both", expand=True)

# 建立頁面並加入 Notebook
page1 = ttk.Frame(nb)
nb.add(page1, text="Page 1")
main_content = setCanvas(page1)

# 建立一些內容放入 main_content 內
for i in range(50):
    tk.Label(main_content, text=f"Label {i}").pack()

root.mainloop()
