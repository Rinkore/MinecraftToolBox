import asyncio
import socket
import codecs
import time
import json
import tkinter as tk
from tkinter import ttk
import statistics

APPName = "Minecraft服务器状态查询"
version = "1.3.0"
author = "Rinkore"
# Pyinstaller -F -w -n=服务器状态查询 .\src\tools\ServerStatusTest\Windows.py

# Minecraft服务器状态测试类
class MinecraftServerStatusTest:
    def __init__(self, hostname, port, timeout=0.6, use_hostname=False):
        self.hostname = hostname
        self.timeout = timeout
        self.port = port
        self.use_hostname = use_hostname

    # 获取服务器信息
    async def get_server_info(self):
        try:
            # 获取IP地址
            ip = self.hostname if self.use_hostname else \
                (await asyncio.get_event_loop().getaddrinfo(self.hostname, self.port, proto=socket.IPPROTO_TCP))[0][4][
                    0]

            # 建立连接并发送请求
            reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, self.port), timeout=self.timeout)
            writer.write(bytearray([0xFE, 0x01]))

            # 读取服务器返回的数据
            start_time = time.time_ns()
            data_raw = await asyncio.wait_for(reader.read(1024), timeout=self.timeout)
            end_time = time.time_ns()
            writer.close()

            # 解码服务器返回的数据
            server_info = codecs.utf_16_be_decode(data_raw[1:])[0].split('\x00')
            info = {'version': server_info[2], 'motd': server_info[3], 'online_players': server_info[4],
                    'max_players': server_info[5]}

            delay = int((end_time - start_time) / 1000000)
            return True, self.port, delay, info

        except asyncio.TimeoutError:
            return False, self.port, 'Connection timed out'
        except Exception as err:
            return False, self.port, f'Error: {err}'


# 获取端口信息
async def get_ports_info(hostname, ports):
    tasks = [asyncio.create_task(MinecraftServerStatusTest(hostname, port).get_server_info()) for port in ports for _ in
             range(5)]
    results = await asyncio.gather(*tasks)
    output = {}
    for result in results:
        port = result[1]
        if result[0]:
            output.setdefault(port, []).append(result)
    for port in ports:
        if not output.get(port):
            # print(f"{hostname}:{port}----ALL REQUEST FAILED")
            pass
    return output


# 打印端口信息
async def print_ports_info(hostname, ports):
    await warmup_connection(hostname, ports[0])  # 预热第一个端口的连接
    ports_info = await get_ports_info(hostname, ports)
    for port, port_results in ports_info.items():
        avg_delay = statistics.mean(result[2] for result in port_results)

        # 将数据添加到表格中
        tree.insert("", "end", values=(port, f"{avg_delay:.2f}ms"
                                       , json.loads(json.dumps(port_results[0][3]["online_players"]))
                                       , json.loads(json.dumps(port_results[0][3]["max_players"]))
                                       , json.loads(json.dumps(port_results[0][3]["version"]))
                                       , json.loads(json.dumps(port_results[0][3]["motd"]))
                                       )
                    )


# 预热连接
async def warmup_connection(hostname, port):
    try:
        ip = (await asyncio.get_event_loop().getaddrinfo(hostname, port, proto=socket.IPPROTO_TCP))[0][4][0]
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=0.1)
        writer.close()
    except:
        pass


# 开始扫描
def start_scan():
    hostname = ip_entry.get()
    start_port = int(start_port_entry.get())
    try:
        stop_port = int(end_port_entry.get())
    except ValueError:
        stop_port = start_port
    ports = range(start_port, stop_port + 1)
    asyncio.run(print_ports_info(hostname, ports))


# 清空Treeview中的内容
def clear_tree():
    tree.delete(*tree.get_children())


# 创建更新日志窗口
def show_update_log():
    update_log_window = tk.Toplevel(root)
    update_log_window.title("更新日志")

    # 在更新日志窗口中显示更新日志内容
    update_log_label = tk.Label(update_log_window, text="广告：多种面版服出租请找Rinkore\n"
                                                        "QQ：2213340209    帮开好服,满意再付款\n"
                                                        "v1.3.1: 中文化了界面元素，微调UI"
                                                        "v1.3.0：新增更新日志和清空查询结果功能\n"
                                                        "v1.2.1：新增了默认查询端口25565"
                                                        "v1.2.0：修复了第一次连接主机造成的延迟虚高的问题\n"
                                                        "v1.1.1：异步多次查询取平均延迟\n"
                                                        "v1.1.0：支持异步同时查询多个服务器\n"
                                                        "v1.0.0：初步支持Minecraft服务器状态（Ping）查询"
                                , justify=tk.LEFT)
    update_log_label.pack()


# 创建GUI窗口
root = tk.Tk()
root.title(f"{APPName} v{version} Powered by {author}")
root.geometry("600x400")
row_tot = 4
column_tot = 4
for i in range(row_tot):
    root.grid_rowconfigure(i, weight=1)
root.grid_rowconfigure(row_tot, weight=99)
for i in range(column_tot):
    root.grid_columnconfigure(i, weight=1)
root.grid_columnconfigure(column_tot, weight=99)

# IP地址标签和输入框
ip_label = tk.Label(root, text="服务器主机地址:")
ip_label.grid(row=0, column=0)

ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, columnspan=column_tot, sticky="ew")
ip_entry.insert(0, "ipv4.rinkore.com")

# 起始端口标签和输入框
start_port_label = tk.Label(root, text="起始端口（必填）:")
start_port_label.grid(row=1, column=0)

start_port_entry = tk.Entry(root)
start_port_entry.grid(row=1, column=1, columnspan=column_tot, sticky="ew")
start_port_entry.insert(0, "25565")

# 终止端口标签和输入框
end_port_label = tk.Label(root, text="结束端口（可空）:")
end_port_label.grid(row=2, column=0)

end_port_entry = tk.Entry(root)
end_port_entry.grid(row=2, column=1, columnspan=column_tot, sticky="ew")

# 创建Clear按钮
clear_button = tk.Button(root, text="清空记录", command=clear_tree)
clear_button.grid(row=3, column=0, sticky="nse")

# 创建Update Log按钮
update_log_button = tk.Button(root, text="更新日志", command=show_update_log)
update_log_button.grid(row=3, column=0, sticky="nsw")

# 开始扫描按钮
scan_button = tk.Button(root, text="开始查询", command=start_scan)
scan_button.grid(row=3, column=1, columnspan=column_tot, sticky="nsew")

# 创建Treeview
tree = ttk.Treeview(root, columns=("port", "delay", "online_players", "max_players", "version", "motd"),
                    show="headings")
tree.grid(row=4, column=0, columnspan=column_tot+1, sticky="nsew")

# 设置列标题
tree.heading("port", text="端口")
tree.heading("delay", text="延迟")
tree.heading("online_players", text="在线玩家数")
tree.heading("max_players", text="最大玩家数")
tree.heading("version", text="游戏版本")
tree.heading("motd", text="服务器今日讯息")


# 调整列宽度
def on_resize(event):
    tree.column("#0", width=0)  # 隐藏列 ID
    tree.column("port", width=int(event.width * 0.1))
    tree.column("delay", width=int(event.width * 0.12))
    tree.column("online_players", width=int(event.width * 0.15))
    tree.column("max_players", width=int(event.width * 0.14))
    tree.column("version", width=int(event.width * 0.1))


tree.bind("<Configure>", on_resize)

root.mainloop()
