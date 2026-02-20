#!/usr/bin/env python3
"""
BPJS TKU Enhanced Login Script with Realistic Device Info
Generate device fingerprint mirip Samsung/Android devices
"""

import requests
import json
import uuid
import hashlib
import random
import string
from datetime import datetime
from typing import Dict, Optional
import getpass
import os


class BPJSRealisticLoginClient:
    def __init__(self, base_url: str = None):
        """
        Initialize dengan device info yang realistic
        """
        self.base_url = base_url or "https://api-jmo.bpjsketenagakerjaan.go.id"
        self.session = requests.Session()
        
        # Generate realistic device info
        self.device_info = self._generate_realistic_device_info()
        self.device_id = self.device_info['device_id']
        self.android_id = self.device_info['android_id']
        
        self.app_version = "4.0.3"
        self.package_name = "com.bpjstku"
        
        # Set headers dengan device info realistic
        self.session.headers.update({
            'User-Agent': self.device_info['user_agent'],
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'X-App-Version': self.app_version,
            'X-Platform': 'Android',
            'X-Device-Type': 'mobile',
            'X-Device-Id': self.device_id,
            'X-Device-Model': self.device_info['model'],
            'X-Device-Manufacturer': self.device_info['manufacturer'],
            'X-OS-Version': self.device_info['os_version'],
            'X-Android-Id': self.android_id,
        })
        
        self.tokens = {
            'access_token': None,
            'refresh_token': None
        }
    
    def _generate_realistic_device_info(self) -> Dict:
        """
        Generate device info yang terlihat seperti device Samsung/Android asli
        """
        device_file = '.bpjs_device_info.json'
        
        # Cek apakah sudah ada device info tersimpan
        if os.path.exists(device_file):
            with open(device_file, 'r') as f:
                return json.load(f)
        
        # List Samsung devices populer
        samsung_devices = [
            {'model': 'SM-A325F', 'name': 'Samsung Galaxy A32', 'codename': 'a32'},
            {'model': 'SM-A525F', 'name': 'Samsung Galaxy A52', 'codename': 'a52'},
            {'model': 'SM-G973F', 'name': 'Samsung Galaxy S10', 'codename': 's10'},
            {'model': 'SM-G998B', 'name': 'Samsung Galaxy S21 Ultra', 'codename': 's21ultra'},
            {'model': 'SM-M315F', 'name': 'Samsung Galaxy M31', 'codename': 'm31'},
            {'model': 'SM-A107F', 'name': 'Samsung Galaxy A10s', 'codename': 'a10s'},
            {'model': 'SM-N975F', 'name': 'Samsung Galaxy Note 10+', 'codename': 'note10plus'},
        ]
        
        # Pilih random device
        device = random.choice(samsung_devices)
        
        # Android versions
        android_versions = [
            {'version': '11', 'api': '30', 'release': 'R'},
            {'version': '12', 'api': '31', 'release': 'S'},
            {'version': '13', 'api': '33', 'release': 'T'},
        ]
        android = random.choice(android_versions)
        
        # Generate Android ID (16 char hex)
        android_id = ''.join(random.choices('0123456789abcdef', k=16))
        
        # Generate Device ID yang terlihat seperti IMEI-based
        # Format: [timestamp]-[random]-[checksum]
        timestamp = str(int(datetime.now().timestamp() * 1000))[-10:]
        random_part = ''.join(random.choices(string.digits, k=6))
        checksum = hashlib.md5(f"{device['model']}{android_id}".encode()).hexdigest()[:4]
        device_id = f"{timestamp}{random_part}{checksum}"
        
        # Build info untuk User-Agent
        build_id = f"{android['release']}.{random.randint(100000, 999999)}.{random.randint(100, 999)}"
        
        device_info = {
            'device_id': device_id,
            'android_id': android_id,
            'model': device['model'],
            'name': device['name'],
            'manufacturer': 'samsung',
            'brand': 'samsung',
            'codename': device['codename'],
            'os_version': android['version'],
            'api_level': android['api'],
            'build_id': build_id,
            'user_agent': f"Dalvik/2.1.0 (Linux; U; Android {android['version']}; {device['model']} Build/{build_id})"
        }
        
        # Save untuk konsistensi
        with open(device_file, 'w') as f:
            json.dump(device_info, f, indent=2)
        
        return device_info
    
    def _generate_request_signature(self, payload: Dict, timestamp: str) -> str:
        """
        Generate request signature - berbagai algoritma untuk testing
        """
        # Method 1: Simple hash
        data_to_sign = json.dumps(payload, sort_keys=True) + timestamp + self.device_id
        signature = hashlib.sha256(data_to_sign.encode()).hexdigest()
        
        return signature
    
    def _generate_alternative_signature(self, payload: Dict) -> str:
        """
        Alternative signature method - MD5 based
        """
        # Coba dengan MD5
        data = f"{payload['email']}{payload['registerId']}{self.device_id}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def login(self, email: str, password: str, register_id: str, use_alt_signature: bool = False) -> Dict:
        """
        Login dengan device info realistic
        """
        endpoint = f"{self.base_url}/login"
        
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        payload = {
            "email": email,
            "password": password,
            "deviceId": self.device_id,
            "registerId": register_id
        }
        
        # Generate signature
        if use_alt_signature:
            signature = self._generate_alternative_signature(payload)
        else:
            signature = self._generate_request_signature(payload, timestamp)
        
        # Custom headers
        headers = {
            'x-request-signature': signature,
            'x-client-id': self.package_name,
            'x-timestamp': timestamp,
        }
        
        print(f"\n{'='*70}")
        print(f"BPJS TKU Login - Realistic Device Fingerprint")
        print(f"{'='*70}")
        print(f"\n[*] Device Info:")
        print(f"    Model: {self.device_info['name']} ({self.device_info['model']})")
        print(f"    Manufacturer: {self.device_info['manufacturer'].upper()}")
        print(f"    Android: {self.device_info['os_version']} (API {self.device_info['api_level']})")
        print(f"    Device ID: {self.device_id}")
        print(f"    Android ID: {self.android_id}")
        print(f"\n[*] Login Info:")
        print(f"    Email: {email}")
        print(f"    Register ID (NIK): {register_id}")
        print(f"    Endpoint: {endpoint}")
        print(f"    Signature Type: {'MD5' if use_alt_signature else 'SHA256'}")
        print(f"    Signature: {signature[:40]}...")
        
        try:
            response = self.session.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            print(f"\n[*] Response:")
            print(f"    Status Code: {response.status_code}")
            print(f"    Response Headers:")
            for key, value in response.headers.items():
                if key.lower().startswith('x-') or key.lower() == 'content-type':
                    print(f"      {key}: {value}")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'accessToken' in data or 'data' in data:
                    # Handle different response formats
                    if 'data' in data and isinstance(data['data'], dict):
                        self.tokens['access_token'] = data['data'].get('accessToken')
                        self.tokens['refresh_token'] = data['data'].get('refreshToken')
                    else:
                        self.tokens['access_token'] = data.get('accessToken')
                        self.tokens['refresh_token'] = data.get('refreshToken')
                    
                    if self.tokens['access_token']:
                        self._save_tokens()
                        
                        print(f"\n{'='*70}")
                        print(f"✓ LOGIN SUCCESS!")
                        print(f"{'='*70}")
                        print(f"\nAccess Token: {self.tokens['access_token'][:60]}...")
                        if self.tokens['refresh_token']:
                            print(f"Refresh Token: {self.tokens['refresh_token'][:60]}...")
                        
                        print(f"\nFull Response:")
                        print(json.dumps(data, indent=2))
                        
                        return data
                
                print(f"\n[!] Response received but no tokens:")
                print(json.dumps(data, indent=2))
                return data
            
            elif response.status_code == 400:
                print(f"\n[✗] Bad Request (400)")
                try:
                    error_data = response.json()
                    print(f"[✗] Error Message: {error_data.get('message', 'Unknown error')}")
                    print(f"\nFull Error Response:")
                    print(json.dumps(error_data, indent=2))
                    
                    # Suggestions based on error
                    message = error_data.get('message', '').lower()
                    if 'signature' in message:
                        print(f"\n[!] Signature issue detected!")
                        print(f"[!] Try running with --alt-signature flag")
                    elif 'ditolak' in message:
                        print(f"\n[!] Request rejected by server")
                        print(f"[!] Possible reasons:")
                        print(f"    - Invalid credentials")
                        print(f"    - Signature mismatch")
                        print(f"    - Missing required headers")
                        print(f"    - Account locked/suspended")
                except:
                    print(f"[✗] Response: {response.text}")
                return None
            
            elif response.status_code == 401:
                print(f"\n[✗] Unauthorized (401)")
                print(f"[✗] Invalid credentials")
                try:
                    print(f"[✗] Response: {response.json()}")
                except:
                    print(f"[✗] Response: {response.text}")
                return None
            
            else:
                print(f"\n[✗] Login failed with status {response.status_code}")
                print(f"[✗] Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"\n[✗] Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _save_tokens(self):
        """Save tokens ke file"""
        token_file = '.bpjs_tokens.json'
        
        with open(token_file, 'w') as f:
            json.dump({
                'access_token': self.tokens['access_token'],
                'refresh_token': self.tokens['refresh_token'],
                'timestamp': datetime.now().isoformat(),
                'device_info': self.device_info
            }, f, indent=2)
        
        print(f"\n[✓] Tokens saved to {token_file}")
    
    def load_tokens(self) -> bool:
        """Load tokens dari file"""
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
        except:
            return False
    
    def show_device_info(self):
        """Display device info"""
        print(f"\n{'='*70}")
        print(f"Device Information")
        print(f"{'='*70}")
        print(f"Device Name: {self.device_info['name']}")
        print(f"Model: {self.device_info['model']}")
        print(f"Manufacturer: {self.device_info['manufacturer']}")
        print(f"Android Version: {self.device_info['os_version']}")
        print(f"API Level: {self.device_info['api_level']}")
        print(f"Build ID: {self.device_info['build_id']}")
        print(f"Device ID: {self.device_id}")
        print(f"Android ID: {self.android_id}")
        print(f"User-Agent: {self.device_info['user_agent']}")
        print(f"{'='*70}\n")


def main():
    """Main function"""
    import sys
    
    print("=" * 70)
    print("BPJS TKU Login - Realistic Device Fingerprint")
    print("v4.0.3 - Samsung/Android Device Emulation")
    print("=" * 70)
    
    # Check for alt signature flag
    use_alt_sig = '--alt-signature' in sys.argv or '-a' in sys.argv
    show_info = '--show-info' in sys.argv or '-i' in sys.argv
    
    # Create client
    client = BPJSRealisticLoginClient()
    
    if show_info:
        client.show_device_info()
        return
    
    # Check saved tokens
    if client.load_tokens():
        print("\n[?] Found saved tokens. Use them? (y/n)")
        use_saved = input("Default: y > ").strip().lower() or 'y'
        
        if use_saved == 'y':
            print("\n[✓] Using saved tokens")
            client.show_device_info()
            return
    
    # Input credentials
    email = input("\nEmail: ").strip()
    password = getpass.getpass("Password: ")
    register_id = input("NIK/Register ID (16 digit): ").strip()
    
    if not register_id:
        print("\n[✗] Error: NIK cannot be blank!")
        return
    
    # Login
    print(f"\n[*] Starting login...")
    if use_alt_sig:
        print(f"[*] Using alternative signature (MD5)")
    
    result = client.login(email, password, register_id, use_alt_signature=use_alt_sig)
    
    if result:
        print(f"\n{'='*70}")
        print(f"✓ LOGIN SUCCESSFUL!")
        print(f"{'='*70}")
    else:
        print(f"\n{'='*70}")
        print(f"✗ LOGIN FAILED")
        print(f"{'='*70}")
        print(f"\nTroubleshooting:")
        print(f"1. Try with alternative signature: python3 {sys.argv[0]} --alt-signature")
        print(f"2. Verify your credentials are correct")
        print(f"3. Make sure NIK matches your account")
        print(f"4. Check if account is active")
        print(f"\nFor device info: python3 {sys.argv[0]} --show-info")


if __name__ == "__main__":
    main()
