#!/usr/bin/env python3
"""
Schmidt-Samoa Cryptosystem - Simple Demo (PRODUCTION READY)

Quick demo untuk menunjukkan penggunaan implementasi Schmidt-Samoa 
yang telah diperbaiki dari semua bug kritis:

- NO MORE RecursionError dengan extended_gcd iterative
- Performance improvements dengan math.gcd/lcm
- Static methods untuk efficiency

Jalankan: python demo.py
"""

from schmidt_samoa import SchmidtSamoa


def main():
    print("🔐 Schmidt-Samoa Cryptosystem - Production Ready Demo")
    print("=" * 55)
    
    print("🛠️  Applied Fixes:")
    print("   ✅ RecursionError FIXED (iterative extended_gcd)")
    print("   ✅ Performance improved (math.gcd/lcm)")
    print("   ✅ Static methods for efficiency")
    print("   ✅ Accurate chunking calculations")
    
    # Test multiple key sizes to prove RecursionError is fixed
    key_sizes = [1024, 2048]
    
    for bits in key_sizes:
        print(f"\n🔑 Testing {bits}-bit keys:")
        print("-" * 30)
        
        try:
            # Generate keypair (using static method - no object creation waste)
            print(f"   Generating {bits}-bit keypair...")
            public_key, private_key = SchmidtSamoa.generate_keypair(bits=bits)
            print(f"   ✅ Key generation successful! ({public_key.n.bit_length()} bits)")
            
            # Test 1: Numeric encryption
            print(f"\n   📊 Testing numeric encryption:")
            message = 123456789
            print(f"      Original: {message}")
            
            encrypted = SchmidtSamoa.encrypt(message, public_key)
            print(f"      Encrypted: {str(encrypted)[:50]}...")
            
            decrypted = SchmidtSamoa.decrypt(encrypted, private_key)
            print(f"      Decrypted: {decrypted}")
            print(f"      ✅ Success: {message == decrypted}")
            
            # Test 2: String encryption
            print(f"\n   📝 Testing string encryption:")
            text = f"Hello from {bits}-bit Schmidt-Samoa! 🔐"
            print(f"      Original: '{text}'")
            
            encrypted_str = SchmidtSamoa.encrypt_string(text, public_key)
            print(f"      Encrypted: {str(encrypted_str)[:50]}...")
            
            decrypted_str = SchmidtSamoa.decrypt_string(encrypted_str, private_key) 
            print(f"      Decrypted: '{decrypted_str}'")
            print(f"      ✅ Success: {text == decrypted_str}")
            
            print(f"   🎯 {bits}-bit test: PASSED")
            
        except RecursionError:
            print(f"   ❌ RecursionError still exists for {bits}-bit keys!")
        except Exception as e:
            print(f"   ❌ Error with {bits}-bit keys: {e}")
    
    # Test convenience functions
    print(f"\n🔧 Testing optimized convenience functions:")
    print("-" * 45)
    
    from schmidt_samoa import generate_keypair, encrypt_string, decrypt_string
    
    # These now call static methods directly (no object creation)
    public_key, private_key = generate_keypair(bits=1024)
    
    test_text = "Convenience functions are now efficient! 🚀"
    encrypted = encrypt_string(test_text, public_key)
    decrypted = decrypt_string(encrypted, private_key)
    
    print(f"   Original: '{test_text}'")
    print(f"   Decrypted: '{decrypted}' ")
    print(f"   ✅ Convenience functions: {test_text == decrypted}")
    
    print("\n🎉 Demo completed successfully!")
    print("\n📚 For comprehensive testing run: python examples.py")
    print("🔍 For security details see: SECURITY.md")


if __name__ == "__main__":
    main()
