# 🚀 Quick Start - BPJS Login Scripts

## ⚡ Cara Tercepat

### 1. Simple Login (Recommended untuk pemula)
```bash
cd /app/backend
python3 simple_login.py
```

Kemudian ikuti prompt:
```
Email: user@example.com
Password: ********
```

### 2. Full Featured Login
```bash
cd /app/backend
python3 bpjs_login.py
```

### 3. Test Suite (Interactive)
```bash
cd /app/backend
python3 test_login.py
```

---

## 📝 Command Line Usage

### Simple Login - Direct
```bash
python3 simple_login.py user@example.com mypassword
```

### Simple Login - Custom URL
```bash
python3 simple_login.py user@example.com mypassword https://api.example.com
```

### Test Specific Feature
```bash
python3 test_login.py simple    # Test simple login
python3 test_login.py class     # Test class login
python3 test_login.py all       # Try all URLs
python3 test_login.py load      # Load saved tokens
python3 test_login.py refresh   # Refresh token
```

---

## 💻 Python Code Usage

### Minimal Example
```python
from simple_login import simple_login

result = simple_login("user@example.com", "mypassword")

if result:
    print(f"Access Token: {result['accessToken']}")
    print(f"Refresh Token: {result['refreshToken']}")
```

### Full Example with Class
```python
from bpjs_login import BPJSLoginClient

# Create client
client = BPJSLoginClient()

# Login
result = client.login("user@example.com", "mypassword")

if result:
    # Use tokens
    profile = client.make_authenticated_request('/user/profile')
    print(profile)
```

### Load Saved Tokens
```python
from bpjs_login import BPJSLoginClient

client = BPJSLoginClient()
client.load_tokens()

# Make request dengan saved tokens
data = client.make_authenticated_request('/endpoint')
```

---

## 🔍 What Happens After Login?

### Files Created:
1. `.bpjs_device_id` - Your persistent device ID
2. `.bpjs_tokens.json` or `bpjs_tokens.json` - Your login tokens

### Tokens Saved:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "timestamp": "2025-02-20T12:00:00"
}
```

### You Can Now:
- ✅ Make authenticated API requests
- ✅ Refresh tokens automatically
- ✅ Reuse saved tokens without re-login

---

## 🆘 Common Issues

### "Connection Failed"
```bash
# Try all possible URLs
python3 test_login.py all
```

### "Invalid Credentials"
- Double check email and password
- Make sure account is active

### "Module not found"
```bash
# Install dependencies
pip install -r requirements.txt
```

### "Permission Denied"
```bash
# Make scripts executable
chmod +x bpjs_login.py simple_login.py test_login.py
```

---

## 📊 Check Requirements

```bash
cd /app/backend
python3 -c "import requests; print('✓ All dependencies OK')"
```

If error, install:
```bash
pip install -r requirements.txt
```

---

## 🎯 Next Steps After Login

Once you have tokens, you can:

1. **Make API Calls**
```python
client.make_authenticated_request('/user/profile', method='GET')
client.make_authenticated_request('/jht/balance', method='GET')
```

2. **Update Device Token**
```python
client.make_authenticated_request(
    '/user/device-token',
    method='POST',
    data={'deviceToken': 'your_firebase_token'}
)
```

3. **Get Account Info**
```python
account = client.make_authenticated_request('/account/info')
```

---

## 🔒 Security Tips

1. **Never commit tokens to git**
   - `.bpjs_tokens.json` already in `.gitignore`

2. **Use environment variables for credentials**
```python
import os
email = os.getenv('BPJS_EMAIL')
password = os.getenv('BPJS_PASSWORD')
```

3. **Clear tokens after use**
```bash
rm .bpjs_tokens.json .bpjs_device_id
```

---

## ✅ Ready to Use!

All scripts are ready in `/app/backend/`:
- ✅ `bpjs_login.py` - Full-featured
- ✅ `simple_login.py` - Quick & simple
- ✅ `test_login.py` - Test suite
- ✅ `requirements.txt` - Already has all dependencies

**Just run and login!** 🎉
