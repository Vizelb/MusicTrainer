"""
MENU SCREEN - Главное меню
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp



# 🏷️ СТАРТ_БЛОКА: MENUSCREEN
# 🏷️ КОНЕЦ_БЛОКА: MENUSCREEN

class MenuScreen(BoxLayout):

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(20)
        self.spacing = dp(15)
        self._build_ui()
    

# 🏷️ СТАРТ_БЛОКА: _BUILD_UI
# 🏷️ КОНЕЦ_БЛОКА: _BUILD_UI

    def _build_ui(self):
        self.add_widget(Label(
            text="MUSICTRAINER",
            font_size=sp(32),
            size_hint=(1, None),
            height=dp(60),
            color=(0.3, 0.9, 0.3, 1),
            bold=True
        ))
        
        self.add_widget(Label(
            text="Version 5.8",
            font_size=sp(16),
            size_hint=(1, None),
            height=dp(30),
            color=(0.6, 0.6, 0.6, 1)
        ))
        
        self.add_widget(Label(size_hint=(1, 0.05)))
        
        # Кнопка "Джойстик"
        btn1 = Button(
            text="🎮 JOYSTICK",
            font_size=sp(24),
            size_hint=(0.8, None),
            height=dp(55),
            pos_hint={"center_x": 0.5},
            background_color=(0.2, 0.5, 0.2, 1),
            background_normal=""
        )
        btn1.bind(on_press=self.go_to_joystick)
        self.add_widget(btn1)
        
        # Кнопка "Информация"
        btn2 = Button(
            text="ℹ️ INFO",
            font_size=sp(24),
            size_hint=(0.8, None),
            height=dp(55),
            pos_hint={"center_x": 0.5},
            background_color=(0.2, 0.3, 0.5, 1),
            background_normal=""
        )
        btn2.bind(on_press=self.go_to_info)
        self.add_widget(btn2)
        
        # Кнопка "Отладка"
        btn3 = Button(
            text="🐛 DEBUG",
            font_size=sp(24),
            size_hint=(0.8, None),
            height=dp(55),
            pos_hint={"center_x": 0.5},
            background_color=(0.5, 0.3, 0.2, 1),
            background_normal=""
        )
        btn3.bind(on_press=self.go_to_debug)
        self.add_widget(btn3)
        
        # Кнопка "Статистика"
        btn_stats = Button(
            text="📊 СТАТИСТИКА",
            font_size=sp(24),
            size_hint=(0.8, None),
            height=dp(55),
            pos_hint={"center_x": 0.5},
            background_color=(0.2, 0.4, 0.2, 1),
            background_normal=""
        )
        btn_stats.bind(on_press=self.go_to_stats)
        self.add_widget(btn_stats)
        
        self.add_widget(Label(size_hint=(1, 0.1)))
        
        self.add_widget(Label(
            text="Development of musical ear",
            font_size=sp(14),
            size_hint=(1, None),
            height=dp(30),
            color=(0.5, 0.5, 0.5, 1),
            halign="center"
        ))
    

# 🏷️ СТАРТ_БЛОКА: GO_TO_JOYSTICK
# 🏷️ КОНЕЦ_БЛОКА: GO_TO_JOYSTICK

    def go_to_joystick(self, instance):
        self.app.switch_to("joystick")
    

# 🏷️ СТАРТ_БЛОКА: GO_TO_INFO
# 🏷️ КОНЕЦ_БЛОКА: GO_TO_INFO

    def go_to_info(self, instance):
        self.app.switch_to("info")
    

# 🏷️ СТАРТ_БЛОКА: GO_TO_DEBUG
# 🏷️ КОНЕЦ_БЛОКА: GO_TO_DEBUG

    def go_to_debug(self, instance):
        self.app.switch_to("debug")
    
    def go_to_stats(self, instance):
        self.app.switch_to("stats")
