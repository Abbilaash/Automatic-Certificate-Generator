from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
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
    result = None
    if request.method == 'POST':
        key = request.form['certificate_key']
        with open('certificates/data.json', 'r') as file:
            data = json.load(file)
            print(data)
            for entry in data:
                #data[entry] = json.loads(entry)
                entry = data[entry]
                if entry['cert_key'] == key:
                    result = {'name': entry['name'], 'key': key}
                    break
    return render_template('verify.html', result=result)



def generate_certificate_pdf(image_path, name, cert_key, output_pdf_path):
    try:
        # Load the PNG image
        image = Image.open(image_path)
        width, height = image.size

        pdfmetrics.registerFont(TTFont('Tangerine', 'Tangerine-Regular.ttf'))

        name_font_size = 30
        name_font_name = "Tangerine"
        cert_key_font_size = 12
        cert_key_font_name = "Helvetica"
        
        # Create a buffer to hold the PDF data
        buffer = io.BytesIO()
        
        # Create a canvas for the PDF
        c = canvas.Canvas(buffer, pagesize=(width, height))
        
        # Draw the PNG image onto the canvas
        c.drawImage(image_path, 0, 0, width=width, height=height)
        
        # Set font and size for the text
        c.setFont(name_font_name, name_font_size)
        
        name_y = 300
        cert_key_x, cert_key_y = 100, 10

        # Calculate the width of the name text
        name_text_width = c.stringWidth(name, name_font_name, name_font_size)

        # Define the area where you want to center the name text
        center_area_x_start = 0  # Starting x-coordinate of the area
        center_area_x_end = width  # Ending x-coordinate of the area
        center_area_width = center_area_x_end - center_area_x_start  # Width of the area

        # Calculate the starting x-coordinate to center the name text
        name_x = center_area_x_start + (center_area_width - name_text_width) / 2

        # Draw the name onto the canvas
        c.drawString(name_x, name_y, name)

        # Set font and size for the certificate key text
        c.setFont(cert_key_font_name, cert_key_font_size)

        # Calculate the width of the certificate key text
        cert_key_text_width = c.stringWidth(cert_key, cert_key_font_name, cert_key_font_size)

        # Calculate the x-coordinate to place the certificate key at the right edge
        cert_key_x = width - cert_key_text_width - 10  # 10 units padding from the right edge

        # Calculate the y-coordinate to place the certificate key at the bottom edge
        cert_key_y = 25  # 10 units padding from the bottom edge

        # Draw the certificate key onto the canvas
        c.drawString(cert_key_x, cert_key_y, f"{cert_key}")

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