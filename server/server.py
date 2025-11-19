from socket import *


from network import WLAN
from utime import sleep

import network 

def connect(ssid, password) -> WLAN:
    wlan: WLAN = WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting a connection...")
        sleep(1)
    config: tuple[str, str, str, str] = wlan.ifconfig()
    print(f"Connected to {config[2]} with IP: {config[0]}, Subnet mask: {config[1]} and DNS of: {config[3]}")
    return wlan


def open_socket(wlan:network.WLAN, port:int = 80) -> socket:
    ip: str = wlan.ifconfig()[0]
    address: tuple[str, int] = (ip, port)
    connection: socket = socket()
    connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #reuse address
    connection.bind(address)
    connection.listen(1)
    print(f'Listening on port: {port}')
    print(connection)
    return connection

def load_template(player_name, wins, losses)-> str:
    #TODO return the HTML tags to help construct the leaderboard itself.
    return f"""
    <tr>
        <td>{player_name}</td>
        <td>{wins}</td>
        <td>{losses}</td>
    </tr>
    """  

def create_webpage() -> str:
    raise NotImplementedError()
    return ""


def serve(connection:socket):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        client.send(create_webpage())
        client.close()


if __name__ == "__main__":
    ssid = ""
    password = ""

    wlan: WLAN = connect(ssid, password)
    connection = open_socket(wlan)
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        client.send("Hi!")
        client.close()
