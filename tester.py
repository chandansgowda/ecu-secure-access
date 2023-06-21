import socket
from rsa import *

def tester():
    # Connect to the ecu socket
    ecu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ecu_socket.connect(('localhost', 9002)) # Requesting access to ECU

    challenge_string = ecu_socket.recv(1024).decode()
    print(challenge_string)

    # Connect to the trust center
    trust_center_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trust_center_socket.connect(('localhost', 8001))

    # Request private key from the trust center
    trust_center_socket.send(challenge_string.encode())
    tester_private_key = trust_center_socket.recv(5096).decode()
    print("Received Private Key:", tester_private_key)

    # Receive signed response from trust center and forward it to ECU
    signed_response = trust_center_socket.recv(5096)
    ecu_socket.send(signed_response)
    print("Forwarded signed response to ECU ✅")

    # Receive requested data from ECU
    encrypted_ecu_response = ecu_socket.recv(1024)
    decrypted_ecu_response = rsa_decrypt(encrypted_ecu_response, tester_private_key)

    print("ECU Response: ",decrypted_ecu_response)
    if True:
        while(True):
            # TODO ECU-Tester Data Exchange
            pass

if __name__ == "__main__":
    tester()
