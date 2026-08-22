"""
PROGRESS SCREEN - Экран прогресса
Отображение статистики и достижений
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp



# 🏷️ СТАРТ_БЛОКА: PROGRESSSCREEN
# 🏷️ КОНЕЦ_БЛОКА: PROGRESSSCREEN

class ProgressScreen(Screen):
    """Экран прогресса"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'progress'
        self._build_ui()
    

# 🏷️ СТАРТ_БЛОКА: _BUILD_UI
# 🏷️ КОНЕЦ_БЛОКА: _BUILD_UI

    def _build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        layout.add_widget(Label(
            text="📊 ПРОГРЕСС",
            font_size=sp(28),
            size_hint=(1, None),
            height=dp(60),
            color=(0.3, 0.9, 0.3, 1)
        ))
        
        layout.add_widget(Label(
            text="Статистика пока не доступна",
            font_size=sp(18),
            size_hint=(1, 0.5),
            color=(1, 1, 1, 1),
            halign='center'
        ))
        
        btn = Button(
            text="В меню",
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5},
            background_color=(0.3, 0.3, 0.5, 1)
        )
        btn.bind(on_press=self.go_to_menu)
        layout.add_widget(btn)
        
        self.add_widget(layout)
    

# 🏷️ СТАРТ_БЛОКА: GO_TO_MENU
# 🏷️ КОНЕЦ_БЛОКА: GO_TO_MENU

    def go_to_menu(self, instance):
        if self.parent:
            self.parent.current = 'main'
