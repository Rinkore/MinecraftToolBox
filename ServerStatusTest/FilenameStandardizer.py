import os
import tkinter as tk
from tkinter import filedialog


def clean_folder(folder_path):
    """接受文件夹路径，遍历文件夹中的每个文件名，
    并使用字符串生成器表达式生成新的文件名，
    其中保留了所有字母数字字符、斜杠、下划线、点和破折号。
    最后，使用os.rename方法将原文件名重命名为新文件名。"""
    for filename in os.listdir(folder_path):
        new_filename = ''.join(c for c in filename if c.isalnum() or c in '/._-')
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))


def choose_folder():
    """创建一个tkinter根窗口并调用filedialog.askdirectory()方法以选择文件夹路径。
    如果用户选择了文件夹路径，则调用clean_folder函数进行文件名清理。"""
    root = tk.Tk()
    root.withdraw()
    root.title("请选择mods文件夹")  # 设置窗口标题
    folder_path = filedialog.askdirectory()
    if folder_path:
        clean_folder(folder_path)


if __name__ == '__main__':
    choose_folder()
