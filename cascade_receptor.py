import os, subprocess

OWNER = os.environ.get("REPO_OWNER", "")
PARENT = os.environ.get("REPO_PARENT", "")
UPSTREAM_SEED = "100048777766367"
TARGET_FILE = "synapse_forward.json"

# Danh sách các giác quan trong hệ sinh thái
SENSORY_ORGANS = ["retina", "cochlea", "tactile", "olfactory"]

def try_fetch(target_owner, organ):
    url = f"https://raw.githubusercontent.com/{target_owner}/{organ}/main/synapse_forward.json"
    res = subprocess.run(["curl", "-s", "-f", url, "-o", TARGET_FILE], capture_output=True)
    return res.returncode == 0 and os.path.exists(TARGET_FILE)

def main():
    # Quét tất cả các giác quan: Local -> Parent -> Seed
    for organ in SENSORY_ORGANS:
        if OWNER and try_fetch(OWNER, organ):
            print(f"📡 [THỤ THỂ ĐỒI THỊ] Đã hút thành công xung từ {OWNER}/{organ}!")
            return
        if PARENT and try_fetch(PARENT, organ):
            print(f"📡 [THỤ THỂ PHẢ HỆ] Bú sữa giác quan từ Parent: {PARENT}/{organ}!")
            return
        if try_fetch(UPSTREAM_SEED, organ):
            print(f"📡 [THỤ THỂ CỘI NGUỒN] Hút xung từ hạt mầm: {UPSTREAM_SEED}/{organ}!")
            return
    print("🍃 [MÔI TRƯỜNG TĨNH] Chưa phát hiện xung giác quan mới.")

if __name__ == "__main__": main()
