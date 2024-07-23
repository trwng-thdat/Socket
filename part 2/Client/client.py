import socket
import signal
import threading
import os
from tqdm import tqdm
import time

IP = '10.124.6.106'
PORT = 65432
ADDRESS = (IP, PORT)
FORMAT = "utf-8"

def Recv_List(conn):
    try:
        data = conn.recv(1024).decode(FORMAT)
        conn.send("Received".encode()) 
        return data  
    except Exception as e:
        print(f"An error occurred: {e}") 

def Read_File():
    try:
        list = []
        with open("input.txt", "r") as file:
            data = file.readlines()
            for item in data:
                item = item.strip()
                if item:
                    list.append(item)
        
        items = []
        for item in list:
            tmp = item.split(" ")
            if not os.path.exists("output/" + tmp[0]):
                items.append(item)
        
        return items
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def write_file(conn: socket, filename, priority):
    bytes = 0
    if priority == "CRITICAL":
        bytes = 11000
    elif priority == "HIGH":
        bytes = 1100
    else:
        bytes = 300
    try:
        size = int(conn.recv(102400).decode())
        conn.send("ok".encode())
        path = "output/" + filename
        with open(path, "ab") as file:
            with tqdm(total=size, unit='B', unit_scale=True, desc=filename) as progress_bar:
                while True:
                    data = conn.recv(1024)
                    progress_bar.update(len(data))
                    if data == b"EOF":
                        conn.send("Finnish".encode())
                        break
                    file.write(data)
                    conn.send("next".encode())
    except KeyboardInterrupt:
        print("[Alert] Stop program")
        conn.close()
        return
    except Exception as e:
        print(f"[Error]: {e}")
        conn.close()

def handle_transfer(item):
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect(ADDRESS)
        conn.send("Thread".encode(FORMAT))
        conn.recv(1024)
        tmp = item.split(" ")
        
        filename = tmp[0]
        conn.send(filename.encode(FORMAT))
        conn.recv(1024)

        priority = tmp[1]
        conn.send(priority.encode(FORMAT))
        conn.recv(1024)
        write_file(conn, filename, priority)
    except KeyboardInterrupt:
        print("[Alert] Stop program")
        conn.close()
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
        print(f"Connected to {ADDRESS}")
        
        client.send("Main thread".encode(FORMAT))
        client.recv(1024)

        items = Recv_List(client)
        print(items)
        while True:
            list = Read_File()
            if list:
                for item in list:
                    thr = threading.Thread(target=handle_transfer, args=(item,))
                    thr.start()
                    time.sleep(0.5)
            time.sleep(2)
    except KeyboardInterrupt:
        print("[Alert] Stop program")
        client.close()
    except ConnectionRefusedError:
        print("[Error] Connection refused or Server is not running")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)  # Catch Ctrl+C
    main()
