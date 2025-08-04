# Changelog

All notable changes to the Schmidt-Samoa Cryptosystem implementation will be documented in this file.

## [2.0.0] - 2025-08-04 - MAJOR SECURITY UPDATE 🔥

### 🚨 CRITICAL SECURITY FIXES

#### Fixed
- **CRITICAL**: Replaced `random` module with `secrets` module for cryptographically secure random number generation
  - **Impact**: Previous versions had predictable random numbers that could compromise key generation
  - **Risk Level**: CRITICAL - All keys generated with v1.x are potentially vulnerable
  
- **CRITICAL**: Fixed ECB-mode vulnerability in string encryption
  - **Impact**: Previous per-character encryption leaked patterns in plaintext
  - **Risk Level**: HIGH - String encryption was vulnerable to frequency analysis

#### Changed
- **BREAKING**: Complete API redesign from stateful to stateless architecture
  - **Old API**: `ss.encrypt(message)` using internal state
  - **New API**: `crypto.encrypt(message, public_key)` with explicit parameters
  - **Impact**: Thread-safe, no race conditions, explicit parameter passing

- **BREAKING**: Miller-Rabin primality test now uses adaptive iterations based on key size
  - **512-bit keys**: 64 iterations (was 5)
  - **1024-bit keys**: 32 iterations (was 5) 
  - **2048-bit keys**: 16 iterations (was 5)
  - **Impact**: Much stronger primality testing, reduces composite number acceptance

- **BREAKING**: String encryption now converts entire string to single integer
  - **Old**: Per-character encryption (vulnerable to patterns)
  - **New**: String-to-integer conversion then single encryption
  - **Impact**: More secure, more efficient, pattern-resistant

#### Added
- Type-safe `PublicKey` and `PrivateKey` dataclasses
- Large string support via chunked encryption (`encrypt_large_string`)
- Comprehensive error handling with specific exception types
- Convenience functions for simplified API usage
- Thread safety validation and examples
- Security parameter recommendations based on key size

#### Removed
- **BREAKING**: All `print()` statements from library code
  - **Impact**: Clean library interface, no unexpected console output
- **BREAKING**: Internal state storage (`self.p`, `self.q`, `self.n`, `self.d`)
  - **Impact**: Stateless design, thread-safe operation

### 📚 Documentation Updates

#### Added
- Comprehensive security documentation
- Migration guide from v1.x to v2.x
- Thread safety examples
- Performance benchmarks
- Security parameter recommendations
- API reference with type annotations

### 🧪 Testing Improvements

#### Added
- Thread safety demonstration
- Large string handling examples
- Error handling test cases
- Performance benchmarks across different key sizes
- Security parameter validation

### 📁 File Structure Changes

#### Added
- `demo.py` - Simple demonstration script
- `CHANGELOG.md` - This changelog
- Enhanced `examples.py` with security-focused demos

#### Modified
- `schmidt_samoa.py` - Complete rewrite with security fixes
- `README.md` - Updated with security warnings and new API
- `examples.py` - Updated to demonstrate secure API

## [1.0.0] - 2025-08-04 - Initial Release ⚠️  DEPRECATED

### ⚠️ SECURITY WARNING
**This version contains critical security vulnerabilities and should not be used in production or security-sensitive applications.**

#### Known Vulnerabilities
- Uses `random` module instead of `secrets` (predictable random numbers)
- Stateful design with race condition vulnerabilities  
- ECB-mode string encryption (pattern leakage)
- Insufficient Miller-Rabin iterations (weak primality testing)
- Library side effects (print statements)

#### Features (Vulnerable Implementation)
- Basic Schmidt-Samoa key generation
- Integer encryption/decryption
- String encryption (insecure per-character method)
- Basic examples and documentation

---

## Migration Guide: v1.x → v2.x

### Critical Action Required
1. **REGENERATE ALL KEYS**: Keys generated with v1.x may be compromised
2. **UPDATE CODE**: API has breaking changes requiring code updates
3. **SECURITY REVIEW**: Review all applications using v1.x for potential compromise

### Code Migration Examples

#### Key Generation
```python
# v1.x (INSECURE)
ss = SchmidtSamoa()
public_key, private_key = ss.generate_keypair()

# v2.x (SECURE)
crypto = SchmidtSamoa()
public_key, private_key = crypto.generate_keypair(bits=2048)
```

#### Encryption
```python
# v1.x (INSECURE - uses internal state)
encrypted = ss.encrypt(message)
decrypted = ss.decrypt(encrypted)

# v2.x (SECURE - explicit parameters)
encrypted = crypto.encrypt(message, public_key)
decrypted = crypto.decrypt(encrypted, private_key)
```

#### String Encryption
```python
# v1.x (INSECURE - ECB mode vulnerability)
encrypted_chars = ss.encrypt_string("hello")
decrypted = ss.decrypt_string(encrypted_chars)

# v2.x (SECURE - single integer conversion)
encrypted_int = crypto.encrypt_string("hello", public_key)
decrypted = crypto.decrypt_string(encrypted_int, private_key)
```

### Compatibility
- **Python**: Minimum version increased to 3.7+ (for dataclasses)
- **API**: Complete breaking changes, no backward compatibility
- **Performance**: Significantly improved for string operations
- **Security**: All critical vulnerabilities fixed

---

## Security Disclosure

If you discover a security vulnerability in this implementation, please report it responsibly:

1. **DO NOT** create a public GitHub issue
2. Contact the maintainer directly via GitHub
3. Provide detailed information about the vulnerability
4. Allow time for fix development before public disclosure

## Acknowledgments

Special thanks to the security researcher who provided the comprehensive security analysis that led to these critical improvements. Their detailed critique transformed this from a "toy example" into a production-ready cryptographic library.
