"""
HARMONIC - Гармонические упражнения
Работа с интервалами
"""

import random
import numpy as np
from ..base.exercise import BaseExercise, ExerciseTask, ExerciseResult



# 🏷️ СТАРТ_БЛОКА: HARMONICEXERCISE
# 🏷️ КОНЕЦ_БЛОКА: HARMONICEXERCISE

class HarmonicExercise(BaseExercise):
    """Упражнение на гармонические интервалы"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, level: int = 1, **kwargs):
        super().__init__(level, **kwargs)
        self.intervals = self._get_intervals_for_level(level)
        self.base_freq = 440.0
        self.current_interval = None
    

# 🏷️ СТАРТ_БЛОКА: _GET_INTERVALS_FOR_LEVEL
# 🏷️ КОНЕЦ_БЛОКА: _GET_INTERVALS_FOR_LEVEL

    def _get_intervals_for_level(self, level: int) -> dict:
        """Получение интервалов для уровня"""
        all_intervals = {
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
            "октава": 1200
        }
        
        level_intervals = {
            1: ["прима", "малая_секунда", "большая_секунда"],
            2: ["малая_терция", "большая_терция", "кварта"],
            3: ["квинта", "малая_секста", "большая_секста"],
            4: ["малая_септима", "большая_септима", "октава"],
            5: ["тритон"] + list(all_intervals.keys())
        }
        
        interval_names = level_intervals.get(level, list(all_intervals.keys()))
        return {name: all_intervals[name] for name in interval_names}
    

# 🏷️ СТАРТ_БЛОКА: GENERATE_TASK
# 🏷️ КОНЕЦ_БЛОКА: GENERATE_TASK

    def generate_task(self) -> ExerciseTask:
        """Генерация задания"""
        interval_name = random.choice(list(self.intervals.keys()))
        cents = self.intervals[interval_name]
        
        self.base_freq = random.uniform(200, 500)
        interval_freq = self.base_freq * (2 ** (cents / 1200))
        
        self.current_interval = {
            "name": interval_name,
            "cents": cents,
            "base_freq": self.base_freq,
            "interval_freq": interval_freq
        }
        
        task_data = {
            "type": "harmonic_interval",
            "base_freq": self.base_freq,
            "interval_name": interval_name,
            "interval_freq": interval_freq,
            "cents": cents,
            "description": f"Настройте частоту на интервал {interval_name}"
        }
        
        return ExerciseTask(task_data)
    

# 🏷️ СТАРТ_БЛОКА: CHECK_ANSWER
# 🏷️ КОНЕЦ_БЛОКА: CHECK_ANSWER

    def check_answer(self, user_input: float) -> ExerciseResult:
        """Проверка ответа"""
        if not self.current_interval:
            return ExerciseResult(False, 0, "Нет активного задания")
        
        expected_freq = self.current_interval["interval_freq"]
        
        if user_input > 0 and expected_freq > 0:
            diff_cents = 1200 * np.log2(user_input / expected_freq)
            tolerance = self.settings.get("tolerance", 10)
            
            is_correct = abs(diff_cents) <= tolerance
            
            if is_correct:
                score = max(10, 100 - int(abs(diff_cents) * 2))
            else:
                score = max(0, 10 - int(abs(diff_cents) / 10))
            
            message = f"Разница: {diff_cents:.1f} центов"
            if is_correct:
                message = f"✅ Правильно! {message}"
            else:
                message = f"❌ Неправильно. {message}"
            
            return ExerciseResult(is_correct, score, message)
        
        return ExerciseResult(False, 0, "Некорректная частота")
    

# 🏷️ СТАРТ_БЛОКА: GET_HINT
# 🏷️ КОНЕЦ_БЛОКА: GET_HINT

    def get_hint(self) -> str:
        """Получение подсказки"""
        if not self.current_interval:
            return "Начните упражнение"
        
        interval_name = self.current_interval["name"]
        base_freq = self.current_interval["base_freq"]
        
        hints = {
            "прима": "Настройте такую же частоту",
            "малая_секунда": "Немного выше базовой ноты",
            "большая_секунда": "Выше на целый тон",
            "малая_терция": "Выше на полтора тона",
            "большая_терция": "Выше на два тона",
            "кварта": "Выше на 2.5 тона",
            "тритон": "Выше на 3 тона",
            "квинта": "Выше на 3.5 тона",
            "малая_секста": "Выше на 4 тона",
            "большая_секста": "Выше на 4.5 тона",
            "малая_септима": "Выше на 5.5 тона",
            "большая_септима": "Выше на 5.5 тона",
            "октава": "Вдвое выше базовой ноты"
        }
        
        hint = hints.get(interval_name, f"Настройте на интервал {interval_name}")
        return f"Подсказка: {hint} (базовая нота: {base_freq:.1f} Гц)"
    

# 🏷️ СТАРТ_БЛОКА: GET_DESCRIPTION
# 🏷️ КОНЕЦ_БЛОКА: GET_DESCRIPTION

    def get_description(self) -> str:
        """Описание упражнения - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        intervals_str = ', '.join(self.intervals.keys())
        tolerance = self.settings.get('tolerance', 10)
        intervals_str = ', '.join(self.intervals.keys())
        tolerance = self.settings.get('tolerance', 10)
        return f"Гармоническое упражнение (Уровень {self.level})\nИнтервалы: {intervals_str}\nДопуск: {tolerance} центов"
    

# 🏷️ СТАРТ_БЛОКА: _GET_TASKS_COUNT
# 🏷️ КОНЕЦ_БЛОКА: _GET_TASKS_COUNT

    def _get_tasks_count(self) -> int:
        """Количество заданий в сессии"""
    

# 🏷️ СТАРТ_БЛОКА: _GET_DEFAULT_SETTINGS
# 🏷️ КОНЕЦ_БЛОКА: _GET_DEFAULT_SETTINGS

    def _get_default_settings(self) -> dict:
        """Настройки по умолчанию"""
        settings = super()._get_default_settings()
        settings.update({
            "tasks_per_session": 10,
            "tolerance": 10,
            "random_base_freq": True,
            "base_freq_range": (200, 500)
        })