"""
ПРОСТЕЙШИЙ ЗАПУСК ДЛЯ PYDROID 3
"""

import os
import sys

# Добавляем путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импорты Kivy ДО импорта pygame
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp, sp

# Теперь импортируем pygame
import pygame

# Импорты проекта
from core.engine import SoundEngine
from ui.widgets import OscilloscopeWidget, InfoLayout
from ui.controls import ControlsLayout



# 🏷️ СТАРТ_БЛОКА: SIMPLEMAINLAYOUT
# 🏷️ КОНЕЦ_БЛОКА: SIMPLEMAINLAYOUT

class SimpleMainLayout(BoxLayout):

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(8)
        self.spacing = dp(4)
        
        self.engine = SoundEngine()
        
        self.add_widget(Label(
            text="🎵 MUSICTRAINER v5.8",
            font_size=sp(18),
            size_hint=(1, None),
            height=dp(30),
            color=(0.3, 0.9, 0.3, 1)
        ))
        
        self.add_widget(InfoLayout(self.engine, size_hint=(1, None), height=dp(40)))
        self.oscilloscope = OscilloscopeWidget(self.engine, size_hint=(1, 0.70))
        self.add_widget(self.oscilloscope)
        self.add_widget(ControlsLayout(self.engine, size_hint=(1, None), height=dp(50)))
        self.add_widget(Label(
            text="🖐️ Касайтесь осциллографа | Влево/Вправо = частота | Вверх/Вниз = громкость",
            font_size=sp(11),
            size_hint=(1, None),
            height=dp(22),
            color=(0.4, 0.4, 0.4, 1),
            halign='center'
        ))



# 🏷️ СТАРТ_БЛОКА: SIMPLEAPP
# 🏷️ КОНЕЦ_БЛОКА: SIMPLEAPP

class SimpleApp(App):

# 🏷️ СТАРТ_БЛОКА: BUILD
# 🏷️ КОНЕЦ_БЛОКА: BUILD

    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.08, 1)
        return SimpleMainLayout()
    

# 🏷️ СТАРТ_БЛОКА: ON_STOP
# 🏷️ КОНЕЦ_БЛОКА: ON_STOP

    def on_stop(self):
        if hasattr(self.root, 'engine'):
            self.root.engine.stop()
        pygame.mixer.quit()


if __name__ == '__main__':
    SimpleApp().run()