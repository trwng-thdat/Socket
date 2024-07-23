import os

def check(path1, path2):
    stream1 = open(path1, "rb")
    stream2 = open(path2, "rb")

    while True:
        data1 = stream1.read(1024)
        data2 = stream2.read(1024)
        if not data1 and not data2:
            return True
        
        if data1 != data2:
            return False
        


def main():
    path1 = "Server/resource/File1.zip"
    path2 = "Client/output/File1.zip"
    if check(path1, path2):
        print("Files are the same")
    else:
        print("Files are different")

main()