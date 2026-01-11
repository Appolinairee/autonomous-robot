"""
ROVER MARS - VERSION SIMPLE EXAMEN
===================================
Mission: Suivre ligne + Détecter obstacle + Prendre photo + Collecter
"""

# Imports de base
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor, servo
from gpiozero import DistanceSensor, InputDevice, LED
from time import sleep
from picamera import PiCamera

# ============================================================================
# CONFIGURATION - Tes pins exacts
# ============================================================================

# I2C et PCA9685
i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c, address=0x5f)
pwm.frequency = 50

# Moteurs - tes pins
motor1 = motor.DCMotor(pwm.channels[15], pwm.channels[14])
motor2 = motor.DCMotor(pwm.channels[12], pwm.channels[13])
motor1.decay_mode = motor.SLOW_DECAY
motor2.decay_mode = motor.SLOW_DECAY

# Capteur ultrason - tes pins
sensor = DistanceSensor(echo=24, trigger=23, max_distance=2)

# Capteurs ligne - tes pins
left = InputDevice(pin=22)
middle = InputDevice(pin=27)
right = InputDevice(pin=17)

# LED
led = LED(25)

# Caméra
camera = PiCamera()

# Vitesse
speed = 0.35

# ============================================================================
# FONCTIONS DE BASE - Exactement comme les tiennes
# ============================================================================

def set_angle(ID, angle):
    servo_angle = servo.Servo(pwm.channels[ID], min_pulse=500, max_pulse=2400, actuation_range=180)
    servo_angle.angle = angle

def avancer(speed=speed):
    motor1.throttle = -speed
    motor2.throttle = -speed

def ARRET():
    motor1.throttle = 0
    motor2.throttle = 0

def tourner_gauche(speed=speed):
    motor1.throttle = -speed
    motor2.throttle = -speed
    set_angle(0, 65)

def tourner_droite(speed=speed):
    motor1.throttle = -speed
    motor2.throttle = -speed
    set_angle(0, 110)

# ============================================================================
# SUIVEUR DE LIGNE - Ta fonction exacte
# ============================================================================

def suiveur():
    status_left = left.value
    status_middle = middle.value
    status_right = right.value
    print('left: %d middle: %d right: %d' % (status_left, status_middle, status_right))

    if (status_left == 0 and status_middle == 1 and status_right == 0) or (status_left == 1 and status_middle == 1 and status_right == 1):
        avancer()

    elif (status_left == 0 and status_middle == 1 and status_right == 1) or (status_left == 0 and status_middle == 0 and status_right == 1):
        tourner_droite()

    elif (status_left == 1 and status_middle == 1 and status_right == 0) or (status_left == 1 and status_middle == 0 and status_right == 0):
        tourner_gauche()

    elif (status_left == 0 and status_middle == 0 and status_right == 0):
        ARRET()

# ============================================================================
# FONCTIONS POUR L'EXAMEN
# ============================================================================

def prendre_photo():
    """Prendre vraie photo avec caméra"""
    import time
    timestamp = time.strftime("%H%M%S")
    nom_fichier = f"/home/pi/echantillon_{timestamp}.jpg"
    
    print("Photo!")
    led.on()
    camera.capture(nom_fichier)
    sleep(1)
    led.off()
    print(f"Photo sauvee: {nom_fichier}")

def bras_collecter():
    """Ta séquence de bras exacte"""
    set_angle(2, 150)  # Position haute
    sleep(1)
    set_angle(4, 30)   # Ouvrir pince
    sleep(1)
    set_angle(2, 100)  # Descendre
    sleep(2)
    set_angle(4, 115)  # Fermer pince
    sleep(2)
    set_angle(2, 150)  # Remonter
    sleep(1)

# ============================================================================
# MISSION SIMPLE
# ============================================================================

echantillons = 0

try:
    while True:
        # 1. Suivre ligne
        suiveur()
        
        # 2. Vérifier distance
        distance = (sensor.distance) * 100
        print("Distance: %.1f cm" % distance)
        
        # 3. Si obstacle proche
        if distance < 20:
            print("Obstacle detecte!")
            ARRET()
            
            # Photo puis collecter
            prendre_photo()
            bras_collecter()
            echantillons += 1
            
            print("Echantillons: %d" % echantillons)
            sleep(2)
        
        sleep(0.1)

except KeyboardInterrupt:
    print("Arret")
    ARRET()
    camera.close()
    pwm.deinit()
