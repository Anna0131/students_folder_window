import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',           # 主要啟動程式
    '--onefile',         # 打包成單個執行檔
    '--noconsole',       # 隱藏控制台窗口（如果是GUI應用程式）
    # 其他選項和參數
])
