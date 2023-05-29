import hashlib
import socket
from rsa import *


def trust_center():
    # Create a socket for the trust center
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8001))
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
        tester_private_key, tester_public_key = generate_rsa_keys()

        print(tester_private_key, tester_public_key)

        # Connect to the ECU
        ecu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ecu_socket.connect(('localhost', 9002))
        print('Connected to ECU ✅')

        # Send tester public key to ecu
        ecu_socket.send(tester_public_key.encode())
        print("Sent tester public key to ECU ✅")

        # Send tester private key to tester
        tester_socket.send(tester_private_key.encode())
        print("Sent tester private key to tester ✅")

        # Encrypt hash using tester private key
        signed_response = rsa_sign(tester_private_key, challenge_string_hash)

        # Send signed response to tester
        tester_socket.send(signed_response)
        print("Sent signed response to tester ✅")

        # Close the connection
        tester_socket.close()
        ecu_socket.close()

if __name__ == "__main__":
    trust_center()
