# Name: Ansh    Roll No: 2401010041
# Contiguous Allocation, Swapping and Address Translation
# All sizes are in KB. Each block holds one process at a time.

def read_numbers(msg, minimum=1):
    while True:
        try:
            values = [int(x) for x in input(msg).split()]
            if values and min(values) >= minimum:
                return values
        except ValueError:
            pass
        print("  Enter whole numbers of at least", minimum)


def read_one(msg, minimum=0):
    while True:
        values = read_numbers(msg, minimum)
        if len(values) == 1:
            return values[0]
        print("  Enter one number")


def choose_block(method, blocks, memory, size):
    free = [b for b in range(len(blocks))
            if memory[b] is None and blocks[b] >= size]
    if not free:
        return None
    if method == "First Fit":
        return free[0]
    if method == "Best Fit":
        return min(free, key=lambda b: blocks[b])
    return max(free, key=lambda b: blocks[b])      # Worst Fit


def show(blocks, memory, procs):
    print(f"{'Block':<7}{'Size':<7}{'Process':<9}Remaining")
    for b, size in enumerate(blocks):
        p = memory[b]
        name = "Free" if p is None else f"P{p + 1}"
        left = size if p is None else size - procs[p]
        print(f"B{b + 1:<6}{size:<7}{name:<9}{left}")


def allocate(method, blocks, procs):
    memory = [None] * len(blocks)           # fresh memory for each method
    print(f"\n{method.upper()}")
    for p, size in enumerate(procs):
        b = choose_block(method, blocks, memory, size)
        if b is None:
            print(f"P{p + 1} ({size} KB): UNALLOCATED")
        else:
            memory[b] = p
            print(f"P{p + 1} ({size} KB): allocated to B{b + 1}")
    show(blocks, memory, procs)
    return memory


def swap(blocks, procs, memory):
    print("\nSWAPPING (First Fit memory)")
    out = read_one("Outgoing process number: ", 1) - 1
    inc = read_one("Incoming process number: ", 1) - 1
    print("Memory before swapping:")
    show(blocks, memory, procs)
    if out not in memory:
        print("REJECTED: outgoing process is not in memory")
    elif inc >= len(procs) or inc in memory:
        print("REJECTED: incoming process is invalid or already in memory")
    else:
        old = memory.index(out)
        memory[old] = None
        b = choose_block("First Fit", blocks, memory, procs[inc])
        if b is None:
            memory[old] = out
            print(f"REJECTED: P{inc + 1} does not fit, P{out + 1} restored")
        else:
            memory[b] = inc
            print(f"P{out + 1} swapped out of B{old + 1}, "
                  f"P{inc + 1} swapped in to B{b + 1}")
    print("Memory after swapping:")
    show(blocks, memory, procs)


def translate():
    print("\nADDRESS TRANSLATION")
    base = read_one("Base: ")
    limit = read_one("Limit: ")
    logical = read_one("Logical address: ")
    print(f"Check: {logical} < {limit} is {logical < limit}")
    if logical < limit:
        print(f"Physical address = {base} + {logical} = {base + logical}")
    else:
        print("REJECTED: logical address is outside the limit")


blocks = read_numbers("Block sizes (KB): ")
procs = read_numbers("Process sizes (KB): ")
memory = allocate("First Fit", blocks, procs)
allocate("Best Fit", blocks, procs)
allocate("Worst Fit", blocks, procs)
swap(blocks, procs, memory)
for _ in range(2):                          # one valid, one invalid test
    translate()
