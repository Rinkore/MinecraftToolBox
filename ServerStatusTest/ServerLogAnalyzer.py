import os
import tkinter as tk
from tkinter import filedialog

# 定义全局变量，分别表示日志文件夹路径、最新日志文件名、fabricloader日志文件名
logs_folder = ""
lastest = "lastest.log"
fabricloader = "fabricloader.log"


# 定义函数，创建窗口并显示两个按钮和文本介绍
def function_select():
    root = tk.Tk()
    root.title("Button Selector")

    # 创建一个 Button，用于选择日志文件夹
    button_1 = tk.Button(root, text="选择文件夹", command=folder_select)
    button_1.grid(row=1, column=0)

    # 创建一个 Button，用于选择fabricloader日志文件
    button_2 = tk.Button(root, text=f"选择{fabricloader}", command=file_select)
    button_2.grid(row=1, column=1)

    # 创建一个 Canvas，用于显示方框介绍
    canvas = tk.Canvas(root, width=400, height=200)
    canvas.grid(row=2, columnspan=2)

    # 显示方框介绍
    rect_1 = canvas.create_rectangle(10, 10, 200, 100, fill="white")
    canvas.create_text(105, 55, text="选择服务端下的logs文件夹", font=("Arial", 10), fill="black")
    rect_2 = canvas.create_rectangle(210, 10, 400, 100, fill="white")
    canvas.create_text(305, 55, text=f"选择{fabricloader}", font=("Arial", 10), fill="black")

    # 为窗口关闭事件绑定处理函数，避免程序出错
    root.protocol("WM_DELETE_WINDOW", root.quit)

    # 进入主循环，等待用户操作
    root.mainloop()


# 定义函数，让用户选择日志文件夹
def folder_select():
    global logs_folder
    # 弹出对话框让用户选择文件夹
    root = tk.Tk()
    root.withdraw()
    logs_folder = filedialog.askdirectory(title="请选择Minecraft日志文件夹（即logs）")


# 定义函数，让用户选择fabricloader日志文件
def file_select():
    global fabricloader
    # 弹出对话框让用户选择文件
    root = tk.Tk()
    root.withdraw()
    fabricloader = filedialog.askopenfilename(title=f"请选择{fabricloader}")


#     TODO：分析fabricloader.log找出阻止服务端启动的原因（java版本或mod）

# 定义函数，分析最新日志文件内容
def lastest_analyzer():
    global lastest
    lastest_file = os.path.join(logs_folder, lastest)
    print(logs_folder, lastest)
    if os.path.exists(lastest_file):
        print("File found:", lastest_file)
        with open(lastest_file, 'r') as f:
            line_count = 0
            for line in f:
                line_count += 1
                print(f"Line {line_count}: {line.strip()}")
    #             TODO：对lastest.log文件分析获取被禁用的客户端mod以及导致服务端无法启动的mod让用户选择删除
    else:
        print("File not found in selected folder.")


# 启动程序
function_select()
