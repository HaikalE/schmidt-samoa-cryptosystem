#!/usr/bin/env python3
"""
Schmidt-Samoa Cryptosystem Implementation - SECURE VERSION

Implementasi yang telah diperbaiki berdasarkan analisis keamanan:
- Menggunakan secrets module untuk cryptographically secure random
- Stateless design untuk thread safety
- Efficient string encryption
- No print statements dalam library
- Improved Miller-Rabin parameters

Author: HaikalE  
Date: August 2025
Version: 2.0 (Security Hardened)
"""

import secrets
import math
from typing import Tuple, Optional, NamedTuple
from dataclasses import dataclass


@dataclass(frozen=True)
class PublicKey:
    """Schmidt-Samoa public key: n = p²q"""
    n: int
    
    def __post_init__(self):
        if self.n <= 1:
            raise ValueError("Public key n must be > 1")


@dataclass(frozen=True) 
class PrivateKey:
    """Schmidt-Samoa private key: (d, p, q)"""
    d: int
    p: int 
    q: int
    
    def __post_init__(self):
        if self.d <= 0 or self.p <= 1 or self.q <= 1:
            raise ValueError("Invalid private key parameters")


class SchmidtSamoa:
    """
    Stateless Schmidt-Samoa Cryptosystem Implementation
    
    This is a secure, thread-safe implementation with:
    - Cryptographically secure random number generation
    - Proper Miller-Rabin parameters based on key size
    - Efficient string-to-integer conversion
    - Clean library interface without side effects
    """
    
    @staticmethod
    def _get_miller_rabin_iterations(bits: int) -> int:
        """
        Get appropriate number of Miller-Rabin iterations based on key size
        
        Based on FIPS 186-4 recommendations:
        - ≤ 512 bits: 64 iterations
        - 513-1024 bits: 32 iterations  
        - 1025-1536 bits: 16 iterations
        - > 1536 bits: 8 iterations
        """
        if bits <= 512:
            return 64
        elif bits <= 1024:
            return 32
        elif bits <= 1536:
            return 16
        else:
            return 8
    
    @staticmethod
    def is_prime(n: int, k: Optional[int] = None) -> bool:
        """
        Miller-Rabin primality test with security-appropriate iterations
        
        Args:
            n: Number to test for primality
            k: Number of iterations (auto-determined if None)
            
        Returns:
            bool: True if n is probably prime, False if composite
        """
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        
        # Auto-determine k based on bit length if not specified
        if k is None:
            k = SchmidtSamoa._get_miller_rabin_iterations(n.bit_length())
        
        # Write n-1 as d * 2^r
        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        # Perform k Miller-Rabin tests
        for _ in range(k):
            a = secrets.randbelow(n - 2) + 2  # Random in [2, n-2]
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
        Generate cryptographically secure prime number
        
        Args:
            bits: Desired bit length
            
        Returns:
            int: Prime number of specified bit length
        """
        if bits < 2:
            raise ValueError("Bit length must be at least 2")
            
        while True:
            # Use secrets for cryptographically secure random generation
            n = secrets.randbits(bits)
            # Ensure it's odd and has correct bit length
            n |= (1 << (bits - 1)) | 1  # Set MSB and LSB
            
            if SchmidtSamoa.is_prime(n):
                return n
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Euclidean algorithm for GCD"""
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Least Common Multiple"""
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // SchmidtSamoa.gcd(a, b)
    
    @staticmethod
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm
        
        Returns:
            Tuple[gcd, x, y] where ax + by = gcd(a, b)
        """
        if a == 0:
            return b, 0, 1
        
        gcd, x1, y1 = SchmidtSamoa.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        
        return gcd, x, y
    
    @staticmethod
    def mod_inverse(a: int, m: int) -> int:
        """
        Modular multiplicative inverse
        
        Args:
            a: Number to find inverse of
            m: Modulus
            
        Returns:
            int: Inverse of a modulo m
            
        Raises:
            ValueError: If inverse doesn't exist
        """
        if m <= 0:
            raise ValueError("Modulus must be positive")
            
        gcd, x, _ = SchmidtSamoa.extended_gcd(a % m, m)
        
        if gcd != 1:
            raise ValueError(f"Modular inverse of {a} mod {m} doesn't exist (gcd = {gcd})")
        
        return (x % m + m) % m
    
    def generate_keypair(self, bits: int = 1024) -> Tuple[PublicKey, PrivateKey]:
        """
        Generate Schmidt-Samoa keypair
        
        Args:
            bits: Bit length for prime generation (default: 1024)
            
        Returns:
            Tuple[PublicKey, PrivateKey]: Generated keypair
            
        Raises:
            ValueError: If parameters are invalid
        """
        if bits < 64:
            raise ValueError("Minimum key size is 64 bits (for testing only)")
        if bits < 1024:
            # Warning for production use could be logged here
            pass
            
        # Generate two distinct primes
        p = self.generate_prime(bits)
        q = self.generate_prime(bits)
        
        # Ensure p != q (extremely unlikely but good practice)
        while q == p:
            q = self.generate_prime(bits)
        
        # Calculate n = p²q (public key)
        n = (p * p) * q
        
        # Calculate private key d = n^(-1) mod lcm(p-1, q-1)
        lcm_val = self.lcm(p - 1, q - 1)
        d = self.mod_inverse(n, lcm_val)
        
        public_key = PublicKey(n=n)
        private_key = PrivateKey(d=d, p=p, q=q)
        
        return public_key, private_key
    
    def encrypt(self, message: int, public_key: PublicKey) -> int:
        """
        Encrypt integer message using Schmidt-Samoa
        
        Formula: c = m^n mod n
        
        Args:
            message: Plaintext integer (must be < n)
            public_key: Public key for encryption
            
        Returns:
            int: Ciphertext
            
        Raises:
            ValueError: If message >= n
        """
        if not isinstance(public_key, PublicKey):
            raise TypeError("public_key must be PublicKey instance")
        
        if message < 0:
            raise ValueError("Message must be non-negative")
        if message >= public_key.n:
            raise ValueError(f"Message must be < n ({public_key.n})")
        
        return pow(message, public_key.n, public_key.n)
    
    def decrypt(self, ciphertext: int, private_key: PrivateKey) -> int:
        """
        Decrypt ciphertext using Schmidt-Samoa
        
        Formula: m = c^d mod pq
        
        Args:
            ciphertext: Encrypted integer
            private_key: Private key for decryption
            
        Returns:
            int: Decrypted plaintext
        """
        if not isinstance(private_key, PrivateKey):
            raise TypeError("private_key must be PrivateKey instance")
        
        if ciphertext < 0:
            raise ValueError("Ciphertext must be non-negative")
            
        pq = private_key.p * private_key.q
        return pow(ciphertext, private_key.d, pq)
    
    def encrypt_string(self, text: str, public_key: PublicKey, encoding: str = 'utf-8') -> int:
        """
        Encrypt string by converting to single large integer
        
        This is much more secure and efficient than per-character encryption
        as it avoids ECB-mode vulnerabilities.
        
        Args:
            text: String to encrypt
            public_key: Public key for encryption
            encoding: Text encoding (default: utf-8)
            
        Returns:
            int: Encrypted integer representing the entire string
            
        Raises:
            ValueError: If string is too large for the key size
        """
        if not text:
            raise ValueError("Cannot encrypt empty string")
            
        # Convert string to bytes then to integer
        text_bytes = text.encode(encoding)
        text_int = int.from_bytes(text_bytes, 'big')
        
        # Check if integer fits in key space
        if text_int >= public_key.n:
            max_bytes = (public_key.n.bit_length() - 1) // 8
            raise ValueError(f"String too large. Maximum {max_bytes} bytes for this key size")
        
        return self.encrypt(text_int, public_key)
    
    def decrypt_string(self, encrypted_int: int, private_key: PrivateKey, encoding: str = 'utf-8') -> str:
        """
        Decrypt integer back to string
        
        Args:
            encrypted_int: Encrypted integer
            private_key: Private key for decryption
            encoding: Text encoding (default: utf-8)
            
        Returns:
            str: Decrypted string
        """
        # Decrypt to integer
        decrypted_int = self.decrypt(encrypted_int, private_key)
        
        # Convert integer back to bytes
        if decrypted_int == 0:
            return ''
            
        # Calculate number of bytes needed
        num_bytes = (decrypted_int.bit_length() + 7) // 8
        decrypted_bytes = decrypted_int.to_bytes(num_bytes, 'big')
        
        # Convert bytes back to string
        return decrypted_bytes.decode(encoding)
    
    def encrypt_large_string(self, text: str, public_key: PublicKey, encoding: str = 'utf-8') -> list:
        """
        Encrypt large string by splitting into chunks
        
        For strings too large to fit in a single encryption operation.
        
        Args:
            text: String to encrypt
            public_key: Public key for encryption
            encoding: Text encoding (default: utf-8)
            
        Returns:
            list: List of encrypted chunks
        """
        if not text:
            return []
            
        # Calculate max chunk size in bytes (leave some safety margin)
        max_bytes = (public_key.n.bit_length() - 8) // 8  # -8 bits for safety
        
        text_bytes = text.encode(encoding)
        chunks = []
        
        # Split into chunks
        for i in range(0, len(text_bytes), max_bytes):
            chunk = text_bytes[i:i + max_bytes]
            chunk_int = int.from_bytes(chunk, 'big')
            encrypted_chunk = self.encrypt(chunk_int, public_key)
            chunks.append(encrypted_chunk)
        
        return chunks
    
    def decrypt_large_string(self, encrypted_chunks: list, private_key: PrivateKey, encoding: str = 'utf-8') -> str:
        """
        Decrypt list of encrypted chunks back to string
        
        Args:
            encrypted_chunks: List of encrypted integer chunks
            private_key: Private key for decryption
            encoding: Text encoding (default: utf-8)
            
        Returns:
            str: Decrypted string
        """
        if not encrypted_chunks:
            return ''
            
        decrypted_bytes = b''
        
        for encrypted_chunk in encrypted_chunks:
            decrypted_int = self.decrypt(encrypted_chunk, private_key)
            
            if decrypted_int == 0:
                continue
                
            # Convert integer back to bytes
            num_bytes = (decrypted_int.bit_length() + 7) // 8
            chunk_bytes = decrypted_int.to_bytes(num_bytes, 'big')
            decrypted_bytes += chunk_bytes
        
        return decrypted_bytes.decode(encoding)


# Convenience functions for backward compatibility and ease of use
def generate_keypair(bits: int = 1024) -> Tuple[PublicKey, PrivateKey]:
    """Convenience function to generate keypair"""
    return SchmidtSamoa().generate_keypair(bits)


def encrypt(message: int, public_key: PublicKey) -> int:
    """Convenience function to encrypt integer"""
    return SchmidtSamoa().encrypt(message, public_key)


def decrypt(ciphertext: int, private_key: PrivateKey) -> int:
    """Convenience function to decrypt integer"""
    return SchmidtSamoa().decrypt(ciphertext, private_key)


def encrypt_string(text: str, public_key: PublicKey) -> int:
    """Convenience function to encrypt string"""
    return SchmidtSamoa().encrypt_string(text, public_key)


def decrypt_string(encrypted_int: int, private_key: PrivateKey) -> str:
    """Convenience function to decrypt string"""
    return SchmidtSamoa().decrypt_string(encrypted_int, private_key)
