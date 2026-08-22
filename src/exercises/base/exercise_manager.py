"""
EXERCISE MANAGER - Управление упражнениями
Координация работы упражнений и сессий
"""

from typing import Optional, List, Dict, Any
from .exercise import BaseExercise, ExerciseState
from .exercise_factory import ExerciseFactory
from .exercise_session import ExerciseSession



# 🏷️ СТАРТ_БЛОКА: EXERCISEMANAGER
# 🏷️ КОНЕЦ_БЛОКА: EXERCISEMANAGER

class ExerciseManager:
    """Менеджер управления упражнениями"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self):
        self.current_exercise: Optional[BaseExercise] = None
        self.current_session: Optional[ExerciseSession] = None
        self.history: List[Dict[str, Any]] = []
    

# 🏷️ СТАРТ_БЛОКА: START_EXERCISE
# 🏷️ КОНЕЦ_БЛОКА: START_EXERCISE

    def start_exercise(self, exercise_type: str, level: int = 1, **kwargs) -> bool:
        """
        Начать упражнение
        Args:
            exercise_type: Тип упражнения
            level: Уровень сложности
            **kwargs: Дополнительные параметры
        Returns:
            bool: Успешность запуска
        """
        # Создаем упражнение
        exercise = ExerciseFactory.create(exercise_type, level=level, **kwargs)
        if not exercise:
            return False
        
        # Начинаем новую сессию
        self.current_session = ExerciseSession(exercise)
        self.current_exercise = exercise
        
        # Стартуем упражнение
        exercise.start()
        
        print(f"🎯 Начато упражнение: {exercise_type} (Уровень {level})")
        return True
    

# 🏷️ СТАРТ_БЛОКА: GET_NEXT_TASK
# 🏷️ КОНЕЦ_БЛОКА: GET_NEXT_TASK

    def get_next_task(self):
        """Получение следующего задания"""
        if not self.current_exercise:
            return None
        return self.current_exercise.get_next_task()
    

# 🏷️ СТАРТ_БЛОКА: SUBMIT_ANSWER
# 🏷️ КОНЕЦ_БЛОКА: SUBMIT_ANSWER

    def submit_answer(self, user_input: Any):
        """Отправка ответа"""
        if not self.current_exercise:
            return None
        
        result = self.current_exercise.submit_answer(user_input)
        
        # Сохраняем в сессию
        if self.current_session:
            self.current_session.add_result(result)
        
        return result
    

# 🏷️ СТАРТ_БЛОКА: GET_HINT
# 🏷️ КОНЕЦ_БЛОКА: GET_HINT

    def get_hint(self) -> str:
        """Получение подсказки"""
        if not self.current_exercise:
            return "Нет активного упражнения"
        return self.current_exercise.get_hint()
    

# 🏷️ СТАРТ_БЛОКА: GET_PROGRESS
# 🏷️ КОНЕЦ_БЛОКА: GET_PROGRESS

    def get_progress(self) -> dict:
        """Получение прогресса"""
        if not self.current_exercise:
            return {"error": "Нет активного упражнения"}
        return self.current_exercise.get_progress()
    

# 🏷️ СТАРТ_БЛОКА: GET_STATISTICS
# 🏷️ КОНЕЦ_БЛОКА: GET_STATISTICS

    def get_statistics(self) -> dict:
        """Получение статистики"""
        if not self.current_exercise:
            return {"error": "Нет активного упражнения"}
        return self.current_exercise.get_statistics()
    

# 🏷️ СТАРТ_БЛОКА: PAUSE
# 🏷️ КОНЕЦ_БЛОКА: PAUSE

    def pause(self):
        """Пауза"""
        if self.current_exercise:
            self.current_exercise.pause()
    

# 🏷️ СТАРТ_БЛОКА: RESUME
# 🏷️ КОНЕЦ_БЛОКА: RESUME

    def resume(self):
        """Возобновление"""
        if self.current_exercise:
            self.current_exercise.resume()
    

# 🏷️ СТАРТ_БЛОКА: COMPLETE
# 🏷️ КОНЕЦ_БЛОКА: COMPLETE

    def complete(self):
        """Завершение"""
        if self.current_exercise:
            self.current_exercise.complete()
            if self.current_session:
                self.current_session.complete()
                self.history.append(self.current_session.to_dict())
    

# 🏷️ СТАРТ_БЛОКА: GET_AVAILABLE_EXERCISES
# 🏷️ КОНЕЦ_БЛОКА: GET_AVAILABLE_EXERCISES

    def get_available_exercises(self) -> list:
        """Получение доступных упражнений"""
        return ExerciseFactory.get_available_types()
    

# 🏷️ СТАРТ_БЛОКА: GET_SESSION_SUMMARY
# 🏷️ КОНЕЦ_БЛОКА: GET_SESSION_SUMMARY

    def get_session_summary(self) -> dict:
        """Получение итогов сессии"""
        if not self.current_session:
            return {"error": "Нет активной сессии"}
        return self.current_session.get_summary()