# 🔍 Temuan Baru dari Analisis Smali & .so Files

## 📊 Informasi Penting yang Ditemukan:

### ✅ Base URL yang Benar:
```
https://api-jmo.bpjsketenagakerjaan.go.id
```

### ✅ App Version:
```
4.0.3 (dari res/values/strings.xml)
```

### ✅ Package Name:
```
com.bpjstku
```

---

## 🔐 Headers yang Diperlukan:

Dari analisis `HeaderInterceptor.smali` dan `AsikDataStore.smali`:

### Standard Headers:
```http
User-Agent: Jamsostek-Mobile/Android/4.0.3
Content-Type: application/json
Accept: application/json
Accept-Encoding: gzip, deflate
Accept-Language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7
X-App-Version: 4.0.3
X-Platform: Android
X-Device-Type: mobile
X-Device-Id: [GENERATED_UUID]
```

### Custom Headers (dari smali):
```http
x-request-signature: [SHA256_HASH]
x-client-id: com.bpjstku
x-timestamp: [ISO8601_TIMESTAMP]
```

### Authorization Header (setelah login):
```http
Authorization: Bearer [ACCESS_TOKEN]
```

---

## 📝 Request Body yang Benar:

```json
{
  "email": "user@example.com",
  "password": "password123",
  "deviceId": "uuid-generated",
  "registerId": "1234567890"  ← WAJIB! Tidak boleh kosong/null
}
```

**PENTING:** `registerId` (NIK) adalah field WAJIB!

---

## ⚠️ Error Messages yang Ditemukan:

### Error 1:
```json
{
  "isSuccessful": false,
  "statusCode": "400",
  "message": "registerId: cannot be blank."
}
```
**Solution:** Isi field `registerId` dengan NIK

### Error 2:
```json
{
  "isSuccessful": false,
  "statusCode": "400",
  "message": "Permintaan ditolak"
}
```
**Kemungkinan:** Signature salah atau header kurang

---

## 🔧 Signature Generation (Estimasi):

Dari analisis, kemungkinan signature dibuat dengan:

```python
import hashlib
import json

def generate_signature(payload, timestamp, device_id):
    # Combine payload + timestamp + device_id
    data_to_sign = json.dumps(payload, sort_keys=True) + timestamp + device_id
    
    # SHA256 hash
    signature = hashlib.sha256(data_to_sign.encode()).hexdigest()
    
    return signature
```

**Note:** Ini adalah estimasi. Signature sebenarnya mungkin menggunakan:
- HMAC dengan secret key
- RSA signature
- Custom algorithm dari Zimperium SDK

---

## 🚀 Cara Menggunakan Script Enhanced:

### Download Script Baru:
```bash
cd ~/bpjs-login
# Copy bpjs_login_enhanced.py dari /app/backend/
```

### Run:
```bash
python3 bpjs_login_enhanced.py
```

### Input:
```
Email: yusufffaqot07@gmail.com
Password: ********
NIK/Register ID (WAJIB!): 1234567890123456
```

---

## 📊 Response Format (Success):

```json
{
  "isSuccessful": true,
  "statusCode": "200",
  "message": "Login successful",
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "user_id",
      "email": "user@example.com",
      "name": "User Name",
      "nik": "1234567890123456"
    }
  }
}
```

---

## 🔍 Untuk Mendapatkan Signature yang Tepat:

### Method 1: Network Sniffer
```bash
# Install mitmproxy
pip3 install mitmproxy

# Run
mitmproxy -p 8080

# Configure Android device to use proxy
# IP: your_computer_ip
# Port: 8080

# Login di aplikasi dan lihat request
```

### Method 2: Frida (Root Required)
```javascript
// Hook OkHttp Interceptor
Java.perform(function() {
    var HeaderInterceptor = Java.use('com.bpjstku.data.lib.HeaderInterceptor');
    
    HeaderInterceptor.intercept.implementation = function(chain) {
        var request = chain.request();
        console.log("Headers:");
        console.log(request.headers().toString());
        
        return this.intercept(chain);
    };
});
```

### Method 3: APK Patching
```bash
# Decompile APK
apktool d base.apk

# Add logging di HeaderInterceptor
# Recompile dan sign
apktool b base -o patched.apk
```

---

## 🎯 Perubahan di Script Enhanced:

### 1. Base URL Fixed:
```python
self.base_url = "https://api-jmo.bpjsketenagakerjaan.go.id"
```

### 2. Headers Lengkap:
```python
self.session.headers.update({
    'User-Agent': f'Jamsostek-Mobile/Android/{self.app_version}',
    'X-App-Version': self.app_version,
    'X-Platform': 'Android',
    'X-Device-Type': 'mobile',
    'X-Device-Id': self.device_id,
})
```

### 3. Custom Headers per Request:
```python
headers = {
    'x-request-signature': signature,
    'x-client-id': self.package_name,
    'x-timestamp': timestamp,
}
```

### 4. Validasi registerId:
```python
if not register_id:
    print("Error: NIK/Register ID tidak boleh kosong!")
    return
```

---

## 📱 Testing dengan Berbagai Skenario:

### Test 1: Login dengan registerId
```bash
python3 bpjs_login_enhanced.py
Email: user@example.com
Password: ******
NIK: 1234567890123456
```

### Test 2: Login tanpa registerId (akan error)
```bash
python3 bpjs_login_enhanced.py
Email: user@example.com
Password: ******
NIK: [Enter] ← Error: cannot be blank
```

### Test 3: Cek Response Headers
Script akan print response headers yang dimulai dengan `x-`:
```
[*] Response Headers:
    x-request-id: abc123
    x-rate-limit: 100
```

---

## 🔄 Next Steps untuk Debugging:

### 1. Capture Real Traffic:
```bash
# Install Charles Proxy atau mitmproxy
# Set sebagai proxy di Android
# Login di aplikasi asli
# Lihat exact headers dan signature
```

### 2. Compare dengan Script:
```python
# Print semua headers yang dikirim
print("Request Headers:")
for key, value in headers.items():
    print(f"  {key}: {value}")
```

### 3. Adjust Signature Algorithm:
```python
# Jika signature masih salah, coba:
# - HMAC-SHA256 dengan secret key
# - MD5 hash
# - Kombinasi berbeda dari payload elements
```

---

## 💡 Tips Tambahan:

### 1. SSL Pinning:
Aplikasi mungkin menggunakan SSL pinning (dari Zimperium SDK).
Jika ada error SSL, bypass dengan:
```python
import urllib3
urllib3.disable_warnings()
session.verify = False
```

### 2. Device Fingerprinting:
Zimperium SDK mungkin generate device fingerprint unik.
Coba extract dari real device.

### 3. Time Sync:
Pastikan timestamp akurat:
```python
import ntplib
client = ntplib.NTPClient()
response = client.request('pool.ntp.org')
timestamp = datetime.fromtimestamp(response.tx_time)
```

---

## ✅ Files Created:

1. `/app/backend/bpjs_login_enhanced.py` - Script dengan header lengkap
2. Original files masih ada:
   - `bpjs_login.py` - Basic version
   - `simple_login.py` - Simple version

---

## 🎬 Ready to Test!

```bash
cd ~/bpjs-login
python3 bpjs_login_enhanced.py
```

**Masukkan NIK yang valid untuk test!** 🚀
