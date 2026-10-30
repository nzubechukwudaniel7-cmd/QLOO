import os
import json
import urllib.request
import urllib.error

def load_env():
    """Load simple .env file manually without external dependencies."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

def test_qloo_connection():
    load_env()
    api_key = os.getenv("QLOO_API_KEY", "").strip()
    base_url = os.getenv("QLOO_BASE_URL", "https://hackathon.api.qloo.com").strip()

    if not api_key or api_key == "your_api_key_here":
        print("\n[!] Please set your actual QLOO_API_KEY in the .env file before running.")
        return False

    print(f"\n[*] Connecting to Qloo Developer Cloud at {base_url}...")
    
    # Test query: Search for a cultural entity (e.g. Miles Davis)
    query_url = f"{base_url}/search?query=Miles+Davis"
    headers = {
        "X-Api-Key": api_key,
        "Accept": "application/json",
        "User-Agent": "NeuroTaste/1.0"
    }

    req = urllib.request.Request(query_url, headers=headers, method="GET")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            body = response.read().decode("utf-8")
            data = json.loads(body)
            print(f"[+] SUCCESS! Qloo Developer Cloud returned HTTP {status_code}")
            print(f"[+] Sample Response Summary:")
            if isinstance(data, dict):
                for k in list(data.keys())[:5]:
                    val = str(data[k])
                    print(f"    - {k}: {val[:80]}...")
            elif isinstance(data, list) and len(data) > 0:
                print(f"    - Found {len(data)} entities. First entity: {data[0]}")
            return True
    except urllib.error.HTTPError as e:
        print(f"[-] HTTP Error {e.code}: {e.reason}")
        try:
            error_body = e.read().decode("utf-8")
            print(f"    Details: {error_body}")
        except Exception:
            pass
        return False
    except Exception as e:
        print(f"[-] Connection Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_qloo_connection()
