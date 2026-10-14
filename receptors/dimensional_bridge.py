import math

class DimensionalBridge:
    @staticmethod
    def lift_2d_to_hyper(features_2d):
        """
        NÂNG CHIỀU: Biến [f1, f2] thành Vector 4 chiều siêu hình học
        [f1, f2, sin(pi*f1), cos(pi*f2)]
        """
        f1 = float(features_2d[0])
        f2 = float(features_2d[1])
        h1 = round(math.sin(math.pi * f1) * 0.5 + 0.5, 4)
        h2 = round(math.cos(math.pi * f2) * 0.5 + 0.5, 4)
        return [f1, f2, h1, h2]

    @staticmethod
    def project_hyper_to_2d(hyper_gradients):
        """
        HẠ CHIỀU (PROJECTION): Nén đạo hàm 4 chiều lại thành đúng 2 con số [g1, g2]
        để repo cũ (retina, cochlea) đọc được và tự vặn kính lúp!
        """
        g1 = round(hyper_gradients[0] + 0.5 * hyper_gradients[2], 4)
        g2 = round(hyper_gradients[1] + 0.5 * hyper_gradients[3], 4)
        # Giới hạn an toàn chống nổ gradient
        return [max(-5.0, min(5.0, g1)), max(-5.0, min(5.0, g2))]
