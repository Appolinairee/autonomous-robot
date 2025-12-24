from gpiozero import LED, TonalBuzzer

led1 = LED(9)
led2 = LED(25)
led3 = LED(11)

tb = TonalBuzzer(18)

led2.blink(on_time=1, off_time=1)
led3.blink(on_time=1, off_time=2)

# import RPi.GPIO as GPIO
# import time as t

# GPIO.setmode(GPIO.BCM)

# GPIO.setup(9, GPIO.OUT)
# GPIO.setup(25, GPIO.OUT)
# GPIO.setup(11, GPIO.OUT)

# while True :
#     GPIO.output(25, 1)
#     GPIO.output(11, 0)
#     t.sleep(1)

#     GPIO.output(25, 0)
#     GPIO.output(11, 1)
#     t.sleep(1)

#     GPIO.output(25, 1)
#     GPIO.output(11, 1)
#     t.sleep(2)

#     GPIO.output(25, 0)
#     GPIO.output(11, 0)
#     t.sleep(1)