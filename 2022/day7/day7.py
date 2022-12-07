from aocd.models import Puzzle

puzzle = Puzzle(year=2022, day = 7)

class Directory:
    def __init__(self, _name):
        self.name = _name
        self.directories = {}
        self.parent = None
        self.files = []
        self.total = 0

    def cd(self, dir):
        assert dir in self.directories
        return self.directories[dir]

    def add_directory(self, dir):
        self.directories[dir] = Directory(dir) 
        self.directories[dir].parent = self

    def add_file(self, name, size):
        self.files.append((name, size))

    def calculate_total(self):
        self.total = 0
        for f in self.files:
            self.total += f[1]
        for d in self.directories.values():
            self.total += d.calculate_total()

        return self.total

    def find_100k_dirs(self):
        total = 0
        if self.total < 100000:
            total += self.total

        for d in self.directories.values():
            total += d.find_100k_dirs()

        return total

    def dir_used_space(self):
        free_space = [ self.total ]
        for d in self.directories.values():
            free_space.extend(d.dir_used_space())

        return free_space

def parse_filesystem(lines):
    root_directory = Directory("/")
    current_directory = None
    parse_files = False
    
    def parse_command(l):
        nonlocal current_directory, parse_files

        args = l.split()
        if args[0] == 'cd':
            if args[1] == '/':
                current_directory = root_directory
            elif args[1] == '..':
                current_directory = current_directory.parent
            else:
                current_directory = current_directory.cd(args[1])

        elif args[0] == 'ls':
            parse_files = True
        else:
            assert("Unknown command")

    for l in lines.splitlines():
        if parse_files == True:
            # stop parsing files when we reach the next comment
            if l[0] == '$':
                parse_files = False
            else:
                # parse file and then continue to next line
                args = l.split()
                if args[0] == 'dir':
                    current_directory.add_directory(args[1])
                else:
                    current_directory.add_file(args[1], int(args[0]))

        if parse_files == False:
            parse_command(l[2:])

    return root_directory


root_directory = parse_filesystem(puzzle.input_data)
root_directory.calculate_total()
print(root_directory.find_100k_dirs())

needed_space = 30000000 - (70000000 - root_directory.total)
used_space = [ x for x in sorted(root_directory.dir_used_space()) if x > needed_space ]
print(used_space[0])