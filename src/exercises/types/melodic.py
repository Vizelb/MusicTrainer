"""
MELODIC - Мелодические упражнения
Работа с последовательностями нот
"""

import random
import numpy as np
from ..base.exercise import BaseExercise, ExerciseTask, ExerciseResult



# 🏷️ СТАРТ_БЛОКА: MELODICEXERCISE
# 🏷️ КОНЕЦ_БЛОКА: MELODICEXERCISE

class MelodicExercise(BaseExercise):
    """Упражнение на мелодические последовательности"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, level: int = 1, **kwargs):
        super().__init__(level, **kwargs)
        self.notes = self._get_notes()
        self.sequence = []
        self.current_note_index = 0
        self.target_sequence = []
    

# 🏷️ СТАРТ_БЛОКА: _GET_NOTES
# 🏷️ КОНЕЦ_БЛОКА: _GET_NOTES

    def _get_notes(self) -> dict:
        """Справочник нот"""
        return {
            "C": 261.63,
            "C#": 277.18,
            "D": 293.66,
            "D#": 311.13,
            "E": 329.63,
            "F": 349.23,
            "F#": 369.99,
            "G": 392.00,
            "G#": 415.30,
            "A": 440.00,
            "A#": 466.16,
            "B": 493.88
        }
    

# 🏷️ СТАРТ_БЛОКА: GENERATE_TASK
# 🏷️ КОНЕЦ_БЛОКА: GENERATE_TASK

    def generate_task(self) -> ExerciseTask:
        """Генерация задания"""
        # Длина последовательности зависит от уровня
        length = min(3 + self.level, 8)
        
        # Генерируем последовательность
        available_notes = list(self.notes.keys())
        self.target_sequence = []
        
        for _ in range(length):
            note_name = random.choice(available_notes)
            self.target_sequence.append({
                "name": note_name,
                "freq": self.notes[note_name]
            })
        
        self.current_note_index = 0
        
        task_data = {
            "type": "melodic_sequence",
            "sequence": self.target_sequence,
            "length": length,
            "current_note": self.target_sequence[0] if self.target_sequence else None,
            "description": f"Воспроизведите последовательность из {length} нот"
        }
        
        return ExerciseTask(task_data)
    

# 🏷️ СТАРТ_БЛОКА: GET_NEXT_NOTE
# 🏷️ КОНЕЦ_БЛОКА: GET_NEXT_NOTE

    def get_next_note(self):
        """Получение следующей ноты последовательности"""
        if self.current_note_index < len(self.target_sequence):
            note = self.target_sequence[self.current_note_index]
            self.current_note_index += 1
            return note
        return None
    

# 🏷️ СТАРТ_БЛОКА: CHECK_ANSWER
# 🏷️ КОНЕЦ_БЛОКА: CHECK_ANSWER

    def check_answer(self, user_input: float) -> ExerciseResult:
        """Проверка текущей ноты"""
        if not self.target_sequence:
            return ExerciseResult(False, 0, "Нет активной последовательности")
        
        if self.current_note_index == 0:
            return ExerciseResult(False, 0, "Сначала получите ноту")
        
        current_note = self.target_sequence[self.current_note_index - 1]
        expected_freq = current_note["freq"]
        
        # Допуск ±10 центов
        diff_cents = 1200 * np.log2(user_input / expected_freq)
        is_correct = abs(diff_cents) <= 10
        
        score = 10 if is_correct else 0
        
        if is_correct:
            message = f"✅ Правильно! Нота {current_note['name']}"
        else:
            message = f"❌ Неправильно. Ожидалась нота {current_note['name']}"
        
        return ExerciseResult(is_correct, score, message)
    

# 🏷️ СТАРТ_БЛОКА: GET_HINT
# 🏷️ КОНЕЦ_БЛОКА: GET_HINT

    def get_hint(self) -> str:
        """Получение подсказки"""
        if self.current_note_index < len(self.target_sequence):
            note = self.target_sequence[self.current_note_index]
            return f"Настройте частоту на ноту {note['name']}"
        return "Последовательность завершена"
    

# 🏷️ СТАРТ_БЛОКА: GET_DESCRIPTION
# 🏷️ КОНЕЦ_БЛОКА: GET_DESCRIPTION

    def get_description(self) -> str:
        """Описание упражнения"""
        return f"Мелодическое упражнение (Уровень {self.level})"