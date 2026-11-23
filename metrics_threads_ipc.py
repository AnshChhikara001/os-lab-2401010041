# Name: Ansh    Roll No: 2401010041
# Scheduling Metrics, Threads and IPC
import multiprocessing as mp
import os
import threading
from collections import deque

# Process ID, arrival time, burst time
PROCS = (("P1", 2, 6), ("P2", 3, 8), ("P3", 4, 3), ("P4", 4, 3), ("P5", 30, 4))
QUANTUM = 3


def non_preemptive(key):
    waiting, time, line = list(PROCS), 0, []
    while waiting:
        ready = [p for p in waiting if p[1] <= time]
        if not ready:
            nxt = min(p[1] for p in waiting)
            line.append(("IDLE", time, nxt))
            time = nxt
            continue
        p = min(ready, key=key)         # tie: input order
        waiting.remove(p)
        line.append((p[0], time, time + p[2]))
        time += p[2]
    return line


def round_robin():
    coming = deque(sorted(PROCS, key=lambda p: p[1]))
    left = {p[0]: p[2] for p in PROCS}
    queue, time, line = deque(), 0, []
    while coming or queue:
        while coming and coming[0][1] <= time:
            queue.append(coming.popleft()[0])
        if not queue:
            line.append(("IDLE", time, coming[0][1]))
            time = coming[0][1]
            continue
        pid = queue.popleft()
        run = min(QUANTUM, left[pid])
        line.append((pid, time, time + run))
        time += run
        left[pid] -= run
        while coming and coming[0][1] <= time:   # new arrivals join first
            queue.append(coming.popleft()[0])
        if left[pid]:
            queue.append(pid)
    return line


def report(title, line):
    print(f"\n{title}\nGantt chart:")
    border = "+" + "------+" * len(line)
    print(border)
    print("|" + "".join(f"{pid:^6}|" for pid, _, _ in line))
    print(border)
    print("".join(f"{start:<7}" for _, start, _ in line) + str(line[-1][2]))
    print("Slices:", ", ".join(f"{p}[{s}-{e}]" for p, s, e in line))
    print(f"{'PID':<6}{'AT':<5}{'BT':<5}{'CT':<5}{'TAT':<5}{'WT':<5}RT")
    total = [0, 0, 0]
    for pid, at, bt in PROCS:
        ct = max(e for p, s, e in line if p == pid)
        rt = min(s for p, s, e in line if p == pid) - at
        tat = ct - at
        wt = tat - bt
        total = [a + b for a, b in zip(total, (tat, wt, rt))]
        print(f"{pid:<6}{at:<5}{bt:<5}{ct:<5}{tat:<5}{wt:<5}{rt}")
    avg = [t / len(PROCS) for t in total]
    print(f"Average TAT = {avg[0]:.2f}, WT = {avg[1]:.2f}, RT = {avg[2]:.2f}")
    return avg


def threads():
    print("\nTHREADS")
    lock, barrier, results = threading.Lock(), threading.Barrier(3), []

    def work(low, high):
        barrier.wait()                  # all threads are alive together
        answer = sum(range(low, high + 1))
        with lock:
            results.append(answer)
            print(f"{threading.current_thread().name}: "
                  f"id={threading.get_ident()}, "
                  f"work: sum {low} to {high} = {answer}")

    pool = [threading.Thread(target=work, name=f"Thread-{i + 1}",
                             args=(i * 100 + 1, (i + 1) * 100))
            for i in range(3)]
    for t in pool:
        t.start()
    for t in pool:
        t.join()
    print("Total of all threads =", sum(results))


def child(conn):
    message = conn.recv()
    conn.send((os.getpid(), message, f"Received {len(message)} characters"))
    conn.close()


def ipc():
    print("\nIPC WITH multiprocessing.Pipe")
    parent_end, child_end = mp.Pipe()
    p = mp.Process(target=child, args=(child_end,))
    p.start()
    child_end.close()
    message = "Hello from parent"
    print(f"Parent (sender, PID {os.getpid()}) transmitted: {message}")
    parent_end.send(message)
    pid, received, reply = parent_end.recv()
    p.join()
    print(f"Child (receiver, PID {pid}) received: {received}")
    print(f"Child (sender, PID {pid}) transmitted reply: {reply}")
    print(f"Parent (receiver, PID {os.getpid()}) received reply: {reply}")
    print("Messages match:", message == received, "| Child exit code:", p.exitcode)


if __name__ == "__main__":
    rows = [(name, report(name, line)) for name, line in (
        ("FCFS", non_preemptive(lambda p: p[1])),
        ("SJF", non_preemptive(lambda p: (p[2], p[1]))),
        (f"ROUND ROBIN (quantum {QUANTUM})", round_robin()))]
    print("\nCOMPARISON OF AVERAGES")
    print(f"{'Algorithm':<26}{'TAT':<8}{'WT':<8}RT")
    for name, a in rows:
        print(f"{name:<26}{a[0]:<8.2f}{a[1]:<8.2f}{a[2]:.2f}")
    threads()
    ipc()
