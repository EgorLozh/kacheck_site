import bcrypt
import hashlib


class PasswordService:
    """Service for password hashing and verification using bcrypt."""

    # Bcrypt cost factor (rounds = 2^cost)
    # 12 is a good balance between security and performance
    BCRYPT_ROUNDS = 12
    # Bcrypt has a 72-byte limit, so we use SHA-256 for longer passwords
    BCRYPT_MAX_LENGTH = 72

    @staticmethod
    def _prepare_password(password: str) -> bytes:
        """
        Prepare password for bcrypt hashing.
        
        If password is longer than 72 bytes, we first hash it with SHA-256
        to get a fixed 32-byte hash, then hash that with bcrypt.
        This is a standard approach to handle long passwords with bcrypt.
        """
        password_bytes = password.encode('utf-8')
        
        # If password is within bcrypt limit, use it directly
        if len(password_bytes) <= PasswordService.BCRYPT_MAX_LENGTH:
            return password_bytes
        
        # For longer passwords, hash with SHA-256 first (always 32 bytes)
        # This allows passwords of any length while maintaining security
        sha256_hash = hashlib.sha256(password_bytes).digest()
        return sha256_hash

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt.
        
        For passwords longer than 72 bytes, we first hash with SHA-256,
        then hash the result with bcrypt. This allows passwords of any length.
        """
        # Ensure password is a string
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        
        # Prepare password (handle long passwords with SHA-256)
        password_to_hash = PasswordService._prepare_password(password)
        
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=PasswordService.BCRYPT_ROUNDS)
        hashed = bcrypt.hashpw(password_to_hash, salt)
        
        # Return as string (bcrypt hash is always ASCII)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash."""
        if not isinstance(plain_password, str):
            raise TypeError("Password must be a string")
        
        try:
            # Prepare password the same way as when hashing
            password_to_check = PasswordService._prepare_password(plain_password)
            hash_bytes = hashed_password.encode('utf-8')
            
            # Verify password
            return bcrypt.checkpw(password_to_check, hash_bytes)
        except (ValueError, TypeError):
            # Invalid hash format or other error
            return False

