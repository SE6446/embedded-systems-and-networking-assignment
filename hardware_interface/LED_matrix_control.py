
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

def update_matrix(matrix: list[list[int]]) -> None:
    """Update the LED matrix. 
    
    Parameter: matrix
    
    A 3x3 matrix.
    
    [[0,0,0],
    [0,0,0],
    [0,0,0]]
    """
    #Continuously refresh the matrix display.
    for i in range(3):
        clear_all_rows()  # Turn off the current row
        
        for j in range(3):
            state: int = matrix[i][j]
            red_pin: Pin = col_pins[j*2]      # Red pin
            green_pin: Pin = col_pins[j*2+1]  # Green pin

            
            if state == 0:  # OFF
                red_pin.high()
                green_pin.high()
        
            elif state == 1:  # RED
                red_pin.low()
                green_pin.high()
        
            elif state == 2:  # GREEN
                red_pin.high()
                green_pin.low()
        
            elif state == 3:  # AMBER (both on)
                red_pin.low()
                green_pin.low()
        
            else:
                clear_matrix()
                raise Exception(f"Invalid state. Expected a value between 0 and 3 inclusive. Got: {state}")

        # Turn on this row briefly
        row_pins[i].high()
        sleep(2)

if __name__ == "__main__":
    try:
        # Define one or more frames
        frame1 = [
            [2, 2, 2],
            [2, 2, 2],
            [2, 2, 2]
        ]

        frame2 = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]

        frame3 = [
            [3, 3, 3],
            [3, 3, 3],
            [3, 3, 3]
        ]
        frame4 = [
            [1, 0, 1],
            [0, 2, 0],
            [1, 0, 1]
        ]


        while True:
            # refreshes each frame for a short time
            for _ in range(400):  
                update_matrix(frame1)

            for _ in range(400):
                update_matrix(frame2)

            for _ in range(400):
                update_matrix(frame3)

            for _ in range(400):
                update_matrix(frame4)
            
            
            while True:
                update_matrix(frame1)



    except KeyboardInterrupt:
        clear_matrix()
