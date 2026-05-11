#!/usr/bin/env bash

# Require root immediately before doing anything else
if [[ $EUID -ne 0 ]]; then
   echo "Error: This script must be run as root" >&2
   exit 1
fi

# ==============================================================================
# Dependency Check
# ==============================================================================
MISSING_DEPS=0
# Added lspci (pciutils) and mkfs.ext4 (e2fsprogs) to the requirements
for cmd in sysbench stress-ng lspci mkfs.ext4; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Error: Required command '$cmd' is not installed." >&2
        MISSING_DEPS=1
    fi
done

if [ "$MISSING_DEPS" -ne 0 ]; then
    echo "Please install missing dependencies and try again." >&2
    exit 1
fi

# ==============================================================================
# Solus Linux Kernel Sanity & Smoke Test Script
# ==============================================================================
clear
echo -e "\033[1m============================================================\033[0m"
echo " Solus Kernel Regression & Smoke Test v0.4"
echo -e "\033[1m============================================================\033[0m"

# Safely create a temporary file
LOG_FILE=$(mktemp /tmp/solus_kernel_test_XXXXXX.log)

# Function to echo to both console and log
log_echo() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

log_echo "============================================================"
log_echo " Starting Kernel Regression & Smoke Test"
log_echo " Date: $(date)"
log_echo " Temporary Log: $LOG_FILE"
log_echo "============================================================\n"


# 1. System & Kernel Information

log_echo "### SYSTEM INFORMATION ###"
log_echo "OS Version: $(grep PRETTY_NAME /etc/os-release | cut -d= -f2 | tr -d '\"')"
log_echo "Kernel Version: $(uname -r)"
log_echo "Architecture: $(uname -m)"
log_echo "Uptime: $(uptime -p)\n"


# 2. Kernel Flags & Modules

log_echo "### KERNEL BOOT FLAGS ###"
# Reads the parameters passed to the kernel at boot by clr-boot-manager/systemd-boot
cat /proc/cmdline | tee -a "$LOG_FILE"
log_echo "\n"

log_echo "### LOADED KERNEL MODULES (Summary) ###"
# Counts modules and lists the top 10 to keep output clean, full list to log
MODULE_COUNT=$(lsmod | wc -l)
log_echo "Total Modules Loaded: $MODULE_COUNT"
log_echo "Top 10 Loaded Modules (See log file for complete list):"
lsmod | head -n 11 | tee -a "$LOG_FILE"
# Silently append the rest to the log
lsmod | tail -n +12 >> "$LOG_FILE"
log_echo "\n"


# 3. Core Function Tests

log_echo "### CORE SUBSYSTEM TESTS ###"

# --- CPU TEST ---
log_echo "[*] Testing CPU Computation..."
if sysbench cpu --cpu-max-prime=10000 run > /dev/null 2>&1; then
    log_echo " -> CPU Test: PASSED (sysbench)"
else
    log_echo " -> CPU Test: FAILED (sysbench error)"
fi

# --- MEMORY TEST ---
log_echo "[*] Testing Memory Allocation..."
if stress-ng --vm 1 --vm-bytes 256M --timeout 5s > /dev/null 2>&1; then
    log_echo " -> Memory Test: PASSED (stress-ng)"
else
    log_echo " -> Memory Test: FAILED (stress-ng error)"
fi

# --- DISK I/O TEST ---
log_echo "[*] Testing Physical Disk I/O..."
TEST_FILE=$(mktemp /var/tmp/kernel_io_test_XXXXXX)
if dd if=/dev/zero of="$TEST_FILE" bs=1M count=50 > /dev/null 2>&1; then
    if dd if="$TEST_FILE" of=/dev/null bs=1M > /dev/null 2>&1; then
        log_echo " -> Disk I/O Test: PASSED"
    else
        log_echo " -> Disk I/O Test: FAILED on Read"
    fi
    rm -f "$TEST_FILE"
else
    log_echo " -> Disk I/O Test: FAILED on Write"
fi

# --- NETWORK TEST ---
log_echo "[*] Testing Network Stack..."
if ip link show lo | grep -q "state UNKNOWN\|state UP"; then
    if ping -c 3 1.1.1.1 > /dev/null 2>&1; then
        log_echo " -> Network Test: PASSED (External Ping Success)"
    else
        log_echo " -> Network Test: WARNING (Routing/External Ping Failed)"
    fi
else
    log_echo " -> Network Test: FAILED (Loopback down)"
fi

# --- RNG / ENTROPY TEST ---
log_echo "[*] Testing Kernel Random Number Generator..."
if dd if=/dev/urandom of=/dev/null bs=1K count=10 > /dev/null 2>&1; then
    log_echo " -> RNG Test: PASSED (/dev/urandom accessible)"
else
    log_echo " -> RNG Test: FAILED (Entropy pool issue)"
fi

# --- VIRTUAL FILESYSTEM TEST ---
log_echo "[*] Testing Virtual Filesystems..."
if [ -d "/proc/1" ] && [ -d "/sys/kernel" ]; then
    log_echo " -> VFS Test: PASSED (/proc and /sys are populated)"
else
    log_echo " -> VFS Test: FAILED (Missing critical VFS structures)"
fi

# --- HARDWARE ENUMERATION TEST ---
log_echo "[*] Testing PCI Bus Enumeration..."
if lspci | grep -q "Host bridge"; then
    log_echo " -> Hardware Test: PASSED (PCI bus enumerated)"
else
    log_echo " -> Hardware Test: FAILED (lspci returned empty or failed)"
fi

# --- FILESYSTEM & BLOCK DEVICE TEST ---
log_echo "[*] Testing Loopback Mount & Filesystem Drivers..."
MNT_DIR=$(mktemp -d /tmp/mnt_test_XXXXXX)
IMG_FILE=$(mktemp /var/tmp/img_test_XXXXXX.img)

if dd if=/dev/zero of="$IMG_FILE" bs=1M count=10 > /dev/null 2>&1 && \
   mkfs.ext4 -q -F "$IMG_FILE" > /dev/null 2>&1 && \
   mount -o loop "$IMG_FILE" "$MNT_DIR" > /dev/null 2>&1; then
   
   umount "$MNT_DIR"
   log_echo " -> Mount Test: PASSED (ext4 loopback successful)"
else
   log_echo " -> Mount Test: FAILED (Block/VFS layer error)"
fi

rm -f "$IMG_FILE"
rmdir "$MNT_DIR"

log_echo "\n"


# 4. Kernel Log (dmesg) Error Audit

log_echo "### KERNEL LOG AUDIT (dmesg warnings/errors) ###"
log_echo "Checking for 'error', 'fail', or 'critical' in recent kernel ring buffer..."

DMESG_ERRORS=$(dmesg --level=err,crit)

if [ -z "$DMESG_ERRORS" ]; then
    log_echo " -> Status: CLEAN (No critical errors found in dmesg)"
else
    log_echo " -> Status: WARNING (Errors found. Displaying last 5):"
    echo "$DMESG_ERRORS" | tail -n 5 | tee -a "$LOG_FILE"
fi

log_echo "\n============================================================"
log_echo " Test Complete."
log_echo "============================================================"


# 5. Move Log to User Home Directory

# Determine the real user's home directory (even if run with sudo)
if [ -n "$SUDO_USER" ]; then
    REAL_USER="$SUDO_USER"
    USER_HOME=$(eval echo ~$REAL_USER)
else
    REAL_USER="$USER"
    USER_HOME="$HOME"
fi

FINAL_LOG="$USER_HOME/solus_kernel_test_$(date +%Y%m%d_%H%M%S).log"

# Move the file and adjust ownership so the user can easily read/delete it
mv "$LOG_FILE" "$FINAL_LOG"
chown "$REAL_USER:$REAL_USER" "$FINAL_LOG"

echo "Log file saved to: $FINAL_LOG"
