import argparse
import socket

def forward_tunnel(local_port, remote_host, remote_port):

    # Create a listening socket on the local port
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind(("", local_port))
    local_socket.listen(1)

    # Accept incoming connections and forward traffic
    while True:
        # Wait for an incoming connection
        client_socket, client_address = local_socket.accept()
        
        # Connect to the remote host and port
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        
        # Forward traffic between the two sockets
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                remote_socket.sendall(data)
            except KeyboardInterrupt:
                break
            
            try:
                data = remote_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)
            except KeyboardInterrupt:
                break
        

        client_socket.close()
        remote_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port forwarding script")
    parser.add_argument("local_port", type=int, help="local port number")
    parser.add_argument("remote_host", help="remote host name or IP address")
    parser.add_argument("remote_port", type=int, help="remote port number")
    args = parser.parse_args()

    forward_tunnel(args.local_port, args.remote_host, args.remote_port)