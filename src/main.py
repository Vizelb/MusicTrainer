"""
MUSICTRAINER v5.8 - С ПЕРЕКЛЮЧЕНИЕМ ЭКРАНОВ
"""

import sys
import os
import pygame

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from simple_menu import SimpleMenu
from simple_info import SimpleInfo
from screens.joystick_screen import JoystickScreen
from screens.debug_screen import DebugScreen
from screens.stats_screen import StatsScreen
from exercises.ui.settings_screen import SettingsScreen
from exercises.ui.exercise_screen import ExerciseScreen


class MusicApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screens = {}
        self.current_screen = None

    def build(self):
        # Проверяем, что Window существует
        if Window:
            try:
                Window.clearcolor = (0.05, 0.05, 0.08, 1)
            except:
                pass

        print("=" * 50)
        print("MUSICTRAINER v5.8 STARTED")
        print("=" * 50)

        self.root_layout = BoxLayout(orientation="vertical")

        # Создаем экраны
        self.screens["menu"] = SimpleMenu(self)
        self.screens["joystick"] = JoystickScreen(self)
        self.screens["info"] = SimpleInfo(self)
        self.screens["debug"] = DebugScreen(self)
        self.screens["stats"] = StatsScreen(self)
        self.screens["exercise_settings"] = SettingsScreen(self)
        self.screens["exercise"] = ExerciseScreen(self)

        self.switch_to("menu")

        return self.root_layout

    def switch_to(self, screen_name):
        if not hasattr(self, 'root_layout') or self.root_layout is None:
            print(f"⚠️ root_layout не инициализирован")
            return
            
        self.root_layout.clear_widgets()

        if screen_name in self.screens:
            screen = self.screens[screen_name]
            self.root_layout.add_widget(screen)
            self.current_screen = screen_name
            print(f"✅ Переключено на: {screen_name}")
            
            # ===== ВАЖНО: ВЫЗЫВАЕМ on_enter() ДЛЯ ЭКРАНОВ =====
            if hasattr(screen, 'on_enter'):
                print(f"   🔄 Вызов on_enter() для {screen_name}")
                screen.on_enter()
        else:
            print(f"❌ Экран не найден: {screen_name}")

    def on_stop(self):
        print("🛑 Остановка приложения...")
        if "joystick" in self.screens:
            try:
                self.screens["joystick"].on_stop()
            except:
                pass
        try:
            pygame.mixer.quit()
        except:
            pass
        print("✅ Приложение остановлено")


if __name__ == "__main__":
    # В Pydroid 3 используем этот способ запуска
    try:
        app = MusicApp()
        app.run()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()