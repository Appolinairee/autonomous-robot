"""
Gestion des servomoteurs (bras 4-DOF, cou)
"""

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Initialisation I2C et PWM
i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c, address=0x5f)
pwm.frequency = 50


# ========== FONCTION GENERIQUE ==========

def set_servo(channel, angle):
    """Configure l'angle d'un servo"""
    servo_obj = servo.Servo(pwm.channels[channel], min_pulse=500, max_pulse=2400)
    servo_obj.angle = angle


# ========== BRAS ROBOTIQUE 4-DOF ==========

def base_tourner(angle):
    """Rotation de la base (Servo A)"""
    set_servo(1, angle)


def epaule_lever(angle):
    """Lever/baisser epaule (Servo B)"""
    set_servo(2, angle)


def coude_plier(angle):
    """Plier le coude (Servo C)"""
    set_servo(3, angle)


def pince_angle(angle):
    """Angle du prehenseur (Servo D)"""
    set_servo(4, angle)


def pince_ouvrir():
    """Ouvre le prehenseur"""
    pince_angle(30)


def pince_fermer():
    """Ferme le prehenseur"""
    pince_angle(115)


# ========== COU / CAMERA ==========

def camera_tourner(angle):
    """Tourne la camera (pan gauche/droite) (Servo E)"""
    set_servo(5, angle)


def camera_centrer():
    """Centre la camera"""
    camera_tourner(90)
