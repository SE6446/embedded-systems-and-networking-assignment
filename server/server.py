from socket import socket


from socket import *


from network import WLAN


import network 
#import socket

from time import sleep  # pyright: ignore[reportUnknownVariableType]

def connect(ssid:str|None = None, password:str|None = None) -> network.WLAN:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid,password)
    while wlan.isconnected() == False:
        print("Waiting connection")
        sleep(1)
    ifconfig: tuple[str,str,str,str] = wlan.ifconfig()
    print(f"Connected! ifconfig: IP:{ifconfig[0]}, Subnet mask {ifconfig[1]}, Gateway: {ifconfig[2]}, DNS: {ifconfig[3]}")
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
    #TODO How this works is that it takes the templates and contstructs the leaderboard and rest of the website
    #See: https://stackoverflow.com/questions/44757222/transform-string-to-f-string
    return ""  # pyright: ignore[reportUnreachable]

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

