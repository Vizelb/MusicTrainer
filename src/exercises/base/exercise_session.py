"""
EXERCISE SESSION - Сессия упражнения
Управление одной сессией упражнений
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from .exercise import ExerciseResult, BaseExercise



# 🏷️ СТАРТ_БЛОКА: EXERCISESESSION
# 🏷️ КОНЕЦ_БЛОКА: EXERCISESESSION

class ExerciseSession:
    """Сессия выполнения упражнения"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, exercise: BaseExercise):
        self.exercise = exercise
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.results: List[ExerciseResult] = []
        self.completed = False
    

# 🏷️ СТАРТ_БЛОКА: ADD_RESULT
# 🏷️ КОНЕЦ_БЛОКА: ADD_RESULT

    def add_result(self, result: ExerciseResult):
        """Добавление результата"""
        self.results.append(result)
    

# 🏷️ СТАРТ_БЛОКА: COMPLETE
# 🏷️ КОНЕЦ_БЛОКА: COMPLETE

    def complete(self):
        """Завершение сессии"""
        self.completed = True
        self.end_time = datetime.now()
    

# 🏷️ СТАРТ_БЛОКА: GET_SUMMARY
# 🏷️ КОНЕЦ_БЛОКА: GET_SUMMARY

    def get_summary(self) -> dict:
        """Получение итогов сессии"""
        total = len(self.results)
        correct = sum(1 for r in self.results if r.correct)
        
        duration = 0
        if self.end_time and self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            "exercise_type": self.exercise.__class__.__name__,
            "level": self.exercise.level,
            "total_tasks": total,
            "correct": correct,
            "accuracy": (correct / total * 100) if total > 0 else 0,
            "score": self.exercise.score,
            "duration": duration,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "completed": self.completed
        }
    

# 🏷️ СТАРТ_БЛОКА: TO_DICT
# 🏷️ КОНЕЦ_БЛОКА: TO_DICT

    def to_dict(self) -> dict:
        """Сериализация сессии"""
        return {
            "exercise": self.exercise.to_dict(),
            "results": [r.to_dict() for r in self.results],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "completed": self.completed
        }