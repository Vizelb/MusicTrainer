"""
JOYSTICK_SCREEN - Экран с джойстиком
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp

from core.engine import SoundEngine
from ui.widgets import OscilloscopeWidget, InfoLayout
from ui.controls import ControlsLayout


# 🏷️ СТАРТ_БЛОКА: JOYSTICKSCREEN
class JoystickScreen(BoxLayout):
    """Экран с джойстиком"""

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(8)
        self.spacing = dp(4)
        
        self.engine = SoundEngine()
        self._build_ui()

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
        
        self.add_widget(Label(
            text="JOYSTICK v5.8",
            font_size=sp(18),
            size_hint=(1, None),
            height=dp(30),
            color=(0.3, 0.9, 0.3, 1)
        ))
        
        self.add_widget(InfoLayout(self.engine, size_hint=(1, None), height=dp(40)))
        
        # Осциллограф (уменьшен для кнопки)
        self.oscilloscope = OscilloscopeWidget(self.engine, size_hint=(1, 0.48))
        self.add_widget(self.oscilloscope)
        
        self.add_widget(ControlsLayout(self.engine, size_hint=(1, None), height=dp(50)))
        
        # ========== КНОПКА СТАРТ/СТОП ==========
        btn_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(45), spacing=dp(10))
        btn_layout.add_widget(Label(text="", size_hint=(0.1, 1)))
        
        self.start_stop_btn = Button(
            text="▶ СТАРТ ЗВУК",
            font_size=sp(16),
            size_hint=(0.8, 1),
            background_color=(0.2, 0.5, 0.2, 1),
            background_normal=""
        )
        self.start_stop_btn.bind(on_press=self.toggle_sound)
        btn_layout.add_widget(self.start_stop_btn)
        
        btn_layout.add_widget(Label(text="", size_hint=(0.1, 1)))
        self.add_widget(btn_layout)
        # =====================================
        
        self.add_widget(Label(
            text="🖐️ Touch oscilloscope | Left/Right = freq | Up/Down = volume",
            font_size=sp(11),
            size_hint=(1, None),
            height=dp(22),
            color=(0.4, 0.4, 0.4, 1),
            halign="center"
        ))

    def toggle_sound(self, instance):
        """Переключение старт/стоп звука"""
        is_playing = self.engine.toggle()
        if is_playing:
            self.start_stop_btn.text = "⏹ СТОП ЗВУК"
            self.start_stop_btn.background_color = (0.5, 0.2, 0.2, 1)
        else:
            self.start_stop_btn.text = "▶ СТАРТ ЗВУК"
            self.start_stop_btn.background_color = (0.2, 0.5, 0.2, 1)

    def go_back(self, instance):
        """Возврат в меню с остановкой звука"""
        if self.engine:
            self.engine.stop()
        self.app.switch_to("menu")

    def on_stop(self):
        """Остановка приложения"""
        if self.engine:
            self.engine.full_stop()
# 🏷️ КОНЕЦ_БЛОКА: JOYSTICKSCREEN