import _thread
import time


def game():
    pass


def server():
    pass


_ = _thread.start_new_thread(game, ())  # pyright: ignore[reportUnknownMemberType, reportAny]
_ = _thread.start_new_thread(server, ())  # pyright: ignore[reportUnknownMemberType, reportAny]

while True:
    time.sleep(1)  # pyright: ignore[reportUnknownMemberType]
