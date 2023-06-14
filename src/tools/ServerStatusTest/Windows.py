import asyncio
import socket
import codecs
import time
import json
import tkinter as tk
from tkinter import ttk
import statistics

class MinecraftServerStatusTest:
    def __init__(self, hostname, port, timeout=0.6, use_hostname=False):
        self.hostname = hostname
        self.timeout = timeout
        self.port = port
        self.use_hostname = use_hostname

    async def get_server_info(self):
        try:
            ip = self.hostname if self.use_hostname else \
                (await asyncio.get_event_loop().getaddrinfo(self.hostname, self.port, proto=socket.IPPROTO_TCP))[0][4][
                    0]
            reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, self.port), timeout=self.timeout)
            start_time = time.time()
            writer.write(bytearray([0xFE, 0x01]))
            data_raw = await asyncio.wait_for(reader.read(1024), timeout=self.timeout)
            writer.close()

            server_info = codecs.utf_16_be_decode(data_raw[1:])[0].split('\x00')
            info = {'version': server_info[2], 'motd': server_info[3], 'online_players': server_info[4],
                    'max_players': server_info[5]}

            end_time = time.time()
            delay = int((end_time - start_time) * 1000)
            return True, self.port, delay, info

        except asyncio.TimeoutError:
            return False, self.port, 'Connection timed out'
        except Exception as err:
            return False, self.port, f'Error: {err}'


async def get_ports_info(hostname, ports):
    tasks = [asyncio.create_task(MinecraftServerStatusTest(hostname, port).get_server_info()) for port in ports for _ in range(5)]
    results = await asyncio.gather(*tasks)
    output = {}
    for result in results:
        port = result[1]
        if result[0]:
            output.setdefault(port, []).append(result)
    for port in ports:
        if not output.get(port):
            print(f"{hostname}:{port}----ALL REQUEST FAILED")
    return output


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


async def warmup_connection(hostname, port):
    try:
        ip = (await asyncio.get_event_loop().getaddrinfo(hostname, port, proto=socket.IPPROTO_TCP))[0][4][0]
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=0.1)
        writer.close()
    except:
        pass


def start_scan():
    hostname = ip_entry.get()
    start_port = int(start_port_entry.get())
    try:
        stop_port = int(end_port_entry.get())
    except ValueError:
        stop_port = start_port
    ports = range(start_port, stop_port + 1)
    asyncio.run(print_ports_info(hostname, ports))


root = tk.Tk()
root.title("Minecraft Server Status Scanner")
root.geometry("600x400")
for i in range(4):
    root.grid_rowconfigure(i, weight=1)
root.grid_rowconfigure(4, weight=99)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=10)

ip_label = tk.Label(root, text="IP:")
ip_label.grid(row=0, column=0)

ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, sticky="ew")
ip_entry.insert(0, "ipv4.rinkore.com")

start_port_label = tk.Label(root, text="Start Port（必填）:")
start_port_label.grid(row=1, column=0)

start_port_entry = tk.Entry(root)
start_port_entry.grid(row=1, column=1, sticky="ew")

end_port_label = tk.Label(root, text="End Port（可空）:")
end_port_label.grid(row=2, column=0)

end_port_entry = tk.Entry(root)
end_port_entry.grid(row=2, column=1, sticky="ew")

scan_button = tk.Button(root, text="Start Scan", command=start_scan)
scan_button.grid(row=3, column=0, columnspan=2, sticky="ew")

# 创建Treeview
tree = ttk.Treeview(root, columns=("port", "delay", "online_players", "max_players", "version", "motd"), show="headings")
tree.grid(row=4, column=0, columnspan=2, sticky="nsew")

# 设置列标题
tree.heading("port", text="Port")
tree.heading("delay", text="Delay")
tree.heading("version", text="version")
tree.heading("motd", text="motd")
tree.heading("online_players", text="online_players")
tree.heading("max_players", text="max_players")


def on_resize(event):
    tree.column("#0", width=0)  # 隐藏列 ID
    tree.column("port", width=int(event.width * 0.1))
    tree.column("delay", width=int(event.width * 0.12))
    tree.column("online_players", width=int(event.width * 0.15))
    tree.column("max_players", width=int(event.width * 0.14))
    tree.column("version", width=int(event.width * 0.1))


tree.bind("<Configure>", on_resize)

root.mainloop()

