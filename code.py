"""Circuit Python Space Mushroom driver
   
   Original Arduino version by Shiura
   https://github.com/sh1ura/Space-Mushroom

   2022 - chris@headstrong.solutions
"""

# pyright: reportShadowedImports=false

import usb_hid
import board
from time import time
import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn
from adafruit_circuitplayground.express import cpx
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Create a software mouse and keyboard
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)

# Set some application defaults
WAKING_DELAY = 0.3
DELAY = 15
DEAD_THRESHOLD = 0
SPEED_PARAMETER = 400
DOF = 6

# translations
TX = 0
TY = 1
TZ = 2

# rotations
RX = 3
RY = 4
RZ = 5

# board.SCL and board.SDA on I2C0
# no numbered pin definition is required as long 
# as I2C devices are on I2C0 pins
i2c = board.I2C()  
pcf1 = PCF.PCF8591(i2c, address=0x048, reference_voltage=3.3)
pcf2 = PCF.PCF8591(i2c, address=0x049, reference_voltage=3.3)

STICK1_VRX_PIN = AnalogIn(pcf1, PCF.A0)
STICK1_VRY_PIN = AnalogIn(pcf1, PCF.A1)
# currently unused
# STICK1_SWI_PIN = AnalogIn(board.D3)

STICK2_VRX_PIN = AnalogIn(pcf1, PCF.A2)
STICK2_VRY_PIN = AnalogIn(pcf1, PCF.A3)
# currently unused
# STICK2_SWI_PIN = AnalogIn(board.D6)

STICK3_VRX_PIN = AnalogIn(pcf2, PCF.A0)
STICK3_VRY_PIN = AnalogIn(pcf2, PCF.A1)
# currently unused
# STICK3_SWI_PIN = AnalogIn(board.D9)

ANALOGUE_PINS = [STICK1_VRX_PIN, STICK2_VRX_PIN, STICK3_VRX_PIN, 
        STICK1_VRY_PIN, STICK2_VRY_PIN, STICK3_VRY_PIN]  

COEFF = {
    {0, 0, 0, -10, -10, 20}, # TX
    {0, 0, 0, -17, 17, 0},   # TY
    {-3, -3, -3, 0, 0, 0},   # TZ
    {-6, 6, 0, 0, 0, 0},     # RY
    {3, 3, -6, 0, 0, 0},     # RX
    {0, 0, 0, 3, 3, 3},      # RZ
}

origin = []

sx = 0
sy = 0
sw = 0

def setup():
    time.sleep(WAKING_DELAY)
    for pin_index in range(len(ANALOGUE_PINS)-1):
        origin[pin_index] = ANALOGUE_PINS[pin_index].value

def move(x: int, y: int, w: int):
    global sx 
    global sy
    global sw

    if x > DEAD_THRESHOLD:
        x -= DEAD_THRESHOLD
    elif x < -DEAD_THRESHOLD:
        x += DEAD_THRESHOLD
    else:
        x = 0
    
    if y > DEAD_THRESHOLD:
        y -= DEAD_THRESHOLD
    elif y < -DEAD_THRESHOLD:
        y += DEAD_THRESHOLD
    else:
        y = 0
    
    if w > DEAD_THRESHOLD:
        w -= DEAD_THRESHOLD
    elif w < -DEAD_THRESHOLD:
        w += DEAD_THRESHOLD
    else:
        w = 0
    
    mouse.move(x, y, w)

    sx += x
    sy += y
    sw += w

def reset_move():
    mouse.move(-sx, -sy, -sw)
    sx = 0
    sy = 0
    sw = 0

def main():
    setup()
    while True:
        sv = []
        mv = []
        move_flag = False

        for pin_index in range(len(ANALOGUE_PINS)-1):
            origin[pin_index] = ANALOGUE_PINS[pin_index].value
        
        for pin_index_coeff in range(len(ANALOGUE_PINS)-1):
            mv[pin_index] = 0
            for pin_index_coeff in range(len(ANALOGUE_PINS)-1):
                mv[pin_index_coeff] += COEFF[pin_index][pin_index_coeff] * sv[pin_index_coeff]
            mv[pin_index] /= SPEED_PARAMETER
            if mv[pin_index] > 127:
                mv[pin_index] = 127
            elif mv[pin_index] < -128:
                mv[pin_index] = -128
        
        if abs(mv[RX]) > DEAD_THRESHOLD or abs(mv[RY]) > DEAD_THRESHOLD:
            Mouse.press(Mouse.MIDDLE_BUTTON)
            move(mv[RX], mv[RY], 0)
            Mouse.release(Mouse.MIDDLE_BUTTON)
        
        if abs(mv[TX]) > DEAD_THRESHOLD or abs(mv[TY]) > DEAD_THRESHOLD:
            Keyboard.press(Keycode.LEFT_SHIFT)
            Mouse.press(Mouse.MIDDLE_BUTTON)
            move(mv[TX], mv[TY], 0)
            Keyboard.release_all()
            Mouse.release(Mouse.MIDDLE_BUTTON)
        
        if abs(mv[TZ]) > DEAD_THRESHOLD or abs(mv[TZ]) > DEAD_THRESHOLD:
            Keyboard.press(Keycode.LEFT_CONTROL)
            Mouse.press(Mouse.MIDDLE_BUTTON)
            move(0, mv[TZ], 0)
            Keyboard.release_all()
            Mouse.release(Mouse.MIDDLE_BUTTON)
        
        reset_move()

        time.sleep(DELAY)

if __name__ == "__main__":
    main()