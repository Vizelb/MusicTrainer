"""
SIMPLE INFO - Простая информация
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp, sp


class SimpleInfo(BoxLayout):
    """Экран информации"""

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(20)
        self.spacing = dp(10)
        
        # Заголовок
        self.add_widget(Label(
            text="🎵 MusicTrainer",
            font_size=sp(32),
            size_hint=(1, None),
            height=dp(60),
            color=(0.3, 0.9, 0.3, 1),
            bold=True
        ))
        
        # Версия
        self.add_widget(Label(
            text="Версия 17.5",
            font_size=sp(16),
            size_hint=(1, None),
            height=dp(30),
            color=(0.6, 0.8, 0.6, 1)
        ))
        
        # Информация
        info_text = (
            "🎯 О ПРИЛОЖЕНИИ\n\n"
            "MusicTrainer — интерактивный тренажёр для развития\n"
            "музыкального слуха.\n\n"
            "В основе приложения лежат исследования:\n"
            "• Германа Гельмгольца (1821-1894)\n"
            "• Александра Майкопа (1867-1938)\n\n"
            "📚 Принцип работы:\n"
            "• Генерация звука\n"
            "• Визуализация на осциллографе\n"
            "• Тренировка интервального слуха\n"
            "• Статистика прогресса"
        )
        
        self.add_widget(Label(
            text=info_text,
            font_size=sp(14),
            size_hint=(1, 0.6),
            color=(0.9, 0.9, 0.9, 1),
            halign="center",
            valign="top"
        ))
        
        # Разработчик
        self.add_widget(Label(
            text="👨‍💻 Разработчик: Костин Никита Андреевич",
            font_size=sp(13),
            size_hint=(1, None),
            height=dp(30),
            color=(0.6, 0.6, 0.8, 1)
        ))
        
        # Кнопка назад
        btn = Button(
            text="◀ НАЗАД",
            font_size=sp(16),
            size_hint=(0.5, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            background_color=(0.3, 0.3, 0.5, 1),
            background_normal=""
        )
        btn.bind(on_press=self.go_back)
        self.add_widget(btn)
    
    def go_back(self, instance):
        """Возврат в меню"""
        if self.app:
            self.app.switch_to("menu")