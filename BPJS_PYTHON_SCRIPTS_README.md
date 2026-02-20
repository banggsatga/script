# 🐍 BPJS TKU Login Python Scripts

Dua script Python untuk login ke aplikasi BPJS Ketenagakerjaan (Jamsostek Mobile).

---

## 📋 Dependencies

### Install Requirements
```bash
cd /app/backend
pip install -r requirements.txt
```

### Required Libraries
- `requests` - untuk HTTP requests (sudah ada di requirements.txt)
- `uuid` - generate device ID (built-in Python)
- `json` - handle JSON (built-in Python)
- `getpass` - secure password input (built-in Python)

**Semua dependencies sudah tersedia!** ✅

---

## 🚀 Cara Penggunaan

### Option 1: Script Lengkap (`bpjs_login.py`)

Script dengan fitur lengkap: token refresh, save/load tokens, auto-retry.

#### Command Line:
```bash
python bpjs_login.py
```

#### Interactive Mode:
```
Email: user@example.com
Password: ********
NIK/Register ID (optional): 1234567890
Use default base URL? (y/n) y
```

#### Programmatic Usage:
```python
from bpjs_login import BPJSLoginClient

# Create client
client = BPJSLoginClient()

# Login
result = client.login(
    email="user@example.com",
    password="mypassword",
    register_id="1234567890"  # Optional
)

if result:
    print("Login successful!")
    print(f"Access Token: {result['accessToken']}")
    print(f"Refresh Token: {result['refreshToken']}")
    
    # Make authenticated request
    profile = client.make_authenticated_request('/user/profile')
    print(profile)
    
    # Refresh token ketika expired
    client.refresh_access_token()
```

#### Load Saved Tokens:
```python
from bpjs_login import BPJSLoginClient

client = BPJSLoginClient()
client.load_tokens()  # Load dari .bpjs_tokens.json

# Use token untuk request
data = client.make_authenticated_request('/endpoint')
```

---

### Option 2: Simple Script (`simple_login.py`)

Script sederhana untuk quick testing.

#### Command Line:
```bash
# Interactive mode
python simple_login.py

# Direct mode
python simple_login.py user@example.com mypassword

# With custom base URL
python simple_login.py user@example.com mypassword https://api.bpjsketenagakerjaan.go.id
```

#### Programmatic Usage:
```python
from simple_login import simple_login

result = simple_login(
    email="user@example.com",
    password="mypassword",
    base_url="https://api.bpjsketenagakerjaan.go.id"  # Optional
)

if result:
    access_token = result['accessToken']
    refresh_token = result['refreshToken']
```

---

## 🔧 Fitur Script

### `bpjs_login.py` (Advanced)
✅ Auto-generate device ID (persistent)  
✅ Save/Load tokens ke file  
✅ Auto token refresh  
✅ Retry dengan multiple base URLs  
✅ Authenticated request helper  
✅ Error handling lengkap  

### `simple_login.py` (Basic)
✅ Quick login  
✅ Try multiple URLs  
✅ Save tokens ke JSON  
✅ Command line support  
✅ Minimal dependencies  

---

## 📁 Generated Files

### `.bpjs_device_id`
Device ID persistent (dibuat otomatis)
```
550e8400-e29b-41d4-a716-446655440000
```

### `.bpjs_tokens.json` atau `bpjs_tokens.json`
Tokens yang tersimpan
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "timestamp": "2025-02-20T12:00:00"
}
```

---

## 🌐 Base URLs

Script akan mencoba URLs berikut (secara otomatis):

1. `https://api.bpjsketenagakerjaan.go.id`
2. `https://mobile-api.bpjsketenagakerjaan.go.id`
3. `https://app.bpjsketenagakerjaan.go.id`
4. `https://jamsostek-api.bpjsketenagakerjaan.go.id`

**Note:** Base URL sebenarnya mungkin berbeda karena di-obfuscate di aplikasi.

---

## 📤 Request Format

### Login Request
```json
{
  "email": "user@example.com",
  "password": "mypassword",
  "deviceId": "550e8400-e29b-41d4-a716-446655440000",
  "registerId": "1234567890"
}
```

### Expected Response
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 🔍 Troubleshooting

### Error: Connection Failed
```
[✗] Connection error. URL might be incorrect
```
**Solution:** 
- Cek koneksi internet
- Coba base URL lain
- Pastikan tidak ada firewall blocking

### Error: Invalid Credentials (401)
```
[✗] Login failed: Invalid credentials
```
**Solution:**
- Periksa email dan password
- Pastikan akun aktif
- Coba login di aplikasi resmi dulu

### Error: Endpoint Not Found (404)
```
[!] Endpoint not found (wrong URL)
```
**Solution:**
- Base URL salah
- Endpoint `/login` mungkin berbeda
- Gunakan network sniffer untuk cari URL sebenarnya

### Error: Token Expired
```
[!] Token expired. Attempting to refresh...
```
**Solution:**
Script akan auto-refresh token. Jika gagal, login ulang.

---

## 🧪 Testing

### Test Login
```bash
cd /app/backend
python simple_login.py test@example.com testpassword
```

### Test dengan Multiple URLs
```python
from bpjs_login import BPJSLoginClient

client = BPJSLoginClient()
result = client.try_all_base_urls(
    email="user@example.com",
    password="mypassword"
)
```

---

## 🔒 Security Notes

1. **Password Storage**: Script tidak menyimpan password, hanya tokens
2. **Device ID**: Persistent device ID untuk security
3. **Token Expiration**: Auto-refresh saat expired
4. **HTTPS Only**: Semua requests menggunakan HTTPS

---

## 💡 Advanced Usage

### Custom Headers
```python
from bpjs_login import BPJSLoginClient

client = BPJSLoginClient()
client.session.headers.update({
    'X-Custom-Header': 'value',
    'X-Device-Model': 'Pixel 6'
})
```

### Use with Proxy
```python
import requests

client = BPJSLoginClient()
client.session.proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}
```

### Debug Mode
```python
import logging

logging.basicConfig(level=logging.DEBUG)

# Akan print semua HTTP requests
```

---

## 📞 API Endpoints Examples

Setelah login berhasil, gunakan tokens untuk akses endpoints lain:

```python
from bpjs_login import BPJSLoginClient

client = BPJSLoginClient()
client.load_tokens()

# Get user profile
profile = client.make_authenticated_request('/user/profile', method='GET')

# Update device token (push notification)
result = client.make_authenticated_request(
    '/user/device-token',
    method='POST',
    data={'deviceToken': 'firebase_token_here'}
)

# Get balance/saldo
balance = client.make_authenticated_request('/jht/balance', method='GET')
```

---

## 📚 Complete Example

```python
#!/usr/bin/env python3
"""
Complete example: Login and get user data
"""
from bpjs_login import BPJSLoginClient
import json

def main():
    # Initialize client
    client = BPJSLoginClient()
    
    # Try to load existing tokens
    if not client.load_tokens():
        print("No saved tokens. Logging in...")
        
        # Login
        result = client.login(
            email="user@example.com",
            password="mypassword",
            register_id="1234567890"
        )
        
        if not result:
            print("Login failed!")
            return
    
    # Make authenticated requests
    print("\nFetching user profile...")
    profile = client.make_authenticated_request('/user/profile')
    
    if profile:
        print(json.dumps(profile, indent=2))
    
    print("\nFetching JHT balance...")
    balance = client.make_authenticated_request('/jht/balance')
    
    if balance:
        print(json.dumps(balance, indent=2))

if __name__ == "__main__":
    main()
```

---

## ✅ Script Siap Digunakan!

Kedua script sudah dibuat di:
- `/app/backend/bpjs_login.py` - Full-featured script
- `/app/backend/simple_login.py` - Simple quick script

Dependencies sudah ada di `requirements.txt` ✅

**Silakan test dengan kredensial BPJS TKU Anda!** 🚀
