import os

def Read_File(): # return list of file that client want to download
    items = []
    with open("input.txt", "r") as f:
        data = f.readlines()
        current_dir = os.path.abspath(__file__)
        parent_dir = os.path.dirname(current_dir) + "\\output\\"
        for item in data:
            path = parent_dir + item
            item = item.strip()
            if item:
                if os.path.isfile(path):
                    print(f"{item} already exists")
                else:
                    items.append(item)
    return items

list = Read_File()
print(list)