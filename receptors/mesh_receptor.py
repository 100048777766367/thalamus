import os, json, urllib.request

TARGET_FILE = "synapse_forward.json"
TOPIC_KEYWORD = "bodhi-synapse"

def search_mesh():
    if os.path.exists(TARGET_FILE): return
    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"User-Agent": "Thalamus-Mesh-Node"}
    if token: headers["Authorization"] = f"Bearer {token}"
    api_url = f"https://api.github.com/search/repositories?q=topic:{TOPIC_KEYWORD}&sort=updated&order=desc"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            items = json.loads(resp.read().decode()).get("items", [])
        for repo in items:
            raw_url = f"https://raw.githubusercontent.com/{repo['full_name']}/main/synapse_forward.json"
            try:
                with urllib.request.urlopen(urllib.request.Request(raw_url, headers=headers), timeout=5) as r:
                    with open(TARGET_FILE, "w") as f: f.write(r.read().decode())
                    print(f"🎉 [KẾT NỐI TOÀN CẦU] Đồi thị đã bắt sóng giác quan từ: {repo['full_name']}!")
                    return
            except Exception: continue
    except Exception as e: print(f"🍃 Anten tĩnh: {e}")

if __name__ == "__main__": search_mesh()
