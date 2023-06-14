import os
from kivy.resources import resource_add_path, resource_find
from kivy.core.text import LabelBase
from kivy.app import App
from kivy.uix.treeview import TreeView, TreeViewLabel
import asyncio
import time
import socket
import codecs
import json

resource_add_path(os.path.abspath('./data/fonts'))
LabelBase.register('Roboto', 'data/fonts/1611458310630572.ttf')


class MinecraftServerStatusTest:
    def __init__(self, hostname, port, timeout=0.6, use_hostname=False):
        self.hostname = hostname
        self.timeout = timeout
        self.port = port
        self.use_hostname = use_hostname

    async def get_server_info(self):
        try:
            start_time = time.time()
            ip = self.hostname if self.use_hostname else \
                (await asyncio.get_event_loop().getaddrinfo(self.hostname, self.port, proto=socket.IPPROTO_TCP))[0][4][
                    0]
            reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, self.port), timeout=self.timeout)
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
    tasks = [MinecraftServerStatusTest(hostname, port).get_server_info() for port in ports for _ in range(5)]
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


async def print_ports_info(hostname, ports):
    ports_info = await get_ports_info(hostname, ports)
    output = {}
    for port, port_results in ports_info.items():
        delay_sum = sum(result[2] for result in port_results)
        avg_delay = delay_sum / len(port_results)
        value=(f"{avg_delay:.2f}ms"
                                       , json.loads(json.dumps(port_results[0][3]["online_players"]))
                                       , json.loads(json.dumps(port_results[0][3]["max_players"]))
                                       , json.loads(json.dumps(port_results[0][3]["version"]))
                                       , json.dumps(port_results[0][3]["motd"])
                                       )
        output.setdefault(port, []).append(value)
    return output

        # 将数据添加到表格中


def start_scan(hostname, start_port, stop_port=None):
    if hostname is None:
        hostname = "ipv4.rinkore.com"
    if stop_port is None:
        stop_port = start_port
    ports = range(start_port, stop_port + 1)
    output = asyncio.run(print_ports_info(hostname, ports))
    return output

# if __name__ == '__main__':

class TestApp(App):

    def build(self):
        tv = TreeView(hide_root=True)
        add = tv.add_node
        root = add(TreeViewLabel(text='13900kf在线的服务器列表', is_open=True))
        root2 = add(TreeViewLabel(text='e5 2667v2在线的服务器列表', is_open=True))
        output = start_scan("ipv4.rinkore.com",13900,13999);
        output2 = start_scan("ipv4.rinkore.com",2100,2299);
        for key in output:
            value_list = output[key]
            port_node = add(TreeViewLabel(text='端口 %d' % key), root)
            for value_tuple in value_list:
                response_time, tps, max_players, version, name = value_tuple
                add(TreeViewLabel(text='延迟 %s' % response_time), port_node)
                add(TreeViewLabel(text='在线人数 %s' % tps), port_node)
                add(TreeViewLabel(text='最大人数 %s' % max_players), port_node)
                add(TreeViewLabel(text='版本 %s' % version), port_node)
                add(TreeViewLabel(text='描述 %s' % name), port_node)

        for key in output2:
            value_list = output2[key]
            port_node = add(TreeViewLabel(text='端口 %d' % key), root2)
            for value_tuple in value_list:
                response_time, tps, max_players, version, name = value_tuple
                add(TreeViewLabel(text='延迟 %s' % response_time), port_node)
                add(TreeViewLabel(text='在线人数 %s' % tps), port_node)
                add(TreeViewLabel(text='最大人数 %s' % max_players), port_node)
                add(TreeViewLabel(text='版本 %s' % version), port_node)
                add(TreeViewLabel(text='描述 %s' % name), port_node)
        return tv


TestApp().run()
