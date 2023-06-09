import json
import os
import shutil
import tkinter as tk
import urllib
import zipfile
import semver
import subprocess
import requests
from tqdm import tqdm
from tkinter import filedialog
import re

version = ""
minecraft_version = "none"
fabric_version = "none"
java_version = "none"
src_folder = ""
dst_folder = ""
minecraft_log = "logs/minecraft.log"
fabric_log = "logs/fabric.log"
java_log = "logs/java.log"
lastest_log = "logs/lastest.log"


def folder_select():
    global src_folder, dst_folder
    # 弹出对话框让用户选择文件夹
    root = tk.Tk()
    root.withdraw()
    src_folder = filedialog.askdirectory(title="请选择Minecraft客户端文件夹")

    # 定义server文件夹路径
    dst_folder = os.path.join(os.path.dirname(src_folder), "config-by-MTB")

    # 如果server文件夹已经存在，则先删除它
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)

    os.makedirs(dst_folder)

    # 复制mods、config、scripts、kubejs和defaultconfigs文件夹到server文件夹中
    folder_list = ["mods", "config", "scripts", "kubejs", "defaultconfigs"]
    for folder_name in folder_list:
        src = os.path.join(src_folder, folder_name)
        dst = os.path.join(dst_folder, folder_name)
        if os.path.exists(src):
            shutil.copytree(src, dst)

    # 执行read_mod_versions函数，读取mod的版本信息
    mods_folder = os.path.join(dst_folder, "mods")
    read_mod_versions(mods_folder)


def read_mod_versions(mods_folder):
    for file_name in os.listdir(mods_folder):
        if not file_name.endswith(".jar"):
            continue

        file_path = os.path.join(mods_folder, file_name)

        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                json_data = zip_ref.read('fabric.mod.json')
            mod_data = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            continue
        except (KeyError, zipfile.BadZipFile):
            continue
        if "depends" not in mod_data:
            continue
        parsed_minecraft_version = mod_data["depends"].get("minecraft")
        parsed_fabric_version = mod_data["depends"].get("fabricloader")
        parsed_java_version = mod_data["depends"].get("java")
        if parsed_minecraft_version:
            write_to_log(parsed_minecraft_version, minecraft_log)
        if parsed_fabric_version:
            write_to_log(parsed_fabric_version, fabric_log)
        if parsed_java_version:
            write_to_log(parsed_java_version, java_log)


def write_to_log(log_version, log_file):
    with open(log_file, "a") as f:
        f.write(f"{log_version}\n")


def init_logs(log_files):
    if os.path.exists("logs"):
        shutil.rmtree("logs")
    os.makedirs("logs")
    for log_file in log_files:
        log = open(log_file, "w")
        log.close()


def get_minecraft_or_fabric_version(input_version):
    with open(input_version, 'r') as f:
        lines = f.readlines()

    min_version, max_version = '', ''

    for line in lines:
        version_range = line.strip()
        if not re.match(r'^\d+\.\d+\.\d+$', version_range):
            continue

        try:
            version = semver.parse_version_info(version_range)
        except ValueError:
            continue

        if min_version:
            min_version = max(min_version, str(version))
        else:
            min_version = str(version)

        if max_version:
            max_version = min(max_version, str(version))
        else:
            max_version = str(version)

    if input_version == 'minecraft_log':
        return minecraft_version
    elif input_version == 'fabric_log':
        return fabric_version


def get_java_version():
    max_version = 0
    with open(java_log, 'r') as f:
        lines = f.readlines()
    for line in lines:
        version_range = line.strip()
        if version_range.startswith(">="):
            max_version = max(max_version, int(version_range[2:]))
    print("java_version", str(max_version))


def install_task(file_to_download):
    # 设置文件下载链接和保存路径
    if file_to_download == "fabric":
        url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.11.2/fabric-installer-0.11.2.jar"
        print("正在下载fabric-installer.jar")
        # 下载文件并显示进度条
        with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1) as t:
            urllib.request.urlretrieve(url, dst_folder + "\\fabric-installer.jar",
                                       reporthook=lambda b, bsize, tsize: t.update(bsize))
        print("fabric-installer.jar下载完成")
        print("安装fabric中")
        command = f'java -jar fabric-installer.jar config -mcversion {minecraft_version} -downloadMinecraft'
        # 使用subprocess运行命令
        install = subprocess.Popen(command, cwd=dst_folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding="GBK")
        for line in install.stdout:
            print(line.rstrip())
        start_server = open(dst_folder + "/StartServer.bat", "w")
        start_server.write("java -Xmx4G -jar -config fabric-config-launch.jar nogui")
        start_server.close()
    else:
        print("安装错误")


# 调用函数
init_logs([minecraft_log, java_log, fabric_log, lastest_log])
folder_select()
get_minecraft_or_fabric_version(minecraft_log)
get_minecraft_or_fabric_version(fabric_log)
get_java_version()
install_task("fabric")
