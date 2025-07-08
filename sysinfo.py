import os
import platform
from pathlib import Path
from shlex import quote
import pwd
import textwrap

def get_distro_info():
    """Return (name, version) for the running distro."""
    try:
        import distro
        return distro.name(pretty=True), distro.version()
    except ModuleNotFoundError:
        pass

    os_release = Path("/etc/os-release")
    if os_release.is_file():
        data = {}
        for line in os_release.read_text().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                data[k] = v.strip('"')
        return data.get("NAME", "Unknown"), data.get("VERSION", "")
    try:
        # Deprecated fallback
        name, ver, _ = platform.dist()      # type: ignore[attr-defined]
        return name or "Unknown", ver or ""
    except Exception:
        return "Unknown", ""

def get_kernel():
    """Return the kernel version."""
    try:
        kernel = platform.release()
        return kernel
    except Exception:
        return "Unknown"

def get_cwd():
    """Return the curent working directory path."""
    cwd = Path.cwd()
    return cwd

def get_shell_type():
    """
    Detect the user’s shell (bash, zsh, fish…).

    Priority:
    1. $SHELL env var
    2. Login shell from /etc/passwd
    3. Parent process name via psutil (optional)
    """
    # 1. $SHELL
    shell = os.environ.get("SHELL")
    if shell:
        return Path(shell).name

    # 2. /etc/passwd
    try:
        login_shell = pwd.getpwuid(os.getuid()).pw_shell
        if login_shell:
            return Path(login_shell).name
    except Exception:
        pass

    # 3. Parent process (if psutil available)
    try:
        import psutil
        parent = psutil.Process(os.getppid()).name()
        return parent
    except Exception:
        return "Unknown"

def get_sysinfo():
    distro_name, distro_ver = get_distro_info()
    kernel = get_kernel()
    cwd = get_cwd()
    shell = get_shell_type()

    return textwrap.dedent(f"""
        System information :
        Distribution: {str(distro_name)} {str(distro_ver)}
        Kernel Version: {str(kernel)}
        Shell: {str(shell)}
        Working Directory: {str(cwd)}
    """)
