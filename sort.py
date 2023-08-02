import tkinter as tk
from tkinter import ttk
#練習sort
def sort_treeview(tree, column, reverse=False):
    data = [(tree.set(child, column), child) for child in tree.get_children('')]
    data.sort(reverse=reverse)
    for index, (value, child) in enumerate(data):
        tree.move(child, '', index)

def create_treeview():
    root = tk.Tk()
    tree = ttk.Treeview(root)
    tree['columns'] = ('學年度', '學期', '科目名稱')
    tree.heading('#0', text='學生')
    tree.heading('學年度', text='學年度', command=lambda: sort_treeview(tree, '學年度'))
    tree.heading('學期', text='學期', command=lambda: sort_treeview(tree, '學期'))
    tree.heading('科目名稱', text='科目名稱', command=lambda: sort_treeview(tree, '科目名稱'))
    tree.pack()
    return tree

# 創建Treeview
treeview = create_treeview()

# 插入資料
treeview.insert('', 'end', text='學生1', values=('109', '1', '數學'))
treeview.insert('', 'end', text='學生2', values=('108', '2', '英文'))
treeview.insert('', 'end', text='學生3', values=('109', '1', '歷史'))

# 啟動主迴圈
tk.mainloop()