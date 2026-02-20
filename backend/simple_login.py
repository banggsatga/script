#!/usr/bin/env python3
"""
BPJS TKU Simple Login Script
Script sederhana untuk login cepat ke BPJS
"""

import requests
import uuid
import json
import sys


def simple_login(email: str, password: str, base_url: str = None):
    """
    Simple login function tanpa class
    
    Args:
        email: Email pengguna
        password: Password pengguna
        base_url: Base URL API (default: auto-detect)
    
    Returns:
        Dict dengan access_token dan refresh_token, atau None jika gagal
    """
    # Default base URLs untuk dicoba
    urls = [
        "https://api.bpjsketenagakerjaan.go.id",
        "https://mobile-api.bpjsketenagakerjaan.go.id", 
        "https://app.bpjsketenagakerjaan.go.id",
        "https://jamsostek-api.bpjsketenagakerjaan.go.id"
    ]
    
    if base_url:
        urls.insert(0, base_url)
    
    # Generate device ID
    device_id = str(uuid.uuid4())
    
    # Request payload
    payload = {
        "email": email,
        "password": password,
        "deviceId": device_id,
        "registerId": None
    }
    
    # Headers
    headers = {
        'User-Agent': 'Jamsostek-Mobile/Android',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    print(f"\n{'='*60}")
    print(f"BPJS TKU Login Script")
    print(f"{'='*60}")
    print(f"\nEmail: {email}")
    print(f"Device ID: {device_id}")
    
    # Try each URL
    for url in urls:
        endpoint = f"{url}/login"
        print(f"\n[*] Trying: {endpoint}")
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            print(f"[*] Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"\n{'='*60}")
                print(f"✓ LOGIN SUCCESS!")
                print(f"{'='*60}")
                print(f"\nAccess Token:")
                print(data.get('accessToken', 'N/A'))
                print(f"\nRefresh Token:")
                print(data.get('refreshToken', 'N/A'))
                print(f"\nFull Response:")
                print(json.dumps(data, indent=2))
                
                # Save to file
                with open('bpjs_tokens.json', 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"\n[✓] Tokens saved to bpjs_tokens.json")
                
                return data
            
            elif response.status_code == 401:
                print(f"[✗] Invalid credentials")
                print(f"Response: {response.text}")
            
            elif response.status_code == 404:
                print(f"[!] Endpoint not found (wrong URL)")
            
            else:
                print(f"[!] Status {response.status_code}: {response.text}")
        
        except requests.exceptions.ConnectionError:
            print(f"[✗] Connection failed")
        
        except requests.exceptions.Timeout:
            print(f"[✗] Request timeout")
        
        except Exception as e:
            print(f"[✗] Error: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"✗ LOGIN FAILED")
    print(f"{'='*60}")
    print(f"\nNo working endpoint found.")
    print(f"Possible issues:")
    print(f"  1. Invalid credentials")
    print(f"  2. Base URL incorrect")
    print(f"  3. Network/firewall blocking")
    print(f"  4. API endpoint changed")
    
    return None


if __name__ == "__main__":
    # Quick usage dari command line
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        password = sys.argv[2]
        base_url = sys.argv[3] if len(sys.argv) > 3 else None
        
        simple_login(email, password, base_url)
    else:
        print("Usage:")
        print("  python simple_login.py <email> <password> [base_url]")
        print("\nExample:")
        print("  python simple_login.py user@example.com mypassword")
        print("  python simple_login.py user@example.com mypassword https://api.example.com")
        
        # Interactive mode
        print(f"\n{'='*60}")
        print("Interactive Mode")
        print(f"{'='*60}")
        
        email = input("\nEmail: ").strip()
        password = input("Password: ").strip()
        
        use_custom_url = input("\nUse custom base URL? (y/n): ").strip().lower()
        base_url = None
        if use_custom_url == 'y':
            base_url = input("Base URL: ").strip()
        
        simple_login(email, password, base_url)
