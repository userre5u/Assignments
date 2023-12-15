import socket
import select
import argparse
import sys
import struct



MAX_BYTES = 1024

def create_ping_packet(user_data, echo_type):
    header = struct.pack('bbHHh', echo_type, 0, 0, 0, 1)
    return header + user_data.encode()

def extract_echo_type(payload):
    payload = payload.split(b" ")[0]
    if len(payload) == 8:
        header = payload
    else:
        header = payload.split(b" ")[0][-8:]
    echo_type = struct.unpack("bbHHh", header)[0]
    if echo_type == 8:
        return 0
    return 8


def handle_connection(icmp_socket, target_ip, username):
    try:
        echo_type = 8
        while True:
            ready_read, _, _ = select.select([icmp_socket, sys.stdin], [], [], 0)
            if ready_read:
                for read_buffer in ready_read:
                    if read_buffer is not icmp_socket:
                        text = read_buffer.readline()
                        payload = create_ping_packet(F" --> {username}: {text}", echo_type)
                        icmp_socket.sendto(payload, (target_ip, 1234))
                        echo_type = extract_echo_type(payload)
                        continue
                    data = icmp_socket.recvfrom(MAX_BYTES)[0]
                    user_data = b" ".join(data.split(b" ")[1:]).decode().strip()
                    print(F"\t\t\t\t{user_data}")
                    echo_type = extract_echo_type(data)

    except KeyboardInterrupt:
        print("\nChat closed")



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_ip', type=str, required=True)
    parser.add_argument('--user', type=str, required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    target_ip, user = args.target_ip, args.user
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    icmp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    handle_connection(icmp_socket, target_ip, user)
    icmp_socket.close()

main()

