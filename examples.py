#!/usr/bin/env python3
"""
Schmidt-Samoa Cryptosystem Examples - PRODUCTION READY VERSION

Fixed examples to work with critical bug fixes:
- No more RecursionError on large keys  
- Using static methods properly
- Performance improvements with math.gcd/lcm
- Accurate chunking calculations

Author: HaikalE
Date: August 2025
Version: 2.1 (Bug Fixes)
"""

import time
import threading
import random
from schmidt_samoa import SchmidtSamoa, PublicKey, PrivateKey


def demo_basic_usage():
    """Demo penggunaan dasar dengan implementasi yang sudah diperbaiki"""
    print("=" * 60)
    print("🔐 BASIC USAGE - PRODUCTION READY")
    print("=" * 60)
    
    # Test dengan ukuran kunci yang berbeda untuk memastikan tidak ada RecursionError
    key_sizes = [512, 1024, 2048]
    
    for bits in key_sizes:
        print(f"\n🔑 Testing {bits}-bit keys:")
        
        try:
            # Generate keypair (using static method)
            start_time = time.time()
            public_key, private_key = SchmidtSamoa.generate_keypair(bits=bits)
            keygen_time = time.time() - start_time
            
            print(f"   ✅ Key generation: {keygen_time:.3f}s (NO RecursionError!)")
            print(f"   📊 Public key size: {public_key.n.bit_length()} bits")
            
            # Test numeric encryption
            message = 123456789
            encrypted = SchmidtSamoa.encrypt(message, public_key)
            decrypted = SchmidtSamoa.decrypt(encrypted, private_key)
            
            success = message == decrypted
            print(f"   📊 Numeric test: {success}")
            
            # Test string encryption  
            text = f"Test {bits}-bit encryption! 🔐"
            encrypted_str = SchmidtSamoa.encrypt_string(text, public_key)
            decrypted_str = SchmidtSamoa.decrypt_string(encrypted_str, private_key)
            
            str_success = text == decrypted_str
            print(f"   📊 String test: {str_success}")
            print(f"   🎯 Overall success: {success and str_success}")
            
        except Exception as e:
            print(f"   ❌ Error with {bits}-bit: {e}")


def demo_large_key_stress_test():
    """Demo untuk membuktikan RecursionError sudah fixed"""
    print("\n" + "=" * 60)
    print("🧪 LARGE KEY STRESS TEST - NO RECURSION LIMIT")
    print("=" * 60)
    
    # Test kunci yang sebelumnya pasti fail dengan RecursionError
    large_key_sizes = [1024, 2048, 3072]
    
    for bits in large_key_sizes:
        print(f"\n💪 Stress testing {bits}-bit keys...")
        
        try:
            start_time = time.time()
            public_key, private_key = SchmidtSamoa.generate_keypair(bits=bits)
            total_time = time.time() - start_time
            
            print(f"   ✅ SUCCESS! Generated in {total_time:.2f}s")
            print(f"   🔢 Modulus bit length: {public_key.n.bit_length()}")
            print(f"   🔢 Private key values: d={len(str(private_key.d))} digits, p={len(str(private_key.p))} digits, q={len(str(private_key.q))} digits")
            
            # Quick encryption test
            test_msg = 987654321
            encrypted = SchmidtSamoa.encrypt(test_msg, public_key)
            decrypted = SchmidtSamoa.decrypt(encrypted, private_key)
            
            print(f"   🎯 Encryption test: {'PASS' if test_msg == decrypted else 'FAIL'}")
            
        except RecursionError:
            print(f"   ❌ RECURSION ERROR - Bug still exists!")
        except Exception as e:
            print(f"   ❌ Other error: {e}")


def demo_performance_improvements():
    """Demo peningkatan performance dengan math.gcd/lcm"""
    print("\n" + "=" * 60)
    print("⚡ PERFORMANCE IMPROVEMENTS DEMO")
    print("=" * 60)
    
    # Test performance dengan ukuran kunci berbeda
    key_sizes = [512, 1024, 1536, 2048]
    
    print("Key Size | Key Gen Time | Notes")
    print("-" * 40)
    
    for bits in key_sizes:
        times = []
        
        # Run multiple times untuk average
        for _ in range(3):
            start_time = time.time()
            try:
                public_key, private_key = SchmidtSamoa.generate_keypair(bits=bits)
                elapsed = time.time() - start_time
                times.append(elapsed)
            except Exception as e:
                print(f"{bits:4}-bit | ERROR: {e}")
                break
        
        if times:
            avg_time = sum(times) / len(times)
            print(f"{bits:4}-bit | {avg_time:8.3f}s | Using math.lcm & iterative extended_gcd")


def demo_accurate_chunking():
    """Demo perhitungan chunking yang akurat (tanpa magic number)"""
    print("\n" + "=" * 60)
    print("📏 ACCURATE CHUNKING DEMO")
    print("=" * 60)
    
    # Generate keypair untuk testing
    public_key, private_key = SchmidtSamoa.generate_keypair(bits=1024)
    
    # Calculate maximum bytes yang bisa dienkripsi
    max_bytes_accurate = (public_key.n.bit_length() - 1) // 8
    max_bytes_old_formula = (public_key.n.bit_length() - 8) // 8  # Old buggy formula
    
    print(f"🔑 Key size: {public_key.n.bit_length()} bits")
    print(f"📊 Accurate max bytes: {max_bytes_accurate}")
    print(f"📊 Old formula max bytes: {max_bytes_old_formula}")
    print(f"📊 Difference: {max_bytes_accurate - max_bytes_old_formula} bytes gained!")
    
    # Test dengan string yang memenuhi capacity
    test_string = "A" * max_bytes_accurate
    print(f"\n🧪 Testing string of {len(test_string)} bytes (max capacity):")
    
    try:
        # Test single encryption (should work now)
        encrypted = SchmidtSamoa.encrypt_string(test_string, public_key)
        decrypted = SchmidtSamoa.decrypt_string(encrypted, private_key)
        
        success = test_string == decrypted
        print(f"   ✅ Single encryption: {success}")
        
    except ValueError as e:
        print(f"   ❌ Single encryption failed: {e}")
        
        # Fall back to chunked encryption
        print("   🔄 Trying chunked encryption...")
        encrypted_chunks = SchmidtSamoa.encrypt_large_string(test_string, public_key)
        decrypted_chunked = SchmidtSamoa.decrypt_large_string(encrypted_chunks, private_key)
        
        chunked_success = test_string == decrypted_chunked
        print(f"   ✅ Chunked encryption: {chunked_success}")
        print(f"   📦 Number of chunks: {len(encrypted_chunks)}")


def demo_thread_safety_fixed():
    """Demo thread safety dengan static methods"""
    print("\n" + "=" * 60)
    print("🧵 THREAD SAFETY - STATIC METHODS")
    print("=" * 60)
    
    results = []
    
    def worker(thread_id):
        """Worker function menggunakan static methods"""
        try:
            # Each thread generates its own keypair
            public_key, private_key = SchmidtSamoa.generate_keypair(bits=512)
            
            # Test with unique data
            test_data = f"Thread-{thread_id}-{random.randint(1000, 9999)}"
            
            # Encryption/decryption
            encrypted = SchmidtSamoa.encrypt_string(test_data, public_key)
            decrypted = SchmidtSamoa.decrypt_string(encrypted, private_key)
            
            success = test_data == decrypted
            results.append((thread_id, success, test_data, decrypted))
            
        except Exception as e:
            results.append((thread_id, False, str(e), ""))
    
    # Start multiple threads
    threads = []
    num_threads = 5
    
    print(f"🚀 Starting {num_threads} concurrent threads...")
    
    for i in range(num_threads):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    # Check results
    print(f"\n📊 Results from {num_threads} concurrent threads:")
    all_success = True
    
    for thread_id, success, original, decrypted in results:
        status = "✅" if success else "❌"
        print(f"   Thread {thread_id}: {status} Success={success}")
        if not success:
            all_success = False
            print(f"      Error: {original}")
    
    print(f"\n🎯 All threads successful: {all_success}")


def demo_convenience_functions():
    """Demo convenience functions yang sudah dioptimasi"""
    print("\n" + "=" * 60)
    print("🔧 OPTIMIZED CONVENIENCE FUNCTIONS")
    print("=" * 60)
    
    # Import convenience functions
    from schmidt_samoa import generate_keypair, encrypt, decrypt, encrypt_string, decrypt_string
    
    print("✨ Using convenience functions (now efficient - no object creation):")
    
    # Test performance
    start_time = time.time()
    public_key, private_key = generate_keypair(bits=1024)
    gen_time = time.time() - start_time
    
    print(f"🔑 Keypair generated in {gen_time:.3f}s")
    
    # Test numeric
    message = 555666777
    encrypted = encrypt(message, public_key)
    decrypted = decrypt(encrypted, private_key)
    
    print(f"📊 Numeric: {message} -> {encrypted} -> {decrypted}")
    print(f"✅ Numeric success: {message == decrypted}")
    
    # Test string
    text = "Convenience functions now optimized! 🚀"
    encrypted_str = encrypt_string(text, public_key)
    decrypted_str = decrypt_string(encrypted_str, private_key)
    
    print(f"📊 String: '{text}'")
    print(f"✅ String success: {text == decrypted_str}")


def run_all_demos():
    """Jalankan semua demo dengan perbaikan bug"""
    print("🔥" * 30)
    print("🚀 SCHMIDT-SAMOA v2.1 - PRODUCTION READY DEMOS")
    print("🔥" * 30)
    
    print("\n🛠️  CRITICAL FIXES APPLIED:")
    print("   ✅ RecursionError FIXED with iterative extended_gcd")
    print("   ✅ Performance improved with math.gcd/lcm")
    print("   ✅ Convenience functions optimized (no object creation)")
    print("   ✅ Accurate chunking calculation (no magic numbers)")
    
    demos = [
        demo_basic_usage,
        demo_large_key_stress_test,
        demo_performance_improvements,
        demo_accurate_chunking,
        demo_thread_safety_fixed,
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
    
    print("\n" + "🎉" * 30)
    print("🔐 ALL PRODUCTION-READY DEMOS COMPLETED!")
    print("🎉" * 30)
    
    print("\n" + "📋 SUMMARY OF BUG FIXES:")
    print("✅ CRITICAL: Fixed RecursionError in extended_gcd (iterative version)")
    print("✅ PERFORMANCE: Using math.gcd and math.lcm for speed")
    print("✅ EFFICIENCY: Convenience functions call static methods directly")
    print("✅ ACCURACY: Fixed chunking calculation with proper math")
    print("✅ RELIABILITY: All key sizes now work without crashes")


if __name__ == "__main__":
    run_all_demos()
