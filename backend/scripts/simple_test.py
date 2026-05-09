#!/usr/bin/env python3
"""Simple test with basic text PDF"""

import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Login to get token
login_data = {
    "email": "supportadmin@policylens.in",
    "password": "admin123"
}

login_response = requests.post("http://localhost:8000/api/v1/admin/login", json=login_data)
if login_response.status_code != 200:
    print(f"Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["access_token"]
print(f"✅ Login successful")

# Create a proper PDF using ReportLab
buffer = io.BytesIO()
p = canvas.Canvas(buffer, pagesize=letter)

# Add sufficient text content
p.setFont("Helvetica", 16)
p.drawString(100, 750, "National Dental Health Scheme 2024")
p.setFont("Helvetica", 12)
p.drawString(100, 720, "Scheme Code: NDHS-2024")
p.drawString(100, 700, "Type: National Scheme")
p.drawString(100, 680, "Ministry: Ministry of Health and Family Welfare")

p.drawString(100, 640, "Eligibility Criteria:")
p.drawString(120, 620, "• Age: 18 to 65 years")
p.drawString(120, 600, "• Annual family income below INR 3,00,000")
p.drawString(120, 580, "• Must belong to BPL or SC/ST category")
p.drawString(120, 560, "• Residential requirement: Indian citizen")
p.drawString(120, 540, "• No existing dental insurance coverage")

p.drawString(100, 500, "Benefits:")
p.drawString(120, 480, "• Free dental check-up twice a year")
p.drawString(120, 460, "• 50% discount on dental treatments")
p.drawString(120, 440, "• Coverage up to INR 10,000 per year")
p.drawString(120, 420, "• Free dental hygiene products")

p.drawString(100, 380, "Required Documents:")
p.drawString(120, 360, "• Aadhaar card")
p.drawString(120, 340, "• Income certificate")
p.drawString(120, 320, "• BPL/SC/ST certificate")
p.drawString(120, 300, "• Address proof")

p.save()

pdf_content = buffer.getvalue()
buffer.close()

# Test PDF upload
headers = {
    "Authorization": f"Bearer {token}"
}

files = {
    "file": ("dental_scheme.pdf", pdf_content, "application/pdf")
}

print("📤 Uploading PDF...")
upload_response = requests.post("http://localhost:8000/api/v1/admin/schemes/upload-pdf", headers=headers, files=files)

if upload_response.status_code != 200:
    print(f"❌ Upload failed: {upload_response.text}")
    exit(1)

upload_data = upload_response.json()
file_id = upload_data["file_id"]
print(f"✅ PDF uploaded successfully, file_id: {file_id}")

# Test extraction
extract_data = {
    "file_id": file_id
}

print("🔍 Extracting content from PDF...")
extract_response = requests.post("http://localhost:8000/api/v1/admin/schemes/extract-from-pdf", headers=headers, data=extract_data)

if extract_response.status_code != 200:
    print(f"❌ Extraction failed: {extract_response.text}")
    exit(1)

extracted = extract_response.json()
print("✅ Content extracted successfully!")
print(f"   Name: {extracted.get('name', 'N/A')}")
print(f"   Code: {extracted.get('code', 'N/A')}")
print(f"   Type: {extracted.get('type', 'N/A')}")

print("\n🎉 PDF upload and extraction flow working correctly!")
