"""
Gestion des LEDs RGB WS2812 (NeoPixel)
"""

from rpi_ws281x import PixelStrip, Color
from time import sleep

# Configuration LEDs WS2812
LED_COUNT = 3           # Nombre de LEDs
LED_PIN = 12            # GPIO 12 (PWM0, pin 32)
LED_FREQ_HZ = 800000    # Frequence LED (800kHz)
LED_DMA = 10            # Canal DMA
LED_BRIGHTNESS = 128    # Luminosite (0-255)
LED_INVERT = False      # Pas d'inversion signal
LED_CHANNEL = 0         # Canal PWM

# Initialisation du strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, 
                   LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()


# ========== CONTROLES DE BASE ==========

def led_eteindre():
    """Eteint toutes les LEDs"""
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


def led_couleur(r, g, b):
    """Allume toutes les LEDs avec une couleur RGB"""
    couleur = Color(g, r, b)  # Format GRB pour WS2812
    for i in range(LED_COUNT):
        strip.setPixelColor(i, couleur)
    strip.show()


def led_individuelle(numero, r, g, b):
    """Allume une LED specifique (0, 1, 2)"""
    if 0 <= numero < LED_COUNT:
        strip.setPixelColor(numero, Color(g, r, b))
        strip.show()


# ========== INDICATEURS DE STATUT ==========

def led_status_ok():
    """Vert: tout va bien"""
    led_couleur(0, 255, 0)


def led_status_erreur():
    """Rouge: erreur detectee"""
    led_couleur(255, 0, 0)


def led_status_attention():
    """Orange: attention requise"""
    led_couleur(255, 100, 0)


def led_status_attente():
    """Bleu: en attente/traitement"""
    led_couleur(0, 0, 255)


def led_status_demarrage():
    """Blanc: initialisation"""
    led_couleur(255, 255, 255)


# ========== EFFETS LUMINEUX ==========

def led_clignoter(r, g, b, fois=3, duree=0.3):
    """Fait clignoter les LEDs"""
    for _ in range(fois):
        led_couleur(r, g, b)
        sleep(duree)
        led_eteindre()
        sleep(duree)


def led_balayage(r, g, b, duree=0.2):
    """Effet de balayage de gauche a droite"""
    led_eteindre()
    for i in range(LED_COUNT):
        led_individuelle(i, r, g, b)
        sleep(duree)
        led_individuelle(i, 0, 0, 0)


def led_progression(niveau):
    """Affiche niveau de progression (0-100%)"""
    led_eteindre()
    leds_actives = int((niveau / 100.0) * LED_COUNT)
    for i in range(leds_actives):
        led_individuelle(i, 0, 255, 0)


def led_rainbow():
    """Effet arc-en-ciel"""
    couleurs = [
        (255, 0, 0),    # Rouge
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Jaune
        (0, 255, 0),    # Vert
        (0, 0, 255),    # Bleu
        (75, 0, 130),   # Indigo
        (148, 0, 211)   # Violet
    ]
    
    for couleur in couleurs:
        led_couleur(*couleur)
        sleep(0.3)


def led_temperature(temp_celsius):
    """Affiche couleur selon temperature"""
    if temp_celsius < 15:
        led_couleur(0, 0, 255)      # Bleu froid
    elif temp_celsius < 25:
        led_couleur(0, 255, 0)      # Vert optimal
    elif temp_celsius < 35:
        led_couleur(255, 127, 0)    # Orange chaud
    else:
        led_couleur(255, 0, 0)      # Rouge critique


# ========== MODES DE FONCTIONNEMENT ==========

def led_mode_ligne():
    """Mode suivi de ligne: vert"""
    led_status_ok()


def led_mode_evitement():
    """Mode evitement obstacle: jaune"""
    led_couleur(255, 200, 0)


def led_mode_exploration():
    """Mode exploration: bleu clair"""
    led_couleur(0, 150, 255)


def led_mode_arret():
    """Mode arret: rouge"""
    led_status_erreur()


# ========== NETTOYAGE ==========

def led_cleanup():
    """Nettoie et eteint les LEDs"""
    led_eteindre()
