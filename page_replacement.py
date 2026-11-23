# Name: Ansh    Roll No: 2401010041
# Demand Paging, Page Replacement and Thrashing

THRASHING_LIMIT = 0.75   # fault ratio at or above this = thrashing example


def read_numbers(msg, minimum):
    while True:
        try:
            values = [int(x) for x in input(msg).split()]
            if values and min(values) >= minimum:
                return values
            print("  Enter values of at least", minimum)
        except ValueError:
            print("  Enter whole numbers separated by spaces")


def choose_victim(name, frames, refs, i, loaded, used):
    if name == "FIFO":                       # oldest loaded page
        return min(frames, key=lambda p: loaded[p])
    if name == "LRU":                        # least recently used page
        return min(frames, key=lambda p: used[p])
    future = refs[i + 1:]                    # Optimal: farthest next use
    return max(frames, key=lambda p: future.index(p) if p in future
               else len(refs))


def simulate(name, refs, count):
    frames, loaded, used = [], {}, {}
    hits = faults = 0
    print(f"\n{name} with {count} frame(s)")
    print(f"{'Ref':<5}{'Result':<8}{'Victim':<8}Frames")
    for i, page in enumerate(refs):
        victim = "-"
        if page in frames:
            hits += 1
            result = "Hit"
        else:
            faults += 1
            result = "Fault"
            if len(frames) < count:          # fill free frames first
                frames.append(page)
            else:
                victim = choose_victim(name, frames, refs, i, loaded, used)
                frames[frames.index(victim)] = page
            loaded[page] = i
        used[page] = i
        state = frames + ["-"] * (count - len(frames))
        print(f"{page:<5}{result:<8}{victim:<8}"
              + " ".join(str(p) for p in state))
    n = len(refs)
    print(f"Hits = {hits}, Faults = {faults}")
    print(f"Hit ratio = {hits}/{n} = {hits / n:.2f}, "
          f"Fault ratio = {faults}/{n} = {faults / n:.2f}")
    return hits, faults


refs = read_numbers("Reference string: ", 0)
counts = read_numbers("Frame counts to test: ", 1)
results = []
for count in counts:
    for name in ("FIFO", "LRU", "Optimal"):
        results.append((count, name) + simulate(name, refs, count))

n = len(refs)
print("\nCOMPARISON")
print(f"{'Frames':<8}{'Algorithm':<11}{'Hits':<6}{'Faults':<8}"
      f"{'Hit ratio':<11}{'Fault ratio':<13}Thrashing")
for count, name, hits, faults in results:
    thrash = "YES" if faults / n >= THRASHING_LIMIT else "no"
    print(f"{count:<8}{name:<11}{hits:<6}{faults:<8}"
          f"{hits / n:<11.2f}{faults / n:<13.2f}{thrash}")
for count in counts:
    rows = [r for r in results if r[0] == count]
    best = min(r[3] for r in rows)
    names = ", ".join(r[1] for r in rows if r[3] == best)
    print(f"Fewest faults with {count} frame(s): {names} ({best})")
