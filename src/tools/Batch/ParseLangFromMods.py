import os
import random
import tkinter as tk
from tkinter import filedialog
import zipfile
from PIL import Image


def create_meta_files(target_folder):
    with open(os.path.join(target_folder, 'pack.mcmeta'), 'w', encoding='utf-8') as f:
        f.write('''{
      "pack": {
        "pack_format": 6,
        "description": "该资源包由Rinkore28的汉化工具生成，资源包务必附上工具作者，工具以及此资源包禁止商业用途的转载和发布"
      }
    }''')

    with open(os.path.join(target_folder, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write('该资源包由Rinkore28的汉化工具生成，资源包务必附上工具作者，工具以及此资源包禁止商业用途的转载和发布\n'
                'pack.mcmeta文件中的pack_format数字代表资源包的版本,它对应Minecraft版本如下:\n'
                'pack_format 6:Minecraft 1.13 - 1.18\n'
                'pack_format 5:Minecraft 1.12 - 1.12.2\n'
                'pack_format 4:Minecraft 1.10 - 1.11.2\n'
                'pack_format 3:Minecraft 1.8 - 1.9\n')


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


def generate_image(width, height):
    num_blocks = 16
    block_size = width // num_blocks * 4

    img = Image.new('RGB', (width, height))

    for i in range(num_blocks):
        x = i % 4 * block_size
        y = i // 4 * block_size
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = (r, g, b)

        block = Image.new('RGB', (block_size, block_size), color)
        img.paste(block, (x, y))

    return img


def extract_assets():
    source_folder = source_folder_entry.get()
    target_folder = os.path.join(source_folder, "..", "langs-by-MTB")

    create_folder(target_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".jar"):
                extract_from_jar(os.path.join(root, file), target_folder)

    create_meta_files(target_folder)
    img = generate_image(64, 64)
    img.save(os.path.join(target_folder, 'pack.png'))
    result_label.config(text="提取完成!")


def choose_source_folder():
    folder_path = filedialog.askdirectory()
    source_folder_entry.delete(0, tk.END)
    source_folder_entry.insert(0, folder_path)


# 创建图形界面
root = tk.Tk()
root.title("提取assets文件夹")
root.geometry("400x200")

source_folder_label = tk.Label(root, text="选择源文件夹:")
source_folder_label.grid(row=0, column=0, padx=10, pady=10)

source_folder_entry = tk.Entry(root)
source_folder_entry.grid(row=0, column=1)

source_folder_button = tk.Button(root, text="选择文件夹", command=choose_source_folder)
source_folder_button.grid(row=0, column=2)

run_button = tk.Button(root, text="开始提取", command=extract_assets)
run_button.grid(row=2, column=1, pady=20)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=1)

root.mainloop()
