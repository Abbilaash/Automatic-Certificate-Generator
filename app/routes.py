from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import io
import json
import zipfile
import os

main = Blueprint('main', __name__)

# Fixed image file name and directory for certificates
IMAGE_PATH = 'certificate.png'
CERTIFICATES_DIR = 'certificates'

CERTIFICATES = {}

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        if 'data' not in request.files:
            flash('No data file part', 'error')
            return redirect(request.url)
        
        data_file = request.files['data']
        
        # Ensure the certificates directory exists
        if not os.path.exists(CERTIFICATES_DIR):
            os.makedirs(CERTIFICATES_DIR)
        
        # Save uploaded data file
        data_path = os.path.join(CERTIFICATES_DIR, 'data.json')
        data_file.save(data_path)
        
        # Load data
        with open(data_path) as f:
            data_dict = json.load(f)

        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            # Generate each certificate
            for item in data_dict:
                name = data_dict[item]['name']
                cert_key = data_dict[item]['cert_key']
                CERTIFICATES[cert_key] = name
                pdf_filename = f"{name.replace(' ', '_')}.pdf"
                output_pdf_path = os.path.join(CERTIFICATES_DIR, pdf_filename)
                generate_certificate_pdf(IMAGE_PATH, name, cert_key, output_pdf_path)
                zip_file.write(output_pdf_path, pdf_filename)
            
        zip_buffer.seek(0)
        
        return send_file(zip_buffer, mimetype='certificates/zip', as_attachment=True, download_name='certificates.zip')
    
    return render_template('index.html')

@main.route('/verify', methods=['GET', 'POST'])


def verify():
    if request.method == 'POST':
        cert_key = request.form.get('cert_key')
        name = CERTIFICATES.get(cert_key, 'Invalid Certificate')
        flash(f'Certificate Key: {cert_key}, Name: {name}', 'info')
        return redirect(url_for('main.verify'))





    
    return render_template('verify.html')

def generate_certificate_pdf(image_path, name, cert_key, output_pdf_path):
    try:
        # Load the PNG image
        image = Image.open(image_path)
        width, height = image.size
        
        # Create a buffer to hold the PDF data
        buffer = io.BytesIO()
        
        # Create a canvas for the PDF
        c = canvas.Canvas(buffer, pagesize=(width, height))
        
        # Draw the PNG image onto the canvas
        c.drawImage(image_path, 0, 0, width=width, height=height)
        
        # Set font and size for the text
        c.setFont("Helvetica", 12)
        
        # Example coordinates, adjust these based on your image layout
        name_x, name_y = 100, 400  # Coordinates for the name
        cert_key_x, cert_key_y = 100, 350  # Coordinates for the certificate key
        
        # Draw the name and certificate key onto the canvas
        c.drawString(name_x, name_y, f"Name: {name}")
        c.drawString(cert_key_x, cert_key_y, f"Certificate Key: {cert_key}")
        
        # Save the PDF to the buffer
        c.save()
        
        # Write the buffer data to the output PDF file
        buffer.seek(0)
        with open(output_pdf_path, 'wb') as f:
            f.write(buffer.read())
    
    except PermissionError:
        print(f"Permission denied while writing to {output_pdf_path}. Check the file path and permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")