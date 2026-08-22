"""
WIDGETS - Осциллограф и информационная панель
Полная копия v5.8
"""

import numpy as np
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Color, Line, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp, sp


# ==================== ОСЦИЛЛОГРАФ (ПОЛНАЯ КОПИЯ v5.8) ====================


# 🏷️ СТАРТ_БЛОКА: OSCILLOSCOPEWIDGET
# 🏷️ КОНЕЦ_БЛОКА: OSCILLOSCOPEWIDGET

class OscilloscopeWidget(Widget):
    """Осциллограф с невидимым джойстиком - полная копия v5.8"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.points = 1000
        self.line_width = 2
        self.grid_color = (0.15, 0.15, 0.25, 0.6)
        self.wave_color = (0.3, 0.9, 0.3, 1)
        self.phase_marker_color = (0.9, 0.3, 0.3, 1)
        self.bg_color = (0.03, 0.03, 0.06, 1)
        
        # Невидимый джойстик
        self.touch_active = False
        self.touch_x = 0.0
        self.touch_y = 0.0
        self.max_freq_speed = 200.0
        self.min_freq = 100.0
        self.max_freq = 3500.0
        self.current_freq = 440.0
        self.current_vol = 0.5
        
        # Режим упражнения (по умолчанию False - джойстик)
        self.is_exercise_mode = False
        
        # Стоп-кадр
        self.frozen_sine_data = None
        self.display_sine_data = np.zeros(1000)
        
        self.bind(size=self.on_size)
        Clock.schedule_interval(self.update_visualization, 0.05)
    

# 🏷️ СТАРТ_БЛОКА: _GET_SPEED
# 🏷️ КОНЕЦ_БЛОКА: _GET_SPEED

    def _get_speed(self, distance):
        normalized = max(0, min(1, distance))
        speed_factor = 3 * normalized**4 - 2 * normalized**6
        return speed_factor * self.max_freq_speed
    

# 🏷️ СТАРТ_БЛОКА: _UPDATE_FREQUENCY
# 🏷️ КОНЕЦ_БЛОКА: _UPDATE_FREQUENCY

    def _update_frequency(self, dt):
        if not self.touch_active:
            return
        
        distance = abs(self.touch_x)
        direction = 1 if self.touch_x > 0 else -1
        speed = self._get_speed(distance) * direction
        
        self.current_freq += speed * dt
        self.current_freq = max(self.min_freq, min(self.max_freq, self.current_freq))
        
        vol_change = self.touch_y * 0.5
        self.current_vol += vol_change * dt
        self.current_vol = max(0.05, min(1.0, self.current_vol))
        
        # Если мы в режиме упражнения - используем update_interval_frequency
        if self.is_exercise_mode and hasattr(self.engine, 'update_interval_frequency'):
            self.engine.update_interval_frequency(self.current_freq)
            # В упражнениях громкость управляется отдельно
        else:
            # В режиме джойстика - обычное управление
            self.engine.set_frequency(self.current_freq)
            self.engine.set_volume(self.current_vol)
    

# 🏷️ СТАРТ_БЛОКА: UPDATE_VISUALIZATION
# 🏷️ КОНЕЦ_БЛОКА: UPDATE_VISUALIZATION

    def update_visualization(self, dt):
        try:
            self.canvas.clear()
            sine_data = self.engine.get_sine_data()
            if self.frozen_sine_data is None:
                self.frozen_sine_data = sine_data.copy()
            if len(self.frozen_sine_data) >= self.points:
                display_data = self.frozen_sine_data[:self.points]
            else:
                display_data = np.pad(self.frozen_sine_data, (0, self.points - len(self.frozen_sine_data)))
            self.display_sine_data = display_data
            
            with self.canvas:
                Color(*self.bg_color)
                Rectangle(pos=self.pos, size=self.size)
                Color(*self.grid_color)
                for i in range(1, 9):
                    y = self.y + (i / 9) * self.height
                    Line(points=[self.x, y, self.x + self.width, y], width=1)
                for i in range(1, 9):
                    x = self.x + (i / 9) * self.width
                    Line(points=[x, self.y, x, self.y + self.height], width=1)
                Color(0.4, 0.8, 0.4, 0.3)
                Line(points=[self.x, self.y + self.height / 2, self.x + self.width, self.y + self.height / 2], width=1)
                Color(*self.wave_color)
                points = []
                for i, val in enumerate(display_data):
                    x = self.x + (i / self.points) * self.width
                    y = self.y + self.height / 2 - val * self.height / 2
                    points.extend([x, y])
                if len(points) > 2:
                    Line(points=points, width=self.line_width)
                
                if self.touch_active:
                    joy_x = self.x + self.width / 2 + self.touch_x * self.width * 0.4
                    joy_y = self.y + self.height / 2 + self.touch_y * self.height * 0.4
                    Color(0.9, 0.9, 0.3, 0.7)
                    radius = 8
                    Ellipse(pos=(joy_x - radius, joy_y - radius), size=(radius * 2, radius * 2))
                    Color(1, 1, 1, 0.2)
                    radius = 12
                    Ellipse(pos=(joy_x - radius, joy_y - radius), size=(radius * 2, radius * 2))
                    Color(0.9, 0.9, 0.3, 0.2)
                    Line(points=[self.x + self.width / 2, self.y + self.height / 2, joy_x, joy_y], width=1)
        except Exception as e:
            pass
    

# 🏷️ СТАРТ_БЛОКА: ON_TOUCH_DOWN
# 🏷️ КОНЕЦ_БЛОКА: ON_TOUCH_DOWN

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.touch_active = True
            self.touch_x = 0.0
            self.touch_y = 0.0
            sine_data = self.engine.get_sine_data()
            self.frozen_sine_data = sine_data.copy()
            return True
        return super().on_touch_down(touch)
    

# 🏷️ СТАРТ_БЛОКА: ON_TOUCH_MOVE
# 🏷️ КОНЕЦ_БЛОКА: ON_TOUCH_MOVE

    def on_touch_move(self, touch):
        if self.touch_active:
            rel_x = (touch.x - (self.x + self.width / 2)) / (self.width / 2)
            rel_y = (touch.y - (self.y + self.height / 2)) / (self.height / 2)
            self.touch_x = max(-1, min(1, rel_x))
            self.touch_y = max(-1, min(1, rel_y))
            self._update_frequency(0.02)
            return True
        return super().on_touch_move(touch)
    

# 🏷️ СТАРТ_БЛОКА: ON_TOUCH_UP
# 🏷️ КОНЕЦ_БЛОКА: ON_TOUCH_UP

    def on_touch_up(self, touch):
        if self.touch_active:
            self.touch_active = False
            self.touch_x = 0.0
            self.touch_y = 0.0
            return True
        return super().on_touch_up(touch)
    

# 🏷️ СТАРТ_БЛОКА: ON_SIZE
# 🏷️ КОНЕЦ_БЛОКА: ON_SIZE

    
    
    def update_frequency_from_engine(self):
        """Обновление текущей частоты из движка"""
        if self.engine and hasattr(self.engine, 'get_current_frequency'):
            self.current_freq = self.engine.get_current_frequency()    
    def set_exercise_mode(self, enabled=True):
        """Установка режима упражнения"""
        self.is_exercise_mode = enabled
        print(f"   🎯 Осциллограф: режим {'упражнения' if enabled else 'джойстика'}")    
    def on_size(self, *args):
        self.update_visualization(None)


# ==================== ИНФОРМАЦИОННАЯ ПАНЕЛЬ (ПОЛНАЯ КОПИЯ v5.8) ====================


# 🏷️ СТАРТ_БЛОКА: INFOLAYOUT
# 🏷️ КОНЕЦ_БЛОКА: INFOLAYOUT

class InfoLayout(BoxLayout):
    """Информационная панель - полная копия v5.8"""
    

# 🏷️ СТАРТ_БЛОКА: __INIT__
# 🏷️ КОНЕЦ_БЛОКА: __INIT__

    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.orientation = 'horizontal'
        self.padding = dp(10)
        self.spacing = dp(20)
        self.size_hint = (1, None)
        self.height = dp(40)
        
        self.timbre_label = Label(
            text="🎹 Синус",
            font_size=sp(16),
            size_hint=(0.4, 1),
            halign='left',
            color=(0.8, 0.8, 0.8, 1)
        )
        self.add_widget(self.timbre_label)
        
        self.volume_label = Label(
            text="🔊 50%",
            font_size=sp(16),
            size_hint=(0.3, 1),
            halign='center',
            color=(0.8, 0.8, 0.8, 1)
        )
        self.add_widget(self.volume_label)
        
        self.freq_label = Label(
            text="🎵 440 Гц",
            font_size=sp(16),
            size_hint=(0.3, 1),
            halign='right',
            color=(0.8, 0.8, 0.8, 1)
        )
        self.add_widget(self.freq_label)
        
        Clock.schedule_interval(self.update_info, 0.1)
    

# 🏷️ СТАРТ_БЛОКА: UPDATE_INFO
# 🏷️ КОНЕЦ_БЛОКА: UPDATE_INFO

    def update_info(self, dt):
        data = self.engine.get_diagnostics()
        self.timbre_label.text = f"🎹 {data['timbre']}"
        self.volume_label.text = f"🔊 {data['volume']*100:.0f}%"
        self.freq_label.text = f"🎵 {data['freq']:.0f} Гц"