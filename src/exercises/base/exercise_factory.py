"""
EXERCISE FACTORY - Фабрика создания упражнений
Регистрация и создание экземпляров упражнений
"""

from typing import Dict, Type, Any, Optional
from .exercise import BaseExercise



# 🏷️ СТАРТ_БЛОКА: EXERCISEFACTORY
# 🏷️ КОНЕЦ_БЛОКА: EXERCISEFACTORY

class ExerciseFactory:
    """Фабрика для создания упражнений"""
    
    _registry: Dict[str, Type[BaseExercise]] = {}
    
    @classmethod

# 🏷️ СТАРТ_БЛОКА: REGISTER
# 🏷️ КОНЕЦ_БЛОКА: REGISTER

    def register(cls, name: str, exercise_class: Type[BaseExercise]):
        """
        Регистрация типа упражнения
        Args:
            name: Имя типа упражнения
            exercise_class: Класс упражнения
        """
        cls._registry[name] = exercise_class
        print(f"✅ Зарегистрирован тип упражнения: {name}")
    
    @classmethod

# 🏷️ СТАРТ_БЛОКА: CREATE
# 🏷️ КОНЕЦ_БЛОКА: CREATE

    def create(cls, name: str, **kwargs) -> Optional[BaseExercise]:
        """
        Создание экземпляра упражнения
        Args:
            name: Имя типа упражнения
            **kwargs: Параметры для конструктора
        Returns:
            BaseExercise: Экземпляр упражнения
        """
        exercise_class = cls._registry.get(name)
        if not exercise_class:
            print(f"❌ Неизвестный тип упражнения: {name}")
            return None
        
        return exercise_class(**kwargs)
    
    @classmethod

# 🏷️ СТАРТ_БЛОКА: GET_AVAILABLE_TYPES
# 🏷️ КОНЕЦ_БЛОКА: GET_AVAILABLE_TYPES

    def get_available_types(cls) -> list:
        """Получение списка доступных типов"""
        return list(cls._registry.keys())
    
    @classmethod

# 🏷️ СТАРТ_БЛОКА: CLEAR
# 🏷️ КОНЕЦ_БЛОКА: CLEAR

    def clear(cls):
        """Очистка реестра"""
        cls._registry.clear()
    
    @classmethod

# 🏷️ СТАРТ_БЛОКА: CREATE_DEFAULT
# 🏷️ КОНЕЦ_БЛОКА: CREATE_DEFAULT

    def create_default(cls, exercise_type: str = None) -> Optional[BaseExercise]:
        """
        Создание упражнения с настройками по умолчанию
        Args:
            exercise_type: Тип упражнения (если None - первый доступный)
        Returns:
            BaseExercise: Экземпляр упражнения
        """
        if not cls._registry:
            print("❌ Нет зарегистрированных упражнений")
            return None
        
        if exercise_type and exercise_type in cls._registry:
            return cls.create(exercise_type)
        
        # Берем первый доступный тип
        first_type = list(cls._registry.keys())[0]
        return cls.create(first_type)