import socket
import signal
import threading
from tqdm import tqdm

IP = 'localhost'
PORT = 65432
ADDRESS = (IP, PORT)
FORMAT = "utf-8"

def Recv_List(conn):
    try:
        while True:
            item = conn.recv(1024).decode(FORMAT)
            conn.send("ok".encode(FORMAT))
            if item == "End":
                break
            print(item)
    except Exception as e:
        print(f"An error occurred: {e}") 

def Read_File():
    list = []
    with open("input.txt", "r") as f:
        data = f.readlines()
        for item in data:
            item = item.strip()
            if item:
                list.append(item)

    return list

def Recv_size(conn):
    total_size = []
    while True:
        data = conn.recv(1024).decode(FORMAT)
        if data == "End":
            conn.send("ok".encode(FORMAT))
            break
        total_size.append(int(data))
        conn.send("ok".encode(FORMAT))
    return total_size
    
def Write_File(conn, total_size, files):
    output_files = ["output/" + file.split(" ")[0] for file in files]

    flag = True
    while flag:
        for i, output_file in enumerate(output_files):
            if total_size[i] <= 0:
                continue
            with open(output_file, "ab") as file:
                with tqdm(total=total_size[i], unit='B', unit_scale=True, desc=output_file) as progress_bar:
                    data = conn.recv(1024)
                    progress_bar.update(len(data))
                    file.write(data)
                    total_size[i] -= len(data)
                    conn.send("ok".encode(FORMAT))
        
        flag = any(size > 0 for size in total_size)

def handle_transfer():
    pass

def main():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDRESS)
        print(f"Connected to {ADDRESS}")
    except ConnectionRefusedError:
        print("[Error] Connection refused or Server is not running")
        return
    
    try:
        Recv_List(client)
        list = Read_File()
        print(list)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)  # Catch Ctrl+C
    main()
