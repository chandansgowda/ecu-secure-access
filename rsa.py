from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


def generate_rsa_keys():
    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Get the public key
    public_key = private_key.public_key()

    # Serialize keys to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Convert keys to strings
    private_key_str = private_key_pem.decode()
    public_key_str = public_key_pem.decode()

    return private_key_str, public_key_str


def rsa_sign(private_key_str, message):
    # Load the private key from string
    private_key = serialization.load_pem_private_key(
        private_key_str.encode(),
        password=None,
        backend=default_backend()
    )

    # Sign the message
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Return the signature as bytes
    return signature


def rsa_verify(public_key_str, message, signature):
    # Load the public key from string
    public_key = serialization.load_pem_public_key(
        public_key_str.encode(),
        backend=default_backend()
    )

    try:
        # Verify the signature
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return True  # Signature is valid
    except Exception:
        return False  # Signature is invalid


def rsa_encrypt(message, public_key_string):
    public_key = serialization.load_pem_public_key(
        public_key_string.encode('utf-8'),
        backend=default_backend()
    )
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def rsa_decrypt(ciphertext, private_key_string):
    private_key = serialization.load_pem_private_key(
        private_key_string.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')