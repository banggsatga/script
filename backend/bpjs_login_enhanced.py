#!/usr/bin/env python3
"""
BPJS TKU Enhanced Login Script
Script dengan header lengkap mirip aplikasi asli
Based on reverse engineering smali files
"""

import requests
import json
import uuid
import platform
import hashlib
import base64
from datetime import datetime
from typing import Dict, Optional
import getpass
import os


class BPJSEnhancedLoginClient:
    def __init__(self, base_url: str = None):
        """
        Initialize BPJS Enhanced Login Client dengan header lengkap
        """
        # Base URL yang benar dari error message
        self.base_url = base_url or "https://api-jmo.bpjsketenagakerjaan.go.id"
        
        self.session = requests.Session()
        
        # Device info
        self.device_id = self._get_or_create_device_id()
        self.app_version = "4.0.3"  # Dari strings.xml
        self.package_name = "com.bpjstku"
        
        # Set headers mirip aplikasi asli
        self.session.headers.update({
            'User-Agent': f'Jamsostek-Mobile/Android/{self.app_version}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'X-App-Version': self.app_version,
            'X-Platform': 'Android',
            'X-Device-Type': 'mobile',
            'X-Device-Id': self.device_id,
        })
        
        self.tokens = {
            'access_token': None,
            'refresh_token': None
        }
    
    def _get_or_create_device_id(self) -> str:
        """Generate atau load device ID yang persistent"""
        device_file = '.bpjs_device_id'
        
        if os.path.exists(device_file):
            with open(device_file, 'r') as f:
                return f.read().strip()
        else:
            # Generate device ID berdasarkan machine info
            machine_info = f"{platform.node()}-{platform.machine()}-{platform.system()}"
            device_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, machine_info))
            
            with open(device_file, 'w') as f:
                f.write(device_id)
            
            return device_id
    
    def _generate_request_signature(self, payload: Dict, timestamp: str) -> str:
        """
        Generate request signature untuk x-request-signature header
        Ini adalah estimasi - perlu diverifikasi dengan traffic sniffer
        """
        # Combine payload dengan timestamp dan secret
        data_to_sign = json.dumps(payload, sort_keys=True) + timestamp + self.device_id
        
        # Generate signature (SHA256)
        signature = hashlib.sha256(data_to_sign.encode()).hexdigest()
        
        return signature
    
    def login(self, email: str, password: str, register_id: str) -> Dict:
        """
        Login ke BPJS TKU dengan parameter lengkap
        
        Args:
            email: Email pengguna
            password: Password pengguna (plain text - akan di-handle oleh server)
            register_id: NIK/Register ID (WAJIB!)
        
        Returns:
            Dict berisi access_token dan refresh_token
        """
        endpoint = f"{self.base_url}/login"
        
        # Timestamp untuk signature
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Payload sesuai dengan struktur dari smali
        payload = {
            "email": email,
            "password": password,
            "deviceId": self.device_id,
            "registerId": register_id  # WAJIB! Dari error message
        }
        
        # Generate signature
        signature = self._generate_request_signature(payload, timestamp)
        
        # Add custom headers untuk request ini
        headers = {
            'x-request-signature': signature,
            'x-client-id': self.package_name,
            'x-timestamp': timestamp,
        }
        
        print(f"\n{'='*60}")
        print(f"BPJS TKU Enhanced Login")
        print(f"{'='*60}")
        print(f"\n[*] Attempting login...")
        print(f"[*] Email: {email}")
        print(f"[*] Register ID: {register_id}")
        print(f"[*] Device ID: {self.device_id}")
        print(f"[*] App Version: {self.app_version}")
        print(f"[*] Endpoint: {endpoint}")
        print(f"[*] Signature: {signature[:30]}...")
        
        try:
            response = self.session.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"\n[*] Status Code: {response.status_code}")
            print(f"[*] Response Headers:")
            for key, value in response.headers.items():
                if key.lower().startswith('x-'):
                    print(f"    {key}: {value}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract tokens
                if 'accessToken' in data:
                    self.tokens['access_token'] = data.get('accessToken')
                    self.tokens['refresh_token'] = data.get('refreshToken')
                    
                    # Save tokens
                    self._save_tokens()
                    
                    print(f"\n{'='*60}")
                    print(f"✓ LOGIN SUCCESS!")
                    print(f"{'='*60}")
                    print(f"\nAccess Token: {self.tokens['access_token'][:50]}...")
                    if self.tokens['refresh_token']:
                        print(f"Refresh Token: {self.tokens['refresh_token'][:50]}...")
                    
                    return data
                else:
                    print(f"\n[!] Success but unexpected response format:")
                    print(json.dumps(data, indent=2))
                    return data
            
            elif response.status_code == 400:
                print(f"\n[✗] Bad Request (400)")
                try:
                    error_data = response.json()
                    print(f"[✗] Error: {error_data.get('message', 'Unknown error')}")
                    
                    if 'registerId' in error_data.get('message', ''):
                        print(f"\n[!] HINT: registerId (NIK) is required and cannot be blank!")
                    
                except:
                    print(f"[✗] Response: {response.text}")
                return None
            
            elif response.status_code == 401:
                print(f"\n[✗] Unauthorized (401)")
                print(f"[✗] Invalid credentials or signature")
                try:
                    print(f"[✗] Response: {response.json()}")
                except:
                    print(f"[✗] Response: {response.text}")
                return None
            
            else:
                print(f"\n[✗] Login failed with status {response.status_code}")
                print(f"[✗] Response: {response.text}")
                return None
                
        except requests.exceptions.ConnectionError as e:
            print(f"\n[✗] Connection error: {str(e)}")
            return None
        
        except requests.exceptions.Timeout:
            print(f"\n[✗] Request timeout")
            return None
        
        except Exception as e:
            print(f"\n[✗] Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def refresh_access_token(self) -> Optional[Dict]:
        """Refresh access token menggunakan refresh token"""
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
                print(f"[✗] Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"[✗] Error refreshing token: {str(e)}")
            return None
    
    def _save_tokens(self):
        """Save tokens ke file"""
        token_file = '.bpjs_tokens.json'
        
        with open(token_file, 'w') as f:
            json.dump({
                'access_token': self.tokens['access_token'],
                'refresh_token': self.tokens['refresh_token'],
                'timestamp': datetime.now().isoformat(),
                'device_id': self.device_id
            }, f, indent=2)
        
        print(f"[✓] Tokens saved to {token_file}")
    
    def load_tokens(self) -> bool:
        """Load tokens dari file yang tersimpan"""
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
        """Buat request dengan authentication header"""
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


def main():
    """Main function untuk menjalankan login script"""
    print("=" * 60)
    print("BPJS TKU (Jamsostek Mobile) Enhanced Login Script")
    print("v4.0.3 - Based on Reverse Engineering")
    print("=" * 60)
    
    # Input dari user
    email = input("\nEmail: ").strip()
    password = getpass.getpass("Password: ")
    register_id = input("NIK/Register ID (WAJIB!): ").strip()
    
    # Validasi NIK tidak kosong
    if not register_id:
        print("\n[✗] Error: NIK/Register ID tidak boleh kosong!")
        print("[!] Ini adalah field wajib berdasarkan API requirement")
        return
    
    # Create client
    client = BPJSEnhancedLoginClient()
    
    # Cek apakah ada tokens tersimpan
    if client.load_tokens():
        print("\n[?] Found saved tokens. Try to use them? (y/n)")
        use_saved = input("Default: y > ").strip().lower() or 'y'
        
        if use_saved == 'y':
            print("\n[*] Using saved tokens...")
            print("[*] You can now use make_authenticated_request() method")
            print("[*] Example: client.make_authenticated_request('/user/profile')")
            return
    
    # Login
    print("\n[*] Attempting to login...")
    result = client.login(email, password, register_id)
    
    if result:
        print("\n" + "=" * 60)
        print("✓ SUCCESS!")
        print("=" * 60)
        print("\nFull Response:")
        print(json.dumps(result, indent=2))
        print("\nTokens have been saved to .bpjs_tokens.json")
        print("You can now use the tokens for API requests")
    else:
        print("\n" + "=" * 60)
        print("✗ LOGIN FAILED")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("1. Pastikan NIK/Register ID sudah benar")
        print("2. Pastikan email dan password sudah benar")
        print("3. Coba login di aplikasi resmi dulu")
        print("4. Signature mungkin perlu adjustment (lihat network traffic)")


if __name__ == "__main__":
    main()
