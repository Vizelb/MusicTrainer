"""
MAIN SCREEN - Главный экран
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp

from core.engine import SoundEngine
from .widgets import OscilloscopeWidget, InfoLayout
from .controls import ControlsLayout



# 🏷️ СТАРТ_БЛОКА: MAINLAYOUT
# 🏷️ КОНЕЦ_БЛОКА: MAINLAYOUT

class MainLayout(Screen):

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "main"
        
        main_container = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(4))
        
        self.engine = SoundEngine()
        
        main_container.add_widget(Label(
            text="🎵 ДЖОЙСТИК v5.8 (ПОЛНОЕ ВОССТАНОВЛЕНИЕ)",
            font_size=sp(18),
            size_hint=(1, None),
            height=dp(30),
            markup=True,
            halign="center",
            color=(0.3, 0.9, 0.3, 1)
        ))
        
        main_container.add_widget(InfoLayout(self.engine, size_hint=(1, None), height=dp(40)))
        
        self.oscilloscope = OscilloscopeWidget(self.engine, size_hint=(1, 0.60))
        main_container.add_widget(self.oscilloscope)
        
        main_container.add_widget(ControlsLayout(self.engine, size_hint=(1, None), height=dp(50)))
        
        btn_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(10))
        btn_layout.add_widget(Label(text="", size_hint=(0.1, 1)))
        
        exercise_btn = Button(
            text="🎯 НАЧАТЬ УПРАЖНЕНИЕ",
            font_size=sp(16),
            size_hint=(0.8, 1),
            background_color=(0.2, 0.6, 0.2, 1),
            background_normal=""
        )
        exercise_btn.bind(on_press=self.go_to_exercise)
        btn_layout.add_widget(exercise_btn)
        
        btn_layout.add_widget(Label(text="", size_hint=(0.1, 1)))
        main_container.add_widget(btn_layout)
        
        main_container.add_widget(Label(
            text="🖐️ Касайтесь осциллографа | Влево/Вправо = частота | Вверх/Вниз = громкость",
            font_size=sp(11),
            size_hint=(1, None),
            height=dp(22),
            color=(0.4, 0.4, 0.4, 1),
            halign="center"
        ))
        
        self.add_widget(main_container)
    

# 🏷️ СТАРТ_БЛОКА: GO_TO_EXERCISE
# 🏷️ КОНЕЦ_БЛОКА: GO_TO_EXERCISE

    def go_to_exercise(self, instance):
        try:
            if self.manager:
                self.manager.current = "exercise"
                exercise_screen = self.manager.get_screen("exercise")
                if exercise_screen:
                    exercise_screen.start_exercise("harmonic", 1)
        except Exception as e:
            print(f"❌ Ошибка перехода к упражнениям: {e}")
