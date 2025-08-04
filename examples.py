#!/usr/bin/env python3
"""
Schmidt-Samoa Cryptosystem Examples - SECURE VERSION

Contoh penggunaan untuk implementasi Schmidt-Samoa yang telah diperbaiki:
- Stateless design yang thread-safe
- Cryptographically secure random generation  
- Efficient string encryption
- Proper error handling

Author: HaikalE
Date: August 2025
Version: 2.0 (Security Hardened)
"""

import time
from schmidt_samoa import SchmidtSamoa, PublicKey, PrivateKey


def demo_basic_usage():
    """Demo penggunaan dasar dengan API baru yang secure"""
    print("=" * 60)
    print("🔐 BASIC USAGE - SECURE API")
    print("=" * 60)
    
    # Inisialisasi (stateless)
    crypto = SchmidtSamoa()
    
    # Generate keypair (default 1024 bits untuk keamanan)
    print("🔑 Generating 1024-bit keypair...")
    public_key, private_key = crypto.generate_keypair(bits=1024)
    
    print(f"📊 Public key size: {public_key.n.bit_length()} bits")
    print(f"📊 Public key (n): {str(public_key.n)[:50]}...")
    
    # Test numeric encryption
    message = 123456789
    print(f"\n📝 Original message: {message}")
    
    encrypted = crypto.encrypt(message, public_key)
    print(f"🔒 Encrypted: {str(encrypted)[:50]}...")
    
    decrypted = crypto.decrypt(encrypted, private_key)
    print(f"🔓 Decrypted: {decrypted}")
    print(f"✅ Success: {message == decrypted}")


def demo_secure_string_encryption():
    """Demo enkripsi string yang efficient dan secure"""
    print("\n" + "=" * 60)
    print("🔤 STRING ENCRYPTION - EFFICIENT & SECURE")
    print("=" * 60)
    
    crypto = SchmidtSamoa()
    
    # Generate keypair
    print("🔑 Generating keypair...")
    public_key, private_key = crypto.generate_keypair(bits=2048)  # Larger key for bigger strings
    
    # Test various strings
    test_strings = [
        "Hello, World!",
        "Schmidt-Samoa Cryptosystem 🔐",
        "This is a longer string that tests the efficiency of our new implementation",
        "Tes dengan karakter Unicode: 你好, مرحبا, こんにちは",
        "Numbers and symbols: 123!@#$%^&*()"
    ]
    
    for i, text in enumerate(test_strings, 1):
        print(f"\n🔤 Test {i}: '{text}'")
        print(f"   Length: {len(text)} characters")
        
        # Time the encryption
        start_time = time.time()
        encrypted = crypto.encrypt_string(text, public_key)
        encrypt_time = time.time() - start_time
        
        # Time the decryption  
        start_time = time.time()
        decrypted = crypto.decrypt_string(encrypted, private_key)
        decrypt_time = time.time() - start_time
        
        success = text == decrypted
        print(f"   🔒 Encrypted to single integer: {str(encrypted)[:40]}...")
        print(f"   🔓 Decrypted: '{decrypted}'")
        print(f"   ⏱️  Encrypt time: {encrypt_time:.6f}s")
        print(f"   ⏱️  Decrypt time: {decrypt_time:.6f}s")
        print(f"   ✅ Match: {success}")


def demo_large_string_handling():
    """Demo handling untuk string yang sangat besar"""
    print("\n" + "=" * 60)
    print("📚 LARGE STRING HANDLING") 
    print("=" * 60)
    
    crypto = SchmidtSamoa()
    public_key, private_key = crypto.generate_keypair(bits=2048)
    
    # Create a very large string
    large_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 100
    print(f"📏 Large text length: {len(large_text)} characters")
    
    try:
        # Try single encryption first
        print("\n🔄 Attempting single encryption...")
        encrypted = crypto.encrypt_string(large_text, public_key)
        decrypted = crypto.decrypt_string(encrypted, private_key)
        print("✅ Single encryption successful!")
        print(f"   Match: {large_text == decrypted}")
        
    except ValueError as e:
        print(f"❌ Single encryption failed: {e}")
        print("\n🔄 Using chunked encryption...")
        
        # Use chunked encryption for very large strings
        encrypted_chunks = crypto.encrypt_large_string(large_text, public_key)
        print(f"📦 Split into {len(encrypted_chunks)} chunks")
        
        decrypted = crypto.decrypt_large_string(encrypted_chunks, private_key)
        success = large_text == decrypted
        
        print(f"✅ Chunked encryption success: {success}")
        print(f"   Original length: {len(large_text)}")
        print(f"   Decrypted length: {len(decrypted)}")


def demo_security_improvements():
    """Demo menunjukkan perbaikan keamanan"""
    print("\n" + "=" * 60)
    print("🛡️  SECURITY IMPROVEMENTS DEMO")
    print("=" * 60)
    
    crypto = SchmidtSamoa()
    
    # Test different key sizes and their Miller-Rabin iterations
    key_sizes = [512, 1024, 1536, 2048]
    
    for bits in key_sizes:
        print(f"\n🔐 Testing {bits}-bit keys:")
        
        # Show Miller-Rabin iterations for this key size
        iterations = crypto._get_miller_rabin_iterations(bits)
        print(f"   🎯 Miller-Rabin iterations: {iterations}")
        
        # Generate keypair and time it
        start_time = time.time()
        public_key, private_key = crypto.generate_keypair(bits=bits)
        keygen_time = time.time() - start_time
        
        print(f"   ⏱️  Key generation time: {keygen_time:.4f}s")
        
        # Test with sample data
        test_msg = 12345
        encrypted = crypto.encrypt(test_msg, public_key)
        decrypted = crypto.decrypt(encrypted, private_key) 
        
        print(f"   ✅ Encryption test: {test_msg == decrypted}")


def demo_thread_safety():
    """Demo thread safety dengan stateless design"""
    print("\n" + "=" * 60)
    print("🧵 THREAD SAFETY DEMO")
    print("=" * 60)
    
    import threading
    import random
    
    crypto = SchmidtSamoa()
    
    # Generate multiple keypairs for concurrent use
    keypairs = []
    for i in range(3):
        public_key, private_key = crypto.generate_keypair(bits=512)  # Smaller for speed
        keypairs.append((public_key, private_key))
        print(f"🔑 Generated keypair {i+1}")
    
    results = []
    
    def worker(thread_id, keypair_id):
        """Worker function that encrypts/decrypts in separate thread"""
        public_key, private_key = keypairs[keypair_id]
        
        # Each thread uses different data
        test_data = f"Thread-{thread_id}-Data-{random.randint(1000, 9999)}"
        
        try:
            # Encrypt and decrypt
            encrypted = crypto.encrypt_string(test_data, public_key)
            decrypted = crypto.decrypt_string(encrypted, private_key)
            
            success = test_data == decrypted
            results.append((thread_id, success, test_data, decrypted))
            
        except Exception as e:
            results.append((thread_id, False, str(e), ""))
    
    # Start multiple threads
    threads = []
    for i in range(6):  # 6 threads, 3 keypairs
        keypair_id = i % 3
        thread = threading.Thread(target=worker, args=(i, keypair_id))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    # Check results
    print(f"\n📊 Results from {len(threads)} concurrent threads:")
    all_success = True
    for thread_id, success, original, decrypted in results:
        status = "✅" if success else "❌"
        print(f"   Thread {thread_id}: {status} {success}")
        if not success:
            all_success = False
    
    print(f"\n🎯 All threads successful: {all_success}")


def demo_error_handling():
    """Demo improved error handling"""
    print("\n" + "=" * 60)
    print("⚠️  ERROR HANDLING DEMO")
    print("=" * 60)
    
    crypto = SchmidtSamoa()
    
    # Test 1: Invalid key sizes
    print("🧪 Test 1: Invalid key sizes")
    try:
        crypto.generate_keypair(bits=32)  # Too small
    except ValueError as e:
        print(f"   ✅ Caught expected error: {e}")
    
    # Test 2: Message too large for key
    print("\n🧪 Test 2: Message larger than modulus")
    public_key, private_key = crypto.generate_keypair(bits=64)  # Small key for testing
    
    try:
        large_message = public_key.n + 1000
        crypto.encrypt(large_message, public_key)
    except ValueError as e:
        print(f"   ✅ Caught expected error: {e}")
    
    # Test 3: String too large for key
    print("\n🧪 Test 3: String too large for key size")
    try:
        very_long_string = "A" * 1000  # Very long string
        crypto.encrypt_string(very_long_string, public_key)
    except ValueError as e:
        print(f"   ✅ Caught expected error: {e}")
    
    # Test 4: Wrong key types
    print("\n🧪 Test 4: Wrong key types")
    try:
        crypto.encrypt(123, "not_a_key")  # Wrong type
    except TypeError as e:
        print(f"   ✅ Caught expected error: {e}")


def demo_convenience_functions():
    """Demo convenience functions untuk kemudahan penggunaan"""
    print("\n" + "=" * 60)
    print("🎯 CONVENIENCE FUNCTIONS DEMO")
    print("=" * 60)
    
    # Import convenience functions
    from schmidt_samoa import generate_keypair, encrypt, decrypt, encrypt_string, decrypt_string
    
    print("🔧 Using convenience functions for simpler syntax:")
    
    # Generate keypair using convenience function
    public_key, private_key = generate_keypair(bits=1024)
    print("✅ Generated keypair using convenience function")
    
    # Test numeric encryption
    message = 987654321
    encrypted = encrypt(message, public_key)
    decrypted = decrypt(encrypted, private_key)
    
    print(f"📊 Numeric test: {message} -> {encrypted} -> {decrypted}")
    print(f"✅ Numeric success: {message == decrypted}")
    
    # Test string encryption
    text = "Convenience functions make the API easier to use!"
    encrypted_str = encrypt_string(text, public_key)
    decrypted_str = decrypt_string(encrypted_str, private_key)
    
    print(f"📊 String test: '{text}'")
    print(f"✅ String success: {text == decrypted_str}")


def run_all_demos():
    """Jalankan semua demo"""
    print("🚀" * 25)
    print("🔐 SCHMIDT-SAMOA CRYPTOSYSTEM - SECURE VERSION DEMOS")
    print("🚀" * 25)
    
    demos = [
        demo_basic_usage,
        demo_secure_string_encryption,
        demo_large_string_handling,
        demo_security_improvements,
        demo_thread_safety,
        demo_error_handling,
        demo_convenience_functions
    ]
    
    for i, demo_func in enumerate(demos, 1):
        try:
            print(f"\n{'='*60}")
            print(f"🎯 RUNNING DEMO {i}/{len(demos)}")
            print(f"{'='*60}")
            demo_func()
        except Exception as e:
            print(f"\n❌ Error in demo {i}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "🎉" * 25)
    print("🔐 ALL SECURE DEMOS COMPLETED!")
    print("🎉" * 25)
    
    print("\n" + "📋 SUMMARY OF SECURITY IMPROVEMENTS:")
    print("✅ Replaced 'random' with 'secrets' module")
    print("✅ Implemented stateless, thread-safe design")
    print("✅ Added proper Miller-Rabin iterations based on key size")
    print("✅ Efficient string-to-integer conversion (no ECB mode)")
    print("✅ Removed all print() statements from library")
    print("✅ Added type-safe PublicKey and PrivateKey classes")
    print("✅ Comprehensive error handling")
    print("✅ Support for large string encryption via chunking")
    print("✅ Convenience functions for ease of use")


if __name__ == "__main__":
    run_all_demos()
