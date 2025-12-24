"""
Robot de manipulation avec parcours A → B
Scénario : saisir un objet en A, parcours avec virage, déposer en B
"""

from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor, servo
from gpiozero import DistanceSensor
from time import sleep

i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c, address=0x5f)
pwm.frequency = 50

# Moteurs
M1_IN1 = 15
M1_IN2 = 14
M2_IN1 = 12
M2_IN2 = 13

motor1 = motor.DCMotor(
    pwm.channels[M1_IN1],
    pwm.channels[M1_IN2]
)
motor2 = motor.DCMotor(
    pwm.channels[M2_IN1],
    pwm.channels[M2_IN2]
)
motor1.decay_mode = motor.SLOW_DECAY
motor2.decay_mode = motor.SLOW_DECAY


# Capteur de distance
SENSOR_TRIGGER = 23
SENSOR_ECHO = 24

sensor = DistanceSensor(
    echo=SENSOR_ECHO,
    trigger=SENSOR_TRIGGER,
    max_distance=2
)

# Servos
SERVO_PILOTAGE = 0
SERVO_BRAS = 2
SERVO_PINCE = 4


def set_servo(servo_id, angle):
    """Configure l'angle d'un servo"""
    servo_obj = servo.Servo(
        pwm.channels[servo_id],
        min_pulse=500,
        max_pulse=2400,
        actuation_range=180
    )
    servo_obj.angle = angle
    sleep(0.1)

def stop_motors():
    motor1.throttle = 0
    motor2.throttle = 0

def conduire(vitesse, angle_direction, duree):
    """Fait rouler le robot avec vitesse, angle et durée donnés"""
    motor1.throttle = -vitesse
    motor2.throttle = -vitesse
    set_servo(SERVO_PILOTAGE, angle_direction)
    sleep(duree)

def conduire_avec_detection(vitesse, angle_direction, duree, distance_securite=10):
    """Fait rouler le robot en surveillant les obstacles"""
    motor1.throttle = -vitesse
    motor2.throttle = -vitesse
    set_servo(SERVO_PILOTAGE, angle_direction)
    
    temps_ecoule = 0
    pas = 0.1  # Vérifie tous les 0.1s
    
    while temps_ecoule < duree:
        distance_cm = sensor.distance * 100
        
        if distance_cm < distance_securite:
            print(f"⚠ OBSTACLE DÉTECTÉ à {distance_cm:.1f} cm !")
            stop_motors()
            raise Exception(f"Obstacle détecté à {distance_cm:.1f} cm")
        
        sleep(pas)
        temps_ecoule += pas


# FONCTIONS DE MANIPULATION
TEMPS_SERVO = 0.5

BRAS_HAUT = 150
BRAS_BAS = 100

PINCE_OUVERTE = 30
PINCE_FERMEE = 115

def saisir_objet():
    print("→ Ouverture de la pince...")
    set_servo(SERVO_PINCE, PINCE_OUVERTE)
    sleep(TEMPS_SERVO)
    
    print("→ Abaissement du bras...")
    set_servo(SERVO_BRAS, BRAS_BAS)
    sleep(TEMPS_SERVO)
    
    print("→ Fermeture de la pince (saisie)...")
    set_servo(SERVO_PINCE, PINCE_FERMEE)
    sleep(TEMPS_SERVO)
    
    print("→ Relèvement du bras...")
    set_servo(SERVO_BRAS, BRAS_HAUT)
    sleep(TEMPS_SERVO)
    print("✓ Objet saisi!\n")

def deposer_objet():
    print("→ Abaissement du bras...")
    set_servo(SERVO_BRAS, BRAS_BAS)
    sleep(TEMPS_SERVO)
    
    print("→ Ouverture de la pince (dépôt)...")
    set_servo(SERVO_PINCE, PINCE_OUVERTE)
    sleep(TEMPS_SERVO)
    
    print("→ Relèvement du bras...")
    set_servo(SERVO_BRAS, BRAS_HAUT)
    sleep(TEMPS_SERVO)
    print("✓ Objet déposé!\n")


# SÉQUENCE PRINCIPALE

VITESSE_NORMALE = 0.5
VITESSE_VIRAGE = 0.4
VITESSE_LENTE = 0.2

ANGLE_DROIT = 90
ANGLE_GAUCHE = 30
ANGLE_DROITE = 150

def parcours_A_vers_B():
    print("PHASE 1 : Saisie de l'objet au point A")
    saisir_objet()
    sleep(0.5)

    print("PHASE 2 : Avancée tout droit")
    conduire_avec_detection(VITESSE_NORMALE, ANGLE_DROIT, 4.0)

    print("PHASE 3 : Virage à gauche")
    conduire(VITESSE_LENTE, ANGLE_DROIT, 0.3)
    conduire_avec_detection(VITESSE_VIRAGE, ANGLE_GAUCHE, 4)

    print("PHASE 4 : Avancée après virage")
    conduire_avec_detection(VITESSE_NORMALE, ANGLE_DROIT, 4.0)

    print("PHASE 5 : Arrêt et dépôt au point B")
    stop_motors()
    sleep(0.5)
    deposer_objet()

    print("="*50)
    print("PARCOURS TERMINÉ AVEC SUCCÈS!")
    print("="*50 + "\n")



def main():
    try:
        set_servo(SERVO_PILOTAGE, ANGLE_DROIT)
        set_servo(SERVO_BRAS, BRAS_HAUT)
        set_servo(SERVO_PINCE, PINCE_OUVERTE)
        sleep(1)
        
        parcours_A_vers_B()
        
        stop_motors()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Interruption utilisateur")
    except Exception as e:
        print(f"\n\n Erreur : {e}")
    finally:
        stop_motors()
        pwm.deinit()


if __name__ == "__main__":
    main()
