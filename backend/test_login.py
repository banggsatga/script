#!/usr/bin/env python3
"""
Test Script - BPJS Login
Script untuk testing login dengan berbagai skenario
"""

import sys
import os

# Add backend to path
sys.path.insert(0, '/app/backend')

from bpjs_login import BPJSLoginClient
from simple_login import simple_login
import json


def test_simple_login():
    """Test simple login function"""
    print("\n" + "="*70)
    print("TEST 1: Simple Login Function")
    print("="*70)
    
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    result = simple_login(email, password)
    
    return result is not None


def test_class_login():
    """Test BPJSLoginClient class"""
    print("\n" + "="*70)
    print("TEST 2: BPJSLoginClient Class")
    print("="*70)
    
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    client = BPJSLoginClient()
    result = client.login(email, password)
    
    if result:
        print("\n[✓] Login successful!")
        print(f"Access Token: {result['accessToken'][:50]}...")
        print(f"Refresh Token: {result['refreshToken'][:50]}...")
        return True
    else:
        print("\n[✗] Login failed!")
        return False


def test_try_all_urls():
    """Test dengan semua possible URLs"""
    print("\n" + "="*70)
    print("TEST 3: Try All Base URLs")
    print("="*70)
    
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    client = BPJSLoginClient()
    result = client.try_all_base_urls(email, password)
    
    return result is not None


def test_load_saved_tokens():
    """Test load tokens yang sudah disimpan"""
    print("\n" + "="*70)
    print("TEST 4: Load Saved Tokens")
    print("="*70)
    
    client = BPJSLoginClient()
    
    if client.load_tokens():
        print("\n[✓] Tokens loaded successfully!")
        print(f"Access Token: {client.tokens['access_token'][:50]}...")
        print(f"Refresh Token: {client.tokens['refresh_token'][:50]}...")
        
        # Test dengan request
        print("\n[*] Testing token with API request...")
        # Note: endpoint /user/profile mungkin berbeda
        result = client.make_authenticated_request('/user/profile')
        
        if result:
            print("\n[✓] Token is valid!")
            print(json.dumps(result, indent=2))
            return True
        else:
            print("\n[!] Token might be expired or invalid")
            return False
    else:
        print("\n[✗] No saved tokens found")
        return False


def test_token_refresh():
    """Test refresh token"""
    print("\n" + "="*70)
    print("TEST 5: Token Refresh")
    print("="*70)
    
    client = BPJSLoginClient()
    
    if not client.load_tokens():
        print("[✗] No tokens to refresh. Login first.")
        return False
    
    result = client.refresh_access_token()
    
    if result:
        print("\n[✓] Token refreshed successfully!")
        print(f"New Access Token: {result['accessToken'][:50]}...")
        return True
    else:
        print("\n[✗] Token refresh failed!")
        return False


def test_custom_base_url():
    """Test dengan custom base URL"""
    print("\n" + "="*70)
    print("TEST 6: Custom Base URL")
    print("="*70)
    
    base_url = input("Base URL: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    
    client = BPJSLoginClient(base_url=base_url)
    result = client.login(email, password)
    
    return result is not None


def interactive_menu():
    """Interactive test menu"""
    while True:
        print("\n" + "="*70)
        print("BPJS TKU Login - Test Suite")
        print("="*70)
        print("\n[1] Test Simple Login")
        print("[2] Test Class Login")
        print("[3] Test Try All URLs")
        print("[4] Test Load Saved Tokens")
        print("[5] Test Token Refresh")
        print("[6] Test Custom Base URL")
        print("[7] Run All Tests")
        print("[0] Exit")
        
        choice = input("\nSelect test [0-7]: ").strip()
        
        if choice == "1":
            test_simple_login()
        elif choice == "2":
            test_class_login()
        elif choice == "3":
            test_try_all_urls()
        elif choice == "4":
            test_load_saved_tokens()
        elif choice == "5":
            test_token_refresh()
        elif choice == "6":
            test_custom_base_url()
        elif choice == "7":
            print("\n[*] Running all tests...")
            results = {
                "Simple Login": test_simple_login(),
                "Class Login": test_class_login(),
                "Try All URLs": test_try_all_urls(),
                "Load Tokens": test_load_saved_tokens(),
                "Token Refresh": test_token_refresh(),
            }
            
            print("\n" + "="*70)
            print("TEST RESULTS")
            print("="*70)
            for test_name, result in results.items():
                status = "✓ PASS" if result else "✗ FAIL"
                print(f"{test_name:.<50} {status}")
        elif choice == "0":
            print("\nExiting...")
            break
        else:
            print("\n[✗] Invalid choice!")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        test_choice = sys.argv[1]
        
        if test_choice == "simple":
            test_simple_login()
        elif test_choice == "class":
            test_class_login()
        elif test_choice == "all":
            test_try_all_urls()
        elif test_choice == "load":
            test_load_saved_tokens()
        elif test_choice == "refresh":
            test_token_refresh()
        elif test_choice == "custom":
            test_custom_base_url()
        else:
            print("Usage: python test_login.py [simple|class|all|load|refresh|custom]")
    else:
        # Interactive mode
        interactive_menu()
