"""
SETTINGS - Настройки упражнения
"""

from typing import List, Dict, Any


class ExerciseSettings:
    """Настройки упражнения"""
    
    # Интервалы в центах (в пределах двух октав)
    ALL_INTERVALS = {
        "прима": 0,
        "малая_секунда": 100,
        "большая_секунда": 200,
        "малая_терция": 300,
        "большая_терция": 400,
        "кварта": 500,
        "тритон": 600,
        "квинта": 700,
        "малая_секста": 800,
        "большая_секста": 900,
        "малая_септима": 1000,
        "большая_септима": 1100,
        "октава": 1200,
        "малая_нона": 1300,
        "большая_нона": 1400,
        "малая_децима": 1500,
        "большая_децима": 1600,
        "ундецима": 1700,
        "дуодецима": 1900,
        "терцдецима": 2100,
        "квартдецима": 2200,
        "квинтдецима": 2400,
    }
    
    # Названия интервалов для отображения
    INTERVAL_NAMES = {
        "прима": "Прима",
        "малая_секунда": "Малая секунда",
        "большая_секунда": "Большая секунда",
        "малая_терция": "Малая терция",
        "большая_терция": "Большая терция",
        "кварта": "Кварта",
        "тритон": "Тритон",
        "квинта": "Квинта",
        "малая_секста": "Малая секста",
        "большая_секста": "Большая секста",
        "малая_септима": "Малая септима",
        "большая_септима": "Большая септима",
        "октава": "Октава",
        "малая_нона": "Малая нона",
        "большая_нона": "Большая нона",
        "малая_децима": "Малая децима",
        "большая_децима": "Большая децима",
        "ундецима": "Ундецима",
        "дуодецима": "Дуодецима",
        "терцдецима": "Терцдецима",
        "квартдецима": "Квартдецима",
        "квинтдецима": "Квинтдецима",
    }
    
    # Частоты нот (равномерно-темперированный строй, A4 = 440 Гц)
    NOTE_FREQUENCIES = {
        "C3": 130.81,
        "C#3": 138.59,
        "D3": 146.83,
        "D#3": 155.56,
        "E3": 164.81,
        "F3": 174.61,
        "F#3": 185.00,
        "G3": 196.00,
        "G#3": 207.65,
        "A3": 220.00,
        "A#3": 233.08,
        "B3": 246.94,
        "C4": 261.63,
        "C#4": 277.18,
        "D4": 293.66,
        "D#4": 311.13,
        "E4": 329.63,
        "F4": 349.23,
        "F#4": 369.99,
        "G4": 392.00,
        "G#4": 415.30,
        "A4": 440.00,
        "A#4": 466.16,
        "B4": 493.88,
        "C5": 523.25,
        "C#5": 554.37,
        "D5": 587.33,
        "D#5": 622.25,
        "E5": 659.25,
        "F5": 698.46,
        "F#5": 739.99,
        "G5": 783.99,
        "G#5": 830.61,
        "A5": 880.00,
        "A#5": 932.33,
        "B5": 987.77,
    }
    
    def __init__(self):
        # ===== НАСТРОЙКИ ПО УМОЛЧАНИЮ =====
        # 1. Музыкальный строй
        self.tuning = "natural"  # "natural" или "equal"
        
        # 2. Диапазон тоники (от C3 до C5)
        self.tonic_range = ("C4", "C4")  # (мин, макс)
        
        # 3. Частота Ля
        self.a4_frequency = 440.0
        
        # 4. Выбранные интервалы (по умолчанию только "прима")
        self.selected_intervals = ["прима"]
        
        # 5. Тип движения
        self.direction = "up"  # "up" или "down"
        
        # 6. Скорость воспроизведения (0-100%)
        self.speed = 30
        
        # 7. Тембр
        self.timbre = "Орган"
        
        # 8. Количество заданий в сессии
        
        # 10. Показывать название интервала
        self.show_interval_name = True
        
        # 11. Громкость тоники и эталонного интервала (1-100%)
        self.tonic_volume = 75

        # 12. Начальная громкость подбираемого интервала (1-100%)
        self.interval_start_volume = 25
        
        # 12. Режим проведения
        self.mode = "melodic"  # "melodic", "harmonic", "both"
        
        # 13. Диапазон настройки в центах
        self.tuning_range = 400
        
        # 14. Диапазон старта (случайная начальная частота) в центах
        self.start_range = 400
        
        # 15. Показывать отклонение
        self.show_deviation = True
        
        # 16. Показывать текущую частоту
        self.show_frequency = True
    
    def get_selected_intervals(self) -> List[str]:
        """Получение списка выбранных интервалов"""
        return self.selected_intervals
    
    def get_interval_cents(self, interval_name: str) -> int:
        """Получение значения интервала в центах"""
        return self.ALL_INTERVALS.get(interval_name, 0)
    
    def get_interval_display_name(self, interval_name: str) -> str:
        """Получение отображаемого имени интервала"""
        return self.INTERVAL_NAMES.get(interval_name, interval_name)
    
    def get_all_interval_names(self) -> List[str]:
        """Получение всех имен интервалов"""
        return list(self.ALL_INTERVALS.keys())
    
    def get_tonic_frequencies(self) -> List[float]:
        """Получение списка частот для диапазона тоники"""
        min_note, max_note = self.tonic_range
        all_notes = list(self.NOTE_FREQUENCIES.keys())
        
        if min_note not in self.NOTE_FREQUENCIES:
            min_note = "C4"
        if max_note not in self.NOTE_FREQUENCIES:
            max_note = "C4"
        
        # Находим индексы
        try:
            min_idx = all_notes.index(min_note)
            max_idx = all_notes.index(max_note)
        except ValueError:
            return [self.NOTE_FREQUENCIES["C4"]]
        
        # Собираем частоты
        frequencies = []
        for i in range(min_idx, max_idx + 1):
            frequencies.append(self.NOTE_FREQUENCIES[all_notes[i]])
        
        return frequencies
    
    def get_tonic_notes(self) -> List[str]:
        """Получение списка нот для диапазона тоники"""
        min_note, max_note = self.tonic_range
        all_notes = list(self.NOTE_FREQUENCIES.keys())
        
        if min_note not in self.NOTE_FREQUENCIES:
            min_note = "C4"
        if max_note not in self.NOTE_FREQUENCIES:
            max_note = "C4"
        
        try:
            min_idx = all_notes.index(min_note)
            max_idx = all_notes.index(max_note)
        except ValueError:
            return ["C4"]
        
        return all_notes[min_idx:max_idx + 1]
    
    def to_dict(self) -> dict:
        """Сериализация настроек"""
        return {
            "tuning": self.tuning,
            "tonic_range": self.tonic_range,
            "a4_frequency": self.a4_frequency,
            "selected_intervals": self.selected_intervals,
            "direction": self.direction,
            "speed": self.speed,
            "timbre": self.timbre,
            "mode": self.mode,
            "tuning_range": self.tuning_range,
            "start_range": self.start_range,
            "tonic_volume": self.tonic_volume,
            "interval_start_volume": self.interval_start_volume,
            "show_deviation": self.show_deviation,
            "show_frequency": self.show_frequency
        }
    
    def from_dict(self, data: dict):
        """Загрузка настроек из словаря"""
        if "tuning" in data:
            self.tuning = data["tuning"]
        if "tonic_range" in data:
            self.tonic_range = data["tonic_range"]
        if "a4_frequency" in data:
            self.a4_frequency = data["a4_frequency"]
        if "selected_intervals" in data:
            self.selected_intervals = data["selected_intervals"]
        if "direction" in data:
            self.direction = data["direction"]
        if "speed" in data:
            self.speed = data["speed"]
        if "timbre" in data:
            self.timbre = data["timbre"]
        if "mode" in data:
            self.mode = data["mode"]
        if "tuning_range" in data:
            self.tuning_range = data["tuning_range"]
        if "start_range" in data:
            self.start_range = data["start_range"]
            # Гарантируем корректность после загрузки
            if self.tuning_range < self.start_range:
                self.tuning_range = self.start_range
        if "tonic_volume" in data:
            self.tonic_volume = data["tonic_volume"]
        if "interval_start_volume" in data:
            self.interval_start_volume = data["interval_start_volume"]
        if "show_deviation" in data:
            self.show_deviation = data["show_deviation"]
        if "show_frequency" in data:
            self.show_frequency = data["show_frequency"]

    # ===== УПРАВЛЕНИЕ РЕЖИМОМ =====
    
    def get_mode(self) -> str:
        """
        Получение режима упражнения.
        
        Returns:
            str: 'melodic', 'harmonic' или 'both'
        """
        return self.mode
    
    def set_mode(self, mode: str):
        """
        Установка режима упражнения.
        
        Args:
            mode: 'melodic', 'harmonic' или 'both'
        """
        valid_modes = ['melodic', 'harmonic', 'both']
        if mode in valid_modes:
            self.mode = mode
            print(f"   Режим установлен: {mode}")
        else:
            print(f"   ⚠️ Неизвестный режим: {mode}. Доступны: {valid_modes}")
    
    def get_mode_display(self) -> str:
        """Получение отображаемого имени режима"""
        modes = {
            "melodic": "Мелодический",
            "harmonic": "Гармонический",
            "both": "Оба"
        }
        return modes.get(self.mode, "Мелодический")
    
    def get_direction_display(self) -> str:
        """Получение отображаемого имени направления"""
        directions = {
            "up": "Вверх",
            "down": "Вниз",
            "both": "Оба"
        }
        return directions.get(self.direction, "Вверх")
    
    # ===== УПРАВЛЕНИЕ ДИАПАЗОНАМИ =====
    
    def set_tuning_range(self, value: int):
        """
        Установка диапазона настройки.
        Автоматически корректируется, если меньше start_range.
        """
        self.tuning_range = max(50, min(1200, value))
        # Гарантируем, что tuning_range >= start_range
        if self.tuning_range < self.start_range:
            self.tuning_range = self.start_range
        print(f"   Диапазон настройки: {self.tuning_range} центов")
    
    def set_start_range(self, value: int):
        """
        Установка диапазона старта.
        Автоматически корректирует tuning_range, если нужно.
        """
        self.start_range = max(50, min(1200, value))
        # Гарантируем, что tuning_range >= start_range
        if self.tuning_range < self.start_range:
            self.tuning_range = self.start_range
            print(f"   ⚠️ Диапазон настройки автоматически расширен до {self.tuning_range} центов")
        print(f"   Диапазон старта: {self.start_range} центов")
    
    def get_tuning_range(self) -> int:
        """Получение диапазона настройки"""
        return self.tuning_range
    
    def get_start_range(self) -> int:
        """Получение диапазона старта"""
        return self.start_range