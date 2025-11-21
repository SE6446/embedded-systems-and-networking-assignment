from machine import Pin
from time import sleep

# Define the keys on a 3x4 keypad
keys = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']
]

# Sets rows and column pins
row_pins = [Pin(26, Pin.OUT), Pin(22, Pin.OUT), Pin(21, Pin.OUT), Pin(20, Pin.OUT)]
col_pins = [Pin(19, Pin.IN, Pin.PULL_DOWN), Pin(18, Pin.IN, Pin.PULL_DOWN), Pin(17, Pin.IN, Pin.PULL_DOWN)]

def scan_keypad():
    """Return the key pressed, or None"""
    for row_idx, row_pin in enumerate(row_pins):
        # Set the current row HIGH
        row_pin.value(1)

        # Read each column
        for col_idx, col_pin in enumerate(col_pins):
            if col_pin.value() == 1:
                row_pin.value(0)
                return keys[row_idx][col_idx]

        # Set row back LOW
        row_pin.value(0)

    return None


def get_key_input() -> str:
    while True:
        key: str | None = scan_keypad()
        if key:
            return key
        sleep(0.2)

if __name__ == "__main__":
    while True:
        key = scan_keypad()
        if key:
            print("Key pressed:", key)
            sleep(0.3) 
