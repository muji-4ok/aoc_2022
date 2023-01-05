from pprint import pprint


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

result = 0

for dir_size in dir_sizes.values():
    if dir_size <= 100000:
        result += dir_size

print(result)
