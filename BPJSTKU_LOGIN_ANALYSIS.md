# 🔐 Analisis Login Aplikasi BPJS TKU (Jamsostek Mobile)

## 📱 Informasi Aplikasi
- **Nama Aplikasi**: Jamsostek Mobile (BPJS Ketenagakerjaan)
- **Package**: com.bpjstku
- **Base Domain**: https://www.bpjsketenagakerjaan.go.id
- **Architecture**: MVVM (Model-View-ViewModel) dengan Clean Architecture
- **Tech Stack**: Kotlin, Retrofit, RxJava, Android Jetpack

---

## 🌐 Struktur API Login

### Base URL
```
https://[API_BASE_URL] (exact URL obfuscated in binary)
```

### Endpoint Login
```http
POST /login
Content-Type: application/json
```

### Request Structure

#### LoginRequest Model
Berdasarkan analisis smali file `/data/user/model/request/LoginRequest.smali`:

```json
{
  "email": "string",
  "password": "string",
  "deviceId": "string",
  "registerId": "string"
}
```

**Field Descriptions:**
- `email`: Email/username pengguna (SerializedName: "email")
- `password`: Password pengguna (SerializedName: "password")  
- `deviceId`: Unique device identifier (SerializedName: "deviceId")
- `registerId`: Registration ID / NIK (SerializedName: "registerId")

### Response Structure

#### LoginItem Model (Success Response)
Berdasarkan analisis smali file `/data/user/model/response/LoginItem.smali`:

```json
{
  "accessToken": "string",
  "refreshToken": "string"
}
```

**Field Descriptions:**
- `accessToken`: JWT Access Token untuk autentikasi API calls (SerializedName: "accessToken")
- `refreshToken`: Refresh token untuk generate access token baru (SerializedName: "refreshToken")

---

## 🔄 Authentication Flow

### 1. Login Process
```
User Input (Email + Password)
       ↓
LoginActivity (UI Layer)
       ↓
LoginViewModel (Presentation Layer)
       ↓
UserRepository (Data Layer)
       ↓
UserApiClient (Network Layer)
       ↓
Retrofit + OkHttp
       ↓
POST /login API
       ↓
LoginItem Response
       ↓
Store Tokens (UserDataStore)
       ↓
Navigate to Home
```

### 2. Token Storage
- **Location**: UserDataStore (SharedPreferences/DataStore)
- **Stored Data**:
  - Access Token
  - Refresh Token
  - User Information
  - Device Token (for push notifications)

### 3. Token Refresh
- **Endpoint**: `POST /refresh-token` atau similar
- **Request**: `RefreshTokenRequest` dengan refresh token
- **Response**: `RefreshTokenResponse` dengan access token baru
- **Trigger**: Saat access token expired (biasanya 401 Unauthorized)

---

## 🏗️ Architecture Components

### 1. Presentation Layer
```
📁 presentation/membership/login/
├── LoginActivity.smali          # UI Activity
├── LoginActivity$b.smali         # Companion object
└── ...ViewModel files            # ViewModel (obfuscated)
```

**LoginActivity Features:**
- Reactive form binding
- Material Design components (MaterialButton)
- Button elements:
  - `btnBsu` - Login button
  - `btnRegister` - Register button
- WindowInsets handling (edge-to-edge UI)

### 2. Domain Layer
```
📁 domain/user/model/
├── User.smali                    # User entity
├── Login.smali                   # Login domain model
├── UserAccessToken.smali         # Access token model
├── ValidationOtp.smali           # OTP validation model
└── ForgotAccount.smali           # Forgot account model
```

### 3. Data Layer
```
📁 data/user/
├── UserRepository.smali          # Repository pattern
├── UserDataStore.smali           # Local data storage
└── remote/
    ├── UserApi.smali             # Retrofit API interface
    └── UserApiClient.smali       # API client implementation
```

**UserApiClient Methods:**
- `postLogin(LoginRequest)` → Observable<LoginItem>
- `postRefreshToken(RefreshTokenRequest)` → Observable<RefreshTokenResponse>
- `updateDeviceToken(UpdateDeviceToken)` → Observable<ResponseBody>
- `postValidationOtpRequestAuth(...)` → OTP validation

---

## 🔒 Security Features

### 1. SessionAuthenticator
- **Location**: `/data/lib/SessionAuthenticator.smali`
- **Purpose**: Handles authentication for HTTP requests
- **Features**:
  - Auto token refresh
  - Request retry dengan token baru
  - Session management

### 2. Code Obfuscation
- ProGuard/R8 obfuscation enabled
- Method names obfuscated:
  - `TuitionPaymentFragmentspecialinlinedviewModeldefault1`
  - `TuitionPaymentFragmentbindingInflater1`
  - etc.

### 3. API Security
- HTTPS only
- Token-based authentication (JWT)
- Device ID binding
- Refresh token mechanism

---

## 📊 Additional Features

### 1. Device Registration
```json
{
  "deviceId": "unique_device_uuid",
  "deviceToken": "firebase_push_token"
}
```

### 2. OTP Verification
- Phone verification
- Email verification
- OTP untuk forgot password

### 3. Biometric Authentication
- Fingerprint support (FingerprintManagerCompat)
- Biometric with Dukcapil integration
- Face recognition untuk scholarship verification

---

## 🔧 Implementation Example (Kotlin/Java Equivalent)

### Login Request
```kotlin
data class LoginRequest(
    @SerializedName("email")
    val email: String,
    
    @SerializedName("password")
    val password: String,
    
    @SerializedName("deviceId")
    val deviceId: String,
    
    @SerializedName("registerId")
    val registerId: String? = null
)
```

### Login Response
```kotlin
data class LoginItem(
    @SerializedName("accessToken")
    val accessToken: String,
    
    @SerializedName("refreshToken")
    val refreshToken: String
)
```

### API Interface
```kotlin
interface UserApiClient {
    @POST("login")
    fun postLogin(
        @Body request: LoginRequest
    ): Observable<LoginItem>
    
    @POST("refresh-token")
    fun postRefreshToken(
        @Body request: RefreshTokenRequest
    ): Observable<RefreshTokenResponse>
    
    @POST("update-device-token")
    fun updateDeviceToken(
        @Body request: UpdateDeviceToken
    ): Observable<ResponseBody>
}
```

### Usage Example
```kotlin
// Login
val loginRequest = LoginRequest(
    email = "user@example.com",
    password = "password123",
    deviceId = UUID.randomUUID().toString(),
    registerId = "NIK_NUMBER"
)

userRepository.login(loginRequest)
    .subscribeOn(Schedulers.io())
    .observeOn(AndroidSchedulers.mainThread())
    .subscribe(
        { loginItem ->
            // Save tokens
            userDataStore.saveAccessToken(loginItem.accessToken)
            userDataStore.saveRefreshToken(loginItem.refreshToken)
            
            // Navigate to home
            navigateToHome()
        },
        { error ->
            // Handle error
            showError(error.message)
        }
    )
```

---

## 🎯 Implementation untuk FastAPI + React

### Backend (FastAPI)

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime, timedelta
import jwt
import bcrypt

# Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    deviceId: str
    registerId: Optional[str] = None

class LoginResponse(BaseModel):
    accessToken: str
    refreshToken: str

class RefreshTokenRequest(BaseModel):
    refreshToken: str

# Login endpoint
@app.post("/api/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    # Validate user credentials
    user = await db.users.find_one({"email": request.email})
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not bcrypt.checkpw(request.password.encode(), user['password'].encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate tokens
    access_token = generate_access_token(user['id'])
    refresh_token = generate_refresh_token(user['id'])
    
    # Save device ID
    await db.users.update_one(
        {"_id": user['_id']},
        {"$set": {"deviceId": request.deviceId, "lastLogin": datetime.utcnow()}}
    )
    
    return LoginResponse(
        accessToken=access_token,
        refreshToken=refresh_token
    )

@app.post("/api/refresh-token", response_model=LoginResponse)
async def refresh_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(request.refreshToken, SECRET_KEY, algorithms=["HS256"])
        user_id = payload['user_id']
        
        # Generate new tokens
        access_token = generate_access_token(user_id)
        refresh_token = generate_refresh_token(user_id)
        
        return LoginResponse(
            accessToken=access_token,
            refreshToken=refresh_token
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
```

### Frontend (React)

```javascript
// Login API call
const login = async (email, password) => {
  const deviceId = getDeviceId(); // Generate or retrieve device ID
  
  try {
    const response = await axios.post(`${BACKEND_URL}/api/login`, {
      email,
      password,
      deviceId,
      registerId: null // Optional
    });
    
    const { accessToken, refreshToken } = response.data;
    
    // Store tokens
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    
    // Set axios default header
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    
    return true;
  } catch (error) {
    console.error('Login failed:', error.response?.data);
    throw error;
  }
};

// Auto token refresh interceptor
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const response = await axios.post(`${BACKEND_URL}/api/refresh-token`, {
          refreshToken
        });
        
        const { accessToken } = response.data;
        localStorage.setItem('accessToken', accessToken);
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
        
        return axios(originalRequest);
      } catch (refreshError) {
        // Logout user
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
```

---

## 📝 Summary

### Key Findings:
1. **Authentication Method**: Email + Password dengan JWT tokens
2. **Token System**: Access token + Refresh token
3. **Device Binding**: Menggunakan device ID untuk security
4. **Architecture**: Clean Architecture dengan MVVM pattern
5. **Network**: Retrofit + OkHttp + RxJava
6. **Security**: Token refresh otomatis via SessionAuthenticator

### Required Implementation:
- ✅ Login endpoint dengan email & password
- ✅ JWT access token generation
- ✅ Refresh token mechanism
- ✅ Device ID tracking
- ✅ Token storage (localStorage/cookies)
- ✅ Auto token refresh on 401
- ⬜ Biometric authentication (optional)
- ⬜ OTP verification (optional)

