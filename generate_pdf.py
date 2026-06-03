from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

BASE_DIR = Path(__file__).parent
MESSAGE_PATH = BASE_DIR / "outputs" / "daily_message.txt"
PDF_PATH = BASE_DIR / "outputs" / "daily_report.pdf"

def main():
    if not MESSAGE_PATH.exists():
        raise FileNotFoundError("找不到 outputs/daily_message.txt，請先執行 generate_report.py")

    text = MESSAGE_PATH.read_text(encoding="utf-8")
    font_name = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))

    doc = SimpleDocTemplate(str(PDF_PATH), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleCJK", parent=styles["Title"], fontName=font_name, fontSize=20, leading=26, spaceAfter=18)
    body_style = ParagraphStyle("BodyCJK", parent=styles["BodyText"], fontName=font_name, fontSize=12, leading=18, spaceAfter=8)

    story = [Paragraph("SleepSense 每日睡眠環境報告", title_style), Spacer(1, 8)]
    for line in text.splitlines():
        if line.strip() == "":
            story.append(Spacer(1, 8))
        else:
            safe = line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            story.append(Paragraph(safe, body_style))

    PDF_PATH.parent.mkdir(exist_ok=True)
    doc.build(story)
    print(f"PDF 已產生：{PDF_PATH}")

if __name__ == "__main__":
    main()
