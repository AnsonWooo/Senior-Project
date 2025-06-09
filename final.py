import time
import board
import busio
import adafruit_drv2605
import adafruit_bno055
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
flex0 = AnalogIn(ads, ADS.P0)
flex1 = AnalogIn(ads, ADS.P1)

drv = adafruit_drv2605.DRV2605(i2c)
drv.sequence[0] = adafruit_drv2605.Effect(118)

bno = adafruit_bno055.BNO055_I2C(i2c)

TCA_ADDR = 0x70
last_accel = None

def select_mux_channel(channel_bit):
    while not i2c.try_lock():
        pass
    i2c.writeto(TCA_ADDR, bytes([1 << channel_bit]))
    i2c.unlock()

def select_mux_channel_flex(channel):
    while not i2c.try_lock():
        pass
    i2c.writeto(TCA_ADDR, channel)
    i2c.unlock()


def buzz_motor(channel):
    select_mux_channel(channel)
    drv = adafruit_drv2605.DRV2605(i2c)
    drv.sequence[0] = adafruit_drv2605.Effect(118)
    drv.play()
    time.sleep(0.3)
    drv.stop()

buzzing0 = False
buzzing1 = False
THRESH_ON = 4700
THRESH_OFF = 4400

while True:
    i2c.writeto(TCA_ADDR, b'\x00')
    accel = bno.acceleration
    if accel and last_accel:
        jerk = sum([(a - b)**2 for a, b in zip(accel, last_accel)]) ** 0.5

        if jerk > 10.0:
            for ch in range(4):
                buzz_motor(ch)

    last_accel = accel

    val0 = flex0.value
    val1 = flex1.value
    print(f"A0: {val0}, A1: {val1}")

    if val0 > THRESH_ON and not buzzing0:
        i2c.writeto(TCA_ADDR, b'\x00')
        select_mux_channel_flex(b'\x01')
        drv.play()
        buzzing0 = True
        print("Motor 0 ON")
    elif val0 < THRESH_OFF and buzzing0:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel_flex(b'\x01')
        drv.stop()
        buzzing0 = False
        print("Motor 0 OFF")

    if val1 > THRESH_ON and not buzzing1:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel_flex(b'\x02')
        drv.play()
        buzzing1 = True
        print("Motor 1 ON")
    elif val1 < THRESH_OFF and buzzing1:
        i2c.writeto(TCA_ADDR, b'\x00') 
        select_mux_channel_flex(b'\x02')
        drv.stop()
        buzzing1 = False
        print("Motor 1 OFF")

    time.sleep(0.1)
