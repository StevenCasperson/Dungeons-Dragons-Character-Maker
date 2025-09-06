import io
from flask import Blueprint, session, send_file, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

bp = Blueprint("download", __name__)

@bp.route("/download/json")
def download_json():
    data = {
        "stats": session.get("adjusted_stats", session.get("stats")),
        "race": session.get("race"),
        "class": session.get("class"),
        "equipment": list(session.get("equipment", {}).keys()),
    }
    if not data["stats"]:
        return redirect(url_for("characters.step1_abilities"))
    return data  # auto-JSONified

@bp.route("/download/pdf")
def download_pdf():
    stats = session.get("adjusted_stats", session.get("stats"))
    if not stats:
        return redirect(url_for("characters.step1_abilities"))

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    x, y = 100, 750

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "D&D Character Overview")
    c.setFont("Helvetica", 12)
    y -= 40

    for key, value in stats.items():
        c.drawString(x, y, f"{key.title()}: {value}")
        y -= 20

    for field in ("race", "class"):
        val = session.get(field)
        if val:
            c.drawString(x, y, f"{field.title()}: {val}")
            y -= 20

    gear = [k for k, v in session.get("equipment", {}).items() if v]
    if gear:
        c.drawString(x, y, "Equipment: " + ", ".join(gear))
        y -= 20

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="character_overview.pdf",
        mimetype="application/pdf"
    )
