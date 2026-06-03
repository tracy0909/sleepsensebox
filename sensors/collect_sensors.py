import json
from datetime import datetime
from pathlib import Path
from statistics import mean
from time import sleep

import board
import adafruit_dht
from gpiozero import DigitalInputDevice, DistanceSensor, LED

from config import (
    GREEN_LED_PIN,
    YELLOW_LED_PIN,
    RED_LED_PIN,
    LIGHT_PIN,
    PIR_PIN,
    HCSR04_TRIG_PIN,
    HCSR04_ECHO_PIN,
    COLLECT_SECONDS,
    DISTANCE_CHANGE_THRESHOLD_CM,
    MIN_VALID_DISTANCE_CM,
    MAX_VALID_DISTANCE_CM,
    FALLBACK_TEMPERATURE,
    FALLBACK_HUMIDITY,
)

BASE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = BASE_DIR / "reports" / "sleep_report.json"

def read_dht():
    dht_device = adafruit_dht.DHT11(board.D26)
    values = []

    for _ in range(5):
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature is not None and humidity is not None:
                values.append((float(temperature), float(humidity)))
        except RuntimeError:
            pass
        sleep(1)

    dht_device.exit()

    if not values:
        return FALLBACK_TEMPERATURE, FALLBACK_HUMIDITY

    temperatures = [v[0] for v in values]
    humidities = [v[1] for v in values]

    return round(mean(temperatures), 1), round(mean(humidities), 1)

def calculate_score(summary):
    score = 100

    if summary["temperature_avg"] > 28:
        score -= 10
    if summary["humidity_avg"] > 70:
        score -= 8

    score -= summary["pir_motion_events"] * 3
    score -= summary["light_events"] * 4
    score -= summary["distance_change_events"] * 5

    return max(score, 0)

def set_status_leds(score):
    green = LED(GREEN_LED_PIN)
    yellow = LED(YELLOW_LED_PIN)
    red = LED(RED_LED_PIN)

    green.off()
    yellow.off()
    red.off()

    if score >= 80:
        green.on()
    elif score >= 60:
        yellow.on()
    else:
        red.on()

def valid_distance_cm(value):
    return MIN_VALID_DISTANCE_CM <= value <= MAX_VALID_DISTANCE_CM

def main():
    print(f"Collecting sensor data for {COLLECT_SECONDS} seconds...")

    light = DigitalInputDevice(LIGHT_PIN)
    pir = DigitalInputDevice(PIR_PIN)
    distance_sensor = DistanceSensor(
        echo=HCSR04_ECHO_PIN,
        trigger=HCSR04_TRIG_PIN,
        max_distance=4
    )

    temperature_avg, humidity_avg = read_dht()

    light_events = 0
    pir_motion_events = 0
    distance_change_events = 0

    last_light = light.value
    last_pir = pir.value
    last_distance = None
    distance_values = []

    for _ in range(COLLECT_SECONDS):
        current_light = light.value
        if current_light != last_light:
            light_events += 1
            last_light = current_light

        current_pir = pir.value
        if last_pir == 0 and current_pir == 1:
            pir_motion_events += 1
        last_pir = current_pir

        try:
            distance_cm = round(distance_sensor.distance * 100, 1)
            if valid_distance_cm(distance_cm):
                distance_values.append(distance_cm)

                if last_distance is not None:
                    if abs(distance_cm - last_distance) >= DISTANCE_CHANGE_THRESHOLD_CM:
                        distance_change_events += 1

                last_distance = distance_cm
        except Exception:
            pass

        sleep(1)

    if distance_values:
        distance_avg_cm = round(mean(distance_values), 1)
        distance_min_cm = round(min(distance_values), 1)
        distance_max_cm = round(max(distance_values), 1)
    else:
        distance_avg_cm = None
        distance_min_cm = None
        distance_max_cm = None

    summary = {
        "temperature_avg": temperature_avg,
        "humidity_avg": humidity_avg,
        "pir_motion_events": pir_motion_events,
        "light_events": light_events,
        "light_current_state": light.value,
        "distance_change_events": distance_change_events,
        "distance_avg_cm": distance_avg_cm,
        "distance_min_cm": distance_min_cm,
        "distance_max_cm": distance_max_cm,
    }

    score = calculate_score(summary)
    set_status_leds(score)

    top_causes = []
    if temperature_avg >= 28:
        top_causes.append("temperature_high")
    if humidity_avg >= 70:
        top_causes.append("humidity_high")
    if pir_motion_events > 0:
        top_causes.append("motion_detected")
    if light_events > 0:
        top_causes.append("light_change")
    if distance_change_events > 0:
        top_causes.append("distance_change")

    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sleep_environment_score": score,
        "summary": summary,
        "top_causes": top_causes[:3],
    }

    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"已輸出到：{REPORT_PATH}")

if __name__ == "__main__":
    main()
