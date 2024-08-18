# CertifyMe - Automatic Certificate Generator
CertifyMe is a Python Flask web application that generates personalized certificates from a template image and a JSON file containing participant details. The generated certificates can be downloaded as a ZIP file. Additionally, the application provides a certificate verification feature where users can enter a certificate key to verify its authenticity.

## Features
- Automatic Certificate Generation: Upload a JSON file with participant names and certificate keys, and generate personalized certificates in PDF format.
- Certificate Verification: Verify the authenticity of certificates by entering a unique certificate key.
- Responsive and Funky Design: A visually appealing and responsive design using Bootstrap and custom CSS.
- ZIP Download: Download all generated certificates in a single ZIP file.

## Installation
1. Clone the repository
   ```
   git clone https://github.com/Abbilaash/Automatic-Certificate-Generator.git
   cd Automatic-Certificate-Generator
   ```
2. Create and activate the virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the dependencies
   ```
   pip install -r requirements.txt
   ```
4. Run the flask app
   ```
   python run.py
   ```
5. Access the application
   ```
   http://127.0.0.1:5000
   ```

## Usage
### 1. Certificate Generation
- Upload the JSON file with participant names and certificate keys.
- The application will generate a personalized certificate for each participant.
- All generated certificates will be available for download as a ZIP file.

## 2. Certicate Verification
- Enter a certificate key on the verification page.
- The application will display the participant's name and key if the certificate is valid.
