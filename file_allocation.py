# Name: Ansh    Roll No: 2401010041
# Contiguous, Linked and Indexed File Allocation

SIZE = 16
OCCUPIED = [3, 8]                   # blocks in use at the start


def longest_run(disk):
    best = run = 0
    for block in disk:
        run = run + 1 if block is None else 0
        best = max(best, run)
    return best


def allocate(method, disk, table, name, text):
    if not name:
        return "REJECTED: empty file name"
    if name in table:
        return "REJECTED: duplicate file name"
    if not text.isdecimal() or int(text) < 1:
        return "REJECTED: invalid file size"
    n = int(text)
    free = [b for b in range(SIZE) if disk[b] is None]

    # All checks are complete before the disk changes.
    if method == "Contiguous":
        start = next((s for s in range(SIZE - n + 1)
                      if all(disk[b] is None for b in range(s, s + n))), None)
        if start is None:
            return (f"REJECTED: no {n} adjacent free blocks "
                    f"(free {len(free)}, longest run {longest_run(disk)})")
        data = list(range(start, start + n))
        table[name] = {"data": data, "start": start, "length": n}
        info = f"start={start}, length={n}, blocks={data}"
    elif method == "Linked":
        if len(free) < n:
            return f"REJECTED: needs {n} blocks, free {len(free)}"
        data = free[:n]
        links = dict(zip(data, data[1:] + [-1]))
        table[name] = {"data": data, "start": data[0], "links": links}
        chain = " -> ".join(map(str, data)) + " -> END"
        info = f"start={data[0]}, end={data[-1]}, chain={chain}"
    else:
        if len(free) < n + 1:
            return f"REJECTED: needs {n + 1} blocks with index, free {len(free)}"
        index, data = free[0], free[1:n + 1]
        table[name] = {"data": data, "index": index}
        disk[index] = name + "*"
        info = f"index block={index}, data blocks={data}"
    for b in data:
        disk[b] = name
    return "ALLOCATED: " + info


def show(disk):
    print("Block map ('.'=free, '#'=occupied at start, '*'=index block):")
    for row in range(0, SIZE, 8):
        print("  " + " ".join(f"{b:>2}:{disk[b] or '.':<4}"
                              for b in range(row, row + 8)))


requests = []
print(f"Disk: {SIZE} blocks, occupied at start: {OCCUPIED}")
while True:
    name = input("File name (done to stop): ").strip()
    if name == "done":
        break
    requests.append((name, input("Number of blocks: ").strip()))

summary = []
for method in ("Contiguous", "Linked", "Indexed"):
    disk = ["#" if b in OCCUPIED else None for b in range(SIZE)]
    table = {}
    print(f"\n{method.upper()} ALLOCATION")
    show(disk)
    for name, text in requests:
        before = disk[:]
        result = allocate(method, disk, table, name, text)
        print(f"{name} ({text}): {result}")
        if result.startswith("REJECTED"):
            print("  Disk unchanged:", disk == before)
    show(disk)
    summary.append((method, len(table), disk.count(None), longest_run(disk)))

print("\nMEASURED RESULTS")
print(f"{'Method':<13}{'Files stored':<14}{'Free blocks':<13}Longest free run")
for row in summary:
    print(f"{row[0]:<13}{row[1]:<14}{row[2]:<13}{row[3]}")
print("\nCOMPARISON")
print("Contiguous: access = direct, 1 read for any block")
print("            overhead = only start and length; fragmentation = external")
print("Linked:     access = sequential, k reads for block k")
print("            overhead = 1 pointer per block; no external fragmentation")
print("Indexed:    access = direct, 2 reads (index + data)")
print("            overhead = 1 index block per file; no external fragmentation")
