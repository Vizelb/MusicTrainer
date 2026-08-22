# 🏷️ СТАРТ_БЛОКА: ФАЙЛ

"""
SCREENS - Экраны приложения
"""

from .menu_screen import MenuScreen
from .joystick_screen import JoystickScreen
# from .info_screen import InfoScreen (удалён)
from .debug_screen import DebugScreen
from .stats_screen import StatsScreen  # ← ДОБАВЛЯЕМ

__all__ = [
    "MenuScreen", 
    "JoystickScreen", 
    "InfoScreen"  # удалён, 
    "DebugScreen",
    "StatsScreen"  # ← ДОБАВЛЯЕМ
]

# 🏷️ КОНЕЦ_БЛОКА: ФАЙЛ