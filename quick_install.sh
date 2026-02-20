#!/bin/bash
#
# COPY-PASTE LANGSUNG KE VPS ANDA
# Script ini akan create semua file yang diperlukan
#

echo "Installing BPJS Login Script..."

# Create directory
mkdir -p ~/bpjs-login
cd ~/bpjs-login

# Create requirements.txt
cat > requirements.txt << 'EOF'
requests>=2.31.0
pyjwt>=2.10.1
EOF

echo "✓ requirements.txt created"

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt --user

echo "✓ Dependencies installed"

# Create bpjs_login.py - File sudah ada di /app/backend/bpjs_login.py
# Silakan copy isi file tersebut atau download dari GitHub

echo ""
echo "============================================"
echo "✓ Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Copy bpjs_login.py to this directory"
echo "2. Run: python3 bpjs_login.py"
echo ""
echo "Location: ~/bpjs-login"
echo ""
