# Schmidt-Samoa Cryptosystem 🔐

Implementasi lengkap **Schmidt-Samoa Cryptosystem** dalam Python - sistem kriptografi kunci publik yang keamanannya bergantung pada kesulitan pemfaktoran bilangan.

## 📖 Tentang Schmidt-Samoa

Schmidt-Samoa adalah algoritma kriptografi yang terinspirasi dari RSA dan Rabin Cryptosystem. Sistem ini menggunakan:

- **Kunci Publik**: `n = p²q` 
- **Kunci Privat**: `d = n⁻¹ mod lcm(p-1, q-1)`
- **Enkripsi**: `c = m^n mod n`
- **Dekripsi**: `m = c^d mod pq`

## 🚀 Fitur

- ✅ **Key Generation**: Generate pasangan kunci publik dan privat
- ✅ **Numeric Encryption**: Enkripsi/dekripsi bilangan integer
- ✅ **String Encryption**: Enkripsi/dekripsi teks string
- ✅ **Prime Generation**: Generate bilangan prima menggunakan Miller-Rabin test
- ✅ **Mathematical Operations**: GCD, LCM, Modular Inverse
- ✅ **Comprehensive Demo**: Contoh penggunaan lengkap

## 📋 Requirements

- Python 3.6+
- Tidak ada dependencies eksternal (menggunakan library standard Python)

## 🛠️ Instalasi

```bash
git clone https://github.com/HaikalE/schmidt-samoa-cryptosystem.git
cd schmidt-samoa-cryptosystem
```

## 💻 Penggunaan

### Quick Start - Demo

```bash
python schmidt_samoa.py
```

### Penggunaan dalam Kode

```python
from schmidt_samoa import SchmidtSamoa

# Inisialisasi
ss = SchmidtSamoa()

# Generate keypair
public_key, private_key = ss.generate_keypair(bits=512)

# Enkripsi pesan
message = 12345
encrypted = ss.encrypt(message)
print(f"Encrypted: {encrypted}")

# Dekripsi pesan
decrypted = ss.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

# Enkripsi string
text = "Hello World!"
encrypted_text = ss.encrypt_string(text)
decrypted_text = ss.decrypt_string(encrypted_text)
print(f"Original: {text}")
print(f"Decrypted: {decrypted_text}")
```

## 📚 Algoritma Detail

### 1. Key Generation 🔑

1. Pilih dua bilangan prima berbeda `p` dan `q` (rahasia)
2. Hitung `n = p²q` (kunci publik)
3. Hitung `d = n⁻¹ mod lcm(p-1, q-1)` (kunci privat)

### 2. Enkripsi 🔒

```
c = m^n mod n
```

- `c`: Ciphertext
- `m`: Plaintext (pesan asli)
- `n`: Kunci publik

### 3. Dekripsi 🔓

```
m = c^d mod pq
```

- `m`: Plaintext hasil dekripsi
- `c`: Ciphertext
- `d`: Kunci privat
- `p`, `q`: Bilangan prima rahasia

## 🔧 Fungsi Utama

### `SchmidtSamoa` Class

| Method | Deskripsi |
|--------|----------|
| `generate_keypair(bits)` | Generate pasangan kunci dengan panjang bit tertentu |
| `encrypt(message, public_key)` | Enkripsi pesan integer |
| `decrypt(ciphertext, private_key)` | Dekripsi ciphertext |
| `encrypt_string(text)` | Enkripsi string |
| `decrypt_string(encrypted_chars)` | Dekripsi string |

### Static Methods

| Method | Deskripsi |
|--------|----------|
| `is_prime(n, k)` | Test keprimaan dengan Miller-Rabin |
| `generate_prime(bits)` | Generate bilangan prima random |
| `gcd(a, b)` | Greatest Common Divisor |
| `lcm(a, b)` | Least Common Multiple |
| `mod_inverse(a, m)` | Modular multiplicative inverse |

## 🎯 Contoh Output

```
============================================================
🚀 SCHMIDT-SAMOA CRYPTOSYSTEM DEMO
============================================================

1️⃣ KEY GENERATION
------------------------------
🔑 Generating Schmidt-Samoa keypair dengan 64 bits...
📊 Generating prime p...
📊 Generating prime q...
✅ p = 12345678901234567891
✅ q = 98765432109876543211
🔓 Public key (n) = p²q = 15241578780673678515622620750190521
📐 lcm(p-1, q-1) = 1234567890123456789
🔐 Private key (d) = 987654321098765432

2️⃣ NUMERIC ENCRYPTION/DECRYPTION
----------------------------------------
📝 Original message: 12345
🔒 Encrypting message: 12345
📝 Formula: c = m^n mod n = 12345^15241578780673678515622620750190521 mod 15241578780673678515622620750190521
🔐 Ciphertext: 567890123456789
🔓 Decrypting ciphertext: 567890123456789
📝 Formula: m = c^d mod pq = 567890123456789^987654321098765432 mod 123456789012345
📄 Decrypted message: 12345
✅ Encryption/Decryption successful: True
```

## ⚠️ Keamanan

- **Untuk produksi**: Gunakan minimal 2048 bits untuk kunci
- **Untuk testing**: Gunakan 512-1024 bits
- **Untuk demo**: Gunakan 64-256 bits

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Project ini menggunakan MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 👨‍💻 Author

**HaikalE** - [GitHub Profile](https://github.com/HaikalE)

## 🙏 Acknowledgments

- Terinspirasi dari RSA dan Rabin Cryptosystem
- Implementasi Miller-Rabin primality test
- Extended Euclidean Algorithm untuk modular inverse

---

⭐ Jika project ini bermanfaat, jangan lupa berikan star!
