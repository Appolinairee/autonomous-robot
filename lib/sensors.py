"""
Gestion des capteurs
"""

from gpiozero import InputDevice, DistanceSensor

# Capteurs de ligne (IR)
capteur_gauche = InputDevice(pin=22)
capteur_centre = InputDevice(pin=27)
capteur_droite = InputDevice(pin=17)

# Capteur ultrason
capteur_distance = DistanceSensor(echo=24, trigger=23, max_distance=2)


def lire_ligne():
    """Retourne l'etat des 3 capteurs IR (gauche, centre, droite)"""
    return (capteur_gauche.value, capteur_centre.value, capteur_droite.value)


def hors_ligne():
    """Tous les capteurs hors ligne"""
    g, c, d = lire_ligne()
    return g == 0 and c == 0 and d == 0


def ligne_a_gauche():
    """Ligne detectee a gauche du robot"""
    g, c, d = lire_ligne()
    return (g == 1 and c == 1 and d == 0) or (g == 1 and c == 0 and d == 0)


def ligne_a_droite():
    """Ligne detectee a droite du robot"""
    g, c, d = lire_ligne()
    return (g == 0 and c == 1 and d == 1) or (g == 0 and c == 0 and d == 1)


def ligne_au_centre():
    """Ligne au centre du robot"""
    g, c, d = lire_ligne()
    return (g == 0 and c == 1 and d == 0) or (g == 1 and c == 1 and d == 1)


def get_distance():
    """Retourne la distance en cm"""
    return capteur_distance.distance * 100


def detecter_obstacle(seuil=15):
    """Verifie si un obstacle est detecte en dessous du seuil (cm)"""
    return get_distance() < seuil