import socket 
import argparse


def client(ip, port):
    s = socket.socket()
    s.connect((ip, port))    
    while True:
        r = s.recv(1024)
        print("Pergunta: {0}".format(r.decode())) 
        if not r:
            print("Finalizando...")
            break
        message_to_server = input("Responder: ")
        s.send(message_to_server.encode())


def main():
    args = argparse.ArgumentParser(description="Server and client")
    args.add_argument("-f", help="function [server] or [client]")
    args.add_argument("-p", help="port", type=int)
    args.add_argument("-hx", help="host", type=str)
    parser = args.parse_args()
    if parser.f == "client":
        client(parser.hx, parser.p)
        
        
if __name__ == '__main__':
        client('localhost', 9997)