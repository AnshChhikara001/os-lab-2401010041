# Name: Ansh    Roll No: 2401010041
# File Operations and Sequential Access
import os
import shutil
import stat
import time

BASE = os.path.realpath("fs_test_dir")


def safe(name):                     # allow paths only inside the test directory
    path = os.path.realpath(os.path.join(BASE, name))
    if os.path.dirname(path) != BASE:
        raise PermissionError(f"'{name}' is outside the test directory")
    return path


def attempt(title, action):
    print(f"\n{title}")
    try:
        action()
    except FileNotFoundError as e:
        print("ERROR: file not found -", os.path.basename(e.filename or ""))
    except FileExistsError as e:
        print("ERROR: already exists -", os.path.basename(e.filename or str(e)))
    except (OSError, ValueError) as e:
        print("ERROR:", e)


def create():
    with open(safe("students.txt"), "x") as f:
        print("File created and opened for writing")
        for roll, name, marks in [(101, "Asha", 82), (102, "Ravi", 75),
                                  (103, "Meera", 91)]:
            f.write(f"{roll},{name},{marks}\n")
    print("3 records written, file closed =", f.closed)


def read(name="students.txt"):
    with open(safe(name)) as f:     # reopen and read in order
        for number, line in enumerate(f, 1):
            roll, student, marks = line.strip().split(",")
            print(f"Record {number}: roll={roll} name={student} marks={marks}")


def append():
    with open(safe("students.txt"), "a") as f:
        f.write("104,Kabir,68\n")
    print("Record appended. File content now:")
    read()


def rename():
    target = safe("records.txt")
    if os.path.exists(target):
        raise FileExistsError("records.txt")
    os.rename(safe("students.txt"), target)
    print("Renamed students.txt to records.txt")
    print("Directory list:", sorted(os.listdir(BASE)))


def metadata():
    s = os.stat(safe("records.txt"))
    print("Size        :", s.st_size, "bytes")
    print("Permissions :", stat.filemode(s.st_mode), oct(s.st_mode & 0o777))
    for label, t in [("Accessed", s.st_atime), ("Modified", s.st_mtime),
                     ("Changed", s.st_ctime)]:
        print(f"{label:<12}:", time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(t)))


def delete():
    shutil.copy2(safe("records.txt"), safe("evidence.txt"))
    print("Evidence saved in evidence.txt:")
    read("evidence.txt")
    os.remove(safe("records.txt"))
    print("records.txt deleted")
    print("Directory list:", sorted(os.listdir(BASE)))


try:
    os.mkdir(BASE)
except FileExistsError:
    raise SystemExit("ERROR: fs_test_dir already exists. Remove it first.")
print("Test directory created: fs_test_dir")
attempt("CREATE AND WRITE", create)
attempt("SEQUENTIAL READ", read)
attempt("APPEND", append)
attempt("RENAME AND LIST", rename)
attempt("METADATA", metadata)
attempt("DELETE", delete)
attempt("FAILED: read a deleted file", lambda: read("records.txt"))
attempt("FAILED: create an existing file", lambda: open(safe("evidence.txt"), "x"))
attempt("FAILED: use a path outside the directory", lambda: read("../other.txt"))
