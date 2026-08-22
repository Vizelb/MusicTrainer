"""
SIMPLE MENU - Простое меню
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp


# 🏷️ СТАРТ_БЛОКА: SIMPLEMENU
class SimpleMenu(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(20)
        self.spacing = dp(15)
        
        # Заголовок
        self.add_widget(Label(
            text="MUSICTRAINER",
            font_size=sp(32),
            size_hint=(1, None),
            height=dp(60),
            color=(0.3, 0.9, 0.3, 1),
            bold=True
        ))
        
        self.add_widget(Label(
            text="Версия 5.8",
            font_size=sp(16),
            size_hint=(1, None),
            height=dp(30),
            color=(0.6, 0.6, 0.6, 1)
        ))
        
        self.add_widget(Label(size_hint=(1, 0.05)))
        
        # Кнопки
        buttons = [
            ("🎮 JOYSTICK", self.go_to_joystick, (0.2, 0.5, 0.2, 1)),
            ("ℹ️ INFO", self.go_to_info, (0.2, 0.3, 0.5, 1)),
            ("📊 СТАТИСТИКА", self.go_to_stats, (0.2, 0.4, 0.2, 1)),
            ("🎯 УПРАЖНЕНИЯ", self.go_to_exercises, (0.2, 0.4, 0.6, 1)),
            ("🐛 DIAGNOSTICS", self.go_to_debug, (0.5, 0.3, 0.2, 1)),
        ]
        
        for text, callback, color in buttons:
            btn = Button(
                text=text,
                font_size=sp(22),
                size_hint=(0.8, None),
                height=dp(55),
                pos_hint={"center_x": 0.5},
                background_color=color,
                background_normal=""
            )
            btn.bind(on_press=callback)
            self.add_widget(btn)
        
        self.add_widget(Label(size_hint=(1, 0.1)))
        
        self.add_widget(Label(
            text="Развитие музыкального слуха",
            font_size=sp(14),
            size_hint=(1, None),
            height=dp(30),
            color=(0.5, 0.5, 0.5, 1),
            halign="center"
        ))
    
    def go_to_joystick(self, instance):
        self.app.switch_to("joystick")
    
    def go_to_info(self, instance):
        self.app.switch_to("info")
    
    def go_to_debug(self, instance):
        self.app.switch_to("debug")
    
    def go_to_stats(self, instance):
        self.app.switch_to("stats")
# 🏷️ КОНЕЦ_БЛОКА: SIMPLEMENU
    
    def go_to_exercises(self, instance):
        self.app.switch_to("exercise_settings")