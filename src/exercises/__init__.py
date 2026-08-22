"""
EXERCISES - Пакет упражнений
"""

from .base.exercise import BaseExercise
from .config.settings import ExerciseSettings
from .ui.settings_screen import SettingsScreen
from .ui.exercise_screen import ExerciseScreen

__all__ = [
    'BaseExercise',
    'ExerciseSettings',
    'SettingsScreen',
    'ExerciseScreen'
]
