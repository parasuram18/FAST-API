from argon2 import PasswordHasher

ph = PasswordHasher()
hash = ph.hash("mysecret")

# Verify
try:
    isvalid = ph.verify(hash, "mysecret")
except:
    isvalid = False
print(isvalid)
