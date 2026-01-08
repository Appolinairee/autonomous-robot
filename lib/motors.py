"""
Controle des moteurs et direction
"""

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor, servo

# Initialisation I2C et PWM
i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c, address=0x5f)
pwm.frequency = 50

# Moteurs DC
motor1 = motor.DCMotor(pwm.channels[15], pwm.channels[14])
motor2 = motor.DCMotor(pwm.channels[12], pwm.channels[13])
motor1.decay_mode = motor.SLOW_DECAY
motor2.decay_mode = motor.SLOW_DECAY

# Servo direction
servo_direction = servo.Servo(pwm.channels[0], min_pulse=500, max_pulse=2400)


def conduire(vitesse, angle):
    """Configure moteurs + direction"""
    motor1.throttle = vitesse
    motor2.throttle = vitesse
    servo_direction.angle = angle


def stop():
    """Arrete les moteurs"""
    motor1.throttle = 0
    motor2.throttle = 0


def avancer(vitesse=0.3):
    """Avance tout droit"""
    conduire(vitesse, 90)


def reculer(vitesse=0.3):
    """Recule tout droit"""
    motor1.throttle = -vitesse
    motor2.throttle = -vitesse
    servo_direction.angle = 90


def tourner_gauche(vitesse=0.2):
    """Avance en tournant a gauche"""
    conduire(vitesse, 75)


def tourner_droite(vitesse=0.2):
    """Avance en tournant a droite"""
    conduire(vitesse, 105)


def pivoter_sur_place(vitesse=0.2):
    """Rotation sur place (moteurs en sens oppose)"""
    servo_direction.angle = 90
    motor1.throttle = -vitesse
    motor2.throttle = vitesse
