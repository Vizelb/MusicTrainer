"""
TIMBRE - Управление тембрами (ПОЛНАЯ КОПИЯ v5.0)
Все параметры из эталонной версии
"""

import numpy as np



# 🏷️ СТАРТ_БЛОКА: TIMBRE
# 🏷️ КОНЕЦ_БЛОКА: TIMBRE

class Timbre:
    """Класс управления тембрами - полная копия v5.0"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, name="Синус"):
        self.name = name
        self.harmonics = []
        self._build_timbre()
    

# 🏷️ СТАРТ_БЛОКА: _BUILD_TIMBRE
# 🏷️ КОНЕЦ_БЛОКА: _BUILD_TIMBRE

    def _build_timbre(self):
        if self.name == "Синус":
            self.harmonics = [(1, 1.0, 0.0)]
        elif self.name == "Орган":
            self.harmonics = [
                (1, 1.00, 0.00), (2, 0.60, 0.10), (3, 0.40, 0.20),
                (4, 0.25, 0.30), (5, 0.15, 0.40), (6, 0.10, 0.50),
                (7, 0.06, 0.60), (8, 0.04, 0.70),
            ]
        elif self.name == "Скрипка":
            self.harmonics = [
                (1, 1.00, 0.00), (2, 0.50, 0.50), (3, 0.30, 1.00),
                (4, 0.15, 1.50), (5, 0.08, 2.00), (6, 0.04, 2.50),
                (7, 0.02, 3.00),
            ]
        elif self.name == "Флейта":
            self.harmonics = [
                (1, 1.00, 0.00), (2, 0.30, 0.20), (3, 0.10, 0.40),
                (4, 0.04, 0.60), (5, 0.01, 0.80),
            ]
        elif self.name == "Кларнет":
            self.harmonics = [
                (1, 1.00, 0.00), (3, 0.60, 0.30), (5, 0.35, 0.60),
                (7, 0.20, 0.90), (9, 0.10, 1.20), (11, 0.05, 1.50),
            ]
        else:
            self.harmonics = [(1, 1.0, 0.0)]
    

# 🏷️ СТАРТ_БЛОКА: GENERATE
# 🏷️ КОНЕЦ_БЛОКА: GENERATE

    def generate(self, phase, freq, num_samples, sample_rate, volume=0.5):
        """Генерация звуковой волны"""
        phase_inc = 2 * np.pi * freq / sample_rate
        phase_array = phase + phase_inc * np.arange(num_samples)
        result = np.zeros(num_samples)
        for n, amp, phase_shift in self.harmonics:
            result += amp * np.sin(n * phase_array + phase_shift)
        max_val = np.max(np.abs(result))
        if max_val > 0:
            result = result / max_val * volume
        return result
    
    @staticmethod

# 🏷️ СТАРТ_БЛОКА: GET_TIMBRE_NAMES
# 🏷️ КОНЕЦ_БЛОКА: GET_TIMBRE_NAMES

    def get_timbre_names():
        return ["Синус", "Орган", "Скрипка", "Флейта", "Кларнет"]