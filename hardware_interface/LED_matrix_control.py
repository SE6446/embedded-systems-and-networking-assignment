from machine import Pin  
from utime import sleep_ms as sleep  # pyright: ignore[reportUnknownVariableType]

row_pins: list[Pin] = [
    Pin(0,Pin.OUT), # Row 1
    Pin(1,Pin.OUT), # Row 2
    Pin(2,Pin.OUT), # Row 3 
]

col_pins: list[Pin] = [
    Pin(3, Pin.OUT),  # Col 1 Red
    Pin(4, Pin.OUT),  # Col 1 Green
    Pin(5, Pin.OUT),  # Col 2 Red
    Pin(6, Pin.OUT),  # Col 2 Green
    Pin(7, Pin.OUT),  # Col 3 Red
    Pin(8, Pin.OUT)  # Col 3 Green
]


def clear_all_rows() -> None:
    """Clear all the rows to prevent LED ghosting"""
    for row in row_pins:
        row.low()

def clear_all_columns() -> None:
    for column in col_pins:
        column.high()
    
def clear_matrix() -> None:
    clear_all_rows()
    clear_all_columns()

def update_matrix(matrix:list[list[int]]) -> None:
    """Update the matrix with the image from the input
    
    0 is off

    1 is red

    2 is green

    3 is amber (red and green)

    example:

    [[1,2,1], # red, green, red

    [0,3,0], # off, amber, off

    [1,2,1]] # red, green, red
    
    """
    clear_matrix()
    # matrix validation
    if len(matrix) != 3 or len(matrix[0]) != 3:
        raise Exception(f"Parameter error: matrix shape is out of bounds. Number of rows: {len(matrix)}.\nNumber of columns: {len(matrix[0])}.\nExpected 3x3.")

    for i in range(3):
        activated = False
        for j in range(3):
            
            state: int = matrix[i][j]
            red_pin: Pin = col_pins[j*2+1]
            green_pin: Pin = col_pins[j*2]
            """Pins are common anode, so setting to low turns on the LED"""

            #The five possible states
            #OFF
            if state == 0:
                red_pin.high()
                green_pin.high()
                
            #RED
            elif state==1:
                red_pin.low()
                green_pin.high()
                activated = True
            #GREEN
            elif state == 2:
                red_pin.high()
                green_pin.low()
                activated = True
            #AMBER
            elif state == 3:
                red_pin.low()
                green_pin.low()
                activated = True
            #FUCK
            else:
                clear_matrix()
                raise Exception(f"Invalid state: Expected a value between 0 and 3. Got {state}")
        # 
        if activated:
            #We set this to high so that the ground pins activate and we get current
            row_pins[i].high()

        #We wait a moment otherwise the world will explode! ...Or the LEDs will flicker.
        sleep(2)

if __name__ == "__main__":
    try:
        while True:
            update_matrix([
                [1,2,1],
                [0,3,0],
                [1,2,1]])
            sleep(3000)
            update_matrix([
                [1,0,1],
                [2,3,2],
                [1,0,1]])
            sleep(3000)
    except KeyboardInterrupt:
        clear_matrix()


    



