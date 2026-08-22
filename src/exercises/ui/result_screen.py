"""
RESULT SCREEN - Экран результатов
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp



# 🏷️ СТАРТ_БЛОКА: RESULTSCREEN
# 🏷️ КОНЕЦ_БЛОКА: RESULTSCREEN

class ResultScreen(Screen):

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "result"
        
        self.results = None
        self.manager = None
        self._build_ui()
    

# 🏷️ СТАРТ_БЛОКА: ON_PARENT
# 🏷️ КОНЕЦ_БЛОКА: ON_PARENT

    def on_parent(self, widget, parent):
        if parent:
            self.manager = parent
            print("✅ ResultScreen привязан к ScreenManager")
    

# 🏷️ СТАРТ_БЛОКА: _BUILD_UI
# 🏷️ КОНЕЦ_БЛОКА: _BUILD_UI

    def _build_ui(self):
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))
        
        self.title_label = Label(
            text="Результаты",
            font_size=sp(28),
            size_hint=(1, None),
            height=dp(60),
            color=(0.3, 0.9, 0.3, 1)
        )
        layout.add_widget(self.title_label)
        
        self.stats_label = Label(
            text="Статистика",
            font_size=sp(18),
            size_hint=(1, 0.5),
            color=(1, 1, 1, 1),
            halign="center"
        )
        layout.add_widget(self.stats_label)
        
        controls = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(60), spacing=dp(10))
        
        self.retry_btn = Button(text="Повторить", size_hint=(0.5, 1), background_color=(0.3, 0.6, 0.3, 1))
        self.retry_btn.bind(on_press=self.retry_exercise)
        controls.add_widget(self.retry_btn)
        
        self.menu_btn = Button(text="В меню", size_hint=(0.5, 1), background_color=(0.3, 0.3, 0.5, 1))
        self.menu_btn.bind(on_press=self.go_to_menu)
        controls.add_widget(self.menu_btn)
        
        layout.add_widget(controls)
        
        self.add_widget(layout)
    

# 🏷️ СТАРТ_БЛОКА: SHOW_RESULTS
# 🏷️ КОНЕЦ_БЛОКА: SHOW_RESULTS

    def show_results(self, results):
        self.results = results
        
        text = f"""
Упражнение: {results.get("exercise_type", "Unknown")}
Уровень: {results.get("level", 1)}
Заданий: {results.get("total_tasks", 0)}
Правильно: {results.get("correct", 0)}
Точность: {results.get("accuracy", 0):.1f}%
Очки: {results.get("score", 0)}
Время: {results.get("duration", 0):.1f} сек
"""
        
        self.stats_label.text = text
        
        accuracy = results.get("accuracy", 0)
        if accuracy >= 90:
            self.title_label.text = "🌟 Отлично!"
            self.title_label.color = (0.3, 0.9, 0.3, 1)
        elif accuracy >= 70:
            self.title_label.text = "👍 Хорошо!"
            self.title_label.color = (0.9, 0.9, 0.3, 1)
        elif accuracy >= 50:
            self.title_label.text = "📖 Учитесь!"
            self.title_label.color = (0.9, 0.6, 0.3, 1)
        else:
            self.title_label.text = "💪 Тренируйтесь!"
            self.title_label.color = (0.9, 0.3, 0.3, 1)
    

# 🏷️ СТАРТ_БЛОКА: RETRY_EXERCISE
# 🏷️ КОНЕЦ_БЛОКА: RETRY_EXERCISE

    def retry_exercise(self, instance):
        if self.manager:
            self.manager.current = "exercise"
            exercise_screen = self.manager.get_screen("exercise")
            if exercise_screen:
                exercise_screen.start_exercise()
    

# 🏷️ СТАРТ_БЛОКА: GO_TO_MENU
# 🏷️ КОНЕЦ_БЛОКА: GO_TO_MENU

    def go_to_menu(self, instance):
        if self.manager:
            self.manager.current = "main"
