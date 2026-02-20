# 🎯 BPJS Login dengan Device ID Realistic

## 📱 Fitur Baru - Realistic Device Fingerprinting

Script baru mensimulasikan device Samsung/Android asli dengan:
- ✅ Device Model realistic (Samsung Galaxy A32, S10, A52, dll)
- ✅ Android ID (16 char hex)
- ✅ Device ID mirip IMEI-based
- ✅ Build ID dan User-Agent authentic
- ✅ Headers lengkap dengan device info

---

## 🚀 Cara Penggunaan:

### Copy Script ke VPS:
```bash
cd ~/bpjs-login

# Method 1: Manual
nano bpjs_login_realistic.py
# Paste isi file

# Method 2: SCP
scp /app/backend/bpjs_login_realistic.py user@vps:~/bpjs-login/

chmod +x bpjs_login_realistic.py
```

### Run Normal:
```bash
python3 bpjs_login_realistic.py
```

### Run dengan Alternative Signature:
```bash
python3 bpjs_login_realistic.py --alt-signature
# atau
python3 bpjs_login_realistic.py -a
```

### Show Device Info:
```bash
python3 bpjs_login_realistic.py --show-info
```

---

## 📊 Contoh Device Info yang Di-generate:

```
Device Name: Samsung Galaxy A52
Model: SM-A525F
Manufacturer: samsung
Android Version: 12
API Level: 31
Device ID: 1708524367123456a1b2
Android ID: 8f4e3d2c1b0a9876
User-Agent: Dalvik/2.1.0 (Linux; U; Android 12; SM-A525F Build/S.654321.123)
```

---

## 🔐 Headers yang Dikirim:

```http
User-Agent: Dalvik/2.1.0 (Linux; U; Android 12; SM-A525F Build/...)
X-App-Version: 4.0.3
X-Platform: Android
X-Device-Type: mobile
X-Device-Id: 1708524367123456a1b2
X-Device-Model: SM-A525F
X-Device-Manufacturer: samsung
X-OS-Version: 12
X-Android-Id: 8f4e3d2c1b0a9876
x-request-signature: [SHA256_HASH]
x-client-id: com.bpjstku
x-timestamp: 2025-02-20T12:00:00Z
```

---

## 🎯 Testing dengan Device Realistic:

### Test 1: Normal Login
```bash
python3 bpjs_login_realistic.py
```

Output:
```
============================================================
BPJS TKU Login - Realistic Device Fingerprint
============================================================

[*] Device Info:
    Model: Samsung Galaxy A52 (SM-A525F)
    Manufacturer: SAMSUNG
    Android: 12 (API 31)
    Device ID: 1708524367123456a1b2
    Android ID: 8f4e3d2c1b0a9876

[*] Login Info:
    Email: jmoa8ee9aca@dollicons.com
    Register ID (NIK): 1103010812640001
    Endpoint: https://api-jmo.bpjsketenagakerjaan.go.id/login
    Signature Type: SHA256
    Signature: 708b4252f1de...
```

### Test 2: Alternative Signature
```bash
python3 bpjs_login_realistic.py --alt-signature
```

Menggunakan MD5 hash untuk signature (coba jika SHA256 gagal)

---

## 📁 Files yang Di-generate:

### `.bpjs_device_info.json`
Device info yang persistent (akan digunakan lagi):
```json
{
  "device_id": "1708524367123456a1b2",
  "android_id": "8f4e3d2c1b0a9876",
  "model": "SM-A525F",
  "name": "Samsung Galaxy A52",
  "manufacturer": "samsung",
  "brand": "samsung",
  "codename": "a52",
  "os_version": "12",
  "api_level": "31",
  "build_id": "S.654321.123",
  "user_agent": "Dalvik/2.1.0 ..."
}
```

### `.bpjs_tokens.json`
Tokens dengan device info:
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "timestamp": "2025-02-20T12:00:00",
  "device_info": { ... }
}
```

---

## 🔄 Generate Device Baru:

Jika ingin ganti device (Samsung model lain):
```bash
rm .bpjs_device_info.json
python3 bpjs_login_realistic.py
```

Script akan generate random Samsung device baru

---

## 📱 Samsung Devices yang Didukung:

Script random memilih dari list ini:
- Samsung Galaxy A32 (SM-A325F)
- Samsung Galaxy A52 (SM-A525F)
- Samsung Galaxy S10 (SM-G973F)
- Samsung Galaxy S21 Ultra (SM-G998B)
- Samsung Galaxy M31 (SM-M315F)
- Samsung Galaxy A10s (SM-A107F)
- Samsung Galaxy Note 10+ (SM-N975F)

---

## 🔍 Debugging:

### Lihat Device Info Saat Ini:
```bash
python3 bpjs_login_realistic.py --show-info
```

### Output:
```
============================================================
Device Information
============================================================
Device Name: Samsung Galaxy A52
Model: SM-A525F
Manufacturer: samsung
Android Version: 12
API Level: 31
Build ID: S.654321.123
Device ID: 1708524367123456a1b2
Android ID: 8f4e3d2c1b0a9876
User-Agent: Dalvik/2.1.0 (Linux; U; Android 12; SM-A525F Build/S.654321.123)
============================================================
```

---

## 💡 Perbedaan dengan Script Sebelumnya:

### Script Lama (bpjs_login_enhanced.py):
```python
device_id = "691638ca-e81b-5455-b7a6-890644fef8cd"  # UUID generic
User-Agent: Jamsostek-Mobile/Android/4.0.3
```

### Script Baru (bpjs_login_realistic.py):
```python
device_id = "1708524367123456a1b2"  # IMEI-like
User-Agent: Dalvik/2.1.0 (Linux; U; Android 12; SM-A525F Build/S.654321.123)
Headers: X-Device-Model, X-Device-Manufacturer, X-OS-Version, X-Android-Id
```

---

## 🎯 Kenapa Pakai Device Realistic?

1. **More Authentic**: Terlihat seperti device Android asli
2. **Better Headers**: Device model, manufacturer, OS version
3. **Android ID**: 16 char hex seperti Settings.Secure.ANDROID_ID
4. **IMEI-like Device ID**: Bukan UUID random
5. **Persistent**: Device info konsisten antar login

---

## ⚠️ Jika Masih Error "Permintaan ditolak":

### Coba langkah ini:

1. **Gunakan Alternative Signature:**
```bash
python3 bpjs_login_realistic.py --alt-signature
```

2. **Generate Device Baru:**
```bash
rm .bpjs_device_info.json
python3 bpjs_login_realistic.py
```

3. **Capture Real Traffic:**
```bash
# Install mitmproxy
pip3 install mitmproxy

# Run
mitmproxy -p 8080

# Setup Android proxy dan login di app
# Lihat exact signature algorithm
```

4. **Verify Credentials:**
- Pastikan email benar
- Pastikan password benar
- Pastikan NIK 16 digit dan valid
- Coba login di app resmi dulu

---

## 🔥 Quick Commands:

```bash
# Normal login
python3 bpjs_login_realistic.py

# Try alternative signature
python3 bpjs_login_realistic.py -a

# Show device info
python3 bpjs_login_realistic.py -i

# Generate new device
rm .bpjs_device_info.json && python3 bpjs_login_realistic.py -i
```

---

## ✅ Files Ready:

```
~/bpjs-login/
├── requirements.txt              ✅
├── bpjs_login.py                ✅ Basic
├── simple_login.py              ✅ Simple
├── bpjs_login_enhanced.py       ✅ Enhanced
└── bpjs_login_realistic.py      ⭐ NEW - Realistic Device!
```

---

## 🚀 Test Sekarang!

```bash
cd ~/bpjs-login
python3 bpjs_login_realistic.py
```

Input:
```
Email: jmoa8ee9aca@dollicons.com
Password: ********
NIK/Register ID (16 digit): 1103010812640001
```

Device akan otomatis di-generate sebagai Samsung Galaxy model! 📱✨
