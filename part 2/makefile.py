import random
import os
from tqdm import tqdm

char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\n']

with open("Server/resource/File4.zip", "ab") as f:
    for i in tqdm(range(50000000)):
        index = random.randint(0, len(char_list) - 1)
        f.write(char_list[index].encode())

# size = os.path.getsize("Server/resource/File1.zip")
# print(size)