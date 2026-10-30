import os
import sys
import dulwich.porcelain as p

def get_github_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    # Read from .env
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GITHUB_TOKEN="):
                    return line.split("=", 1)[1].strip()
    return None

def main():
    token = get_github_token()
    if not token:
        print("[-] GITHUB_TOKEN not found in environment or .env file.")
        sys.exit(1)

    repo_url = f"https://{token}@github.com/nzubechukwudaniel7-cmd/QLOO.git"
    print("[*] Staging project files...")

    files_to_add = [
        "README.md",
        "DEMO_VIDEO_SCRIPT.md",
        "PROMPT_MOTION_SKILLS.md",
        ".gitignore",
        "requirements.txt",
        "run.py",
        "START_NEUROTASTE.bat",
        "PUSH_TO_GITHUB.bat",
        "push_repo.py",
        "test_backend.py",
        "test_qloo.py",
        "app/main.py",
        "app/services/qloo_service.py",
        "app/services/rppg_service.py",
        "app/services/agent_service.py",
        "app/static/console.html",
        "app/static/index.html",
        "app/static/demo.html",
        "generate_voiceovers.py",
        "app/static/audio/scene_1.mp3",
        "app/static/audio/scene_2.mp3",
        "app/static/audio/scene_3.mp3",
        "app/static/audio/scene_4.mp3",
        "app/static/audio/scene_5.mp3",
        "app/static/audio/scene_6.mp3",
        "app/static/audio/neurotaste_full_voiceover.mp3",
        "app/static/js/cortex.js",
        "app/static/js/rppg.js"
    ]

    for f in files_to_add:
        try:
            p.add(".", paths=[f])
        except Exception as e:
            print(f"[-] Could not add {f}: {e}")

    try:
        commit_id = p.commit(".", message="feat: add Prompt-Motion 3D cinematic demo experience and ElevenLabs voiceovers", author=b"nzubechukwudaniel7-cmd <nzube@example.com>")
        print(f"[+] Committed: {commit_id}")
    except Exception as e:
        print(f"[*] Commit note: {e}")

    print("[*] Pushing to GitHub (branch: main)...")
    p.push(".", repo_url, "main")
    print("[+] SUCCESS! All changes pushed to GitHub successfully.")

if __name__ == "__main__":
    main()
