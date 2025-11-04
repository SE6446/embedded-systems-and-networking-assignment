import _thread
import time


def game():
    pass


def server():
    pass


_ = _thread.start_new_thread(game, ())
_ = _thread.start_new_thread(server, ())

while True:
    time.sleep(1)
