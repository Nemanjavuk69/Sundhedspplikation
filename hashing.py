import hashlib  # Importing the hashlib module for hashing


def hash_string(input_string):  # Defining the function to hash a string
    # Create a sha256 hash object
    # Creating a SHA-256 hash of the input string
    sha_signature = hashlib.sha256(input_string.encode()).hexdigest()
    print(sha_signature)  # Printing the SHA-256 hash
    return sha_signature  # Returning the SHA-256 hash
