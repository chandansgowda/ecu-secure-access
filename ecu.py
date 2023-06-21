import socket
import hashlib
import secrets
import string
from rsa import *


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string

def ecu():
    # Create a socket for the ecu
    ecu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ecu_socket.bind(('localhost', 9002))
    ecu_socket.listen(1)
    print("ecu started and listening...")

    while True:
        # Accept tester connection
        tester_socket, address = ecu_socket.accept()
        print("Received connection from tester:", address)

        # Send challenge string to the tester
        challenge_string = generate_random_string(128)
        challenge_string_hash = hashlib.sha256(challenge_string.encode('utf-8')).hexdigest()
        print(challenge_string_hash)
        tester_socket.send(challenge_string.encode())

        # Connect to the trust center
        trust_center_socket, address = ecu_socket.accept()
        print("Received connection from trust center:", address)

        # Request tester public key from the trust center
        tester_public_key = trust_center_socket.recv(4096).decode()
        print("Received Tester Public Key:", tester_public_key)

        # Receive signed response from tester
        signed_response = tester_socket.recv(4096)
        signed_response_is_valid = rsa_verify(tester_public_key, challenge_string_hash, signed_response)

        if signed_response_is_valid:
            print("Signature is VALID\nI can now talk to the tester securely. 🔐✅")
            response = "All the sensors in the car are working correctly."
            encrypted_response = rsa_encrypt(response,tester_public_key)
            tester_socket.send(encrypted_response)

        else:
            print("Incorrect Signature!")


if __name__ == "__main__":
    ecu()
