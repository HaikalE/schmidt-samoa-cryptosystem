#!/usr/bin/env python3
"""
Contoh-contoh penggunaan Schmidt-Samoa Cryptosystem

File ini berisi berbagai contoh implementasi dan use case untuk
Schmidt-Samoa Cryptosystem dengan berbagai ukuran kunci dan jenis data.
"""

from schmidt_samoa import SchmidtSamoa


def example_basic_usage():
    """
    Contoh penggunaan dasar Schmidt-Samoa
    """
    print("\n" + "=" * 50)
    print("📚 EXAMPLE 1: Basic Usage")
    print("=" * 50)
    
    ss = SchmidtSamoa()
    
    # Generate keypair dengan 256 bits
    public_key, private_key = ss.generate_keypair(bits=256)
    
    # Test dengan pesan sederhana
    message = 2024
    print(f"\n📝 Testing with message: {message}")
    
    encrypted = ss.encrypt(message)
    decrypted = ss.decrypt(encrypted)
    
    print(f"✅ Success: {message == decrypted}")


def example_string_encryption():
    """
    Contoh enkripsi string lengkap
    """
    print("\n" + "=" * 50)
    print("📚 EXAMPLE 2: String Encryption")
    print("=" * 50)
    
    ss = SchmidtSamoa()
    
    # Generate keypair
    public_key, private_key = ss.generate_keypair(bits=512)
    
    # Test berbagai string
    test_strings = [
        "Hello",
        "Python",
        "Crypto",
        "2025",
        "ABC123"
    ]
    
    for test_str in test_strings:
        print(f"\n🔤 Testing string: '{test_str}'")
        
        # Enkripsi
        encrypted = ss.encrypt_string(test_str)
        print(f"🔐 Encrypted length: {len(encrypted)} integers")
        
        # Dekripsi
        decrypted = ss.decrypt_string(encrypted)
        
        print(f"✅ Match: {test_str == decrypted}")
        print(f"   Original:  '{test_str}'")
        print(f"   Decrypted: '{decrypted}'")


def example_large_numbers():
    """
    Contoh dengan bilangan besar
    """
    print("\n" + "=" * 50)
    print("📚 EXAMPLE 3: Large Numbers")
    print("=" * 50)
    
    ss = SchmidtSamoa()
    
    # Generate keypair dengan 1024 bits untuk angka besar
    public_key, private_key = ss.generate_keypair(bits=1024)
    
    # Test dengan berbagai ukuran angka
    test_numbers = [
        123,
        123456,
        123456789,
        123456789012345
    ]
    
    for num in test_numbers:
        print(f"\n🔢 Testing number: {num}")
        print(f"   Digits: {len(str(num))}")
        
        try:
            encrypted = ss.encrypt(num)
            decrypted = ss.decrypt(encrypted)
            
            print(f"✅ Success: {num == decrypted}")
            print(f"   Encrypted: {str(encrypted)[:50]}{'...' if len(str(encrypted)) > 50 else ''}")
            
        except ValueError as e:
            print(f"❌ Error: {e}")


def example_performance_test():
    """
    Test performa dengan berbagai ukuran kunci
    """
    print("\n" + "=" * 50)
    print("📚 EXAMPLE 4: Performance Test")
    print("=" * 50)
    
    import time
    
    key_sizes = [64, 128, 256, 512]
    test_message = 12345
    
    for bits in key_sizes:
        print(f"\n⚡ Testing with {bits}-bit keys")
        
        ss = SchmidtSamoa()
        
        # Measure key generation time
        start_time = time.time()
        public_key, private_key = ss.generate_keypair(bits=bits)
        keygen_time = time.time() - start_time
        
        # Measure encryption time
        start_time = time.time()
        encrypted = ss.encrypt(test_message)
        encrypt_time = time.time() - start_time
        
        # Measure decryption time
        start_time = time.time()
        decrypted = ss.decrypt(encrypted)
        decrypt_time = time.time() - start_time
        
        print(f"   Key Generation: {keygen_time:.4f}s")
        print(f"   Encryption:     {encrypt_time:.4f}s")
        print(f"   Decryption:     {decrypt_time:.4f}s")
        print(f"   Total:          {(keygen_time + encrypt_time + decrypt_time):.4f}s")
        print(f"   Success:        {test_message == decrypted}")


def example_key_reuse():
    """
    Contoh penggunaan ulang kunci untuk multiple enkripsi
    """
    print("\n" + "=" * 50)
    print("📚 EXAMPLE 5: Key Reuse")
    print("=" * 50)
    
    ss = SchmidtSamoa()
    
    # Generate keypair sekali
    print("🔑 Generating keypair...")
    public_key, private_key = ss.generate_keypair(bits=512)
    
    # Gunakan kunci yang sama untuk multiple enkripsi
    messages = [100, 200, 300, 400, 500]
    
    print("\n📦 Encrypting multiple messages with same keypair:")
    
    encrypted_messages = []
    for i, msg in enumerate(messages, 1):
        print(f"\n   Message {i}: {msg}")
        
        encrypted = ss.encrypt(msg, public_key)
        encrypted_messages.append(encrypted)
        
        decrypted = ss.decrypt(encrypted, private_key)
        print(f"   Encrypted: {str(encrypted)[:30]}...")
        print(f"   Decrypted: {decrypted}")
        print(f"   Match: {msg == decrypted}")
    
    print(f"\n✅ All {len(messages)} messages processed successfully!")


def example_error_handling():
    """
    Contoh error handling
    """
    print("\n" + "=" * 50)
    print("📚 EXAMPLE 6: Error Handling")
    print("=" * 50)
    
    ss = SchmidtSamoa()
    
    # Generate keypair kecil untuk demo error
    public_key, private_key = ss.generate_keypair(bits=64)
    
    print(f"\n🔑 Generated public key: {public_key}")
    
    # Test 1: Message terlalu besar
    print("\n🚫 Test 1: Message larger than n")
    try:
        large_message = public_key + 1000
        print(f"   Trying to encrypt: {large_message}")
        ss.encrypt(large_message)
    except ValueError as e:
        print(f"   ❌ Caught expected error: {e}")
    
    # Test 2: Encrypt tanpa keypair
    print("\n🚫 Test 2: Encrypt without keypair")
    try:
        ss_new = SchmidtSamoa()
        ss_new.encrypt(123)
    except ValueError as e:
        print(f"   ❌ Caught expected error: {e}")
    
    # Test 3: Decrypt tanpa keypair
    print("\n🚫 Test 3: Decrypt without keypair")
    try:
        ss_new = SchmidtSamoa()
        ss_new.decrypt(12345)
    except ValueError as e:
        print(f"   ❌ Caught expected error: {e}")
    
    print("\n✅ Error handling examples completed")


def run_all_examples():
    """
    Jalankan semua contoh
    """
    print("🎯" * 20)
    print("🚀 SCHMIDT-SAMOA CRYPTOSYSTEM - ALL EXAMPLES")
    print("🎯" * 20)
    
    examples = [
        example_basic_usage,
        example_string_encryption,
        example_large_numbers,
        example_performance_test,
        example_key_reuse,
        example_error_handling
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"\n❌ Error in example {i}: {e}")
    
    print("\n" + "🎯" * 20)
    print("🎉 ALL EXAMPLES COMPLETED!")
    print("🎯" * 20)


if __name__ == "__main__":
    run_all_examples()
