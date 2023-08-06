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
    target_folder = os.path.abspath(os.path.join(source_folder, "..", "langs-by-MTB"))

    create_folder(target_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith(".jar"):
                extract_from_jar(os.path.join(root, file), target_folder)

    create_meta_files(target_folder)
    img = generate_image(64, 64)
    img.save(os.path.join(target_folder, 'pack.png'))

    result_label.config(text="提取完成!\n"
                             "本地化文件提取到\n"
                             f"{target_folder}")

    # 在提取完成后打开目标文件夹
    os.startfile(target_folder)


def choose_source_folder():
    folder_path = filedialog.askdirectory()
    source_folder_entry.delete(0, tk.END)
    source_folder_entry.insert(0, folder_path)


# 创建图形界面
root = tk.Tk()
root.title("Minecraft本地化资源包提取器")

# 禁止调整窗口大小
root.minsize(width=350, height=300)
root.resizable(width=False, height=False)

# 使用Frame容器
main_frame = tk.Frame(root, padx=20, pady=10)
main_frame.grid(sticky="nsew")

# 在Frame上设置行列权重
main_frame.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)

# 放置元素

source_folder_label = tk.Label(main_frame, text="选择mods文件夹:")
source_folder_label.grid(row=0, column=0, pady=20, padx=10, sticky="w")

source_folder_entry = tk.Entry(main_frame)
source_folder_entry.grid(row=0, column=0, pady=20, padx=10, sticky="e")

source_folder_button = tk.Button(main_frame, text="选择文件夹", command=choose_source_folder)
source_folder_button.grid(row=1, column=0, pady=20, padx=10, sticky="w")

run_button = tk.Button(main_frame, text="开始提取", command=extract_assets)
run_button.grid(row=1, column=0, pady=20, padx=10, sticky="e")

result_label = tk.Label(main_frame, text="")
result_label.grid(row=2, column=0, padx=10, sticky="ew")

version_label = tk.Label(main_frame, text="Minecraft本地化资源包提取器 v1.1 Powered by Rinkore")
version_label.grid(row=3, column=0, padx=10, sticky="ew")

root.mainloop()
