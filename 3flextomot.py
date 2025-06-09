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
flex2 = AnalogIn(ads, ADS.P2)

TCA_ADDR = 0x70

def select_mux_channel(channel):
    while not i2c.try_lock():
        pass
    i2c.writeto(TCA_ADDR, channel)
    i2c.unlock()

drv = adafruit_drv2605.DRV2605(i2c)
drv.sequence[0] = adafruit_drv2605.Effect(118)

buzzing0 = False
buzzing1 = False
buzzing2 = False

while True:
    val0 = flex0.value
    val1 = flex1.value
    val2 = flex2.value
    print(f"A0: {val0}, A1: {val1}, A2: {val2}")

    if val0 > 5500 and not buzzing0:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel(b'\x01')
        drv.play()
        buzzing0 = True
        print("Motor 0 ON")
    elif val0 < 4600 and buzzing0:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel(b'\x01')
        drv.stop()
        buzzing0 = False
        print("Motor 0 OFF")

    if val1 > 4900 and not buzzing1:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel(b'\x02')
        drv.play()
        buzzing1 = True
        print("Motor 1 ON")
    elif val1 < 4400 and buzzing1:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel(b'\x02')
        drv.stop()
        buzzing1 = False
        print("Motor 1 OFF")

    if val2 > 5500 and not buzzing2:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel(b'\x04')
        drv.play()
        buzzing2 = True
        print("Motor 2 ON")
    elif val2 < 4600 and buzzing2:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel(b'\x04')
        drv.stop()
        buzzing2 = False
        print("Motor 2 OFF")

    time.sleep(0.1)
