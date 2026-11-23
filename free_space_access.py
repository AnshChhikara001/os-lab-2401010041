# Name: Ansh    Roll No: 2401010041
# Free-Space Management, Deletion and Access Control
import os
import platform
import stat
import subprocess
import tempfile
import time

SIZE = 16
bitmap = [0] * SIZE                 # 0 = free, 1 = occupied
free_list = list(range(SIZE))
files = {}


def show():
    print("Bitmap   :", "".join(map(str, bitmap)))
    print("Free list:", free_list)
    print("Files    :", files)
    used = [b for blocks in files.values() for b in blocks]
    ok = (len(used) == len(set(used))
          and not set(used) & set(free_list)
          and sorted(used + free_list) == list(range(SIZE))
          and all(bitmap[b] == (b in used) for b in range(SIZE)))
    print("Check    :", "PASS - no block is both allocated and free"
          if ok else "FAIL")


def allocate(name, n):
    print(f"\nAllocate {name}, {n} blocks")
    if name in files or n < 1:
        print("REJECTED: duplicate name or invalid size")
    elif n > len(free_list):
        print(f"REJECTED: only {len(free_list)} blocks are free")
    else:
        files[name] = free_list[:n]
        del free_list[:n]
        for b in files[name]:
            bitmap[b] = 1
    show()


def delete(name):
    print(f"\nDelete {name}")
    if name not in files:
        print("REJECTED: file not found")
    else:
        for b in files.pop(name):
            bitmap[b] = 0
            free_list.append(b)
        free_list.sort()
    show()


def chmod(mode, path):
    subprocess.run(["chmod", mode, path], check=True)
    print(f"\nchmod {mode} ->", stat.filemode(os.stat(path).st_mode),
          oct(os.stat(path).st_mode & 0o777))


def test(label, mode, path):
    try:
        with open(path, mode) as f:
            f.read() if mode == "r" else f.write("new line\n")
        print(f"{label}: ALLOWED")
    except PermissionError:
        print(f"{label}: DENIED (permission denied)")


print("FREE-SPACE MANAGEMENT")
show()
allocate("A", 5)
allocate("B", 4)
allocate("C", 20)
delete("A")
allocate("D", 6)
delete("X")

print("\nACCESS CONTROL")
print("System:", platform.system())
if os.geteuid() == 0:
    raise SystemExit("Run as a normal user. Root bypasses permissions.")
folder = tempfile.mkdtemp()
path = os.path.join(folder, "test.txt")
try:
    with open(path, "w") as f:
        f.write("test data\n")
    s = os.stat(path)
    print("Test file created: test.txt")
    print(f"Owner UID={s.st_uid}, GID={s.st_gid}, inode={s.st_ino}, "
          f"links={s.st_nlink}")
    print("Size:", s.st_size, "bytes, modified:",
          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s.st_mtime)))
    print("Permissions:", stat.filemode(s.st_mode), oct(s.st_mode & 0o777))
    chmod("u=rw,g=r,o=", path)      # symbolic
    test("Read", "r", path)
    test("Write", "a", path)
    chmod("400", path)              # octal, least privilege for a reader
    print("Least privilege: a reader needs only read permission")
    test("Read", "r", path)
    test("Write", "a", path)
    chmod("u-r", path)
    test("Read", "r", path)
finally:
    if os.path.exists(path):
        chmod("600", path)
        print("Safe permissions restored")
        os.remove(path)
    os.rmdir(folder)
    print("Temporary file and directory removed:", not os.path.exists(folder))
