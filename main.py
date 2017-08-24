import mmap
import os

path = "D:/Work/DC_1/Data/Scripts/"
path_to_str_keys = "D:/Work/DC_1/Data/Strings.txt"
ignore = [".git"]


def is_exception_path(path_str):
    for exception_dir in ignore:
        if path_str.find(exception_dir) != -1:
            return True
    return False


def get_srt_keys(path):
    str_file = open(path, 'r')
    lines = [line.rstrip('\n') for line in str_file]
    str_file.close()
    keys = []
    for string in lines:
        if len(string) > 0 and string[0] != ";":
            end_index = string.find("=")
            keys.append(string[:end_index])

    return keys



def get_files_names():
    files_names = []

    for root, dirs, files in os.walk(path, topdown=False):
        if not is_exception_path(root):
            for name in files:
                if name.find(".lua") != -1:
                    files_names.append(os.path.join(root, name))

    return files_names


def get_separated_keys(all_keys):
    item_keys = []
    other_keys = []
    for key in all_keys:
        if key.find('ITEM_NAME'):
            item_keys.append(key)
        else:
            other_keys.append(key)
    return item_keys, other_keys

def check_other_keys(files, str_keys):
    unuseful_keys = str_keys[:]


    for file in files:
        print(file)
        lua_file = open(file, 'r')
        if os.stat(file).st_size == 0:
            continue

        file_mmap = mmap.mmap(lua_file.fileno(), 0, access=mmap.ACCESS_READ)
        for key in str_keys:
            if file_mmap.find(key.encode('utf-8')) != -1:
                try:
                    unuseful_keys.remove(key)
                except ValueError:
                    pass
                print('Key_REMOVED_FROM______:\n' + file)
                print('______:KEYS:________' + key)
        lua_file.close()

    return unuseful_keys


files_names = get_files_names()
keys = get_srt_keys(path_to_str_keys)
other_keys, item_keys = get_separated_keys(keys)
unuseful_keys = check_other_keys(files_names, other_keys)

t_file = open("keys.txt", "w")
for k in other_keys:
    t_file.write(k + "\n")
for k in item_keys:
    t_file.write(k + "\n")
t_file.close()

print('_________UNUSEFUL KEYS (NOT ITEMS)_____')
result_file = open("result.txt", "w")
for k in unuseful_keys:
    result_file.write(k + "\n")
result_file.close()