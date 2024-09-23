def encrypt(text):
    encryption_map = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/:.",
        "mlpoknjiuhbvgytfcdrxeszawqZCXVBMNLJKHGDFSAQPOWUIERYT8906735142&$@"
    )
    return text.translate(encryption_map)

def decrypt(text):
    decryption_map = str.maketrans(
        "mlpoknjiuhbvgytfcdrxeszawqZCXVBMNLJKHGDFSAQPOWUIERYT8906735142&$@",
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/:."
    )
    return text.translate(decryption_map)
