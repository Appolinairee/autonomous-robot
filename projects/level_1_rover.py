"""
MARS ROVER - NIVEAU 1
Suivi de ligne avec detection et collecte d'objets
"""

from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor, servo
from gpiozero import InputDevice, DistanceSensor, LED, TonalBuzzer
from time import sleep, strftime
from picamera import PiCamera
import google.generativeai as genai
from PIL import Image

i2c = busio.I2C(SCL, SDA)
pwm = PCA9685(i2c, address=0x5f)
pwm.frequency = 50

motor1 = motor.DCMotor(pwm.channels[15], pwm.channels[14])
motor2 = motor.DCMotor(pwm.channels[12], pwm.channels[13])
motor1.decay_mode = motor.SLOW_DECAY
motor2.decay_mode = motor.SLOW_DECAY

capteur_gauche = InputDevice(pin=22)
capteur_centre = InputDevice(pin=27)
capteur_droite = InputDevice(pin=17)

capteur_distance = DistanceSensor(echo=24, trigger=23, max_distance=2)

phare_gauche = LED(25)
phare_droit = LED(11)
buzzer = TonalBuzzer(18)

camera = PiCamera()

# Configuration Gemini API
GEMINI_API_KEY = "VOTRE_CLE_API_ICI"
genai.configure(api_key=GEMINI_API_KEY)
model_gemini = genai.GenerativeModel('gemini-1.5-flash')

compteur_objets = 0


def set_servo(channel, angle):
    """Configure l'angle d'un servo"""
    servo_obj = servo.Servo(
        pwm.channels[channel],
        min_pulse=500,
        max_pulse=2400,
        actuation_range=180
    )
    servo_obj.angle = angle


def conduire(vitesse, angle):
    """Fait rouler le robot avec vitesse et direction donnees"""
    motor1.throttle = -vitesse
    motor2.throttle = -vitesse
    set_servo(0, angle)


def stop():
    """Arret des moteurs"""
    motor1.throttle = 0
    motor2.throttle = 0


def demi_tour():
    """Fait un demi-tour sur place"""
    print("Demi-tour...")
    phares_clignoter()
    
    motor1.throttle = -0.3
    motor2.throttle = 0.3
    set_servo(0, 90)
    
    sleep(2.0)
    
    stop()
    phares_allumer()
    print("Demi-tour termine")


def phares_allumer():
    """Allume les phares"""
    phare_gauche.on()
    phare_droit.on()


def phares_eteindre():
    """Eteint les phares"""
    phare_gauche.off()
    phare_droit.off()


def phares_clignoter():
    """Fait clignoter les phares"""
    phare_gauche.blink(on_time=0.3, off_time=0.3)
    phare_droit.blink(on_time=0.3, off_time=0.3)


def bip_court():
    """Bip court"""
    buzzer.play("C4")
    sleep(0.15)
    buzzer.stop()


def bip_double():
    """Double bip"""
    buzzer.play("C4")
    sleep(0.15)
    buzzer.stop()
    sleep(0.1)
    buzzer.play("C4")
    sleep(0.15)
    buzzer.stop()


def initialiser():
    """Initialise le rover et ses servos"""
    print("Initialisation...")
    phares_eteindre()
    set_servo(0, 90)
    set_servo(2, 150)
    set_servo(4, 30)
    sleep(1)
    print("Pret")


def get_distance():
    """Mesure la distance devant le rover en cm"""
    try:
        return capteur_distance.distance * 100
    except:
        return 999


def prendre_photo():
    """Prend une photo avec timestamp"""
    timestamp = strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"/home/pi/echantillon_{timestamp}.jpg"
    
    print("Prise de photo...")
    phare_gauche.on()
    phare_droit.on()
    
    camera.capture(nom_fichier)
    sleep(0.5)
    
    print(f"Photo sauvee: {nom_fichier}")
    return nom_fichier


def analyser_avec_gemini(chemin_photo):
    """Analyse la photo avec Gemini et determine l'action"""
    print("Analyse IA en cours...")
    
    try:
        image = Image.open(chemin_photo)
        
        prompt = """Analyse cette image prise par un rover Mars.
        Reponds UNIQUEMENT par un mot parmi:
        - COLLECTER (objet interessant a ramasser)
        - DEGAGER (obstacle a pousser hors du chemin)
        - IGNORER (rien d'important)
        
        Reponse:"""
        
        response = model_gemini.generate_content([prompt, image])
        decision = response.text.strip().upper()
        
        print(f"Decision IA: {decision}")
        return decision
        
    except Exception as e:
        print(f"Erreur IA: {e}")
        return "COLLECTER"  # Par defaut


def saisir_objet():
    """Sequence pour saisir un objet"""
    print("Saisie objet...")
    phares_clignoter()
    
    set_servo(4, 30)
    sleep(0.5)
    
    set_servo(2, 100)
    sleep(0.5)
    
    set_servo(4, 115)
    sleep(0.5)
    
    set_servo(2, 150)
    sleep(0.5)
    
    bip_court()
    phares_allumer()
    print("Objet saisi")


def deposer_objet():
    """Sequence pour deposer un objet"""
    print("Depot objet...")
    phares_clignoter()
    
    set_servo(2, 100)
    sleep(0.5)
    
    set_servo(4, 30)
    sleep(0.5)
    
    set_servo(2, 150)
    sleep(0.5)
    
    bip_double()
    print("Objet depose")


def degager_obstacle():
    """Pousse un obstacle hors du chemin"""
    print("Degagement obstacle...")
    phares_clignoter()
    
    # Approche doucement
    conduire(0.2, 90)
    sleep(0.8)
    
    # Pousse a droite
    conduire(0.3, 120)
    sleep(1.5)
    
    # Recule
    motor1.throttle = 0.3
    motor2.throttle = 0.3
    sleep(1.0)
    
    stop()
    phares_allumer()
    print("Obstacle degage")


def detecter_et_collecter():
    """Detecte, photographie et analyse avec IA"""
    global compteur_objets
    
    distance_detection = 15
    distance = get_distance()
    
    if distance < distance_detection:
        print("Objet detecte a %.1f cm" % distance)
        phares_eteindre()
        stop()
        sleep(0.5)
        
        # Photo et analyse IA
        chemin_photo = prendre_photo()
        decision = analyser_avec_gemini(chemin_photo)
        
        # Action selon decision IA
        if decision == "COLLECTER":
            saisir_objet()
            compteur_objets += 1
            print("Objet collecte #%d" % compteur_objets)
        
        elif decision == "DEGAGER":
            degager_obstacle()
            print("Obstacle degage")
        
        else:  # IGNORER
            print("Rien a faire - Continue")
        
        sleep(1)
        return True
    
    return False


def suivre_ligne():
    vitesse_normale = 0.3
    vitesse_virage = 0.2
    
    # Suivi de ligne
    gauche = capteur_gauche.value
    centre = capteur_centre.value
    droite = capteur_droite.value
    
    print('G:%d C:%d D:%d' % (gauche, centre, droite))
    
    # Sur la ligne - avancer droit
    if (gauche == 0 and centre == 1 and droite == 0) or \
       (gauche == 1 and centre == 1 and droite == 1):
        conduire(vitesse_normale, 90)
    
    # Derive a droite - corriger a droite
    elif (gauche == 0 and centre == 1 and droite == 1) or \
         (gauche == 0 and centre == 0 and droite == 1):
        conduire(vitesse_virage, 105)
    
    # Derive a gauche - corriger a gauche
    elif (gauche == 1 and centre == 1 and droite == 0) or \
         (gauche == 1 and centre == 0 and droite == 0):
        conduire(vitesse_virage, 75)
    
    # Ligne perdue - fin du trajet
    elif gauche == 0 and centre == 0 and droite == 0:
        stop()
        if compteur_objets > 0:
            deposer_objet()
        return True
    
    return False


def executer_mission():
    """Execute une mission complete : collecter et livrer des objets"""
    global compteur_objets
    
    compteur_objets = 0
    print("\n--- Mission ALLER ---")
    
    while True:
        detecter_et_collecter()
        
        if suivre_ligne():
            print("Arrivee - Objets collectes: %d" % compteur_objets)
            break
        
        sleep(0.05)
    
    sleep(1)
    demi_tour()
    sleep(1)


def main():
    try:
        print("MARS ROVER - Niveau 1")
        print("Suivi ligne + Collecte objet")
        print("Missions continues - Ctrl+C pour arreter\n")
        
        initialiser()
        phares_allumer()
        
        while True:
            executer_mission()
    
    except KeyboardInterrupt:
        print("\nArret demande")
    
    finally:
        phares_eteindre()
        stop()
        camera.close()
        pwm.deinit()
        print("Arret propre")

if __name__ == "__main__":
    main()