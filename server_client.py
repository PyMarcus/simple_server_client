import socket
import argparse
import configparser
import threading
from typing import TypeVar, Dict
from string import ascii_lowercase

Socket = TypeVar("Socket")
RIGHT_ANSWERS = ['a', 'a', 'd', 'c', 'a']
UTF8 = 'utf-8'
BYTES = 1024
EXIT = 'exit'


def read_questions() -> Dict:
    questions = dict()
    config = configparser.RawConfigParser()
    config.read('questions.ini')
    for k, v in config['questions'].items():
        questions[k] = v
    return questions


def get_my_ip() -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(f"YOUR LOCAL IP ADDRESS IS: {s.getsockname()[0]}")
    s.close()


def server(host: str, port: int) -> None:
    get_my_ip()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(f"Listen in {host, port}...")
    s.listen(50)
    while True:
        client_socket, client_address = s.accept()
        print(f"received from {client_address}")
        threading.Thread(target=server_worker, args=(client_socket, )).start()


def server_worker(sock: Socket) -> None:
    i: int = 0
    for key, value in read_questions().items():
        sock.send(f"{key}  {value}".encode(UTF8))
        response = sock.recv(BYTES)
        print(f"Response {response.decode(UTF8)}")
        print(RIGHT_ANSWERS[i])
        if response:
            if response.decode(UTF8).lower() in ascii_lowercase:
                if response.decode(UTF8).lower() == RIGHT_ANSWERS[i]:
                    sock.send("Parabéns!".encode(UTF8))
                else:
                    sock.send("Resposta incorreta!".encode(UTF8))
                i += 1
            else:
                sock.send("Resposta inválida".encode(UTF8))
        else:
            sock.send("Resposta inválida".encode(UTF8))
    sock.close()


def client(server_address: str, server_port: int) -> None:
    message_to_server: str = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, server_port))
    while message_to_server != EXIT:
        message_from_server = sock.recv(BYTES).decode(UTF8)
        if message_from_server:
            print(f"Server diz: {message_from_server}")
            if "Parabéns!" not in  message_from_server and "Resposta incorreta!" not in message_from_server and "Resposta inválida" not in message_from_server:
                message_to_server = input("Responder: ")
                sock.send(message_to_server.encode(UTF8))
        else:
            sock.close()
            break


def main() -> None:
    args = argparse.ArgumentParser(description="Server and client")
    args.add_argument("-f", help="function [server] or [client]")
    args.add_argument("-p", help="port", type=int)
    args.add_argument("-hx", help="host", type=str)
    parser = args.parse_args()
    if parser.f == "server":
        server(parser.hx, parser.p)
    elif parser.f == "client":
        client(parser.hx, parser.p)
    else:
        print("Execute python server_client.py -f [server/client] -hx [ip] -p [port]")


if __name__ == '__main__':
    main()