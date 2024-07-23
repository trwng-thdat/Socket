import socket
import time
import os
import signal
import requests
from tqdm import tqdm

IP = 'localhost'
PORT = 65432
ADDRESS = (IP, PORT)
FORMAT = "utf-8"

def Recv_List(conn: socket):
    try:
        item = ""
        while True:
            item = conn.recv(1024).decode(FORMAT)
            conn.send("ok".encode(FORMAT))
            if item == "End":
                break
            print(item)
    except KeyboardInterrupt:
        print("[Alert] Stop program")
    except Exception as e:
        print(f"An error occurred: {e}") 

def Read_File(): # return list of file that client want to download
    items = []
    with open("input.txt", "r") as f:
        data = f.readlines()
        # current_dir = os.path.abspath(__file__)
        # parent_dir = os.path.dirname(current_dir) + "\\output\\"
        for item in data:
            # path = parent_dir + item
            item = item.strip()
            if item:
                path = "output/" + item
                if os.path.exists(path):
                    continue
                else:
                    items.append(item)
    return items

def write_file(conn: socket, filename):

    conn.send(filename.encode())
    conn.recv(1024).decode()

    msg = conn.recv(1024).decode()
    if msg == "Not Found":
        print(f"{filename} not found")
        conn.send("ok".encode())
        return
    else:
        conn.send("ok".encode())

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

def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
        print(f"Connected to {ADDRESS}")
    except ConnectionRefusedError:
        print("[Error] Connection refused or Server is not running")
        return
    except KeyboardInterrupt:
        print("[Alert] Stop program")
        client.close()
        return
    
    try:
        Recv_List(client)
        while True:
            items = Read_File()
            if not items:
                continue
            for item in items:
                write_file(client, item)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("[Alert] Stop program")
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        client.close()
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)  # Catch Ctrl+C
    main()
