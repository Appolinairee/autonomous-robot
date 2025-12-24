from board import SCL, SDA
import busio
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685
from gpiozero import DistanceSensor
from time import sleep

i2c=busio.I2C(SCL, SDA)
pca = PCA9685(i2c, address=0x5f)
pca.frequency = 50

def set_angle(ID, angle):
    servo_angle=servo.Servo(pca.channels[ID], min_pulse=500, max_pulse=2400, actuation_range=180)
    servo_angle.angle = angle

Tr = 23
Ec = 24

sensor = DistanceSensor(echo=Ec, trigger=Tr, max_distance=2)
distance = (sensor.distance)*100

if True:
    print("%.2f cm;" % distance)
        
    set_angle(2, 150)
    sleep(2)

    set_angle(4, 115)
    sleep(2)

    set_angle(2, 100)
    sleep(2)

    set_angle(1, 180)
    sleep(2)

    set_angle(4, 180)
    sleep(2)

    set_angle(1, 40)
    sleep(2)