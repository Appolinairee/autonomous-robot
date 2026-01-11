"""
Test du servo de direction pour diagnostiquer le blocage
"""

from lib.motors import servo_direction
import time

print("=== TEST SERVO DIRECTION ===\n")

# Test position centrale
print("1. Position centrale (90°)...")
servo_direction.angle = 90
time.sleep(2)

# Test rotation progressive vers la GAUCHE (diminution angle)
print("\n2. Test rotation vers la GAUCHE (90° -> 45°)...")
for angle in range(90, 45, -5):
    print(f"   Angle: {angle}°")
    try:
        servo_direction.angle = angle
        time.sleep(0.5)
    except Exception as e:
        print(f"   ❌ ERREUR à {angle}°: {e}")
        break

# Retour centre
servo_direction.angle = 90
time.sleep(2)

# Test rotation progressive vers la DROITE (augmentation angle)
print("\n3. Test rotation vers la DROITE (90° -> 135°)...")
for angle in range(90, 135, 5):
    print(f"   Angle: {angle}°")
    try:
        servo_direction.angle = angle
        time.sleep(0.5)
    except Exception as e:
        print(f"   ❌ ERREUR à {angle}°: {e}")
        break

# Retour centre
servo_direction.angle = 90
time.sleep(1)

# Test des limites extrêmes
print("\n4. Test des LIMITES EXTRÊMES...")
angles_test = [0, 30, 60, 90, 120, 150, 180]
for angle in angles_test:
    print(f"   Test angle {angle}°...")
    try:
        servo_direction.angle = angle
        time.sleep(1.5)
        reponse = input(f"   Le servo a-t-il atteint {angle}° sans bloquer? (o/n): ")
        if reponse.lower() != 'o':
            print(f"   ⚠️ PROBLÈME détecté à {angle}°")
    except Exception as e:
        print(f"   ❌ ERREUR à {angle}°: {e}")

# Retour position neutre
servo_direction.angle = 90
print("\n✅ Test terminé - Servo en position neutre (90°)")
