from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor,servo
from gpiozero import DistanceSensor
from time import sleep

i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c, address=0x5f)
pwm.frequency = 50

M1_in1 = 15
M1_in2 = 14

M2_in1 = 12
M2_in2 = 13

motor1 = motor.DCMotor(
    pwm.channels[M1_in1],
    pwm.channels[M1_in2] )

motor2 = motor.DCMotor(
    pwm.channels[M2_in1],
    pwm.channels[M2_in2] )

motor1.decay_mode = motor.SLOW_DECAY
motor2.decay_mode = motor.SLOW_DECAY

Tr = 23
Ec = 24
sensor = DistanceSensor(echo=Ec, trigger=Tr, max_distance=2)
distance = (sensor.distance)*100

def set_angle(ID, angle):
    servo_angle=servo.Servo(pwm.channels[ID], min_pulse=500, max_pulse=2400, actuation_range=180)
    servo_angle.angle = angle

def avancer(speed=0.5) :
    motor1.throttle = -speed
    motor2.throttle = -speed
    set_angle(0, 90)
    
def reculer(speed=0.5):
    motor1.throttle = speed
    motor2.throttle = speed
    set_angle(0, 90)

def stop():
    motor1.throttle = 0
    motor2.throttle = 0
    set_angle(0, 90)

def tourner_gauche(speed=0.5):
    motor1.throttle = -speed
    motor2.throttle = -speed
    set_angle(0, 60)

def tourner_droite(speed=0.5):
    motor1.throttle = -speed
    motor2.throttle = -speed
    set_angle(0, 120)

def sequence_bras_debut():
    """Séquence d'ouverture du bras robotique"""
    set_angle(2, 150)
    sleep(2)
    set_angle(4, 30)
    sleep(2)
    set_angle(2, 100)
    sleep(2)

def sequence_bras_fin():
    """Séquence de fermeture du bras robotique"""
    set_angle(2, 150)
    sleep(2)
    set_angle(4, 115)
    sleep(2)

def gerer_obstacle():
    """Gère l'évitement d'obstacle selon la distance détectée"""
    distance_actuelle = sensor.distance * 100
    
    if distance_actuelle < 20:
        ARRET()
    else:
        tourner_gauche(speed=0.4)
        sleep(1)
        tourner_droite(speed=0.4)
        sleep(1)
        avancer()
        sleep(1)
        ARRET()

try :
    while True:
        sequence_bras_debut()
        avancer()
        sleep(1)
        gerer_obstacle()
        sequence_bras_fin()

except KeyboardInterrupt:
    print("stop")
    ARRET()
    pwm.deinit()