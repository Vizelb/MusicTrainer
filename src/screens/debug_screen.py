"""
DEBUG SCREEN - Отладка приложения с самодиагностикой
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.metrics import dp, sp
import sys
import platform

from diagnostics import Diagnostics


# 🏷️ СТАРТ_БЛОКА: DEBUGSCREEN
# 🏷️ КОНЕЦ_БЛОКА: DEBUGSCREEN

class DebugScreen(BoxLayout):

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(5)
        
        self.test_results = None
        self._build_ui()
        
        # Запускаем диагностику при входе
        Clock.schedule_once(self.run_diagnostics, 0.5)
    

# 🏷️ СТАРТ_БЛОКА: _BUILD_UI
# 🏷️ КОНЕЦ_БЛОКА: _BUILD_UI

    def _build_ui(self):
        # Кнопка назад
        back_btn = Button(
            text="◀ BACK TO MENU",
            size_hint=(1, None),
            height=dp(35),
            font_size=sp(14),
            background_color=(0.3, 0.3, 0.5, 1),
            background_normal=""
        )
        back_btn.bind(on_press=self.go_back)
        self.add_widget(back_btn)
        
        # Заголовок
        header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50))
        header.add_widget(Label(
            text="🐛 ДИАГНОСТИКА",
            font_size=sp(24),
            size_hint=(0.8, 1),
            color=(0.9, 0.6, 0.3, 1)
        ))
        
        # Кнопка обновления
        refresh_btn = Button(
            text="🔄",
            font_size=sp(20),
            size_hint=(0.2, 1),
            background_color=(0.3, 0.3, 0.5, 1),
            background_normal=""
        )
        refresh_btn.bind(on_press=self.refresh_diagnostics)
        header.add_widget(refresh_btn)
        
        self.add_widget(header)
        
        # Контейнер для результатов
        scroll = ScrollView(size_hint=(1, 0.8))
        self.content = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=dp(5), padding=dp(10))
        self.content.bind(minimum_height=self.content.setter("height"))
        
        # Статус загрузки
        self.status_label = Label(
            text="⏳ Запуск диагностики...",
            font_size=sp(16),
            size_hint=(1, None),
            color=(0.8, 0.8, 0.8, 1)
        )
        self.content.add_widget(self.status_label)
        
        scroll.add_widget(self.content)
        self.add_widget(scroll)
    

# 🏷️ СТАРТ_БЛОКА: RUN_DIAGNOSTICS
# 🏷️ КОНЕЦ_БЛОКА: RUN_DIAGNOSTICS

    def run_diagnostics(self, dt):
        """Запуск самодиагностики"""
        self.status_label.text = "⏳ Выполнение тестов..."
        
        try:
            diag = Diagnostics()
            results = diag.run_all_tests()
            self.test_results = diag.get_report()
            self._display_results()
        except Exception as e:
            self.status_label.text = f"❌ Ошибка диагностики: {e}"
            print(f"❌ Ошибка диагностики: {e}")
    

# 🏷️ СТАРТ_БЛОКА: _DISPLAY_RESULTS
# 🏷️ КОНЕЦ_БЛОКА: _DISPLAY_RESULTS

    def _display_results(self):
        """Отображение результатов диагностики"""
        if not self.test_results:
            return
        
        # Очищаем контейнер
        self.content.clear_widgets()
        
        # Сводка
        total = self.test_results["total"]
        passed = self.test_results["passed"]
        failed = self.test_results["failed"]
        
        # Статус
        if failed == 0:
            status_text = "✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ"
            status_color = (0.3, 0.9, 0.3, 1)
        else:
            status_text = f"⚠️ НАЙДЕНО {failed} ПРОБЛЕМ"
            status_color = (0.9, 0.6, 0.3, 1)
        
        self.content.add_widget(Label(
            text=f"{status_text} ({passed}/{total})",
            font_size=sp(18),
            size_hint=(1, None),
            height=dp(40),
            color=status_color,
            bold=True
        ))
        
        self.content.add_widget(Label(
            text="",
            size_hint=(1, None),
            height=dp(5)
        ))
        
        # Список результатов
        for result in self.test_results["results"]:
            if result["passed"]:
                icon = "✅"
                color = (0.3, 0.8, 0.3, 1)
            else:
                icon = "❌"
                color = (0.9, 0.3, 0.3, 1)
            
            # Каждый результат в отдельной строке
            row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(30))
            
            row.add_widget(Label(
                text=f"{icon} {result['name']}",
                font_size=sp(14),
                size_hint=(0.7, 1),
                color=color,
                halign="left"
            ))
            
            row.add_widget(Label(
                text=result["message"],
                font_size=sp(12),
                size_hint=(0.3, 1),
                color=(0.7, 0.7, 0.7, 1),
                halign="right"
            ))
            
            self.content.add_widget(row)
        
        # Информация о системе
        self.content.add_widget(Label(
            text="",
            size_hint=(1, None),
            height=dp(10)
        ))
        
        self.content.add_widget(Label(
            text=f"🖥️ {platform.platform()}",
            font_size=sp(12),
            size_hint=(1, None),
            height=dp(25),
            color=(0.5, 0.5, 0.5, 1)
        ))
        
        self.content.add_widget(Label(
            text=f"🐍 Python {sys.version.split()[0]}",
            font_size=sp(12),
            size_hint=(1, None),
            height=dp(25),
            color=(0.5, 0.5, 0.5, 1)
        ))
        
        # Если есть ошибки, показываем их отдельно
        if failed > 0:
            self.content.add_widget(Label(
                text="",
                size_hint=(1, None),
                height=dp(10)
            ))
            
            self.content.add_widget(Label(
                text="⚠️ ПРОБЛЕМЫ ТРЕБУЮЩИЕ ВНИМАНИЯ:",
                font_size=sp(14),
                size_hint=(1, None),
                height=dp(30),
                color=(0.9, 0.6, 0.3, 1),
                bold=True
            ))
            
            for result in self.test_results["results"]:
                if not result["passed"]:
                    self.content.add_widget(Label(
                        text=f"   ❌ {result['name']}: {result['message']}",
                        font_size=sp(13),
                        size_hint=(1, None),
                        height=dp(25),
                        color=(0.9, 0.3, 0.3, 1)
                    ))
    

# 🏷️ СТАРТ_БЛОКА: REFRESH_DIAGNOSTICS
# 🏷️ КОНЕЦ_БЛОКА: REFRESH_DIAGNOSTICS

    def refresh_diagnostics(self, instance):
        """Обновление диагностики"""
        self.content.clear_widgets()
        self.content.add_widget(Label(
            text="⏳ Перезапуск диагностики...",
            font_size=sp(16),
            size_hint=(1, None),
            color=(0.8, 0.8, 0.8, 1)
        ))
        Clock.schedule_once(self.run_diagnostics, 0.5)
    

# 🏷️ СТАРТ_БЛОКА: GO_BACK
# 🏷️ КОНЕЦ_БЛОКА: GO_BACK

    def go_back(self, instance):
        """Возврат в меню"""
        self.app.switch_to("menu")