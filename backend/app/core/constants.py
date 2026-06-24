"""Uygulama genelinde kullanılan sabitler. Magic number/string kullanmayız."""

# ----- JWT -----
JWT_ALGORITHM: str = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 saat

# ----- Parola hashleme (bcrypt) -----
BCRYPT_ROUNDS: int = 12
# bcrypt parolanın yalnızca ilk 72 byte'ını dikkate alır; daha uzun girdileri kırparız.
BCRYPT_MAX_PASSWORD_BYTES: int = 72

# ----- Parola politikası -----
MIN_PASSWORD_LENGTH: int = 8
MAX_PASSWORD_LENGTH: int = 128

# ----- Sayfalama (gelecekteki listeleme endpoint'leri için) -----
DEFAULT_PAGE_SIZE: int = 20
MAX_PAGE_SIZE: int = 100
