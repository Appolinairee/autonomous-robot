# 🤖 Electro-Robot

Projet de robot autonome sur Raspberry Pi avec manipulation d'objets et détection d'obstacles.

## 📂 Structure du projet

```
electro-robot/
├── capteurs/              # Tests individuels des composants
│   ├── test_leds.py      # Test LEDs et buzzer
│   ├── test_servos.py    # Test servomoteurs
│   └── test_ultrason.py  # Test capteur ultrason
└── projects/              # Projets complets
    ├── parcours_complet.py    # Parcours A→B avec manipulation
    └── drive_robot_old.py     # Ancienne version (archivée)
```

## 🔧 Composants utilisés

### Matériel
- **Raspberry Pi** (GPIO)
- **PCA9685** (contrôleur PWM I2C, adresse 0x5f)
- **2× Moteurs DC** (pins 12-15)
- **Servomoteurs** (bras, pince, direction)
- **Capteur ultrason HC-SR04** (Trigger: GPIO23, Echo: GPIO24)
- **LEDs** (GPIO 9, 25, 11)
- **Buzzer tonal** (GPIO 18)

### Bibliothèques Python
- `gpiozero` - Contrôle GPIO simplifié
- `adafruit-circuitpython-pca9685` - Contrôleur PWM
- `adafruit-circuitpython-motor` - Moteurs DC et servos
- `board`, `busio` - Communication I2C

## 🚀 Utilisation

### Tests unitaires des composants

```bash
# Tester les LEDs et le buzzer
python3 capteurs/test_leds.py

# Tester le capteur ultrason
python3 capteurs/test_ultrason.py

# Tester les servomoteurs
python3 capteurs/test_servos.py
```

### Projet complet

```bash
# Lancer le parcours A→B avec manipulation d'objet
python3 projects/parcours_complet.py
```

## 📋 Fonctionnalités

### Tests des capteurs (`capteurs/`)
- Clignotement de LEDs avec différents patterns
- Détection de distance avec alerte sonore/visuelle
- Contrôle de servomoteurs

### Projet principal (`parcours_complet.py`)
- ✅ Saisie d'objet au point A
- ✅ Déplacement avec détection d'obstacles
- ✅ Virage programmé
- ✅ Dépôt d'objet au point B
- ✅ Gestion des erreurs et interruptions

## ⚙️ Configuration

### Pins GPIO
```python
# Capteur ultrason
TRIGGER = 23
ECHO = 24

# LEDs
LED1 = 9
LED2 = 25
LED3 = 11

# Buzzer
BUZZER = 18
```

### PCA9685 (adresse I2C: 0x5f)
```python
# Moteurs
M1_IN1 = 15, M1_IN2 = 14
M2_IN1 = 12, M2_IN2 = 13

# Servos
SERVO_PILOTAGE = 0
SERVO_BRAS = 2
SERVO_PINCE = 4
```

## 🐛 Notes importantes

- **Interruption** : Utilisez `Ctrl+C` pour arrêter proprement
- **Calibration** : Ajustez les angles de servos selon votre montage
- **Distance de sécurité** : Par défaut 10 cm pour la détection d'obstacles

## 📝 Auteur

Projet Centrale - PLBD

---

**Date de dernière mise à jour** : Décembre 2025
