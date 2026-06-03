import time
import board
import adafruit_dht

# GPIO26 對應 board.D26
# 如果你是 DHT22，請把 DHT11 改成 DHT22
dht_device = adafruit_dht.DHT11(board.D26)

print("Testing DHT11/DHT22 on GPIO26")
print("If you use DHT22, change DHT11 to DHT22 in this file.")
print("Press Ctrl+C to stop")

try:
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            print({"temperature": temperature, "humidity": humidity})
        except RuntimeError as e:
            print("Read error:", e)
        time.sleep(2)
except KeyboardInterrupt:
    dht_device.exit()
    print("Stopped")
