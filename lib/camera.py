"""
Gestion de la camera
"""

from picamera import PiCamera
from time import strftime

DOSSIER_PHOTOS = "/home/pi"

def prendre_photo():
    """Capture une photo avec timestamp"""
    timestamp = strftime("%Y%m%d_%H%M%S")
    chemin = f"{DOSSIER_PHOTOS}/echantillon_{timestamp}.jpg"
    
    print(f"Capture photo: {chemin}")

    with PiCamera() as camera:
        camera.capture(chemin)
    
    return chemin


def fermer_camera():
    """Fonction gardee pour compatibilite (n'est plus necessaire)"""
    pass


def test_camera(nombre_photos=3, delai=2):
    """
    Fonction de test : prend plusieurs photos successives
    
    Args:
        nombre_photos: Nombre de photos a capturer (defaut: 3)
        delai: Delai en secondes entre chaque photo (defaut: 2)
    
    Returns:
        Liste des chemins des photos prises
    """
    import time
    
    print(f"\n=== TEST CAMERA ===")
    print(f"Prise de {nombre_photos} photos avec {delai}s d'intervalle\n")
    
    photos = []
    
    for i in range(1, nombre_photos + 1):
        print(f"[{i}/{nombre_photos}] ", end="")
        try:
            chemin = prendre_photo()
            photos.append(chemin)
            print(f" Photo enregistree: {chemin}")
            
            if i < nombre_photos:
                print(f"    Attente de {delai}s...\n")
                time.sleep(delai)
        
        except Exception as e:
            print(f"ERREUR lors de la capture {i}: {e}")
            break
    
    print(f"\n=== RESULTAT ===")
    print(f"{len(photos)}/{nombre_photos} photos reussies")
    
    if photos:
        print("\nPhotos capturees:")
        for p in photos:
            print(f"  - {p}")
    
    return photos


if __name__ == "__main__":
    test_camera(nombre_photos=3, delai=2)
