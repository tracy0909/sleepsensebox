from gpiozero import DigitalInputDevice
from time import sleep
from config import LIGHT_PIN, PIR_PIN

light = DigitalInputDevice(LIGHT_PIN)
pir = DigitalInputDevice(PIR_PIN)

print("Testing light sensor DO on GPIO17 and PIR on GPIO23")
print("Press Ctrl+C to stop")

try:
    while True:
        print({
            "light_value": light.value,
            "pir_motion": pir.value,
        })
        sleep(1)
except KeyboardInterrupt:
    print("Stopped")
