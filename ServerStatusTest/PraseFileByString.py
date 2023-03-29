import tkinter as tk
from tkinter import filedialog
import os

def find_and_save():
    # 获取选择的文件路径
    filepath = filedialog.askopenfilename()

    # 获取输入的字符串
    search_string = search_input.get()

    # 获取选择文件的目录
    directory = os.path.dirname(filepath)

    # 获取输出文件名
    output_filename = os.path.join(directory, search_string + ".txt")

    # 打开文件并查找包含字符串的行
    with open(filepath, "r") as f, open(output_filename, "w") as output_file:
        for line in f:
            if search_string in line:
                output_file.write(line)

    # 输出完成信息
    status_label.config(text="Done! Results saved in {}".format(output_filename))

# 创建窗口
window = tk.Tk()

# 创建选择文件按钮
file_button = tk.Button(text="Select File", command=find_and_save)
file_button.pack()

# 创建搜索字符串输入框
search_input = tk.Entry()
search_input.pack()

# 创建状态标签
status_label = tk.Label(text="")
status_label.pack()

# 运行窗口
window.mainloop()
