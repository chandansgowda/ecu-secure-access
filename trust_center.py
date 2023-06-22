import hashlib
import socket
from rsa import *
from constants import *


def trust_center():
    # Create a socket for the trust center
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((TRUST_CENTER_HOST, TRUST_CENTER_PORT))
    server_socket.listen(1)
    print("Trust Center started and listening...")

    while True:
        # Accept client connection
        tester_socket, address = server_socket.accept()
        print("Received connection from:", address)

        challenge_string = tester_socket.recv(1024).decode()
        challenge_string_hash = hashlib.sha256(challenge_string.encode('utf-8')).hexdigest()
        print(challenge_string)

        # Generate public and private keys
        trust_center_private_key, trust_center_public_key = generate_rsa_keys()

        print(trust_center_private_key, trust_center_public_key)

        # Connect to the ECU
        ecu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ecu_socket.connect((ECU_HOST, ECU_PORT))
        print('Connected to ECU ✅')

        # Send trust center public key to ecu
        ecu_socket.send(trust_center_public_key.encode())
        print("Sent my public key to ECU ✅")

        # Sign hash using private key
        signed_response = rsa_sign(trust_center_private_key, challenge_string_hash)

        # Send signed response to tester
        tester_socket.send(signed_response)
        print("Sent signed response to tester ✅")

        print("Listening for new connections")

        # Close the connection
        tester_socket.close()
        ecu_socket.close()

if __name__ == "__main__":
    trust_center()
