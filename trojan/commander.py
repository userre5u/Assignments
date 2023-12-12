import socket
import argparse




def accept_connection(server_socket):
    client, address = server_socket.accept()
    print(F'[+] Connection established from: {address}')
    handle_data(client)
    

def handle_data(client):
    try:    
        while True:
            prompt = input("$ ")
            if len(prompt.strip()) == 0:
                continue
            client.send(prompt.encode())
            if prompt == "exit":
                break
            data = client.recv(1024).decode()
            if data:
                print(data)
    except KeyboardInterrupt:
        print('Server closed')
    client.close()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, required=True)
    parser.add_argument('--port', type=int, required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    ip, port = args.ip, args.port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen()
    print(F"Server is ls listening on {ip}:{port}")
    accept_connection(server_socket)



if __name__ == "__main__":
    main()


