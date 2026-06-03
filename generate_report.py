import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
REPORT_PATH = BASE_DIR / "reports" / "sleep_report.json"
OUTPUT_PATH = BASE_DIR / "outputs" / "daily_message.txt"

def main():
    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    score = data.get("sleep_environment_score", 0)
    s = data.get("summary", {})

    temp = s.get("temperature_avg", 0)
    hum = s.get("humidity_avg", 0)
    motion = s.get("pir_motion_events", 0)
    light_events = s.get("light_events", 0)
    distance_events = s.get("distance_change_events", 0)
    distance_avg = s.get("distance_avg_cm", None)

    factors = []
    tips = []

    if temp >= 28:
        factors.append("房間溫度偏高，可能讓睡眠環境較悶熱。")
        tips.append("睡前先通風，或用風扇讓房間保持涼爽。")

    if hum >= 70:
        factors.append("濕度偏高，房間可能較潮濕。")
        tips.append("可以使用除濕機或保持空氣流通。")

    if motion > 0:
        factors.append(f"偵測到 {motion} 次夜間活動事件。")
        tips.append("睡前整理床邊環境，減少半夜起身或走動干擾。")

    if light_events > 0:
        factors.append(f"偵測到 {light_events} 次光線變化。")
        tips.append("睡前關閉不必要光源，或使用遮光窗簾。")

    if distance_events > 0:
        if distance_avg is not None:
            factors.append(f"偵測到 {distance_events} 次床邊距離變化，平均距離約 {distance_avg:.1f} 公分。")
        else:
            factors.append(f"偵測到 {distance_events} 次床邊距離變化。")
        tips.append("可以觀察是否與翻身、起身或床邊活動有關。")

    factors = factors[:3] or ["昨晚睡眠環境整體穩定。"]
    tips = tips[:3] or ["維持目前睡眠環境，持續觀察變化。"]

    while len(factors) < 3:
        factors.append("沒有明顯額外干擾。")
    while len(tips) < 3:
        tips.append("保持固定睡前習慣，讓環境更穩定。")

    msg = f"""早安 TC🌙

昨晚睡眠環境分數：{score} / 100

主要影響因素：
1. {factors[0]}
2. {factors[1]}
3. {factors[2]}

今日建議：
- {tips[0]}
- {tips[1]}
- {tips[2]}

推薦內容：
📖 觀察床邊距離變化與夜間活動
連結：https://example.com/distance
"""
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(msg, encoding="utf-8")
    print(msg)
    print(f"已輸出到：{OUTPUT_PATH}")

if __name__ == "__main__":
    main()
