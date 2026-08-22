"""
EXERCISE - Базовый класс для всех упражнений
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class ExerciseTask:
    """Задание упражнения"""
    
    def __init__(self, data: Dict[str, Any], task_id: str = None):
        self.id = task_id or str(datetime.now().timestamp())
        self.data = data
        self.created_at = datetime.now()
        self.completed = False
        self.result = None
    
    def get(self, key: str, default=None):
        return self.data.get(key, default)


class ExerciseResult:
    """Результат выполнения задания"""
    
    def __init__(self, correct: bool, score: int, message: str = "", details: dict = None):
        self.correct = correct
        self.score = score
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "correct": self.correct,
            "score": self.score,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }


class BaseExercise(ABC):
    """Абстрактный базовый класс упражнения"""
    
    def __init__(self, settings, **kwargs):
        self.settings = settings
        self.score = 0
        self.total_attempts = 0
        self.correct_attempts = 0
        self.tasks_completed = 0
        self.total_tasks = 0
        self.current_task = None
        self.tasks = []
        self.is_active = False
        self.metadata = kwargs
    
    @abstractmethod
    def generate_task(self) -> ExerciseTask:
        """
        Генерация задания
        Returns:
            ExerciseTask: Сгенерированное задание
        """
        pass
    
    @abstractmethod
    def check_answer(self, user_input: Any) -> ExerciseResult:
        """
        Проверка ответа пользователя
        Args:
            user_input: Ввод пользователя
        Returns:
            ExerciseResult: Результат проверки
        """
        pass
    
    @abstractmethod
    def get_hint(self) -> str:
        """
        Получение подсказки
        Returns:
            str: Текст подсказки
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Получение описания упражнения
        Returns:
            str: Описание упражнения
        """
        pass
    
    def start(self):
        """Начало упражнения"""
        self.is_active = True
        self.score = 0
        self.total_attempts = 0
        self.correct_attempts = 0
        self.tasks_completed = 0
        self.tasks = []
        self._generate_all_tasks()
    
    def _generate_all_tasks(self):
        """Генерация всех заданий для сессии"""
        self.total_tasks = self._get_tasks_count()
        self.tasks = []
        for _ in range(self.total_tasks):
            self.tasks.append(self.generate_task())
    
    def _get_tasks_count(self) -> int:
        """Количество заданий в сессии"""
        return self.settings.get("tasks_per_session", 10)
    
    def get_next_task(self) -> Optional[ExerciseTask]:
        """Получение следующего задания"""
        if self.tasks_completed < len(self.tasks):
            self.current_task = self.tasks[self.tasks_completed]
            return self.current_task
        return None
    
    def submit_answer(self, user_input: Any) -> ExerciseResult:
        """Отправка ответа на текущее задание"""
        if not self.current_task:
            return ExerciseResult(False, 0, "Нет активного задания")
        
        self.total_attempts += 1
        result = self.check_answer(user_input)
        
        if result.correct:
            self.correct_attempts += 1
            self.score += result.score
        
        self.tasks_completed += 1
        self.current_task.completed = True
        self.current_task.result = result
        
        return result
    
    def get_progress(self) -> dict:
        """Получение прогресса"""
        return {
            "completed": self.tasks_completed,
            "total": self.total_tasks,
            "progress": (self.tasks_completed / self.total_tasks * 100) if self.total_tasks > 0 else 0,
            "score": self.score,
            "accuracy": (self.correct_attempts / self.total_attempts * 100) if self.total_attempts > 0 else 0,
            "is_active": self.is_active
        }
    
    def get_statistics(self) -> dict:
        """Получение статистики"""
        return {
            "total_attempts": self.total_attempts,
            "correct_attempts": self.correct_attempts,
            "accuracy": (self.correct_attempts / self.total_attempts * 100) if self.total_attempts > 0 else 0,
            "score": self.score,
            "tasks_completed": self.tasks_completed,
            "total_tasks": self.total_tasks
        }
