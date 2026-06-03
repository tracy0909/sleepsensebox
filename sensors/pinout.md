# SleepSense Box Final 接線表

以下全部使用 Raspberry Pi **BCM 編號**。

## GPIO 總表

| 元件 | GPIO / 接法 | 實體腳位 |
|---|---:|---:|
| 綠燈 LED | GPIO2 | Pin 3 |
| 黃燈 LED | GPIO27 | Pin 13 |
| 紅燈 LED | GPIO22 | Pin 15 |
| DHT11 / DHT22 DATA | GPIO26 | Pin 37 |
| PIR OUT | GPIO23 | Pin 16 |
| 光敏電阻 DO | GPIO17 | Pin 11 |
| HC-SR04 Trig | GPIO24 | Pin 18 |
| HC-SR04 Echo | GPIO25，必須分壓 | Pin 22 |
| 光敏電阻 AO | 不接 | 不使用 |
| 麥克風 | 已移除 | 不使用 |
| Camera | 已移除 | 不使用 |
| 繼電器 | 已移除 | 不使用 |

---

# 1. 三色 LED

## 綠燈 GPIO2

```text
GPIO2 → 220Ω 電阻 → 綠燈長腳
綠燈短腳 → GND
```

意義：
- 環境良好時亮綠燈。

## 黃燈 GPIO27

```text
GPIO27 → 220Ω 電阻 → 黃燈長腳
黃燈短腳 → GND
```

意義：
- 環境需要注意時亮黃燈。

## 紅燈 GPIO22

```text
GPIO22 → 220Ω 電阻 → 紅燈長腳
紅燈短腳 → GND
```

意義：
- 環境較差時亮紅燈。

---

# 2. DHT11 / DHT22 溫濕度 GPIO26

| DHT 感測器 | Raspberry Pi |
|---|---|
| VCC / + | 3.3V 或 5V |
| DATA / OUT | GPIO26 |
| GND / - | GND |

意義：
- 偵測房間是否太熱。
- 偵測房間是否太潮濕。
- 用來計算睡眠環境分數。

---

# 3. PIR 人體紅外線 GPIO23

| PIR HC-SR501 | Raspberry Pi |
|---|---|
| VCC | 5V |
| OUT | GPIO23 |
| GND | GND |

意義：
- 偵測夜間活動事件。
- 例如半夜起身、房間有人走動、床邊活動。
- 不適合判斷靜止不動的人。

---

# 4. 光敏電阻模組 DO GPIO17

| 光敏電阻模組 | Raspberry Pi |
|---|---|
| VCC | 3.3V |
| GND | GND |
| DO | GPIO17 |
| AO | 不接 |

意義：
- 偵測夜間光線變化。
- 例如開燈、手機螢幕、窗外車燈。
- Raspberry Pi 沒有類比輸入，所以 AO 不接，不需要 MCP3008。

---

# 5. HC-SR04 超音波

| HC-SR04 | Raspberry Pi |
|---|---|
| VCC | 5V |
| GND | GND |
| Trig | GPIO24 |
| Echo | 分壓後接 GPIO25 |

意義：
- 偵測床邊距離變化。
- 可用來判斷可能起身、離床、床邊有人靠近、或大幅移動。

## Echo 一定要分壓

HC-SR04 Echo 是 5V，Raspberry Pi GPIO 只能接受 3.3V。  
Echo 不能直接接 GPIO25。

分壓接法：

```text
HC-SR04 Echo --- R1 ---+--- GPIO25
                       |
                       R2
                       |
                      GND
```

建議：

```text
R1 = 1kΩ
R2 = 2kΩ
```

意思：

```text
Echo 先接 1kΩ
1kΩ 和 2kΩ 中間那個點接 GPIO25
2kΩ 另一端接 GND
```

---

# 6. 本版移除的項目

- 麥克風：不偵測分貝。
- Camera：不用拍照，避免隱私問題。
- 繼電器：不控制外部設備。
- 光敏 AO：不接。
- MCP3008：不需要。
