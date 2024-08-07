from flask import Blueprint, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    name = request.form.get('name')
    buffer = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Draw text
    c.drawString(100, height - 100, f"Certificate of Achievement")
    c.drawString(100, height - 150, f"This certificate is awarded to {name}")
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='certificate.pdf', mimetype='application/pdf')
