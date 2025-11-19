from socket import *


from network import WLAN
from utime import sleep

from game_engine.infoSaving import Entry, InfoSaving as infoManager
from game_engine.infoSaving import Entry

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

def load_template(entry:Entry)-> str:
    #TODO return the HTML tags to help construct the leaderboard itself.
    return f"""
    <tr>
        <td>{entry.name}</td>
        <td>{entry.wins}</td>
        <td>{entry.losses}</td>
    </tr>
    """  

def create_webpage(textFile:str) -> str:
    fileManager = infoManager(textFile)
    entry_list: list[Entry] = fileManager.readFile()
    del fileManager
    with open("main.html","r") as file:
        html:str = file.read()
        leaderboard = ""
        for entry in entry_list:
            leaderboard: str = leaderboard + load_template(entry) + "\n"
        return html.format(leaderboard=leaderboard)


def serve(connection:socket):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        client.send(create_webpage("db.txt"))
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
