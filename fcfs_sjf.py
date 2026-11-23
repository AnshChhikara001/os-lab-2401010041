# Name: Ansh    Roll No: 2401010041
# FCFS and non-preemptive SJF scheduling

def read_int(msg, minimum):
    while True:
        try:
            value = int(input(msg))
            if value >= minimum:
                return value
        except ValueError:
            pass
        print(f"  INVALID: enter a whole number of at least {minimum}")


def read_processes():
    procs = []
    for _ in range(read_int("Number of processes: ", 1)):
        while True:
            pid = input("Process ID: ").strip()
            if pid and pid not in [p[0] for p in procs]:
                break
            print("  INVALID: Process ID is empty or duplicate")
        arrival = read_int("  Arrival time: ", 0)
        burst = read_int("  Burst time: ", 1)
        procs.append((pid, arrival, burst))
    return tuple(procs)                 # a tuple cannot be changed


def fcfs_key(i, p):                     # arrival, then input order
    return (p[1], i)


def sjf_key(i, p):                      # burst, then arrival, then input order
    return (p[2], p[1], i)


def schedule(procs, key):
    waiting = list(enumerate(procs))    # a copy, original data is preserved
    time, timeline = 0, []
    while waiting:
        ready = [x for x in waiting if x[1][1] <= time]
        if not ready:
            next_time = min(p[1] for _, p in waiting)
            timeline.append(("IDLE", time, next_time))
            time = next_time
            continue
        chosen = min(ready, key=lambda x: key(*x))
        waiting.remove(chosen)
        pid, _, burst = chosen[1]
        timeline.append((pid, time, time + burst))
        time += burst
    return timeline


def show(title, rule, procs, timeline):
    print(f"\n{title}\nTie-breaking rule: {rule}")
    print("Execution sequence:", " -> ".join(t[0] for t in timeline))
    print(f"{'Process':<10}{'Start':<8}End")
    for pid, start, end in timeline:
        print(f"{pid:<10}{start:<8}{end}")
    ends = {pid: end for pid, _, end in timeline}
    tat = [ends[pid] - a for pid, a, b in procs]
    wait = [ends[pid] - a - b for pid, a, b in procs]
    print(f"Average waiting time    = {sum(wait)}/{len(procs)}"
          f" = {sum(wait) / len(procs):.2f}")
    print(f"Average turnaround time = {sum(tat)}/{len(procs)}"
          f" = {sum(tat) / len(procs):.2f}")


def show_input(procs):
    print(f"{'Process':<10}{'Arrival':<10}Burst")
    for pid, arrival, burst in procs:
        print(f"{pid:<10}{arrival:<10}{burst}")


processes = read_processes()
print("\nORIGINAL DATA")
show_input(processes)
show("FCFS", "same arrival time -> input order",
     processes, schedule(processes, fcfs_key))
show("SJF (NON-PREEMPTIVE)", "same burst time -> earlier arrival, then input order",
     processes, schedule(processes, sjf_key))
print("\nDATA AFTER BOTH ALGORITHMS (unchanged)")
show_input(processes)
