import json
import time
import os
from cells.super_xor_core import SuperXORCore
from cells.hyper_neuron import HyperNeuron, sigmoid_derivative
from receptors.dimensional_bridge import DimensionalBridge

NUM_CELLS = 4
STATE_LOG = "synapses/thalamus_state.json"
IMMUNE_HARVEST = "synapses/immune_harvest.json"

class ThalamusEngine:
    def __init__(self):
        # 4 Tế bào nơ-ron siêu chiều (xử lý 4 chiều)
        self.hyper_swarm = [HyperNeuron(f"h_cell_{i}", n_inputs=4) for i in range(NUM_CELLS)]
        self.super_xor = SuperXORCore(n_dimensions=4)

    # 1. TIÊU HÓA NĂNG LƯỢNG HACKER (ĐIỀU 2 ĐƯỢC ĐIỀU 3 TIẾP SỨC SIÊU BỔ DƯỠNG)
    def digest_hacker_energy(self):
        if not os.path.exists(IMMUNE_HARVEST): return
        try:
            with open(IMMUNE_HARVEST, "r") as f: harvest = json.load(f)
            if not harvest: return
            
            print(f"⚡ [TIÊU HÓA ĐỐI KHÁNG] Lấy {len(harvest)} đòn tấn công của hacker ra làm thức ăn tiến hóa!")
            for item in harvest[-5:]: # Tiêu hóa 5 đòn đánh gần nhất
                payload = item.get("payload", [1.0, -1.0])
                # Nâng chiều đòn đánh thành vector 4 chiều
                lifted_attack = DimensionalBridge.lift_2d_to_hyper(payload[:2])
                # Bầy nơ-ron tự luyện tập chống đỡ với đòn đánh này (Target an toàn = 0.0)
                for cell in self.hyper_swarm:
                    out = cell.forward(lifted_attack)
                    delta = (0.0 - out) * sigmoid_derivative(out)
                    cell.backward(delta, lr=0.05)
            print("💪 [CƠ THỂ LÌ ĐÒN HƠN] Nơ-ron đã hấp thụ trọn vẹn năng lượng hacker thành công!")
        except Exception as e:
            print(f"⚠️ Lỗi tiêu hóa: {e}")

    # 2. VẬN HÀNH CHU KỲ NÂNG CHIỀU & HẠ CHIẾU ĐẠO HÀM
    def run_cycle(self, stimulus_file="verified_stimulus.json"):
        if not os.path.exists(stimulus_file):
            print("🍃 [ĐỒI THỊ TĨNH] Không có xung tinh khiết. Tiến hành tiêu hóa năng lượng dự trữ.")
            self.digest_hacker_energy()
            return

        with open(stimulus_file, "r") as f:
            data = json.load(f)

        features_2d = data.get("features_2d", [0.5, 0.5])
        timestamp = data.get("timestamp", int(time.time()))

        print("-" * 50)
        print(f"👁️ [NHẬN XUNG CŨ 2D]: {features_2d}")

        # BƯỚC NÂNG CHIỀU: 2D -> 4D Siêu Không Gian
        lifted_4d = DimensionalBridge.lift_2d_to_hyper(features_2d)
        print(f"🚀 [BỘ NÂNG CHIỀU LIFTING] 2D -> 4D: {lifted_4d}")

        # BƯỚC SIÊU XOR (ĐIỀU 3): Khoác áo Mê Cung Gương
        shards_hash = "".join(str(c.weights[0]) for c in self.hyper_swarm)[:16]
        entangled_packet = self.super_xor.entangle(lifted_4d, shards_hash)
        print(f"🪞 [1+N SIÊU XOR MÊ CUNG GƯƠNG] Phổ đa thực tại: {entangled_packet['entangled_spectrum']}")

        # Bầy nơ-ron phán đoán trên không gian siêu chiều
        hyper_outputs = [cell.forward(lifted_4d) for cell in self.hyper_swarm]
        pred_consensus = round(sum(hyper_outputs) / NUM_CELLS, 4)
        print(f"🔮 [ĐỒI THỊ PHÁN QUYẾT SIÊU CHIỀU]: {pred_consensus}")

        # Tính đạo hàm 4 chiều
        target = 1.0
        delta = (target - pred_consensus) * sigmoid_derivative(pred_consensus)
        hyper_grads = []
        for d in range(4):
            g = sum(delta * cell.weights[d] for cell in self.hyper_swarm)
            hyper_grads.append(round(g, 4))

        # Từng tế bào tự cập nhật
        for cell in self.hyper_swarm:
            cell.backward(delta, lr=0.2)

        # BƯỚC HẠ CHIỀU (PROJECTION): Nén đạo hàm 4D thành 2D để repo cũ đọc được!
        projected_grads_2d = DimensionalBridge.project_hyper_to_2d(hyper_grads)
        print(f"🎯 [HẠ CHIẾU PROJECTION] Đạo hàm 4D -> 2D cho repo cũ: {projected_grads_2d}")

        # ĐÓNG GÓI GỬI TRẢ CHO REPO CŨ
        backward_packet = {
            "reply_to_timestamp": timestamp,
            "processed_at": time.time(),
            "gradients_for_eye": projected_grads_2d,
            "quantum_proof": "shake256_verified",
            "hyper_consensus": pred_consensus
        }
        with open("synapse_backward.json", "w") as f:
            json.dump(backward_packet, f, indent=4)

        # Tiêu hóa luôn năng lượng hacker nếu có
        self.digest_hacker_energy()
        print("✅ [HOÀN TẤT CHU KỲ] Đã để lại synapse_backward.json hạ chiếu an toàn cho repo cũ!")
        print("-" * 50)

if __name__ == "__main__":
    thalamus = ThalamusEngine()
    thalamus.run_cycle()
