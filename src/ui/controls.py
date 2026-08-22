"""
CONTROLS - Панель управления тембрами
Полная копия v5.8
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp, sp



# 🏷️ СТАРТ_БЛОКА: CONTROLSLAYOUT
# 🏷️ КОНЕЦ_БЛОКА: CONTROLSLAYOUT

class ControlsLayout(BoxLayout):
    """Панель управления - полная копия v5.8"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.orientation = 'horizontal'
        self.padding = dp(10)
        self.spacing = dp(8)
        self.size_hint = (1, None)
        self.height = dp(50)
        
        timbres = ["Синус", "Орган", "Скрипка", "Флейта", "Кларнет"]
        self.timbre_buttons = {}
        
        for name in timbres:
            btn = Button(
                text=name,
                font_size=sp(12),
                size_hint=(0.2, 1),
                background_normal='',
                background_color=(0.2, 0.2, 0.3, 1) if name != "Синус" else (0.3, 0.6, 0.3, 1)
            )
            btn.bind(on_press=lambda x, n=name: self.select_timbre(n))
            self.add_widget(btn)
            self.timbre_buttons[name] = btn
    

# 🏷️ СТАРТ_БЛОКА: SELECT_TIMBRE
# 🏷️ КОНЕЦ_БЛОКА: SELECT_TIMBRE

    def select_timbre(self, name):
        """Выбор тембра"""
        while self.engine.get_timbre_name() != name:
            self.engine.next_timbre()
        for btn_name, btn in self.timbre_buttons.items():
            btn.background_color = (0.3, 0.6, 0.3, 1) if btn_name == name else (0.2, 0.2, 0.3, 1)