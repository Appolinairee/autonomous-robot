from gpiozero import DistanceSensor, LED, TonalBuzzer
from time import sleep

led2 = LED(25)
led3 = LED(11)

sensor = DistanceSensor(echo=24, trigger=23, max_distance=2)

tb = TonalBuzzer(18)

while True:
    distance = (sensor.distance)*100

    if distance <= 5:
        tb.play("C4")
        led2.on()
        led3.on()
    else:
        tb.stop()
        led2.off()
        led3.off()
        
    print("%.2f cm" % distance)
    sleep(0.5)