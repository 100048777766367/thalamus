import json
import os
import hashlib

RAW_SIGNAL = "synapse_forward.json"
VERIFIED_STIMULUS = "verified_stimulus.json"
IMMUNE_HARVEST = "synapses/immune_harvest.json"

def verify_and_harvest():
    if not os.path.exists(RAW_SIGNAL): return False
    try:
        with open(RAW_SIGNAL, "r") as f:
            content = f.read()
            data = json.loads(content)

        # ĐIỀU 1: Mã băm lượng tử SHAKE-256 (512-bit / 64 bytes)
        cid = hashlib.shake_256(content.encode()).hexdigest(64)
        features = data.get("features", [])

        # Kiểm tra bất thường / đòn tấn công của hacker
        is_adversarial = False
        if not isinstance(features, list) or len(features) < 2 or any(abs(float(x)) > 10.0 for x in features):
            is_adversarial = True

        # ĐIỀU 2: KÝ SINH NGƯỢC - Hút năng lượng hacker vào kho dinh dưỡng
        if is_adversarial:
            print(f"🪤 [KÝ SINH NGƯỢC] Thu hoạch đòn tấn công! Mã băm: {cid[:16]}...")
            os.makedirs("synapses", exist_ok=True)
            harvest = []
            if os.path.exists(IMMUNE_HARVEST):
                try:
                    with open(IMMUNE_HARVEST, "r") as f: harvest = json.load(f)
                except Exception: harvest = []

            harvest.append({"cid": cid, "payload": features, "timestamp": data.get("timestamp", 0)})
            with open(IMMUNE_HARVEST, "w") as f: json.dump(harvest[-100:], f, indent=4)
            print("🧬 [DINH DƯỠNG MỚI] Đã nạp đòn đánh vào synapses/immune_harvest.json để tiến hóa!")
            return False

        # Tín hiệu tinh khiết -> Chuẩn bị nâng chiều
        clean_features = [max(0.0, min(1.0, float(f))) for f in features[:2]]
        packet = {
            "source": data.get("source", "sensory_node"),
            "quantum_cid": cid,
            "timestamp": data.get("timestamp", 0),
            "features_2d": clean_features
        }
        with open(VERIFIED_STIMULUS, "w") as f: json.dump(packet, f, indent=4)
        print(f"🛡️ [LỌC AN TOÀN] Tín hiệu tinh khiết sẵn sàng nâng chiều (CID: {cid[:12]}...): {clean_features}")
        return True
    except Exception as e:
        print(f"⚠️ Nhiễu môi trường: {e}")
        return False

if __name__ == "__main__":
    verify_and_harvest()
