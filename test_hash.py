from hashlib import md5, sha256

# Test password
password = "test123"

# Current MD5 implementation
md5_hash = md5(password.encode('utf-8')).hexdigest()

# New SHA256 implementation
sha256_hash = sha256(password.encode('utf-8')).hexdigest()

print(f"Password: {password}")
print(f"Current MD5 hash: {md5_hash} (length: {len(md5_hash)})")
print(f"New SHA256 hash: {sha256_hash} (length: {len(sha256_hash)})")