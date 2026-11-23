# Name: Ansh    Roll No: 2401010041
# Paging and Segmentation - address translation

def read_int(msg, minimum=0):
    while True:
        try:
            value = int(input(msg))
            if value >= minimum:
                return value
            print("  Value must be at least", minimum)
        except ValueError:
            print("  Enter a whole number")


def paging():
    print("\n--- PAGING ---")
    size = read_int("Page size (bytes): ", 1)
    n = read_int("Number of pages: ", 1)
    table = [read_int(f"Frame for page {i} (-1 = unmapped): ", -1)
             for i in range(n)]
    logical = read_int("Logical address: ")

    page = logical // size
    offset = logical % size
    print(f"Page number = {logical} // {size} = {page}")
    print(f"Offset      = {logical} % {size} = {offset}")

    if page >= n:
        print(f"REJECTED: invalid page {page} (valid: 0 to {n - 1})")
    elif table[page] == -1:
        print(f"REJECTED: page {page} is unmapped (page fault)")
    else:
        frame = table[page]
        print(f"Page-table entry is valid: page {page} -> frame {frame}")
        print(f"Physical address = {frame} * {size} + {offset}"
              f" = {frame * size + offset}")


def segmentation():
    print("\n--- SEGMENTATION ---")
    n = read_int("Number of segments: ", 1)
    table = []
    for i in range(n):
        base = read_int(f"Base of segment {i}: ")
        limit = read_int(f"Limit of segment {i}: ")
        table.append((base, limit))
    seg = read_int("Segment number: ")
    offset = read_int("Offset: ")

    if seg >= n:
        print(f"REJECTED: invalid segment {seg} (valid: 0 to {n - 1})")
        return
    base, limit = table[seg]
    print(f"Segment {seg}: base = {base}, limit = {limit}")
    print(f"Check offset < limit: {offset} < {limit} is {offset < limit}")
    if offset >= limit:
        print("REJECTED: offset is outside the segment")
    else:
        print(f"Physical address = {base} + {offset} = {base + offset}")


while True:
    print("\n1. Paging  2. Segmentation  3. Exit")
    choice = read_int("Choice: ", 1)
    if choice == 1:
        paging()
    elif choice == 2:
        segmentation()
    elif choice == 3:
        break
    else:
        print("Invalid choice")
