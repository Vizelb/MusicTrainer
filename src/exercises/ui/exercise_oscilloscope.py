"""
EXERCISE OSCILLOSCOPE - Осциллограф для упражнений
Адаптированная версия с суженным диапазоном частот
"""

import numpy as np
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.clock import Clock
from kivy.metrics import dp

from ui.widgets import OscilloscopeWidget


# 🏷️ СТАРТ_БЛОКА: EXERCISEOSCILLOSCOPE
# 🏷️ КОНЕЦ_БЛОКА: EXERCISEOSCILLOSCOPE

class ExerciseOscilloscope(OscilloscopeWidget):
    """
    Осциллограф для упражнений с суженным диапазоном частот
    Наследуется от основного OscilloscopeWidget
    """
    
    def __init__(self, engine, target_freq=None, range_cents=400, exercise_engine=None, **kwargs):
        """
        Args:
            engine: SoundEngine (для визуализации)
            target_freq: целевая частота (центр диапазона)
            range_cents: диапазон в центах (±)
            exercise_engine: ExerciseEngine (для управления частотой)
        """
        super().__init__(engine, **kwargs)
        
        self.target_freq = target_freq or 440.0
        self.range_cents = range_cents
        
        # Сохраняем ссылку на ExerciseEngine для управления
        self.exercise_engine = exercise_engine or engine
        
        # Режим упражнения (по умолчанию False - джойстик)
        self.is_exercise_mode = False
        
        # Переопределяем границы частот
        self._update_frequency_range()
        
        # Устанавливаем начальную частоту в центр диапазона
        self.current_freq = self.target_freq
        self.engine.set_frequency(self.current_freq)
        
        print(f"🎯 ExerciseOscilloscope: target={self.target_freq:.1f} Гц, range=±{self.range_cents} центов")
        print(f"   Диапазон: {self.min_freq:.1f} - {self.max_freq:.1f} Гц")
    
    def _update_frequency_range(self):
        """Обновление диапазона частот на основе целевой частоты"""
        if self.target_freq:
            # Рассчитываем границы в Гц
            self.min_freq = self.target_freq * (2 ** (-self.range_cents / 1200))
            self.max_freq = self.target_freq * (2 ** (self.range_cents / 1200))
        else:
            self.min_freq = 100.0
            self.max_freq = 3500.0
        
        # Минимальные значения для защиты
        self.min_freq = max(self.min_freq, 20.0)
        self.max_freq = min(self.max_freq, 20000.0)
    
    def set_target_frequency(self, target_freq):
        """Установка новой целевой частоты"""
        self.target_freq = target_freq
        self._update_frequency_range()
        # ⚠️ НЕ МЕНЯЕМ current_freq на target_freq!
        # Сохраняем текущую частоту, если она в пределах диапазона
        if self.current_freq < self.min_freq or self.current_freq > self.max_freq:
            self.current_freq = self.target_freq
            self.engine.set_frequency(self.current_freq)
        print(f"   Целевая частота обновлена: {self.target_freq:.1f} Гц")
        print(f"   Диапазон: {self.min_freq:.1f} - {self.max_freq:.1f} Гц")
        print(f"   Текущая частота: {self.current_freq:.1f} Гц (не изменена)")
    
    def _update_frequency(self, dt):
        """Обновление частоты и громкости с защитой от сброса"""
        if not self.touch_active:
            return
        
        # ===== ЗАЩИТА ОТ СБРОСА =====
        # Синхронизация с движком перед каждым обновлением
        if self.is_exercise_mode and self.exercise_engine:
            # Получаем текущую частоту из движка
            if hasattr(self.exercise_engine, "interval_engine") and self.exercise_engine.interval_engine:
                engine_freq = self.exercise_engine.interval_engine.current_frequency
            else:
                engine_freq = self.exercise_engine.get_current_frequency()
            
            # Синхронизируем если частота из движка отличается от current_freq
            if engine_freq > 0:
                diff = abs(engine_freq - self.current_freq)
                # Синхронизируем если разница > 10 Гц или current_freq на границе
                if diff > 10 or self.current_freq <= 1.0 or self.current_freq >= self.max_freq - 1.0:
                    self.current_freq = engine_freq
                    print(f"   ⚠️ Авто-синхронизация: {self.current_freq:.1f} Гц (diff={diff:.1f})")
        
        # ===== УПРАВЛЕНИЕ ЧАСТОТОЙ (ОСЬ X) =====
        distance = abs(self.touch_x)
        direction = 1 if self.touch_x > 0 else -1
        
        # Адаптивная скорость: чем дальше от центра, тем быстрее
        normalized = max(0, min(1, distance))
        speed_factor = 3 * normalized**4 - 2 * normalized**6
        
        # Максимальная скорость = 5% от диапазона в секунду
        max_speed = (self.max_freq - self.min_freq) * 0.05
        speed = speed_factor * max_speed * direction
        
        self.current_freq += speed * dt
        self.current_freq = max(self.min_freq, min(self.max_freq, self.current_freq))
        
        # ===== УПРАВЛЕНИЕ ГРОМКОСТЬЮ (ОСЬ Y) =====
        y_normalized = max(-1, min(1, self.touch_y))
        
        # Логарифмическая зависимость
        if y_normalized >= 0:
            volume_factor = 0.5 + 0.5 * (y_normalized ** 0.7)
        else:
            volume_factor = 0.5 * ((1 + y_normalized) ** 0.7)
        
        self.current_vol = max(0.01, min(1.0, volume_factor))
        
        # Если мы в режиме упражнения - используем update_interval_frequency
        if self.is_exercise_mode and self.exercise_engine:
            self.exercise_engine.update_interval_frequency(self.current_freq)
            if hasattr(self.exercise_engine, "interval_engine") and self.exercise_engine.interval_engine:
                self.exercise_engine.interval_engine.set_volume(self.current_vol)
        else:
            self.engine.set_frequency(self.current_freq)
            self.engine.set_volume(self.current_vol)
    
    def set_exercise_mode(self, enabled=True):
        """Установка режима упражнения"""
        self.is_exercise_mode = enabled
        if enabled and self.exercise_engine:
            # Получаем частоту из движка
            freq = self.exercise_engine.get_current_frequency()
            if freq > 0:
                self.current_freq = freq
            
            # Сбрасываем громкость на начальную (из настроек)
            if hasattr(self.exercise_engine, 'settings'):
                start_vol = self.exercise_engine.settings.interval_start_volume / 100.0
                self.current_vol = start_vol
                # Применяем громкость к интервалу
                if hasattr(self.exercise_engine, 'interval_engine') and self.exercise_engine.interval_engine:
                    self.exercise_engine.interval_engine.set_volume(start_vol)

    def sync_frequency_from_engine(self):
        """Синхронизация частоты из движка."""
        """Синхронизация частоты из движка."""
        if self.exercise_engine:
            # Пытаемся получить частоту напрямую из interval_engine
            freq = 0.0
            if hasattr(self.exercise_engine, "interval_engine") and self.exercise_engine.interval_engine:
                freq = self.exercise_engine.interval_engine.current_frequency
                print(f"   🔍 sync: частота из interval_engine = {freq:.1f} Гц")
            
            # Если не получилось, пробуем через get_current_frequency
            if freq <= 0:
                freq = self.exercise_engine.get_current_frequency()
                print(f"   🔍 sync: частота из get_current_frequency = {freq:.1f} Гц")
            
            if freq > 0:
                self.current_freq = freq
                print(f"   🔄 Осциллограф синхронизирован: {freq:.1f} Гц")
                
                # Также синхронизируем громкость
                if hasattr(self.exercise_engine, "settings"):
                    start_vol = self.exercise_engine.settings.interval_start_volume / 100.0
                    self.current_vol = start_vol
                    if hasattr(self.exercise_engine, "interval_engine") and self.exercise_engine.interval_engine:
                        self.exercise_engine.interval_engine.set_volume(start_vol)
                return True
        return False

    def update_frequency_from_engine(self):
        """Обновление текущей частоты из движка"""
        if self.exercise_engine and hasattr(self.exercise_engine, 'get_current_frequency'):
            freq = self.exercise_engine.get_current_frequency()
            if freq > 0:
                self.current_freq = freq
                print(f"   📊 ExerciseOscilloscope обновил частоту: {freq:.1f} Гц")
    
    def update_visualization(self, dt):
        """
        Обновление визуализации осциллографа.
        В режиме упражнения показывает данные из интервала.
        """
        try:
            self.canvas.clear()
            
            # Получаем данные для визуализации
            if self.is_exercise_mode and self.exercise_engine:
                sine_data = self.exercise_engine.get_sine_data()
            else:
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
    
    def on_touch_down(self, touch):
        """Обработка касания"""
        if self.collide_point(touch.x, touch.y):
            self.touch_active = True
            self.touch_x = 0.0
            self.touch_y = 0.0
            if self.is_exercise_mode and self.exercise_engine:
                sine_data = self.exercise_engine.get_sine_data()
            else:
                sine_data = self.engine.get_sine_data()
            self.frozen_sine_data = sine_data.copy()
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        """Обработка движения касания"""
        if self.touch_active:
            rel_x = (touch.x - (self.x + self.width / 2)) / (self.width / 2)
            rel_y = (touch.y - (self.y + self.height / 2)) / (self.height / 2)
            self.touch_x = max(-1, min(1, rel_x))
            self.touch_y = max(-1, min(1, rel_y))
            self._update_frequency(0.02)
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        """Обработка отпускания касания"""
        if self.touch_active:
            self.touch_active = False
            self.touch_x = 0.0
            self.touch_y = 0.0
            return True
        return super().on_touch_up(touch)
    
    def get_current_frequency(self):
        """Получение текущей частоты"""
        return self.current_freq
    
    def get_target_frequency(self):
        """Получение целевой частоты"""
        return self.target_freq
    
    def update_range(self, range_cents):
        """
        Обновление диапазона частот из настроек.
        """
        self.range_cents = range_cents
        self._update_frequency_range()
        print(f"   📊 Диапазон обновлен: ±{self.range_cents} центов")
        print(f"   Диапазон: {self.min_freq:.1f} - {self.max_freq:.1f} Гц")

    def get_range_cents(self):
        """Получение текущего диапазона в центах"""
        return self.range_cents
    
    def get_deviation_cents(self):
        """Получение отклонения в центах от целевой частоты"""
        if self.target_freq > 0 and self.current_freq > 0:
            return 1200 * np.log2(self.current_freq / self.target_freq)
        return 0.0
# 🏷️ КОНЕЦ_БЛОКА: EXERCISEOSCILLOSCOPE