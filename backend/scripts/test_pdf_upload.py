#!/usr/bin/env python3
"""Test PDF upload and extraction flow"""

import requests
import json

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
print(f"✅ Login successful, token: {token[:20]}...")

# Test PDF upload
headers = {
    "Authorization": f"Bearer {token}"
}

# Create a simple test PDF content
pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Sample PDF Content) Tj\nET\nendstream\nendobj\n\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000174 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n299\n%%EOF"

files = {
    "file": ("test.pdf", pdf_content, "application/pdf")
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
print(f"   Eligibility: {extracted.get('eligibility_criteria', 'N/A')[:100]}...")

print("\n🎉 PDF upload and extraction flow working correctly!")
