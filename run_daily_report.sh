#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "$HOME/miniforge3/etc/profile.d/conda.sh" ]; then
  source "$HOME/miniforge3/etc/profile.d/conda.sh"
  conda activate openclaw
fi

python sensors/collect_sensors.py
python generate_report.py
python generate_pdf.py
python send_ntfy.py

echo "SleepSense daily report complete"
echo "Text: outputs/daily_message.txt"
echo "PDF: outputs/daily_report.pdf"
