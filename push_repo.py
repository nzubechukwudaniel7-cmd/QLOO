import subprocess
import sys
import dulwich.porcelain as p

try:
    print("[*] Retrieving GitHub authentication token from gh CLI...")
    result = subprocess.run([r".\gh.exe", "auth", "token"], capture_output=True, text=True)
    if result.returncode != 0 or not result.stdout.strip():
        print("[-] Not authenticated yet. Please run: .\\gh.exe auth login")
        sys.exit(1)

    token = result.stdout.strip()
    remote_url = f"https://{token}@github.com/nzubechukwudaniel7-cmd/QLOO.git"
    print("[*] Pushing repository to https://github.com/nzubechukwudaniel7-cmd/QLOO.git (branch: main)...")
    
    p.push(".", remote_url, "main")
    print("[+] SUCCESS! Project successfully pushed to https://github.com/nzubechukwudaniel7-cmd/QLOO")
except Exception as e:
    print(f"[-] Push failed: {e}")
    sys.exit(1)
