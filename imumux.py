import time
import board
import busio
import adafruit_drv2605
import adafruit_bno055

i2c = busio.I2C(board.SCL, board.SDA)

bno = adafruit_bno055.BNO055_I2C(i2c)

TCA_ADDR = 0x70

JERK_THRESHOLD = 10.0
last_accel = None

def select_mux_channel(channel_bit):
    while not i2c.try_lock():
        pass
    i2c.writeto(TCA_ADDR, bytes([1 << channel_bit]))
    i2c.unlock()

def buzz_motor(channel):
    select_mux_channel(channel)
    drv = adafruit_drv2605.DRV2605(i2c)
    drv.sequence[0] = adafruit_drv2605.Effect(118)
    drv.play()
    time.sleep(0.3)
    drv.stop()

while True:
    accel = bno.acceleration
    if accel and last_accel:
        jerk = sum([(a - b)**2 for a, b in zip(accel, last_accel)]) ** 0.5

        if jerk > JERK_THRESHOLD:
            print("Jerk detected.")
            for ch in range(5):
                buzz_motor(ch)

    last_accel = accel
    time.sleep(0.1)
