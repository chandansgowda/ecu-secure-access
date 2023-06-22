import socket
import hashlib
import secrets
import string
from rsa import *
from constants import *


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

def ecu():
    # Create a socket for the ecu
    ecu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ecu_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ecu_socket.bind((ECU_HOST, ECU_PORT))
    ecu_socket.listen(1)
    print("ecu started and listening...")

    while True:
        # Accept tester connection
        tester_socket, address = ecu_socket.accept()
        print("Received connection from tester:", address)

        # Check if the tester is trusted
        tester_mac = tester_socket.recv(1024).decode()
        if tester_mac not in TRUSTED_MAC_LIST:
            print("This tester is not trusted ❌")
            tester_socket.close()
            continue

        # Send challenge string to the tester
        challenge_string = generate_random_string(128)
        challenge_string_hash = hashlib.sha256(challenge_string.encode('utf-8')).hexdigest()
        tester_socket.send(challenge_string.encode())

        # Connect to the trust center
        trust_center_socket, address = ecu_socket.accept()
        print("Received connection from trust center:", address)

        # Request trust center public key from the trust center
        trust_center_public_key = trust_center_socket.recv(4096).decode()
        print("Received Tester Public Key:", trust_center_public_key)

        # Receive signed response from tester
        signed_response = tester_socket.recv(4096)
        signed_response_is_valid = rsa_verify(trust_center_public_key, challenge_string_hash, signed_response)

        if signed_response_is_valid:
            print("Signature is VALID\nI can now talk to the tester securely. 🔐✅")
            response = "Access Granted!"
            tester_socket.send(response.encode())

        else:
            print("Invalid Signature")
            response = "Signature was not verified!"
            tester_socket.send(response.encode())


if __name__ == "__main__":
    ecu()
