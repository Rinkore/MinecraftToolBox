import os
import tkinter as tk
from tkinter import filedialog
import json
import re

# 定义全局变量，分别表示日志文件夹路径、最新日志文件名、fabricloader日志文件名
logs_folder = ""
fabricloader = "fabricloader.log"


# 定义函数，让用户选择fabricloader日志文件
def file_select():
    global fabricloader
    # 弹出对话框让用户选择文件
    root = tk.Tk()
    root.withdraw()
    fabricloader = filedialog.askopenfilename(title=f"请选择{fabricloader}")
    with open(fabricloader, 'r', encoding='gbk') as f:
        log = f.read()

    # 读取错误信息和错误原因的JSON文件
    with open('../../config/fabricloader.log.json', 'r', encoding='utf-8') as f:
        error_dict = json.load(f)

    # 遍历错误信息和错误原因的字典，查找匹配错误信息的正则表达式
    # 遍历错误信息和错误原因的字典，查找匹配错误信息的正则表达式
    for error, error_info in error_dict.items():
        match = re.search(error_info['regex'], log)
        if match:
            # 如果找到匹配的正则表达式，输出对应的错误原因
            message = error_info['message']
            # 使用正则表达式查找所有的$+数字，并替换为对应的匹配组
            for i in range(1, len(match.groups()) + 1):
                message = re.sub(f'\${i}', match.group(i), message)
            print(f"Error: {error}")
            print(f"Reason: {message}")
            break
    else:
        # 如果没有找到匹配的正则表达式，输出未知错误
        print("Unknown error.")


# 启动程序
file_select()
