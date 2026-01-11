"""
Detection de couleur avec OpenCV (HSV)
"""

import cv2
import numpy as np
from lib.camera import prendre_photo


# ========== SEUILS HSV POUR CHAQUE COULEUR ==========

COULEURS_HSV = {
    'rouge': {
        'lower1': np.array([0, 100, 100]),      # Rouge bas (0-10°)
        'upper1': np.array([10, 255, 255]),
        'lower2': np.array([170, 100, 100]),    # Rouge haut (170-180°)
        'upper2': np.array([180, 255, 255])
    },
    'orange': {
        'lower': np.array([10, 100, 100]),
        'upper': np.array([25, 255, 255])
    },
    'jaune': {
        'lower': np.array([25, 100, 100]),
        'upper': np.array([35, 255, 255])
    },
    'vert': {
        'lower': np.array([35, 50, 50]),
        'upper': np.array([85, 255, 255])
    },
    'bleu': {
        'lower': np.array([100, 100, 100]),
        'upper': np.array([130, 255, 255])
    },
    'violet': {
        'lower': np.array([130, 50, 50]),
        'upper': np.array([170, 255, 255])
    },
    'blanc': {
        'lower': np.array([0, 0, 200]),
        'upper': np.array([180, 30, 255])
    },
    'noir': {
        'lower': np.array([0, 0, 0]),
        'upper': np.array([180, 255, 50])
    }
}


# ========== DETECTION COULEUR ==========

def detecter_couleur_image(image_path, seuil_pixels=500):
    """
    Detecte la couleur dominante dans une image
    
    Args:
        image_path: chemin vers l'image
        seuil_pixels: nombre minimum de pixels pour valider une couleur
    
    Returns:
        str: nom de la couleur detectee ou 'inconnu'
    """
    # Charger image
    img = cv2.imread(image_path)
    if img is None:
        return 'erreur_lecture'
    
    # Convertir BGR -> HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Tester chaque couleur
    resultats = {}
    
    for nom_couleur, seuils in COULEURS_HSV.items():
        if nom_couleur == 'rouge':
            # Rouge est special (0-10° et 170-180°)
            mask1 = cv2.inRange(hsv, seuils['lower1'], seuils['upper1'])
            mask2 = cv2.inRange(hsv, seuils['lower2'], seuils['upper2'])
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv, seuils['lower'], seuils['upper'])
        
        # Compter pixels
        nb_pixels = cv2.countNonZero(mask)
        resultats[nom_couleur] = nb_pixels
    
    # Trouver couleur dominante
    couleur_max = max(resultats, key=resultats.get)
    pixels_max = resultats[couleur_max]
    
    if pixels_max < seuil_pixels:
        return 'inconnu'
    
    return couleur_max


def detecter_couleur_camera(seuil_pixels=500):
    """
    Prend une photo et detecte la couleur
    
    Returns:
        tuple: (couleur_detectee, chemin_photo)
    """
    chemin = prendre_photo()
    couleur = detecter_couleur_image(chemin, seuil_pixels)
    return (couleur, chemin)


def detecter_couleur_region(image_path, x, y, largeur, hauteur):
    """
    Detecte couleur dans une region specifique de l'image
    
    Args:
        image_path: chemin image
        x, y: coordonnees coin superieur gauche
        largeur, hauteur: dimensions region
    
    Returns:
        str: couleur detectee
    """
    img = cv2.imread(image_path)
    if img is None:
        return 'erreur_lecture'
    
    # Extraire region
    region = img[y:y+hauteur, x:x+largeur]
    
    # Convertir HSV
    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
    
    # Analyser
    resultats = {}
    for nom_couleur, seuils in COULEURS_HSV.items():
        if nom_couleur == 'rouge':
            mask1 = cv2.inRange(hsv, seuils['lower1'], seuils['upper1'])
            mask2 = cv2.inRange(hsv, seuils['lower2'], seuils['upper2'])
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv, seuils['lower'], seuils['upper'])
        
        resultats[nom_couleur] = cv2.countNonZero(mask)
    
    return max(resultats, key=resultats.get)


# ========== DETECTION MULTI-OBJETS ==========

def detecter_objets_par_couleur(image_path, couleur_cible, min_area=1000):
    """
    Detecte tous les objets d'une couleur specifique
    
    Args:
        image_path: chemin image
        couleur_cible: nom de la couleur a chercher
        min_area: surface minimale d'un objet (pixels)
    
    Returns:
        list: liste de (x, y, largeur, hauteur) pour chaque objet
    """
    img = cv2.imread(image_path)
    if img is None:
        return []
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Creer masque pour la couleur cible
    if couleur_cible not in COULEURS_HSV:
        return []
    
    seuils = COULEURS_HSV[couleur_cible]
    
    if couleur_cible == 'rouge':
        mask1 = cv2.inRange(hsv, seuils['lower1'], seuils['upper1'])
        mask2 = cv2.inRange(hsv, seuils['lower2'], seuils['upper2'])
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        mask = cv2.inRange(hsv, seuils['lower'], seuils['upper'])
    
    # Trouver contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrer par taille et extraire bounding boxes
    objets = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            objets.append((x, y, w, h))
    
    return objets


def compter_objets_couleur(image_path, couleur, min_area=1000):
    """
    Compte le nombre d'objets d'une couleur donnee
    
    Returns:
        int: nombre d'objets detectes
    """
    objets = detecter_objets_par_couleur(image_path, couleur, min_area)
    return len(objets)


# ========== UTILITAIRES ==========

def get_couleur_pixel_central(image_path):
    """
    Retourne la couleur du pixel central de l'image
    
    Returns:
        str: couleur du centre
    """
    img = cv2.imread(image_path)
    if img is None:
        return 'erreur_lecture'
    
    h, w = img.shape[:2]
    x_centre, y_centre = w // 2, h // 2
    
    return detecter_couleur_region(image_path, x_centre-10, y_centre-10, 20, 20)


def afficher_detection(image_path, couleur_cible, save_path=None):
    """
    Affiche/sauvegarde image avec objets detectes encadres
    
    Args:
        image_path: image source
        couleur_cible: couleur a detecter
        save_path: chemin sauvegarde (optionnel)
    """
    img = cv2.imread(image_path)
    if img is None:
        return
    
    objets = detecter_objets_par_couleur(image_path, couleur_cible)
    
    # Dessiner rectangles
    for (x, y, w, h) in objets:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(img, couleur_cible, (x, y-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    if save_path:
        cv2.imwrite(save_path, img)
    
    return img


def calibrer_couleur_interactive(image_path):
    """
    Outil interactif pour trouver seuils HSV optimaux
    Affiche l'image avec trackbars pour ajuster H, S, V
    """
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    def nothing(x):
        pass
    
    # Creer fenetre avec trackbars
    cv2.namedWindow('Calibration HSV')
    cv2.createTrackbar('H Min', 'Calibration HSV', 0, 179, nothing)
    cv2.createTrackbar('H Max', 'Calibration HSV', 179, 179, nothing)
    cv2.createTrackbar('S Min', 'Calibration HSV', 0, 255, nothing)
    cv2.createTrackbar('S Max', 'Calibration HSV', 255, 255, nothing)
    cv2.createTrackbar('V Min', 'Calibration HSV', 0, 255, nothing)
    cv2.createTrackbar('V Max', 'Calibration HSV', 255, 255, nothing)
    
    while True:
        # Lire trackbars
        h_min = cv2.getTrackbarPos('H Min', 'Calibration HSV')
        h_max = cv2.getTrackbarPos('H Max', 'Calibration HSV')
        s_min = cv2.getTrackbarPos('S Min', 'Calibration HSV')
        s_max = cv2.getTrackbarPos('S Max', 'Calibration HSV')
        v_min = cv2.getTrackbarPos('V Min', 'Calibration HSV')
        v_max = cv2.getTrackbarPos('V Max', 'Calibration HSV')
        
        # Creer masque
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        
        # Afficher
        cv2.imshow('Calibration HSV', result)
        
        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(f"\nSeuils trouves:")
            print(f"lower = np.array([{h_min}, {s_min}, {v_min}])")
            print(f"upper = np.array([{h_max}, {s_max}, {v_max}])")
            break
    
    cv2.destroyAllWindows()


# ========== TESTS ==========

def test_vision():
    """Test detection couleur avec camera"""
    import time
    
    print("\n=== TEST VISION ===\n")
    
    # Test 1 : Photo + detection
    print("[1/3] Capture et detection...")
    chemin = prendre_photo()
    couleur = detecter_couleur_image(chemin)
    print(f"✅ Couleur detectee: {couleur}\n")
    time.sleep(1)
    
    # Test 2 : Compter objets rouges
    print("[2/3] Comptage objets rouges...")
    nb_rouges = compter_objets_couleur(chemin, 'rouge')
    print(f"✅ Objets rouges: {nb_rouges}\n")
    time.sleep(1)
    
    # Test 3 : Toutes les couleurs
    print("[3/3] Detection toutes couleurs...")
    for nom_couleur in COULEURS_HSV.keys():
        nb = compter_objets_couleur(chemin, nom_couleur)
        if nb > 0:
            print(f"  - {nom_couleur}: {nb}")
    
    print("\n✅ Test termine\n")


if __name__ == "__main__":
    test_vision()
