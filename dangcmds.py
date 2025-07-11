dangerous_linux_commands = {
    "File Deletion": [
        "rm -fr",
        "rm -r"
        "rm --no-preserve-root",
        "rm -r --no-preserve-root",
        "mkfs",
        "mkfs.ext4",
        "mkfs.xfs",
        "mkfs.vfat",
        "dd if=",
        "dd of=/dev/",
        "shred",      # Securely deletes disk content
        "mv /",
        "find / ",
        "crontab -r",
        "wipefs",
    ],
    "Fork Bombs": [
        ":(){:|:&};:",       # Bash fork bomb
        ">:()",
        "perl -e 'fork while 1'",  # Perl fork bomb
    ],
    "Network Manipulation": [
        "ifconfig eth0 down",  # Disables network interface
        "ip link set eth0 down",
        "iptables -F",         # Flushes all firewall rules
        "route del default",   # Deletes default route
    ],
    "Overwriting Or Corrupting Files": [
        ">:filename",          # Truncates a file
        "cat /dev/zero >",  # Overwrites file with zeros
        "cat /dev/urandom >",
        "echo > file",         # Clears file content
    ],
    "System Shutdown Reboot": [
        "halt",                # Shuts down system
        "reboot",              # Reboots system
        "shutdown",        # Immediate shutdown
        "poweroff",
        "init 0",
        "init 6",
        "kill -9 1",
    ],
    "User And Permission Manipulation": [
        "chmod",
        "chown",  # Changes ownership recursively
        "userdel",        # Deletes root user
        "passwd",      # Removes root password
    ],
    "Dangerous Variables": [
        "eval $(rm -rf /)",    # Executes dangerous eval
        "command $(rm -rf *)", # Dangerous command substitution
    ],
    "Writing To Disk": [
        "> /dev/",
        ">/dev/",
    ],
    "Resource Exhaustion": [
        "dd if=/dev/zero of=/dev/null &",  # CPU hog
        "tail -f /dev/null",  # Keeps process running forever
    ],
    "Filesystem Modification": [
        "mount",    # Overwrites root mount
        "umount",            # Unmounts root
    ]
}


def is_dangerous(command: str):
    for category, commands in dangerous_linux_commands.items():
        for dangerous in commands:
            if command.lower() in dangerous:
                return True, category
    return False, ""
