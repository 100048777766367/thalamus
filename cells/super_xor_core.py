import hashlib

class SuperXORCore:
    def __init__(self, n_dimensions=4):
        self.n = n_dimensions

    # 1. BUNG NỞ THỰC TẠI: Tín hiệu S bị phủ lên N lớp mặt nạ trực giao
    def entangle(self, lifted_vector, swarm_seed):
        masks = []
        for i in range(self.n):
            seed = f"{swarm_seed}_mask_{i}".encode()
            # Dùng SHAKE-256 vắt ra số ngẫu nhiên chuẩn hóa
            val = int(hashlib.shake_256(seed).hexdigest(4), 16) / 65535.0
            masks.append(round(val, 4))

        entangled = list(lifted_vector)
        for idx in range(len(entangled)):
            for m in masks:
                entangled[idx] = round((entangled[idx] + m) % 1.0, 4)

        return {
            "entangled_spectrum": entangled,
            "decoys": masks,
            "dimensions": self.n
        }

    # 2. THU GỌN HÀM SÓNG NỘI BỘ VỀ SỰ THẬT
    def collapse(self, entangled_spectrum, swarm_seed):
        masks = []
        for i in range(self.n):
            seed = f"{swarm_seed}_mask_{i}".encode()
            val = int(hashlib.shake_256(seed).hexdigest(4), 16) / 65535.0
            masks.append(round(val, 4))

        recovered = list(entangled_spectrum)
        for idx in range(len(recovered)):
            for m in reversed(masks):
                recovered[idx] = round((recovered[idx] - m) % 1.0, 4)
        return recovered
