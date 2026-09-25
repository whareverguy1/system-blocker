import platform
import sys

def get_hosts_path():
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"

HOSTS_PATH = get_hosts_path()
REDIRECT_IP = "127.0.0.1"
START_MARKER = "# >>> SYSTEM BLOCKER APP START >>>"
END_MARKER = "# <<< SYSTEM BLOCKER APP END <<<"

def load_domains():
    try:
        with open("blocklist.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("[INFO] blocklist.txt not found.")
        return []

def apply_blocks():
    domains = load_domains()
    if not domains:
        print("[INFO] No domains to block.")
        return
    try:
        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        if START_MARKER in content:
            content = content.split(START_MARKER)[0].rstrip("\n") + "\n"

        block_lines = [f"\n{START_MARKER}\n"]
        for domain in domains:
            block_lines.append(f"{REDIRECT_IP}\t{domain}\n")
        block_lines.append(f"{END_MARKER}\n")

        with open(HOSTS_PATH, "w", encoding="utf-8") as f:
            f.write(content)
            f.writelines(block_lines)

        print(f"[SUCCESS] Successfully blocked {len(domains)} domains system-wide!")
    except PermissionError:
        print("[ERROR] Permission denied! Run your terminal as Administrator / with sudo.")

def remove_blocks():
    try:
        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        if START_MARKER in content:
            content = content.split(START_MARKER)[0].rstrip("\n") + "\n"
            with open(HOSTS_PATH, "w", encoding="utf-8") as f:
                f.write(content)
            print("[SUCCESS] All custom blocks removed successfully!")
        else:
            print("[INFO] No active blocks found in the hosts file.")
    except PermissionError:
        print("[ERROR] Permission denied! Run your terminal as Administrator / with sudo.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        choice = input("Do you want to 'apply' or 'remove' the blocks? (apply/remove): ").strip().lower()
    else:
        choice = sys.argv[1].lower()

    if choice == "apply":
        apply_blocks()
    elif choice == "remove":
        remove_blocks()
    else:
        print("Invalid option. Use 'apply' or 'remove'.")
