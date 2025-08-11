
def create_product_key():
    """
        Creates a product key for the application using bitwise operations.
        The key is generated from a random 56-bit integer, encoded as 14 hex digits,
        and includes a simple checksum for easy validation.
    """
    import random

    def int_to_key(n):
        # Convert 56 bits to 14 hex chars
        key = f"{n:014X}"
        # Compute a simple checksum: XOR all nibbles
        checksum = 0
        for c in key:
            checksum ^= int(c, 16)
        # Append checksum as 2 hex digits
        return key + f"{checksum:02X}"

    n = random.getrandbits(56)  # 14 hex digits
    return int_to_key(n)

def validate_product_key(product_key):
    """
        Validates a product key by checking its format and checksum.
        The key must be 16 characters long, consist of hex digits,
        and the checksum must match the computed value.
    """
    if len(product_key) != 16 or not all(c in "0123456789ABCDEF" for c in product_key):
        return False

    # Extract the checksum from the last two characters
    checksum = int(product_key[-2:], 16)
    # Compute the checksum from the first 14 characters
    computed_checksum = 0
    for c in product_key[:-2]:
        computed_checksum ^= int(c, 16)

    return checksum == computed_checksum