#!/usr/bin/env python3
import sys
import time

from serial import Serial
from serial.tools import list_ports

# MediaTek Preloader VID/PID
MTK_VID = 0x0e8d
MTK_PID = 0x2000

BOOTCMD = sys.argv[1].strip().upper() if len(sys.argv) > 1 else "FASTBOOT"
BOOTSEQ = BOOTCMD.encode("ascii")
CONFIRM = b"READY" + BOOTSEQ[:-4:-1]  # from your original logic

def find_mtk_ports():
    """Return list of candidate MTK preloader ports."""
    ports = list_ports.comports()
    candidates = []
    for p in ports:
        vid, pid = p.vid, p.pid
        if vid is not None and pid is not None:
            if vid == MTK_VID and pid == MTK_PID:
                candidates.append(p.device)
        # fallback: any ttyACM* is a maybe
        if p.device and p.device.startswith("/dev/ttyACM"):
            if p.device not in candidates:
                candidates.append(p.device)
    return candidates

def wait_for_mtk_port(timeout=30.0, poll_interval=0.2):
    print(f"Requested mode: {BOOTCMD}")
    print(f"Waiting for MTK preloader (VID=0x{MTK_VID:04x}, PID=0x{MTK_PID:04x})...")
    print("Run this, THEN plug the phone in / short-press power.")
    start = time.time()
    while time.time() - start < timeout:
        ports = find_mtk_ports()
        if ports:
            print(f"\nFound port(s): {', '.join(ports)}")
            return ports[0]
        print(".", end="", flush=True)
        time.sleep(poll_interval)
    print("\nTimeout: no suitable port found.")
    return None

def send_boot_sequence(dev_path):
    print(f"Opening {dev_path} at 115200...")
    s = Serial(dev_path, 115200, timeout=1)
    try:
        while True:
            s.write(BOOTSEQ)
            resp = s.read(8)
            print(f"Got: {resp!r}")
            if resp == CONFIRM:
                print("Boot sequence confirmed by device.")
                break
    finally:
        s.close()
    print("Done.")

def main():
    dev = wait_for_mtk_port()
    if not dev:
        sys.exit(2)
    send_boot_sequence(dev)

if __name__ == "__main__":
    try:
        main()
    except ModuleNotFoundError:
        print("pyserial not installed. Install with:")
        print("  sudo apt install python3-serial")
        sys.exit(1)
