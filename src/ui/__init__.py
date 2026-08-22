# 🏷️ СТАРТ_БЛОКА: ФАЙЛ

"""
UI - Пользовательский интерфейс
Содержит все виджеты для отображения и управления
"""

from .main_screen import MainLayout
from .widgets import OscilloscopeWidget, InfoLayout
from .controls import ControlsLayout

__all__ = ['MainLayout', 'OscilloscopeWidget', 'InfoLayout', 'ControlsLayout']

# 🏷️ КОНЕЦ_БЛОКА: ФАЙЛ