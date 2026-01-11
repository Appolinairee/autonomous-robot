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


def test_display():
    """
    Fonction de test : teste toutes les fonctions d'affichage
    """
    import time
    
    print("\n=== TEST ECRAN OLED ===\n")
    
    # Test 1 : Effacer l'ecran
    print("[1/6] Test effacement...")
    effacer()
    time.sleep(1)
    
    # Test 2 : Afficher un message simple
    print("[2/6] Test message simple...")
    afficher_message("Bonjour!")
    time.sleep(2)
    
    # Test 3 : Afficher 3 lignes de texte
    print("[3/6] Test 3 lignes...")
    afficher_texte("Ligne 1", "Ligne 2", "Ligne 3")
    time.sleep(2)
    
    # Test 4 : Afficher info robot
    print("[4/6] Test info robot...")
    afficher_info_robot(etat="Actif", distance=42.5, objets=3)
    time.sleep(2)
    
    # Test 5 : Animation de progression
    print("[5/6] Test animation progression...")
    for i in range(0, 101, 20):
        afficher_texte("Chargement...", f"Progress: {i}%", "=" * (i // 10))
        time.sleep(0.5)
    
    # Test 6 : Test de caracteres speciaux
    print("[6/6] Test caracteres speciaux...")
    afficher_texte("Temp: 25°C", "Bat: 12.3V", "Status: OK!")
    time.sleep(2)
    
    # Test 7 : Cycle rapide
    print("[7/7] Test cycle rapide...")
    etats = ["INIT", "SCAN", "MOVE", "STOP"]
    for etat in etats:
        afficher_info_robot(etat=etat, distance=15.2, objets=2)
        time.sleep(1)
    
    # Fin du test
    print("\n=== FIN DU TEST ===")
    afficher_texte("Test termine", "Ecran OK!", "✓✓✓")
    time.sleep(2)
    
    # Effacer pour finir proprement
    effacer()
    print("✅ Test reussi - Ecran efface\n")


if __name__ == "__main__":
    # Execution directe du fichier = lance le test
    test_display()
