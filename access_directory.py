# Name: Ansh    Roll No: 2401010041
# Direct Access, Indexed Access and Directory Structures
import os
import struct
import tempfile

RECORD = struct.Struct("<i12si")        # roll, name, marks = 20 bytes
STUDENTS = [(105, "Asha", 82), (101, "Ravi", 75), (109, "Meera", 91),
            (103, "Kabir", 68)]


def fetch(f, position):
    f.seek(position)
    roll, name, marks = RECORD.unpack(f.read(RECORD.size))
    return f"roll={roll} name={name.rstrip(bytes(1)).decode()} marks={marks}"


def number(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("  Enter a whole number")


def direct(f):
    n = number("Record number: ")
    if not 1 <= n <= len(STUDENTS):
        print(f"REJECTED: record must be 1 to {len(STUDENTS)}")
        return
    position = (n - 1) * RECORD.size
    print(f"Location = ({n} - 1) * {RECORD.size} = byte {position}")
    print("Record:", fetch(f, position))


def indexed(f, index):
    key = number("Roll number to find: ")
    low, high = 0, len(index) - 1       # binary search in the sorted index
    while low <= high:
        mid = (low + high) // 2
        print(f"Index check: entry {mid}, key {index[mid][0]}")
        if index[mid][0] == key:
            print(f"Key found, position = byte {index[mid][1]}")
            print("Record:", fetch(f, index[mid][1]))
            return
        if index[mid][0] < key:
            low = mid + 1
        else:
            high = mid - 1
    print(f"REJECTED: key {key} is not in the index")


# A directory is a dict. A file is None.
def execute(root, line, tree):
    parts = line.split()
    if len(parts) not in (1, 2):
        return "ERROR: use mkdir/create/search/list/delete and one name"
    cmd, path = parts[0], parts[1] if len(parts) == 2 else ""
    if cmd == "search":
        found = find(root, path)
        return "Found: " + ", ".join(found) if found else "Not found"
    names = [p for p in path.split("/") if p]
    if not tree and (len(names) > 1 or cmd == "mkdir"):
        return "ERROR: a single-level directory has no subdirectories"
    here = root
    for p in (names if cmd == "list" else names[:-1]):
        if not isinstance(here.get(p), dict):
            return f"ERROR: directory '{p}' not found"
        here = here[p]
    if cmd == "list":
        return "List: " + (", ".join(n + ("/" if v is not None else "")
                           for n, v in sorted(here.items())) or "(empty)")
    if not names:
        return "ERROR: name is missing"
    name = names[-1]
    if cmd in ("create", "mkdir"):
        if name in here:
            return f"REJECTED: duplicate name '{name}' in this directory"
        here[name] = None if cmd == "create" else {}
        return f"Created {path}"
    if cmd == "delete":
        if name not in here:
            return f"ERROR: '{name}' not found"
        if here[name]:
            return f"REJECTED: directory '{name}' is not empty"
        del here[name]
        return f"Deleted {path}"
    return "ERROR: unknown command"


def find(here, name, path=""):
    out = []
    for n, v in here.items():
        if n == name:
            out.append(f"{path}/{n}")
        if v is not None:
            out += find(v, name, f"{path}/{n}")
    return out


def show(here, depth=1):
    for n, v in sorted(here.items()):
        print("    " * depth + "|-- " + n + ("/" if v is not None else ""))
        if v is not None:
            show(v, depth + 1)


def session(title, tree):
    print(f"\n{title} (type end to stop)")
    root = {}
    while (line := input("> ").strip()) != "end":
        print(" ", execute(root, line, tree))
    print("Final structure:\nroot/")
    show(root)


with tempfile.TemporaryDirectory() as folder:
    with open(os.path.join(folder, "records.dat"), "w+b") as f:
        index = []
        for roll, name, marks in STUDENTS:
            index.append((roll, f.tell()))
            f.write(RECORD.pack(roll, name.encode(), marks))
        f.flush()
        print("FIXED-SIZE RECORD FILE")
        print(f"{len(STUDENTS)} records * {RECORD.size} bytes = "
              f"{os.path.getsize(f.name)} bytes")
        print("\nDIRECT ACCESS")
        direct(f)
        direct(f)
        index.sort()
        print("\nINDEXED ACCESS")
        print("Index (key -> position):",
              ", ".join(f"{k} -> {p}" for k, p in index))
        indexed(f, index)
        indexed(f, index)
session("SINGLE-LEVEL DIRECTORY", False)
session("TREE DIRECTORY", True)
