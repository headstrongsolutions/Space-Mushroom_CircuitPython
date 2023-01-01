# Space-Mushroom in Adafruit's Circuit Python

Python to support a 6 Degrees Of Freedom (6dof) 'mouse' puck used primarily to support 3D modelling to Rotate/Pan/Zoom.

## Original source repo and 3D print files

This repo is forked from sh1ra's github repo here: [https://github.com/sh1ura/Space-Mushroom](https://github.com/sh1ura/Space-Mushroom)
The 3D Printable models for which are here: [https://www.printables.com/model/353764-space-mushroom-full-6-dofs-space-mouse](https://www.printables.com/model/353764-space-mushroom-full-6-dofs-space-mouse)

They do a much better job of explaining using it with example videos etc, so to find out about that head over to their pages.

## Circuit Python

This fork is to change the original Arduino software implementation with a Circuit Python implementation as my personal MCU of choice is the Raspberry Pi Pico.
Unfortunately the current Micropython builds for Raspberry Pi Pico doesn't have Human Interface Device (HID) implementation yet, or that would be my perfect choice as I feel the toolchain for that is much more mature than Adafruit's Circuit Python.

## Setup

First you need to get the latest stable build of the Circuit Python firmware from: [https://circuitpython.org/board/raspberry_pi_pico/](https://circuitpython.org/board/raspberry_pi_pico/)

For me at time of writing it was top of the page on the right, version 7.3.3, click the purple `DOWNLOAD .UF2 NOW` button.
When that's downloaded unplug your Pico (if it's plugged in), hold the `BOOTSEL` button on it and plug it into your computer, keep holding the button for a couple of seconds after plugging it in and you should see a new usb media device connected to your computer.
Copy and paste the file that was downloaded from circuitpython.org to the pico usb media device and it will automatically reboot the pico when it's finished.

You should now see a different usb media device, on my machine it's `CIRCUITPY`, in that device open up the `code.py` in any text editor and replace the contents with the following:

```python
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
```

...and save the file.
As soon as you save the file it will automatically run it and the LED on the Pico will start flashing!

This is all you need to set up to deploy code changes to Circuit Python on the Pico, it really is as simple as that :)

## Analogue Pins

The Raspberry Pico only has 3 analogue pins, and the Space Mushroom needs 6, so to get around this I'll be using 2 PCF8591's to add 8 additional analogue input pins.

I could use just one PCF8591 and use the on board analogue pins, however the PCF8591 uses I2C to communicate the digital signals back to the Pico, so rather than have some of the inputs directly as analog reads and the others as digital it's simpler to manage if they are all of the same type.

There is a Adafruit Circuit Python library to manage PCF8591's (details [here](https://docs.circuitpython.org/projects/pcf8591/en/latest/).

There are jumpers on them to manage the I2C addresses each module uses, so multiples can be operated on the same I2C bus.
