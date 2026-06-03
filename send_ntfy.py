import os
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
MESSAGE_PATH = BASE_DIR / "outputs" / "daily_message.txt"
PDF_PATH = BASE_DIR / "outputs" / "daily_report.pdf"

load_dotenv(BASE_DIR / ".env")
NTFY_SERVER = os.getenv("NTFY_SERVER", "https://ntfy.sh").rstrip("/")
NTFY_TOPIC = os.getenv("NTFY_TOPIC")

def main():
    if not NTFY_TOPIC:
        raise RuntimeError("請在 .env 設定 NTFY_TOPIC，例如 NTFY_TOPIC=sleepsense-tc-2026")
    if not MESSAGE_PATH.exists():
        raise FileNotFoundError("找不到 outputs/daily_message.txt，請先執行 generate_report.py")

    url = f"{NTFY_SERVER}/{NTFY_TOPIC}"
    message = MESSAGE_PATH.read_text(encoding="utf-8")

    r = requests.post(
        url,
        data=message.encode("utf-8"),
        headers={"Title":"SleepSense Report", "Tags":"bed,ruler", "Priority":"default"},
        timeout=30,
    )
    r.raise_for_status()
    print("ntfy 文字通知已送出")

    if PDF_PATH.exists():
        with PDF_PATH.open("rb") as f:
            r = requests.put(
                url,
                data=f,
                headers={"Title":"SleepSense PDF", "Filename":"daily_report.pdf", "Tags":"page_facing_up"},
                timeout=60,
            )
        r.raise_for_status()
        print("ntfy PDF 附件已送出")

if __name__ == "__main__":
    main()
