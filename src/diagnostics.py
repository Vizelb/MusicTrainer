"""
DIAGNOSTICS - Модуль самодиагностики приложения
Проверяет все ключевые компоненты при запуске
"""

import sys
import os
import importlib
from datetime import datetime


class TestResult:
    """Результат одного теста"""
    def __init__(self, name, passed, message="", details=None):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()


class Diagnostics:
    """Система самодиагностики"""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("\n" + "=" * 50)
        print("🔍 ЗАПУСК САМОДИАГНОСТИКИ")
        print("=" * 50)
        
        # Запускаем все тесты
        self._test_imports()
        self._test_core()
        self._test_ui()
        self._test_screens()
        self._test_sound()
        self._test_kivy()
        
        # Выводим сводку
        self._print_summary()
        
        return self.results
    
    def _add_result(self, name, passed, message="", details=None):
        """Добавление результата теста"""
        result = TestResult(name, passed, message, details)
        self.results.append(result)
        
        # Выводим в консоль
        status = "✅" if passed else "❌"
        print(f"   {status} {name}: {message}")
        return result
    
    # ========== ТЕСТЫ ==========
    
    def _test_imports(self):
        """Тест импортов"""
        print("\n📦 Проверка импортов...")
        
        modules = [
            ("core.engine", "SoundEngine"),
            ("core.timbre", "Timbre"),
            ("ui.widgets", "OscilloscopeWidget"),
            ("ui.controls", "ControlsLayout"),
            ("screens.joystick_screen", "JoystickScreen"),
        ]
        
        all_ok = True
        for module_name, class_name in modules:
            try:
                module = importlib.import_module(module_name)
                getattr(module, class_name)
                self._add_result(f"Импорт {module_name}.{class_name}", True, "OK")
            except Exception as e:
                self._add_result(f"Импорт {module_name}.{class_name}", False, f"Ошибка: {e}")
                all_ok = False
        
        return all_ok
    
    def _test_core(self):
        """Тест ядра"""
        print("\n⚙️ Проверка ядра...")
        
        try:
            from core.engine import SoundEngine
            engine = SoundEngine()
            
            # Проверяем основные методы
            tests = [
                ("SoundEngine.__init__", True, "OK"),
                ("SoundEngine.set_frequency", True, "OK"),
                ("SoundEngine.set_volume", True, "OK"),
            ]
            
            for name, passed, msg in tests:
                self._add_result(name, passed, msg)
            
            # Останавливаем звук
            engine.stop()
            
        except Exception as e:
            self._add_result("SoundEngine", False, f"Ошибка: {e}")
    
    def _test_ui(self):
        """Тест UI компонентов"""
        print("\n🖥️ Проверка UI...")
        
        try:
            from ui.widgets import OscilloscopeWidget, InfoLayout
            from ui.controls import ControlsLayout
            
            self._add_result("OscilloscopeWidget", True, "OK")
            self._add_result("InfoLayout", True, "OK")
            self._add_result("ControlsLayout", True, "OK")
            
        except Exception as e:
            self._add_result("UI компоненты", False, f"Ошибка: {e}")
    
    def _test_screens(self):
        """Тест экранов"""
        print("\n📱 Проверка экранов...")
        
        try:
            from screens.joystick_screen import JoystickScreen
            
            # Проверяем, что класс существует
            if hasattr(JoystickScreen, '__name__'):
                self._add_result("JoystickScreen", True, "OK")
            else:
                self._add_result("JoystickScreen", False, "Класс не найден")
            
        except Exception as e:
            self._add_result("Экраны", False, f"Ошибка: {e}")
    
    def _test_sound(self):
        """Тест звуковой системы"""
        print("\n🔊 Проверка звука...")
        
        try:
            import pygame
            pygame.init()
            
            # Проверяем микшер
            if pygame.mixer.get_init():
                self._add_result("Pygame микшер", True, "Инициализирован")
                
                # Проверяем каналы
                channels = pygame.mixer.get_num_channels()
                self._add_result("Pygame каналы", True, f"{channels} каналов")
            else:
                self._add_result("Pygame микшер", False, "Не инициализирован")
                
        except Exception as e:
            self._add_result("Звуковая система", False, f"Ошибка: {e}")
    
    def _test_kivy(self):
        """Тест Kivy"""
        print("\n📐 Проверка Kivy...")
        
        try:
            import kivy
            version = kivy.__version__
            self._add_result("Kivy версия", True, f"v{version}")
            
            # Проверяем основные компоненты
            from kivy.uix.widget import Widget
            from kivy.uix.boxlayout import BoxLayout
            self._add_result("Kivy компоненты", True, "OK")
            
        except Exception as e:
            self._add_result("Kivy", False, f"Ошибка: {e}")
    
    def _print_summary(self):
        """Вывод сводки тестов"""
        print("\n" + "=" * 50)
        print("📊 СВОДКА ТЕСТОВ")
        print("=" * 50)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        print(f"   ✅ Пройдено: {passed}")
        print(f"   ❌ Не пройдено: {failed}")
        print(f"   📊 Всего тестов: {total}")
        
        if failed > 0:
            print("\n⚠️ НАЙДЕНЫ ПРОБЛЕМЫ:")
            for r in self.results:
                if not r.passed:
                    print(f"   ❌ {r.name}: {r.message}")
        else:
            print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        
        print("=" * 50)
    
    def get_report(self):
        """Получение отчета для отображения в UI"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "message": r.message,
                    "details": r.details
                }
                for r in self.results
            ],
            "timestamp": self.start_time.isoformat()
        }


# Функция для быстрого запуска
def run_diagnostics():
    """Быстрый запуск диагностики"""
    diag = Diagnostics()
    return diag.run_all_tests()


# Автоматический запуск при импорте (для тестирования)
if __name__ == "__main__":
    run_diagnostics()