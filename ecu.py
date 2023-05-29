import socket
import hashlib
from rsa import rsa_verify


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
        challenge_string = "Thisisasecretstringchallenge"
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
            tester_socket.send(b"Hey Tester, The signature is verified.")

        else:
            print("Incorrect Signature!")


if __name__ == "__main__":
    ecu()
