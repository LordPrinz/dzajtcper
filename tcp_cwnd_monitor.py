#!/usr/bin/env python3
import os
import sys
import socket
import struct
from datetime import datetime

# Dodaj systemową ścieżkę dla BCC
sys.path.insert(0, '/usr/lib/python3/dist-packages')
from bcc import BPF

# Ścieżka do pliku CSV w katalogu projektu
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(SCRIPT_DIR, "cwnd_log.csv")

def check_root():
    if os.geteuid() != 0:
        print("[ERROR] Ten skrypt wymaga uprawnień roota.")
        sys.exit(1)

bpf_program = r"""
#include <uapi/linux/ptrace.h>
#include <uapi/linux/tcp.h>

struct data_t {
    u32 pid;
    u32 saddr;
    u32 daddr;
    u16 sport;
    u16 dport;
    u32 snd_cwnd;
};

BPF_PERF_OUTPUT(events);

TRACEPOINT_PROBE(tcp, tcp_probe) {
    struct data_t data = {};
    u64 id = bpf_get_current_pid_tgid();
    data.pid = id >> 32;

    bpf_probe_read_kernel(&data.saddr, sizeof(data.saddr), args->saddr);
    bpf_probe_read_kernel(&data.daddr, sizeof(data.daddr), args->daddr);

    data.sport    = args->sport;
    data.dport    = args->dport;
    data.snd_cwnd = args->snd_cwnd;

    events.perf_submit(args, &data, sizeof(data));
    return 0;
}
"""

def inet_ntoa(addr):
    return socket.inet_ntop(socket.AF_INET, struct.pack("I", addr))

def init_log():
    # Jeśli plik nie istnieje, dodaj nagłówek CSV
    if not os.path.exists(LOGFILE):
        with open(LOGFILE, "w") as f:
            f.write("timestamp,pid,saddr,sport,daddr,dport,cwnd\n")

def print_event(cpu, data, size):
    ev = b["events"].event(data)
    ts = datetime.now().isoformat()
    line = (
        f"{ts},"
        f"{ev.pid},"
        f"{inet_ntoa(ev.saddr)},{ev.sport},"
        f"{inet_ntoa(ev.daddr)},{ev.dport},"
        f"{ev.snd_cwnd}"
    )
    # wypisz na konsolę
    print(f"{ts}  PID {ev.pid:>5}  "
          f"{inet_ntoa(ev.saddr)}:{ev.sport:>5} -> "
          f"{inet_ntoa(ev.daddr)}:{ev.dport:>5}   cwnd={ev.snd_cwnd}")
    # zapisz do pliku
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")

def main():
    check_root()
    init_log()

    global b
    b = BPF(text=bpf_program)
    b["events"].open_perf_buffer(print_event)

    print(f"Śledzenie tcp_probe (cwnd)... (Ctrl+C aby zakończyć)\nLog zapisuje się do {LOGFILE}\n")
    try:
        while True:
            b.perf_buffer_poll()
    except KeyboardInterrupt:
        print("\nZakończono monitorowanie.")

if __name__ == "__main__":
    main()
