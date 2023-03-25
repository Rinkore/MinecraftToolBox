import json
import os
import shutil
import tkinter as tk
import zipfile
from tkinter import filedialog
import semver

minecraft_version = "none"
fabric_version = "none"
java_version = "none"
version = ""
lastest = "logs/lastest.log"


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
    init_log("logs/minecraft.log")
    init_log("logs/java.log")
    init_log("logs/fabric.log")

    # 遍历mods文件夹中的所有.jar文件
    global minecraft_version, fabric_version, java_version
    for file_name in os.listdir(mods_folder):
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

            # 输出版本信息到日志文件
            try:
                minecraft_version = mod_data["depends"]["minecraft"]
                write_to_log(minecraft_version, "logs/minecraft.log")
            except KeyError:
                print("fabric.mod.json file does not contain minecraft_version")
            try:
                fabric_version = mod_data["depends"]["fabricloader"]
                write_to_log(fabric_version, "logs/fabric.log")
            except KeyError:
                print("fabric.mod.json file does not contain fabric_version")
            try:
                java_version = mod_data["depends"]["java"]
                write_to_log(java_version, "logs/java.log")
            except KeyError:
                print("fabric.mod.json file does not contain java_version")

            print(f"Minecraft {minecraft_version}\nFabricLoader {fabric_version}\nJava {java_version}")


def write_to_log(log_version, log_file):
    with open(log_file, "a") as f:
        f.write(f"{log_version}\n")


def init_log(log_file):
    if os.path.exists(log_file):
        os.remove(log_file)


def get_minecraft_or_fabric_version(input_version):
    global version, lastest
    with open(input_version + '.log', 'r') as f:
        lines = f.readlines()

    # 初始化版本号区间为最小和最大版本
    min_version = "0.0.0"
    max_version = "999999999.999999999.999999999"

    # 循环读取每个版本号区间，更新最小和最大版本
    for line in lines:
        version_range = line.strip()
        if version_range == '*':
            continue
        if version_range.startswith("~"):
            # 如果版本区间以 ~ 开头，则表示是最新的修订版，只需要更新最小版本号
            min_version = version_range[1:]
        elif version_range.startswith(">="):
            # 如果版本区间以 >= 开头，则更新最小版本号
            try:
                version = semver.parse_version_info(str(version_range[2:]))
                if not semver.match(min_version, version_range):
                    min_version = str(version)
            except ValueError:
                write_to_log(("不规范的版本号", line), lastest)
            except TypeError:
                write_to_log(("不规范的版本类型", line), lastest)

        elif version_range.startswith("<"):
            # 如果版本区间以 < 开头，则更新最大版本号
            version = semver.parse_version_info(version_range[1:])
            if not semver.match(max_version, version_range):
                max_version = str(version)
        else:
            try:
                # 如果版本区间既不是以 ~ 开头，也不是以 >= 或 < 开头，则表示是精确版本号
                version = semver.parse_version_info(version_range)
                min_version = max_version = str(version)
            except ValueError:
                write_to_log(("不规范的版本号" + line), lastest)
        write_to_log("Yes" + str(version), lastest)
    # 最终返回符合所有版本区间的最新的正式版本号
    print(input_version[5:] + "_version", str(min_version))


def get_java_version():
    max_version = 0
    with open('logs/java.log', 'r') as f:
        lines = f.readlines()
    for line in lines:
        version_range = line.strip()
        if version_range.startswith(">="):
            max_version = max(max_version, int(version_range[2:]))
    print("java_version", str(max_version))


# 调用函数
folder_select()
init_log(lastest)
get_minecraft_or_fabric_version("logs/minecraft")
get_minecraft_or_fabric_version("logs/fabric")
get_java_version()
