"""
Gestion de la signalisation (LEDs, buzzer)
"""

from gpiozero import LED, TonalBuzzer
from time import sleep

# LEDs et buzzer
phare_gauche = LED(25)
phare_droit = LED(11)
buzzer = TonalBuzzer(18)


# ========== LEDs ==========

def phares_allumer():
    """Allume les deux phares"""
    phare_gauche.on()
    phare_droit.on()


def phares_eteindre():
    """Eteint les deux phares"""
    phare_gauche.off()
    phare_droit.off()


def phares_clignoter(duree=0.5):
    """Fait clignoter les phares"""
    phare_gauche.blink(on_time=duree, off_time=duree)
    phare_droit.blink(on_time=duree, off_time=duree)


# ========== BUZZER ==========

def bip_court():
    """Bip court"""
    buzzer.play(440)
    sleep(0.2)
    buzzer.stop()


def bip_double():
    """Double bip"""
    bip_court()
    sleep(0.1)
    bip_court()


def bip_long():
    """Bip long"""
    buzzer.play(440)
    sleep(0.5)
    buzzer.stop()
