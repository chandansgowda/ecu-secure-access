import socket
from rsa import *
from constants import *

def tester():
    # Connect to the ecu socket
    try:
        ecu_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ecu_socket.connect((ECU_HOST, ECU_PORT)) # Requesting access to ECU
    except:
        print("ECU server down ❌")
        return

    challenge_string = ecu_socket.recv(1024).decode()

    # Connect to the trust center
    trust_center_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trust_center_socket.connect((TRUST_CENTER_HOST, TRUST_CENTER_PORT))

    # Forward challenge string to trust center
    trust_center_socket.send(challenge_string.encode())

    # Receive signed response from trust center and forward it to ECU
    signed_response = trust_center_socket.recv(5096)
    ecu_socket.send(signed_response)
    print("Forwarded signed response to ECU ✅")

    # Receive requested data from ECU
    ecu_response = ecu_socket.recv(1024).decode()

    print("ECU Response: ",ecu_response)
    if True:
        while(True):
            # TODO ECU-Tester Data Exchange
            pass

if __name__ == "__main__":
    tester()
