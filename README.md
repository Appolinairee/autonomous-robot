# Electro-Robot

Projet de robot autonome sur Raspberry Pi avec manipulation d'objets et détection d'obstacles.

## Composants utilisés

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