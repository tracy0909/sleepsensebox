from gpiozero import DistanceSensor
from time import sleep
from config import HCSR04_TRIG_PIN, HCSR04_ECHO_PIN

sensor = DistanceSensor(
    echo=HCSR04_ECHO_PIN,
    trigger=HCSR04_TRIG_PIN,
    max_distance=4
)

print("Testing HC-SR04")
print(f"TRIG = GPIO{HCSR04_TRIG_PIN}")
print(f"ECHO = GPIO{HCSR04_ECHO_PIN}")
print("Move your hand closer/farther from the sensor.")
print("Press Ctrl+C to stop")

try:
    while True:
        distance_cm = sensor.distance * 100
        print(f"distance: {distance_cm:.1f} cm")
        sleep(1)
except KeyboardInterrupt:
    print("Stopped")
