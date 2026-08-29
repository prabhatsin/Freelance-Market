'''
argon2
bcrypt
pbkdf2_sha256 / pbkdf2_sha512
sha256_crypt / sha512_crypt

'''

# These are password-hashing algorithms/schemes.

# Passlib is a popular password-hashing library for Python,
# Passlib is a higher-level password-hashing library.

# Mental Model 
'''
ALGORITHM
    │
    ├── bcrypt
    ├── Argon2
    ├── PBKDF2
    └── scrypt

IMPLEMENTATION / PYTHON PACKAGE
    │
    ├── bcrypt
    └── argon2-cffi

ABSTRACTION LIBRARY
    │
    └── Passlib

YOUR APPLICATION
    │
    └── FastAPI authentication

'''

