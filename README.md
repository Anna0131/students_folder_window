# 系統功能
輔助評分委員線上瀏覽高中生申請入學的學習歷程，提升審查效率和方便性，強化審查的準確度，並優化學生的強項顯示。可於系統瀏覽各學生的基本資料、修課紀錄、課程成果、多元表現，並將各項目分數由高到低顯示。系統提供快速檢視學上傳之圖片及影片功能，和比較同項目比分差並進行排序功能。 

- 負責項目：需求訪談、系統開發。 

- 系統畫面

    - 可查看學生上傳之課程學習成果 
        -  ![image](https://hackmd.io/_uploads/Hy4HZ5uWJe.png)

    - 顯示學生之修課紀錄，可排序推估相對表現和學業成績
        -  ![image](https://hackmd.io/_uploads/HJvHZquW1l.png)



# 系統畫面
![image](https://github.com/user-attachments/assets/005508cf-6c0b-4392-8e0f-9ccc7b3c8c63)
![評分審查基本](https://github.com/user-attachments/assets/4c9547c4-935a-4003-ba7b-8ed9dfdb9b54)


# JSON分割資料/圖片顯示

### 程式功能說明

- 按下 "Open Folder" 按鈕來選擇一個資料夾上傳

程式會把該資料夾中所有的JSON檔案處理好後，顯示在 **Notebook widget(一個包含多個分頁的控件)** 中的不同 **tab(分頁上方的標籤，用來標示出不同分頁的內容。)** 中。
- 按下 "Close" 按鈕可以關閉此應用程式。
> 使用者無法編輯視窗顯示的內容，只能查看。





### 引入模組/函式庫
- `import os`: 提供與作業系統互動的方法，例如檔案、目錄管理。
- `import json`: 將 JSON 格式的字串轉換為 Python 物件。
- `import tkinter as tk`: Tkinter 是 Python 的標準 GUI 庫，用來建立桌面應用程式。
- `from tkinter import ttk`: 提供多種小組件（widget），例如 Notebook、Button 。
- `from tkinter import filedialog`: 提供使用者`選擇檔案`的對話框。

## 圖形化使用者界面 GUI(Graphical User Interface)
使用者介面上的個別元素稱為Widget。

用GUI框架開發應用程式時，需要在視窗中顯示各種元素(ex: 按鈕、文字、輸入框)，所以要使用 **容器 widget(一種可以容納其他 widget 的 widget)** ，才能將元素們放置到視窗中。
> 把widget想像成手機用來添加小功能的組件，可以放不同小組鍵在手機桌面

Frame是一個容器widget，用來佈置 GUI 界面，且可以嵌套使用。
> 嵌套: 
> 將一個小的組件放在另一個更大的組件內的過程。
> 舉例來說，可以**創建一個按鈕放在frame這個容器widget中**

在ttk模塊中也提供了類似的容器(ttk.Frame、ttk.LabelFrame)。


範例 (用ttk.Frame創建一個框架)
```python=
import tkinter as tk
from tkinter import ttk

# 創建主窗口
root = tk.Tk()

# 創建一個名為 frame 的 ttk.Frame 物件
frame = ttk.Frame(root)

# 將 frame 加入到視窗中顯示
frame.pack()

# 創建一個按鈕，並將其放入 frame 中
button = ttk.Button(frame, text="Click Me!")

#pack()用於將 widget 排列在其父容器中。
button.pack()

# 開始主事件循環
root.mainloop()
```


### 放置 Widget 至容器/視窗中
- 讓元素(元件)根據容器自動調整大小 -> `pack()`
- 控制元件在容器中的位置 -> `grid()`
- 精確地指定元件在容器中的位置和大小 -> `place()`

### Notebook widget/Tab
`frame = ttk.Frame(nb)`
nb 是一個新創的 Notebook 物件，是有多個 Tab (標籤、便利貼）的容器widget，用來顯示多個子視窗(可以切換不同的內容或功能)，每個 Tab 是一個 frame (容器 widget)


## 主要程式碼

1. `display_json` :讀取一個 JSON 檔案，並以視窗標籤的方式顯示資料出來。
- isinstance() 檢查物件是否屬於某種特定類型。
它的語法如下：
obj 是要檢查的物件，classinfo 是要檢查的類型。
如果 obj 是 classinfo 的實例，則該函式返回 True，否則返回 False。
```python=
isinstance(obj, classinfo)
```

isinstance()`範例
```python=
x = 42
if isinstance(x, int):
    print("x is an integer")
else:
    print("x is not an integer")
```

- wraplength、anchor 和 justify 等參數用於控制標籤顯示的方式和格式。



3. `open_folder` 打開一個資料夾，遍歷資料夾中的所有JSON檔案並顯示在一個Notebook widget中。
4. GUI部分 : 包括創建主視窗、按鈕、Notebook widget等，以及啟動主事件迴圈。

## 顯示讀入的資料夾內容
- display_pdf() ->將 PDF 檔案顯示在 GUI 的視窗中
```python=
def display_pdf(filename, page):
    doc = fitz.open(filename) # 使用 fitz 套件打開 PDF 文件
    for i in range(doc.page_count): # 遍歷 PDF 文件中的每一頁
        img = doc.load_page(i).get_pixmap() # 將每一頁轉換成圖像格式
        imgtk = tk.PhotoImage(data=img.tobytes()) # 將圖像轉換為 tkinter 可以使用的 PhotoImage 格式

        # 創建了一個 ttk 標籤(Label)物件，其中包含一個圖像(image)作為屬性
        panel = ttk.Label(page, image=imgtk) 
        # 將該圖像(image)存儲在標籤(Label)物件上的 image 屬性中，從而防止它被垃圾回收機制刪除。
        panel.image = imgtk 

        # 將元件加入到頁面中
        panel.pack(side="left", fill="both", expand=True)
        page.add(panel)
```
> 在 Tkinter 中創建一個標籤(Label)，可以設置一個圖像(image)作為其屬性，以顯示該圖像。但是，由於 Tkinter 的垃圾回收機制，該圖像將會被回收並從內存中刪除，這將導致標籤(Label)不再顯示圖像。為了解決這個問題，可以將圖像(image)賦值給標籤(Label)的另一個屬性(panel.image)，這樣就可以保留圖像的引用，從而避免圖像被回收並刪除。

- open_folder() ->選擇資料夾，並將該資料夾下的檔案顯示在 ttk.Notebook 中
```python=
def open_folder():
    # folder_path = 所選資料夾的路徑 
    folder_path = tk.filedialog.askdirectory() 
    if folder_path: # 如果選擇了資料夾
        nb = ttk.Notebook(root) # 創建 ttk.Notebook 對象
        nb.pack(fill="both", expand=True) # 將 ttk.Notebook 對象填充整個窗口並展開

        for filename in os.listdir(folder_path): # 遍歷所選資料夾下的所有檔案
            filepath = os.path.join(folder_path, filename) # 獲取檔案路徑
            display_file(filepath, nb) # 將檔案顯示在 ttk.Notebook 中
```
> askdirectory() 是 filedialog 模組中的一個函數，專門用於選擇目錄或文件夾

>  fill="both" 指定視窗填滿 root 物件的寬度和高度，而 expand=True 指定視窗隨著 root 物件的大小變化而擴展
