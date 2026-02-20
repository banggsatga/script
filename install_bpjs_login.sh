#!/bin/bash
#
# BPJS TKU Login Script Installer
# Install script Python untuk login ke BPJS Ketenagakerjaan
#
# Usage: curl -fsSL [URL] | bash
# Or: wget -qO- [URL] | bash
#

set -e

echo "=============================================================="
echo "  BPJS TKU Login Script Installer"
echo "=============================================================="
echo ""

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create directory
INSTALL_DIR="$HOME/bpjs-login"
echo -e "${YELLOW}[*]${NC} Creating installation directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Check Python
echo -e "${YELLOW}[*]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[✗]${NC} Python 3 not found. Please install Python 3 first."
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}[✓]${NC} Found: $PYTHON_VERSION"

# Check pip
echo -e "${YELLOW}[*]${NC} Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}[✗]${NC} pip3 not found. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    rm get-pip.py
fi
echo -e "${GREEN}[✓]${NC} pip3 is available"

# Create requirements.txt
echo -e "${YELLOW}[*]${NC} Creating requirements.txt..."
cat > requirements.txt << 'EOF'
requests>=2.31.0
pyjwt>=2.10.1
EOF
echo -e "${GREEN}[✓]${NC} requirements.txt created"

# Install dependencies
echo -e "${YELLOW}[*]${NC} Installing Python dependencies..."
pip3 install -r requirements.txt --user
echo -e "${GREEN}[✓]${NC} Dependencies installed"

# Create bpjs_login.py (Advanced version)
echo -e "${YELLOW}[*]${NC} Creating bpjs_login.py..."
cat > bpjs_login.py << 'EOFPYTHON'
#!/usr/bin/env python3
"""
BPJS TKU Login Script
Script untuk login ke aplikasi BPJS Ketenagakerjaan
"""

import requests
import json
import uuid
import platform
from datetime import datetime
from typing import Dict, Optional
import getpass
import os


class BPJSLoginClient:
    def __init__(self, base_url: str = None):
        """
        Initialize BPJS Login Client
        
        Args:
            base_url: Base URL API BPJS (jika kosong akan di-detect otomatis)
        """
        # Possible base URLs (bisa dicoba satu per satu)
        self.possible_urls = [
            "https://api.bpjsketenagakerjaan.go.id",
            "https://mobile-api.bpjsketenagakerjaan.go.id",
            "https://app.bpjsketenagakerjaan.go.id",
            "https://jamsostek-api.bpjsketenagakerjaan.go.id"
        ]
        
        self.base_url = base_url or self.possible_urls[0]
        self.session = requests.Session()
        
        # Set default headers (mirip dengan aplikasi mobile)
        self.session.headers.update({
            'User-Agent': 'Jamsostek-Mobile/Android',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-App-Version': '3.0.0',
            'X-Platform': 'Android'
        })
        
        self.tokens = {
            'access_token': None,
            'refresh_token': None
        }
        
        self.device_id = self._get_or_create_device_id()
    
    def _get_or_create_device_id(self) -> str:
        """
        Generate atau load device ID yang persistent
        """
        device_file = '.bpjs_device_id'
        
        if os.path.exists(device_file):
            with open(device_file, 'r') as f:
                return f.read().strip()
        else:
            # Generate device ID berdasarkan machine info
            machine_info = f"{platform.node()}-{platform.machine()}-{platform.system()}"
            device_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, machine_info))
            
            # Save untuk digunakan lagi
            with open(device_file, 'w') as f:
                f.write(device_id)
            
            return device_id
    
    def login(self, email: str, password: str, register_id: str = None) -> Dict:
        """
        Login ke BPJS TKU
        
        Args:
            email: Email pengguna
            password: Password pengguna
            register_id: NIK/Register ID (optional)
        
        Returns:
            Dict berisi access_token dan refresh_token
        """
        endpoint = f"{self.base_url}/login"
        
        payload = {
            "email": email,
            "password": password,
            "deviceId": self.device_id,
            "registerId": register_id
        }
        
        print(f"\n[*] Attempting login...")
        print(f"[*] Email: {email}")
        print(f"[*] Device ID: {self.device_id}")
        print(f"[*] Endpoint: {endpoint}")
        
        try:
            response = self.session.post(
                endpoint,
                json=payload,
                timeout=30
            )
            
            print(f"[*] Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract tokens
                self.tokens['access_token'] = data.get('accessToken')
                self.tokens['refresh_token'] = data.get('refreshToken')
                
                # Save tokens
                self._save_tokens()
                
                print(f"[✓] Login successful!")
                print(f"[✓] Access Token: {self.tokens['access_token'][:50]}...")
                print(f"[✓] Refresh Token: {self.tokens['refresh_token'][:50]}...")
                
                return data
            
            elif response.status_code == 401:
                print(f"[✗] Login failed: Invalid credentials")
                print(f"[✗] Response: {response.text}")
                return None
            
            else:
                print(f"[✗] Login failed with status {response.status_code}")
                print(f"[✗] Response: {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            print(f"[✗] Connection error. URL might be incorrect: {endpoint}")
            print(f"[!] Try another base URL from the list")
            return None
        
        except requests.exceptions.Timeout:
            print(f"[✗] Request timeout")
            return None
        
        except Exception as e:
            print(f"[✗] Error: {str(e)}")
            return None
    
    def refresh_access_token(self) -> Optional[Dict]:
        """
        Refresh access token menggunakan refresh token
        """
        if not self.tokens.get('refresh_token'):
            print("[✗] No refresh token available")
            return None
        
        endpoint = f"{self.base_url}/refresh-token"
        
        payload = {
            "refreshToken": self.tokens['refresh_token']
        }
        
        print(f"\n[*] Refreshing access token...")
        
        try:
            response = self.session.post(
                endpoint,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                self.tokens['access_token'] = data.get('accessToken')
                self.tokens['refresh_token'] = data.get('refreshToken')
                
                self._save_tokens()
                
                print(f"[✓] Token refreshed successfully!")
                return data
            
            else:
                print(f"[✗] Token refresh failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[✗] Error refreshing token: {str(e)}")
            return None
    
    def _save_tokens(self):
        """
        Save tokens ke file untuk digunakan lagi
        """
        token_file = '.bpjs_tokens.json'
        
        with open(token_file, 'w') as f:
            json.dump({
                'access_token': self.tokens['access_token'],
                'refresh_token': self.tokens['refresh_token'],
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"[✓] Tokens saved to {token_file}")
    
    def load_tokens(self) -> bool:
        """
        Load tokens dari file yang tersimpan
        """
        token_file = '.bpjs_tokens.json'
        
        if not os.path.exists(token_file):
            return False
        
        try:
            with open(token_file, 'r') as f:
                data = json.load(f)
                
            self.tokens['access_token'] = data.get('access_token')
            self.tokens['refresh_token'] = data.get('refresh_token')
            
            print(f"[✓] Tokens loaded from {token_file}")
            return True
        
        except Exception as e:
            print(f"[✗] Error loading tokens: {str(e)}")
            return False
    
    def make_authenticated_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Optional[Dict]:
        """
        Buat request dengan authentication header
        
        Args:
            endpoint: API endpoint (e.g., '/user/profile')
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request body (untuk POST/PUT)
        """
        if not self.tokens.get('access_token'):
            print("[✗] No access token. Please login first.")
            return None
        
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f"Bearer {self.tokens['access_token']}"
        }
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'PUT':
                response = self.session.put(url, headers=headers, json=data, timeout=30)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers, timeout=30)
            else:
                print(f"[✗] Unsupported method: {method}")
                return None
            
            # Handle token expired
            if response.status_code == 401:
                print("[!] Token expired. Attempting to refresh...")
                if self.refresh_access_token():
                    # Retry request dengan token baru
                    headers['Authorization'] = f"Bearer {self.tokens['access_token']}"
                    response = self.session.request(method, url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[✗] Request failed: {response.status_code}")
                print(f"[✗] Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[✗] Error: {str(e)}")
            return None
    
    def try_all_base_urls(self, email: str, password: str, register_id: str = None) -> Optional[Dict]:
        """
        Coba login dengan semua possible base URLs
        """
        print(f"\n[*] Trying all possible base URLs...")
        
        for url in self.possible_urls:
            print(f"\n[*] Trying: {url}")
            self.base_url = url
            
            result = self.login(email, password, register_id)
            
            if result:
                print(f"\n[✓] Successfully connected to: {url}")
                return result
        
        print(f"\n[✗] Failed to connect to any base URL")
        return None


def main():
    """
    Main function untuk menjalankan login script
    """
    print("=" * 60)
    print("BPJS TKU (Jamsostek Mobile) Login Script")
    print("=" * 60)
    
    # Input dari user
    email = input("\nEmail: ").strip()
    password = getpass.getpass("Password: ")
    register_id = input("NIK/Register ID (optional, press Enter to skip): ").strip() or None
    
    # Custom base URL (optional)
    print("\n[?] Use default base URL? (y/n)")
    use_default = input("Default: y > ").strip().lower() or 'y'
    
    base_url = None
    if use_default != 'y':
        base_url = input("Enter base URL: ").strip()
    
    # Create client
    client = BPJSLoginClient(base_url=base_url)
    
    # Cek apakah ada tokens tersimpan
    if client.load_tokens():
        print("\n[?] Found saved tokens. Try to use them? (y/n)")
        use_saved = input("Default: y > ").strip().lower() or 'y'
        
        if use_saved == 'y':
            print("\n[*] Using saved tokens. Testing with a request...")
            result = client.make_authenticated_request('/user/profile')
            
            if result:
                print("[✓] Saved tokens are valid!")
                print(json.dumps(result, indent=2))
                return
            else:
                print("[!] Saved tokens invalid or expired. Proceeding with login...")
    
    # Login
    print("\n[*] Attempting to login...")
    result = client.login(email, password, register_id)
    
    # Jika gagal, coba semua URLs
    if not result:
        print("\n[?] Try all possible base URLs? (y/n)")
        try_all = input("Default: n > ").strip().lower() or 'n'
        
        if try_all == 'y':
            result = client.try_all_base_urls(email, password, register_id)
    
    if result:
        print("\n" + "=" * 60)
        print("LOGIN SUCCESS!")
        print("=" * 60)
        print("\nTokens have been saved. You can use them for API requests.")
        print("\nExample usage:")
        print("  from bpjs_login import BPJSLoginClient")
        print("  client = BPJSLoginClient()")
        print("  client.load_tokens()")
        print("  data = client.make_authenticated_request('/endpoint')")
    else:
        print("\n" + "=" * 60)
        print("LOGIN FAILED")
        print("=" * 60)
        print("\nPossible reasons:")
        print("1. Invalid credentials")
        print("2. Incorrect base URL")
        print("3. Network connection issue")
        print("4. API endpoint changed")


if __name__ == "__main__":
    main()
EOFPYTHON

chmod +x bpjs_login.py
echo -e "${GREEN}[✓]${NC} bpjs_login.py created"

# Create simple_login.py
echo -e "${YELLOW}[*]${NC} Creating simple_login.py..."
cat > simple_login.py << 'EOFPYTHON2'
#!/usr/bin/env python3
"""
BPJS TKU Simple Login Script
"""

import requests
import uuid
import json
import sys


def simple_login(email: str, password: str, base_url: str = None):
    urls = [
        "https://api.bpjsketenagakerjaan.go.id",
        "https://mobile-api.bpjsketenagakerjaan.go.id", 
        "https://app.bpjsketenagakerjaan.go.id",
    ]
    
    if base_url:
        urls.insert(0, base_url)
    
    device_id = str(uuid.uuid4())
    
    payload = {
        "email": email,
        "password": password,
        "deviceId": device_id,
        "registerId": None
    }
    
    headers = {
        'User-Agent': 'Jamsostek-Mobile/Android',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    print(f"\nEmail: {email}")
    print(f"Device ID: {device_id}\n")
    
    for url in urls:
        endpoint = f"{url}/login"
        print(f"[*] Trying: {endpoint}")
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
            print(f"[*] Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✓ LOGIN SUCCESS!\n")
                print(f"Access Token: {data.get('accessToken', 'N/A')}")
                print(f"Refresh Token: {data.get('refreshToken', 'N/A')}")
                
                with open('bpjs_tokens.json', 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"\n[✓] Tokens saved to bpjs_tokens.json")
                return data
            
        except Exception as e:
            print(f"[✗] Error: {str(e)}")
    
    print(f"\n✗ LOGIN FAILED")
    return None


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        password = sys.argv[2]
        base_url = sys.argv[3] if len(sys.argv) > 3 else None
        simple_login(email, password, base_url)
    else:
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        simple_login(email, password)
EOFPYTHON2

chmod +x simple_login.py
echo -e "${GREEN}[✓]${NC} simple_login.py created"

# Create README
echo -e "${YELLOW}[*]${NC} Creating README.md..."
cat > README.md << 'EOFREADME'
# BPJS TKU Login Scripts

## Quick Start

### Simple Login:
```bash
python3 simple_login.py
```

### Advanced Login:
```bash
python3 bpjs_login.py
```

### Command Line:
```bash
python3 simple_login.py user@example.com mypassword
```

## Files:
- `bpjs_login.py` - Advanced login with token refresh
- `simple_login.py` - Simple quick login
- `requirements.txt` - Python dependencies
- `.bpjs_device_id` - Your device ID (auto-generated)
- `.bpjs_tokens.json` - Saved tokens

## Python Usage:
```python
from bpjs_login import BPJSLoginClient

client = BPJSLoginClient()
result = client.login("email@example.com", "password")

if result:
    # Make authenticated requests
    data = client.make_authenticated_request('/user/profile')
```
EOFREADME

echo -e "${GREEN}[✓]${NC} README.md created"

# Summary
echo ""
echo "=============================================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "=============================================================="
echo ""
echo "Location: $INSTALL_DIR"
echo ""
echo "Files created:"
echo "  ✓ bpjs_login.py      - Advanced login script"
echo "  ✓ simple_login.py    - Simple login script"
echo "  ✓ requirements.txt   - Dependencies"
echo "  ✓ README.md          - Documentation"
echo ""
echo "Quick start:"
echo "  cd $INSTALL_DIR"
echo "  python3 simple_login.py"
echo ""
echo "Or:"
echo "  cd $INSTALL_DIR"
echo "  python3 bpjs_login.py"
echo ""
echo "=============================================================="
