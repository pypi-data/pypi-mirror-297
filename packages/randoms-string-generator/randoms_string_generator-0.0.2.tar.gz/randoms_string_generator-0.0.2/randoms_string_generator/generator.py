import secrets

class RandomPassword:
    """
    Random password generator
    """
    RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    RANDOM_STRING_SIGN = "!@#$%^&*()_+-/?."
    
    @classmethod
    def random_password(cls, length: int) -> str:
        """Generate random char-[!@#$%^&*()_+-/?.] code."""
        allowed_chars = cls.RANDOM_STRING_CHARS
        allowed_signs = cls.RANDOM_STRING_SIGN
        allowed = allowed_signs + allowed_chars
        return "".join(secrets.choice(allowed) for i in range(length))

    @classmethod
    def random_code(cls, length: int) -> str:
        """Generate random char code. """
        allowed_chars = cls.RANDOM_STRING_CHARS
        return "".join(secrets.choice(allowed_chars) for i in range(length))
    

 
