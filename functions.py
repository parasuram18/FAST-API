from argon2 import PasswordHasher

ph = PasswordHasher()
hash = ph.hash("mysecret")

# Verify
try:
    isvalid = ph.verify(hash, "mysecret")
except:
    isvalid = False

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")

password = "$argon2id$v=19$m=65536,t=3,p=4$CWcMeoDuZlQIzOW8Jf5bQg$UwCB+YsV9A+9aRSsObKejhJaavt28Xy12ig2lzvcg8M" #pwd_context.hash('admin@123')

is_valid = pwd_context.verify('parasu@123', password)

print(is_valid)