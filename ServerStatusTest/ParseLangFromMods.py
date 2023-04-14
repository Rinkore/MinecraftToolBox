import os
import shutil
import tkinter as tk
from tkinter import filedialog
import zipfile


def extract_assets():
    source_folder = source_folder_entry.get()
    target_folder = os.path.join(source_folder, "..", "langs-by-MTB")

    create_folder(target_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".jar"):
                extract_from_jar(os.path.join(root, file), target_folder)

    result_label.config(text="提取完成!")


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def extract_from_jar(jar_file, target_folder):
    langs_path = os.path.join(target_folder)
    create_folder(langs_path)
    with zipfile.ZipFile(jar_file, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if 'assets/' in file_name and '/lang/' in file_name:
                zip_ref.extract(file_name, langs_path)


def choose_source_folder():
    folder_path = filedialog.askdirectory()
    source_folder_entry.delete(0, tk.END)
    source_folder_entry.insert(0, folder_path)


# 创建主窗口
root = tk.Tk()
root.title("提取assets文件夹")
root.geometry("400x200")

# 创建文件夹选择控件
source_folder_label = tk.Label(root, text="选择源文件夹：")
source_folder_label.grid(row=0, column=0, padx=10, pady=10)
source_folder_entry = tk.Entry(root)
source_folder_entry.grid(row=0, column=1)
source_folder_button = tk.Button(root, text="选择文件夹", command=choose_source_folder)
source_folder_button.grid(row=0, column=2)

# 创建运行按钮
run_button = tk.Button(root, text="开始提取", command=extract_assets)
run_button.grid(row=2, column=1, pady=20)

# 创建结果标签
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=1)

# 启动主循环
root.mainloop()
