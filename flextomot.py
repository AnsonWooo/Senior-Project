import time
import board
import busio
import adafruit_drv2605
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
flex_channel = AnalogIn(ads, ADS.P1)

while not i2c.try_lock():
    pass
i2c.writeto(0x70, b'\x02')
i2c.unlock()

drv = adafruit_drv2605.DRV2605(i2c)
drv.sequence[0] = adafruit_drv2605.Effect(118)

buzzing = False

while True:
    val = flex_channel.value
    print("Flex Value:", val)

    if val > 4700 and not buzzing:
        drv.play()
        buzzing = True
        print("Buzz ON")

    elif val < 4400 and buzzing:
        drv.stop()
        buzzing = False
        print("Buzz OFF")

    time.sleep(0.1)
