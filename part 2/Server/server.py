import socket
import time
import os
import signal
import threading

IP = '10.124.6.106'
PORT = 65432
ADDRESS = (IP, PORT)
FORMAT = "utf-8"

def send_list(conn: socket):
    try:
        with open("List_File.txt", "r") as file:
            data = file.read()
            conn.send(data.encode(FORMAT))
            conn.recv(1024)
    except Exception as e:
        print(f"An error occurred: {e}")

def transfer(conn: socket, filename, priority):
    try:
        path = "resource/" + filename
        bytes = 0
        if priority == "CRITICAL":
            bytes = 1024 * 10
        elif priority == "HIGH":
            bytes = 1024
        else:
            bytes = 208

        filesize = os.path.getsize(path)
        conn.send(str(filesize).encode())
        conn.recv(1024)
        with open(path, "rb") as file:
            while data := file.read(bytes):
                conn.send(data)
                conn.recv(1024).decode()
            conn.send("EOF".encode())
            conn.recv(1024)

    except KeyboardInterrupt:
        print("[Alert] Stop program")
        conn.close()
    except ConnectionResetError:
        print("[Alert] Connection reset error")
        conn.close()
    except ConnectionError:
        print("[Alert] Connection error")
        conn.close()
    except Exception as e:
        print(f"[Error]: {e}")
        conn.close()   

def handle_client(client_conn: socket, client_addr):
    try:
        msg = client_conn.recv(1024).decode(FORMAT)
        client_conn.send("ok".encode(FORMAT))
        if msg == "Main thread":
            send_list(client_conn)
        else:
            while True:
                filename = client_conn.recv(1024).decode(FORMAT)
                client_conn.send("ok".encode(FORMAT))
                priority = client_conn.recv(1024).decode(FORMAT)
                client_conn.send("ok".encode(FORMAT))
                transfer(client_conn, filename, priority)
    except Exception as e:
        print(f"[Error]: {e}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen()
    print(f"Listening on {ADDRESS}")

    while True:
        client_conn, client_addr = server.accept()
        threading.Thread(target=handle_client, args=(client_conn, client_addr)).start()
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)
    main()