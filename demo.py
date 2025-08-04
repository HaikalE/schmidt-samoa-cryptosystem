#!/usr/bin/env python3
"""
Schmidt-Samoa Cryptosystem - Simple Demo

Quick demo untuk menunjukkan penggunaan dasar dari implementasi
Schmidt-Samoa yang telah diperbaiki dan diamankan.

Jalankan: python demo.py
"""

from schmidt_samoa import SchmidtSamoa


def main():
    print("🔐 Schmidt-Samoa Cryptosystem - Simple Demo")
    print("=" * 50)
    
    # Initialize the cryptosystem
    crypto = SchmidtSamoa()
    
    # Generate keypair (menggunakan 1024-bit untuk keamanan yang baik)
    print("🔑 Generating 1024-bit keypair...")
    public_key, private_key = crypto.generate_keypair(bits=1024)
    print(f"✅ Keys generated successfully!")
    print(f"   Public key size: {public_key.n.bit_length()} bits")
    
    # Test 1: Numeric encryption
    print("\n📊 Testing numeric encryption:")
    message = 123456789
    print(f"   Original: {message}")
    
    encrypted = crypto.encrypt(message, public_key)
    print(f"   Encrypted: {str(encrypted)[:50]}...")
    
    decrypted = crypto.decrypt(encrypted, private_key)
    print(f"   Decrypted: {decrypted}")
    print(f"   ✅ Success: {message == decrypted}")
    
    # Test 2: String encryption
    print("\n📝 Testing string encryption:")
    text = "Hello, Schmidt-Samoa! 🔐"
    print(f"   Original: '{text}'")
    
    encrypted_str = crypto.encrypt_string(text, public_key)
    print(f"   Encrypted: {str(encrypted_str)[:50]}...")
    
    decrypted_str = crypto.decrypt_string(encrypted_str, private_key) 
    print(f"   Decrypted: '{decrypted_str}'")
    print(f"   ✅ Success: {text == decrypted_str}")
    
    print("\n🎉 Demo completed successfully!")
    print("\nFor more advanced examples, run: python examples.py")


if __name__ == "__main__":
    main()
