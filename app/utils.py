from passlib.context import CryptContext

# ---------------------------------------------------------
# Password Security Setup
# ---------------------------------------------------------

# We use 'pbkdf2_sha256' to avoid version conflicts/errors with bcrypt
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    Checks if the password typed by the user matches the hash in the DB.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Converts a plain text password into a secure hash.
    """
    return pwd_context.hash(password)