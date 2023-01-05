from pprint import pprint
import bisect


def traverse_to_dir(fs: dict, path: list[str]) -> dict:
    cur_dict = fs

    for part in cwd:
        if part in cur_dict:
            cur_dict = cur_dict[part]
        else:
            cur_dict[part] = {}

    return cur_dict


def consume_cd(command: str, fs: dict, cwd: list[str]):
    if command == '/':
        cwd.clear()
        cwd.append('/')
    elif command == '..':
        cwd.pop()
    else:
        cwd.append(command)
        traverse_to_dir(fs, cwd)


def consume_ls(i: int, lines: list[str], fs: dict, cwd: list[str]) -> int:
    directory = traverse_to_dir(fs, cwd)

    while i < len(lines) and not lines[i].startswith('$'):
        line = lines[i]

        if line.startswith('dir '):
            inner_dir_name = line[4:]

            if inner_dir_name not in directory:
                directory[inner_dir_name] = {}
        else:
            size, filename = line.split()
            size = int(size)
            directory[filename] = size

        i += 1

    return i


def dfs(directory: dict, cwd: tuple[str], dir_sizes: dict[tuple[str], int]):
    if cwd not in dir_sizes:
        dir_sizes[cwd] = 0

    for name, contents in directory.items():
        if isinstance(contents, int):
            dir_sizes[cwd] += contents
        else:
            inner_dir_path = cwd + (name,)
            dfs(directory[name], inner_dir_path, dir_sizes)
            dir_sizes[cwd] += dir_sizes[inner_dir_path]


with open('input.txt') as f:
    lines = f.read().split('\n')[:-2]

fs = {'/': {}}
cwd = ['/']
i = 0

while i < len(lines):
    line = lines[i]

    if line.startswith('$ cd '):
        consume_cd(line[5:], fs, cwd)
        i += 1
    elif line.startswith('$ ls'):
        i = consume_ls(i + 1, lines, fs, cwd)
    else:
        assert False

dir_sizes = {}
dfs(fs['/'], ('/',), dir_sizes)

pprint(dir_sizes)

total_size = 70000000
need_free = 30000000
used_size = dir_sizes[('/',)]
need_to_free = need_free - (total_size - used_size)

print('Used size:', used_size)
print('Have free:', total_size - used_size)
print('Need free:', need_free)
print('Need to free:', need_to_free)

sizes_of_directories = list(dir_sizes.values())
sizes_of_directories = sorted(sizes_of_directories)

print(sizes_of_directories)

i = bisect.bisect_right(sizes_of_directories, need_to_free)
print(i)
print(sizes_of_directories[i])
