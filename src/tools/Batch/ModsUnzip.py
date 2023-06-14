import os
import shutil
import tkinter as tk
from tkinter import filedialog
import zipfile


# 定义函数，用于解压jar文件中的assets文件夹
def extract_assets(jar_path):
    # 创建langs/A文件夹
    langs_path = os.path.join(os.path.dirname(jar_path), '', 'langs-by-MTB')
    print(langs_path)
    if not os.path.exists(langs_path):
        os.makedirs(langs_path)

    # 打开jar文件
    with zipfile.ZipFile(jar_path, 'r') as zip_ref:
        # 遍历jar文件中的所有文件和文件夹
        for file_name in zip_ref.namelist():
            # 如果文件名包含assets/，则提取到langs/A文件夹中
            if 'assets/' in file_name:
                # 提取文件
                zip_ref.extract(file_name, langs_path)


# 创建窗口
root = tk.Tk()


# 定义函数，用于选择原mods文件夹
def choose_folder():
    global mods_folder_path
    mods_folder_path = filedialog.askdirectory()
    mods_folder_label.config(text='已选择：' + mods_folder_path)


# 定义函数，用于运行程序
def run_program():
    # 将选择的文件夹设置为当前工作目录
    os.chdir(mods_folder_path)

    # 遍历目标文件夹中的所有文件
    for file_name in os.listdir('../ServerStatusTest'):
        print(file_name)
        # 如果文件是一个jar文件，则解压assets文件夹
        if file_name.endswith('.jar'):
            extract_assets(file_name)

    # 显示完成信息
    finish_label.config(text='完成！')


# 创建选择文件夹按钮
choose_button = tk.Button(root, text='选择原mods文件夹', command=choose_folder)
choose_button.pack(pady=10)

# 创建已选择文件夹标签
mods_folder_label = tk.Label(root, text='未选择')
mods_folder_label.pack()

# 创建运行程序按钮
run_button = tk.Button(root, text='运行程序', command=run_program)
run_button.pack(pady=10)

# 创建完成标签
finish_label = tk.Label(root, text='')
finish_label.pack()

# 运行窗口
root.mainloop()
