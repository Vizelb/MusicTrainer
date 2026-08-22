"""Проверка импортов приложения. Запуск: python tools/check_imports.py"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

print("=" * 50)
print("🔍 ДИАГНОСТИКА ИМПОРТОВ")
print("=" * 50)

errors = []

try:
    print("1. Проверка pygame...")
    import pygame
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"pygame: {e}")

try:
    print("2. Проверка kivy...")
    from kivy.app import App
    from kivy.core.window import Window
    from kivy.uix.boxlayout import BoxLayout
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"kivy: {e}")

try:
    print("3. Проверка simple_menu...")
    from simple_menu import SimpleMenu
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"simple_menu: {e}")

try:
    print("4. Проверка simple_info...")
    from simple_info import SimpleInfo
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"simple_info: {e}")

try:
    print("5. Проверка joystick_screen...")
    from screens.joystick_screen import JoystickScreen
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"joystick_screen: {e}")

try:
    print("6. Проверка debug_screen...")
    from screens.debug_screen import DebugScreen
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"debug_screen: {e}")

try:
    print("7. Проверка settings_screen...")
    from exercises.ui.settings_screen import SettingsScreen
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"settings_screen: {e}")

try:
    print("8. Проверка exercise_screen...")
    from exercises.ui.exercise_screen import ExerciseScreen
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"exercise_screen: {e}")

try:
    print("9. Проверка settings...")
    from exercises.config.settings import ExerciseSettings
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"settings: {e}")

try:
    print("10. Проверка settings_manager...")
    from exercises.config.settings_manager import SettingsManager
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"settings_manager: {e}")

try:
    print("11. Проверка exercise_engine...")
    from exercises.engine.exercise_engine import ExerciseEngine
    print("   ✅ OK")
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    errors.append(f"exercise_engine: {e}")

print("\n" + "=" * 50)
if errors:
    print("❌ ОБНАРУЖЕНЫ ОШИБКИ:")
    for err in errors:
        print(f"   • {err}")
else:
    print("✅ ВСЕ ИМПОРТЫ УСПЕШНЫ!")
print("=" * 50)