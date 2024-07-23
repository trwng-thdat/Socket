import socket
import os

PORT = 5000
IP = 'localhost'
ADDRESS = (IP, PORT)

def transfer(conn: socket, filename):
    try:
        size = os.path.getsize(filename)
        conn.send(str(size).encode())
        conn.recv(1024)
        with open(filename, "rb") as file:
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

    print("Listening...")

    conn, addr = server.accept()
    
    filename = conn.recv(1024).decode()
    conn.send("ok".encode())
    transfer(conn, filename)

if __name__ == "__main__":
    main()