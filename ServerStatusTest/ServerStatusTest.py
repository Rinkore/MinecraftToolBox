import asyncio
import socket
import codecs
import time
import json


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
            print(f"{hostname}:{port}----ALL REQUEST FAILED")

    return output


async def print_ports_info(hostname, ports):
    ports_info = await get_ports_info(hostname, ports)
    for port, port_results in ports_info.items():
        delay_sum = sum(result[2] for result in port_results)
        avg_delay = delay_sum / len(port_results)
        print(f"{hostname}:{port}----{avg_delay:.2f}ms delay, Info: {port_results[0][3]}")

with open('./Server/ServerList.json') as ServerListJson:
    data = json.load(ServerListJson)
    ServerList = data['hosts']
    for servers in ServerList:
        asyncio.run(print_ports_info(servers['ip'], servers['ports']))
