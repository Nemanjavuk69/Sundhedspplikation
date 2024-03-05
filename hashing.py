import hashlib


def hash_string(input_string):
    # Create a sha256 hash object
    sha_signature = hashlib.sha256(input_string.encode()).hexdigest()
    print(sha_signature)
    return sha_signature
