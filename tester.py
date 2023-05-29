import socket

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

    verification_status = ecu_socket.recv(1024).decode()
    print("ECU Message: ",verification_status)
    if True:
        while(True):
            # TODO ECU-Tester Data Exchange
            pass

if __name__ == "__main__":
    tester()
