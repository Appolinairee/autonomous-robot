""" Gestion de l'ecran OLED """

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas

# Initialisation OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32)


def afficher_texte(ligne1="", ligne2="", ligne3=""):
    """Affiche jusqu'a 3 lignes de texte"""
    with canvas(device) as draw:
        draw.text((0, 0), ligne1, fill="white")
        draw.text((0, 11), ligne2, fill="white")
        draw.text((0, 22), ligne3, fill="white")


def afficher_info_robot(etat="", distance=0, objets=0):
    """Affiche l'etat du robot"""
    ligne1 = f"Etat: {etat}"
    ligne2 = f"Dist: {distance:.1f}cm"
    ligne3 = f"Objets: {objets}"
    afficher_texte(ligne1, ligne2, ligne3)


def afficher_message(message):
    """Affiche un message"""
    with canvas(device) as draw:
        draw.text((0, 12), message, fill="white")


def effacer():
    """Efface l'ecran"""
    device.clear()
