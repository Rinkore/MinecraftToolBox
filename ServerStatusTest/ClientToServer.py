import json
import os
import shutil
import tkinter as tk
import zipfile
from tkinter import filedialog

minecraft_version = "none"
fabric_version = "none"
java_version = "none"


def folder_select():
    # 弹出对话框让用户选择文件夹
    root = tk.Tk()
    root.withdraw()
    src_folder = filedialog.askdirectory(title="请选择Minecraft客户端文件夹")

    # 定义server文件夹路径
    dst_folder = os.path.join(os.path.dirname(src_folder), "server")

    # 如果server文件夹已经存在，则先删除它
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)

    os.makedirs(dst_folder)

    # 复制mods、config、scripts、kubejs和defaultconfigs文件夹到server文件夹中
    folder_list = ["mods", "config", "scripts", "kubejs", "defaultconfigs"]
    for folder_name in folder_list:
        src = os.path.join(src_folder, folder_name)
        dst = os.path.join(dst_folder, folder_name)
        shutil.copytree(src, dst)

    # 执行read_mod_versions函数，读取mod的版本信息

    mods_folder = os.path.join(dst_folder, "mods")
    read_mod_versions(mods_folder)


def read_mod_versions(mods_folder):
    # 遍历mods文件夹中的所有.jar文件
    global minecraft_version, fabric_version, java_version
    for file_name in os.listdir(mods_folder):
        print()
        print(file_name)
        if file_name.endswith(".jar"):
            file_path = os.path.join(mods_folder, file_name)

            # 使用zipfile模块读取fabric.mod.json文件
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                try:
                    json_data = zip_ref.read('fabric.mod.json')
                except KeyError:
                    print(f"{file_name} does not contain a fabric.mod.json file")
                    continue

            # 解析json数据
            try:
                mod_data = json.loads(json_data)
            except json.decoder.JSONDecodeError:
                print(f"{file_name} can not be decoded")
                continue

            # 读取depends下的版本信息
            try:
                minecraft_version = mod_data["depends"]["minecraft"]
            except KeyError:
                print(f"fabric.mod.json file does not contain minecraft_version")
            try:
                fabric_version = mod_data["depends"]["fabricloader"]
            except KeyError:
                print(f"fabric.mod.json file does not contain fabric_version")
            try:
                java_version = mod_data["depends"]["java"]
            except KeyError:
                print(f"fabric.mod.json file does not contain java_version")

            print(f"Minecraft {minecraft_version}\nFabricLoader {fabric_version}\nJava {java_version}")


# 调用函数
folder_select()
