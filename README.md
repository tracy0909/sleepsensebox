# SleepSense Box - Final HC-SR04 版本

這是目前正式整合版，包含：

- 綠燈 LED：GPIO2
- 黃燈 LED：GPIO27
- 紅燈 LED：GPIO22
- DHT11 / DHT22 溫濕度：GPIO26
- PIR 人體紅外線：GPIO23
- 光敏電阻 DO：GPIO17
- HC-SR04 Trig：GPIO24
- HC-SR04 Echo：GPIO25，需要分壓
- ntfy 手機通知
- PDF 每日報告

已移除：

- 麥克風
- Camera
- 繼電器
- 光敏電阻 AO
- MCP3008

---

## 1. 安裝套件

```bash
cd ~/Documents/project/sleepsense-box-final
conda activate openclaw
pip install -r requirements.txt
```

---

## 2. 設定 ntfy

請把 topic 換成你手機 ntfy App 訂閱的 topic。

```bash
echo NTFY_TOPIC=sleepsense-tc-2026 > .env
echo NTFY_SERVER=https://ntfy.sh >> .env
```

---

## 3. 測試各元件

### LED

```bash
python sensors/test_leds.py
```

### PIR + 光敏電阻 DO

```bash
python sensors/test_gpio_inputs.py
```

### DHT 溫濕度

```bash
python sensors/test_dht.py
```

如果你用 DHT22，請把 `sensors/test_dht.py` 和 `sensors/collect_sensors.py` 裡的 `DHT11` 改成 `DHT22`。

### HC-SR04 超音波

```bash
python sensors/test_hcsr04.py
```

---

## 4. 正式執行每日報告

```bash
chmod +x run_daily_report.sh
./run_daily_report.sh
```

流程：

1. 收集感測器資料
2. 產生 `reports/sleep_report.json`
3. 產生 `outputs/daily_message.txt`
4. 產生 `outputs/daily_report.pdf`
5. 發送 ntfy 手機通知與 PDF 附件

---

## 5. 接線

請看：

```text
sensors/pinout.md
```
