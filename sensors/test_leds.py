from gpiozero import LED
from time import sleep
from config import GREEN_LED_PIN, YELLOW_LED_PIN, RED_LED_PIN

green = LED(GREEN_LED_PIN)
yellow = LED(YELLOW_LED_PIN)
red = LED(RED_LED_PIN)

print("Testing LEDs: green GPIO2, yellow GPIO27, red GPIO22")
print("Press Ctrl+C to stop")

try:
    while True:
        green.on(); yellow.off(); red.off()
        print("green on")
        sleep(1)

        green.off(); yellow.on(); red.off()
        print("yellow on")
        sleep(1)

        green.off(); yellow.off(); red.on()
        print("red on")
        sleep(1)

        green.off(); yellow.off(); red.off()
        sleep(1)
except KeyboardInterrupt:
    green.off(); yellow.off(); red.off()
    print("Stopped")
