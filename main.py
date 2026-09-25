import platform
import sys
import urllib.request

def get_hosts_path():
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"

HOSTS_PATH = get_hosts_path()
REDIRECT_IP = "127.0.0.1"
START_MARKER = "# >>> CLOUD SYSTEM BLOCKER START >>>"
END_MARKER = "# <<< CLOUD SYSTEM BLOCKER END <<<"

# Your live GitHub raw blocklist URL
BLOCKLIST_URL = "https://raw.githubusercontent.com/whareverguy1/system-blocker/main/blocklist.txt"

def fetch_cloud_domains():
    print("[INFO] Fetching live blocklist from your GitHub repository...")
    req = urllib.request.Request(BLOCKLIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            # Decode line by line to safely handle the large file size
            domains = []
            for line in response:
                decoded_line = line.decode('utf-8').strip()
                if decoded_line and not decoded_line.startswith('#'):
                    domains.append(decoded_line)
        print(f"[SUCCESS] Downloaded {len(domains)} domains from GitHub!")
        return domains
    except Exception as e:
        print(f"[ERROR] Failed to fetch cloud blocklist: {e}")
        return []

def apply_blocks():
    domains = fetch_cloud_domains()
    if not domains:
        print("[INFO] No domains found to block.")
        return

    try:
        print("[INFO] Reading local system hosts file...")
        with open(HOSTS_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Remove old block section if it exists
        if START_MARKER in content:
            content = content.split(START_MARKER)[0].rstrip("\n") + "\n"

        print("[INFO] Applying system-wide blocks (this may take a moment for large lists)...")
        block_lines = [f"\n{START_MARKER}\n"]
        for domain in domains:
            block_lines.append(f"{REDIRECT_IP}\t{domain}\n")
        block_lines.append(f"{END_MARKER}\n")

        with open(HOSTS_PATH, "w", encoding="utf-8") as f:
            f.write(content)
            f.writelines(block_lines)

        print(f"[SUCCESS] Successfully blocked {len(domains)} adult and distraction domains system-wide!")
    except PermissionError:
        print("[ERROR] Permission denied! You must run your terminal or command prompt as Administrator (Windows) or with sudo (Linux/Mac).")

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
            print("[INFO] No active cloud blocks found in the hosts file.")
    except PermissionError:
        print("[ERROR] Permission denied! Run with Administrator/root privileges.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        choice = input("Do you want to 'apply' or 'remove' the cloud blocks? (apply/remove): ").strip().lower()
    else:
        choice = sys.argv[1].lower()

    if choice == "apply":
        apply_blocks()
    elif choice == "remove":
        remove_blocks()
    else:
        print("Invalid option. Use 'apply' or 'remove'.")
