"""
Gestion de la camera
"""

from picamera import PiCamera
from time import strftime

# Dossier de sauvegarde
DOSSIER_PHOTOS = "/home/pi"

# Camera
camera = PiCamera()


def prendre_photo():
    """Capture une photo avec timestamp"""
    timestamp = strftime("%Y%m%d_%H%M%S")
    chemin = f"{DOSSIER_PHOTOS}/echantillon_{timestamp}.jpg"
    
    print(f"Capture photo: {chemin}")
    camera.capture(chemin)
    
    return chemin


def fermer_camera():
    """Ferme proprement la camera"""
    camera.close()
