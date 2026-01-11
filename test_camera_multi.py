"""
Test camera - Prendre plusieurs photos successives
"""

from lib.camera import prendre_photo
from time import sleep

print("=== TEST CAMERA MULTI-PHOTOS ===\n")

# Prendre 3 photos avec 2 secondes entre chaque
for i in range(1, 4):
    print(f"Photo {i}/3...")
    chemin = prendre_photo()
    print(f"  -> Sauvegardee: {chemin}")
    sleep(2)

print("\n=== TEST TERMINE ===")
print("Si vous voyez ce message, le probleme est RESOLU !")
print("Toutes les photos ont ete prises sans erreur.")
