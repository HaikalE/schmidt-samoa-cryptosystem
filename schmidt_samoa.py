#!/usr/bin/env python3
"""
Schmidt-Samoa Cryptosystem Implementation

Algoritma Schmidt-Samoa adalah sistem kriptografi kunci publik yang keamanannya 
bergantung pada kesulitan pemfaktoran bilangan. Algoritme ini terinspirasi dari 
RSA dan Rabin Cryptosystem.

Author: HaikalE
Date: August 2025
"""

import random
import math
from typing import Tuple, Optional


class SchmidtSamoa:
    """
    Implementasi Schmidt-Samoa Cryptosystem
    
    Sistem kriptografi kunci publik dengan:
    - Kunci publik: n = p²q
    - Kunci privat: d = n^(-1) mod lcm(p-1, q-1)
    - Enkripsi: c = m^n mod n
    - Dekripsi: m = c^d mod pq
    """
    
    def __init__(self):
        self.public_key = None
        self.private_key = None
        self.p = None
        self.q = None
        self.n = None
        self.d = None
    
    @staticmethod
    def is_prime(n: int, k: int = 5) -> bool:
        """
        Test Miller-Rabin untuk menguji keprimaan bilangan
        
        Args:
            n: Bilangan yang akan diuji
            k: Jumlah iterasi test (default: 5)
            
        Returns:
            bool: True jika n kemungkinan prima, False jika komposit
        """
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        
        # Tulis n-1 sebagai d * 2^r
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Miller-Rabin test
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            
            if x == 1 or x == n - 1:
                continue
                
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
                
        return True
    
    @staticmethod
    def generate_prime(bits: int) -> int:
        """
        Generate bilangan prima random dengan panjang bit tertentu
        
        Args:
            bits: Panjang bit yang diinginkan
            
        Returns:
            int: Bilangan prima
        """
        while True:
            # Generate random odd number
            n = random.getrandbits(bits)
            n |= (1 << bits - 1) | 1  # Set MSB dan LSB ke 1
            
            if SchmidtSamoa.is_prime(n):
                return n
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Algoritma Euclidean untuk mencari GCD
        """
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """
        Least Common Multiple
        """
        return abs(a * b) // SchmidtSamoa.gcd(a, b)
    
    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm
        
        Returns:
            Tuple[gcd, x, y] dimana ax + by = gcd(a, b)
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = SchmidtSamoa.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    @staticmethod
    def mod_inverse(a: int, m: int) -> Optional[int]:
        """
        Modular multiplicative inverse
        
        Args:
            a: Bilangan yang akan dicari inversnya
            m: Modulus
            
        Returns:
            int: Inverse dari a modulo m, atau None jika tidak ada
        """
        gcd, x, _ = SchmidtSamoa.extended_gcd(a % m, m)
        
        if gcd != 1:
            return None
        
        return (x % m + m) % m
    
    def generate_keypair(self, bits: int = 512) -> Tuple[int, Tuple[int, int, int]]:
        """
        Generate pasangan kunci Schmidt-Samoa
        
        Args:
            bits: Panjang bit untuk bilangan prima (default: 512)
            
        Returns:
            Tuple[public_key, (private_key, p, q)]
        """
        print(f"🔑 Generating Schmidt-Samoa keypair dengan {bits} bits...")
        
        # Step 1: Pilih dua bilangan prima berbeda p dan q
        print("📊 Generating prime p...")
        self.p = self.generate_prime(bits)
        
        print("📊 Generating prime q...")
        while True:
            self.q = self.generate_prime(bits)
            if self.q != self.p:  # Pastikan p dan q berbeda
                break
        
        print(f"✅ p = {self.p}")
        print(f"✅ q = {self.q}")
        
        # Step 2: Hitung n = p²q (kunci publik)
        self.n = (self.p ** 2) * self.q
        print(f"🔓 Public key (n) = p²q = {self.n}")
        
        # Step 3: Hitung kunci privat d = n^(-1) mod lcm(p-1, q-1)
        lcm_val = self.lcm(self.p - 1, self.q - 1)
        print(f"📐 lcm(p-1, q-1) = {lcm_val}")
        
        self.d = self.mod_inverse(self.n, lcm_val)
        if self.d is None:
            raise ValueError("Tidak dapat menghitung modular inverse")
        
        print(f"🔐 Private key (d) = {self.d}")
        
        self.public_key = self.n
        self.private_key = (self.d, self.p, self.q)
        
        return self.public_key, self.private_key
    
    def encrypt(self, message: int, public_key: Optional[int] = None) -> int:
        """
        Enkripsi pesan menggunakan Schmidt-Samoa
        
        Formula: c = m^n mod n
        
        Args:
            message: Pesan yang akan dienkripsi (integer)
            public_key: Kunci publik (opsional, gunakan yang sudah di-generate)
            
        Returns:
            int: Ciphertext
        """
        if public_key is None:
            if self.public_key is None:
                raise ValueError("Public key belum di-generate")
            public_key = self.public_key
        
        if message >= public_key:
            raise ValueError(f"Message harus lebih kecil dari n ({public_key})")
        
        print(f"🔒 Encrypting message: {message}")
        print(f"📝 Formula: c = m^n mod n = {message}^{public_key} mod {public_key}")
        
        ciphertext = pow(message, public_key, public_key)
        print(f"🔐 Ciphertext: {ciphertext}")
        
        return ciphertext
    
    def decrypt(self, ciphertext: int, private_key: Optional[Tuple[int, int, int]] = None) -> int:
        """
        Dekripsi ciphertext menggunakan Schmidt-Samoa
        
        Formula: m = c^d mod pq
        
        Args:
            ciphertext: Ciphertext yang akan didekripsi
            private_key: Tuple (d, p, q) kunci privat
            
        Returns:
            int: Plaintext yang sudah didekripsi
        """
        if private_key is None:
            if self.private_key is None:
                raise ValueError("Private key belum di-generate")
            private_key = self.private_key
        
        d, p, q = private_key
        pq = p * q
        
        print(f"🔓 Decrypting ciphertext: {ciphertext}")
        print(f"📝 Formula: m = c^d mod pq = {ciphertext}^{d} mod {pq}")
        
        plaintext = pow(ciphertext, d, pq)
        print(f"📄 Decrypted message: {plaintext}")
        
        return plaintext
    
    def encrypt_string(self, text: str, public_key: Optional[int] = None) -> list:
        """
        Enkripsi string dengan mengenkripsi setiap karakter
        
        Args:
            text: String yang akan dienkripsi
            public_key: Kunci publik (opsional)
            
        Returns:
            list: List ciphertext untuk setiap karakter
        """
        print(f"🔤 Encrypting string: '{text}'")
        encrypted_chars = []
        
        for i, char in enumerate(text):
            ascii_val = ord(char)
            encrypted = self.encrypt(ascii_val, public_key)
            encrypted_chars.append(encrypted)
            print(f"  '{char}' (ASCII {ascii_val}) -> {encrypted}")
        
        return encrypted_chars
    
    def decrypt_string(self, encrypted_chars: list, private_key: Optional[Tuple[int, int, int]] = None) -> str:
        """
        Dekripsi list ciphertext menjadi string
        
        Args:
            encrypted_chars: List ciphertext
            private_key: Kunci privat (opsional)
            
        Returns:
            str: String yang sudah didekripsi
        """
        print(f"🔤 Decrypting encrypted characters...")
        decrypted_text = ""
        
        for i, encrypted in enumerate(encrypted_chars):
            decrypted_ascii = self.decrypt(encrypted, private_key)
            char = chr(decrypted_ascii)
            decrypted_text += char
            print(f"  {encrypted} -> {decrypted_ascii} ('{char}')")
        
        print(f"📄 Decrypted string: '{decrypted_text}'")
        return decrypted_text


def demo():
    """
    Demonstrasi penggunaan Schmidt-Samoa Cryptosystem
    """
    print("=" * 60)
    print("🚀 SCHMIDT-SAMOA CRYPTOSYSTEM DEMO")
    print("=" * 60)
    
    # Inisialisasi
    ss = SchmidtSamoa()
    
    # Generate keypair
    print("\n1️⃣ KEY GENERATION")
    print("-" * 30)
    public_key, private_key = ss.generate_keypair(bits=64)  # Gunakan bit kecil untuk demo
    
    # Test enkripsi/dekripsi angka
    print("\n2️⃣ NUMERIC ENCRYPTION/DECRYPTION")
    print("-" * 40)
    
    test_message = 12345
    print(f"📝 Original message: {test_message}")
    
    # Enkripsi
    encrypted = ss.encrypt(test_message)
    
    # Dekripsi
    decrypted = ss.decrypt(encrypted)
    
    print(f"✅ Encryption/Decryption successful: {test_message == decrypted}")
    
    # Test enkripsi/dekripsi string
    print("\n3️⃣ STRING ENCRYPTION/DECRYPTION")
    print("-" * 38)
    
    test_string = "HELLO"
    print(f"📝 Original string: '{test_string}'")
    
    # Enkripsi string
    encrypted_string = ss.encrypt_string(test_string)
    print(f"🔐 Encrypted: {encrypted_string}")
    
    # Dekripsi string
    decrypted_string = ss.decrypt_string(encrypted_string)
    
    print(f"✅ String encryption/decryption successful: {test_string == decrypted_string}")
    
    print("\n" + "=" * 60)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    demo()
