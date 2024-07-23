import socket
import time
import os
import signal

IP = 'localhost'
PORT = 65432
ADDRESS = (IP, PORT)
FORMAT = "utf-8"

def send_list(conn: socket):
    try:
        with open("List_File.txt", "r") as file:
            items = file.readlines()
            items.append("End")
            for item in items:
                item = item.strip()
                conn.sendall(item.encode(FORMAT))
                conn.recv(1024).decode(FORMAT)
    except Exception as e:
        print(f"An error occurred: {e}")

def transfer(conn: socket, filename):
    try:
        path = "resource/" + filename
        if not os.path.exists(path):
            conn.send("Not Found".encode())
            conn.recv(1024)
            return
        else:
            conn.send("FOUND".encode())
            conn.recv(1024)

        filesize = os.path.getsize(path)
        conn.send(str(filesize).encode())
        conn.recv(1024)
        with open(path, "rb") as file:
            while data := file.read(1):
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
        print(f"An error occurred: {e}")
        conn.close()    

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen(5)
    print(f"Listening on {ADDRESS}")

    while True:
        client_conn, client_addr = server.accept()
        send_list(client_conn)
        while True:
            try:
                file_name = client_conn.recv(1024).decode(FORMAT)
                client_conn.send("ok".encode(FORMAT))
                transfer(client_conn, file_name)
            except ConnectionAbortedError:
                print(f"Connection {client_addr} closed")
                break
            except ConnectionError:
                print(f"Connection {client_addr} closed")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break
     
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)
    main()