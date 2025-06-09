import time
import board
import busio
import adafruit_drv2605
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
flex0 = AnalogIn(ads, ADS.P0)
flex1 = AnalogIn(ads, ADS.P1)

def select_mux_channel(chan_num):
    while not i2c.try_lock():
        pass
    i2c.writeto(0x70, bytes([1 << chan_num])) 
    i2c.unlock()
    time.sleep(0.01)

def buzz_motor(channel):
    select_mux_channel(channel)
    drv = adafruit_drv2605.DRV2605(i2c)
    drv.sequence[0] = adafruit_drv2605.Effect(118)
    drv.play()
    time.sleep(0.2)
    drv.stop()

buzzing0 = False
buzzing1 = False

while True:

    if flex0.value > 4700 and not buzzing0:
        buzz_motor(0)
        buzzing0 = True
        print("Motor 0 ON")
    elif flex0.value < 4400 and buzzing0:
        buzzing0 = False
        print("Motor 0 OFF")

    if flex1.value > 4700 and not buzzing1:
        buzz_motor(1)
        buzzing1 = True
        print("Motor 1 ON")
    elif flex1.value < 4400 and buzzing1:
        buzzing1 = False
        print("Motor 1 OFF")

    time.sleep(0.1)
