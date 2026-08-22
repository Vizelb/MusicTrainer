"""
SOUND ENGINE - Звуковой движок с управлением старт/стоп
"""

import pygame
import numpy as np
from kivy.clock import Clock

from .timbre import Timbre
from .mixer import mixer


class SoundEngine:
    """Звуковой движок с управлением старт/стоп"""
    
    def __init__(self):
        # ============ ИНИЦИАЛИЗАЦИЯ PYGAME ============
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=2048)
            pygame.init()
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=2048)
                print("✅ Pygame микшер инициализирован (МОНО)")
            except Exception as e:
                print(f"⚠️ Ошибка инициализации микшера: {e}")
                pygame.mixer.init()
                print("✅ Pygame микшер инициализирован (с параметрами по умолчанию)")
        else:
            print("ℹ️ Pygame микшер уже инициализирован")
        
        self.SAMPLE_RATE = 44100
        
        # 🔧 ВОЗВРАЩАЕМ: буфер 2.0 для плавности (было 0.5)
        self.buffer_duration = 2.0
        self.buffer_size = int(self.SAMPLE_RATE * self.buffer_duration)
        
        # Параметры звука
        self.current_frequency = 440.0
        self.current_volume = 0.5
        self._freq_target = 440.0
        self._vol_target = 0.5
        
        # Фаза
        self.phase = 0.0
        
        # Тембр
        self.timbre_names = ["Синус", "Орган", "Скрипка", "Флейта", "Кларнет"]
        self.timbre_index = 0
        self.timbre = Timbre(self.timbre_names[0])
        
        # Ramp (плавное изменение частоты)
        self.ramp_time = 0.02
        self.ramp_progress = 1.0
        self.ramp_start_freq = 440.0
        self.ramp_end_freq = 440.0
        
        # Кроссфейд (плавные переходы)
        self.crossfade_active = False
        self.old_buffer = None
        self.crossfade_size = 256
        self.crossfade_in = np.linspace(0, 1, self.crossfade_size) ** 2
        self.crossfade_out = np.linspace(1, 0, self.crossfade_size) ** 2
        
        # Phase Locking
        self.phase_locked = True
        self.reference_phase = 0.0
        
        # Режим осциллографа
        self.oscilloscope_mode = True
        
        # Данные для визуализации
        self.sine_data = np.zeros(1000)
        self.update_count = 0
        self.freq_changes = 0
        
        # Управление старт/стоп
        self.is_playing = False
        self.sound = None
        self.sound_array = None
        self.channel = None
        
        # Глобальный лимитер громкости (предотвращает клиппинг)
        self.MAX_VOLUME = 0.9  # 90% от максимума
        
        # Громкость для микшера
        self._volume = 0.5
        
        # Регистрируемся в микшере
        mixer.register_engine(self)
        
        
        
        print(f"   🎹 Тембр: {self.timbre.name}")
        print("   ⏸️ Звук остановлен (нажмите СТАРТ)")
        
        # 🔧 ВОЗВРАЩАЕМ: частота обновления 0.01 (было 0.02)
        Clock.schedule_interval(self._update_sound, 0.01)
    
    # ============================================
    # ПУБЛИЧНЫЕ МЕТОДЫ
    # ============================================
    
    def start(self):
        """Запуск генерации звука"""
        if self.is_playing:
            print("   ℹ️ Звук уже играет")
            return
        
        print("▶️ Запуск звука...")
        
        # Ищем свободный канал
        self.channel = None
        for i in range(pygame.mixer.get_num_channels()):
            if not pygame.mixer.Channel(i).get_busy():
                self.channel = pygame.mixer.Channel(i)
                break
        
        # Если все заняты, используем первый
        if self.channel is None:
            self.channel = pygame.mixer.Channel(0)
        
        self.channel.set_volume(1.0)
        
        initial_buffer = self._generate_buffer(self.current_frequency, self.current_volume)
        self.sound = pygame.sndarray.make_sound(initial_buffer)
        self.sound_array = pygame.sndarray.samples(self.sound)
        self.channel.play(self.sound, loops=-1)
        
        self.is_playing = True
        
        # Обновляем микшер
        mixer.apply_mix()
        
        print(f"✅ Звук запущен на канале {self.channel}")
    
    def stop(self):
        """Остановка генерации звука"""
        if not self.is_playing:
            print("   ℹ️ Звук уже остановлен")
            return
        
        print("⏹️ Остановка звука...")
        
        if self.channel:
            self.channel.stop()
            self.channel = None
        
        self.sound = None
        self.sound_array = None
        self.is_playing = False
        
        # Обновляем микшер
        mixer.apply_mix()
        
        print("✅ Звук остановлен")
    
    def toggle(self):
        """Переключение старт/стоп"""
        if self.is_playing:
            self.stop()
        else:
            self.start()
        return self.is_playing
    
    def full_stop(self):
        """Полная остановка (для завершения приложения)"""
        # Удаляем из микшера
        mixer.unregister_engine(self)
        self.stop()
        if pygame.mixer.get_init():
            pygame.mixer.quit()
    def _generate_buffer(self, freq, volume):
        """
        Генерация звукового буфера.
        ВАЖНО: Для МОНО-режима используется 1D массив.
        """
        freq = max(100, min(10000, freq))
        volume = max(0, min(1, volume))
        size = self.buffer_size
        
        if self.oscilloscope_mode:
            start_phase = 0.0
        else:
            start_phase = self.phase
        
        wave = self.timbre.generate(start_phase, freq, size, self.SAMPLE_RATE, volume)
        
        phase_inc = 2 * np.pi * freq / self.SAMPLE_RATE
        if not self.oscilloscope_mode:
            self.phase = (self.phase + phase_inc * size) % (2 * np.pi)
        else:
            self.phase = 0.0
        
        self.sine_data = wave[-1000:].copy()
        return (wave * 32767).astype(np.int16)
    
    def _apply_ramp(self, target_freq, dt):
        """Плавное изменение частоты"""
        if self.ramp_progress < 1.0:
            self.ramp_progress += dt / self.ramp_time
            if self.ramp_progress >= 1.0:
                self.ramp_progress = 1.0
                self.current_frequency = self.ramp_end_freq
                return self.ramp_end_freq
            p = self.ramp_progress
            p_smooth = 3 * p**2 - 2 * p**3
            freq = self.ramp_start_freq + (self.ramp_end_freq - self.ramp_start_freq) * p_smooth
            self.current_frequency = freq
            return freq
        else:
            return self.current_frequency
    
    def _update_sound(self, dt):
        """Обновление звука (вызывается каждый кадр)"""
        # Если звук не играет - только обновляем данные для осциллографа
        if not self.is_playing:
            wave = np.zeros(self.buffer_size)
            self.sine_data = wave[-1000:].copy()
            return
        
        if not self.channel:
            return
        
        if abs(self._freq_target - self.ramp_end_freq) > 0.1:
            self.ramp_start_freq = self.current_frequency
            self.ramp_end_freq = self._freq_target
            self.ramp_progress = 0.0
            self.crossfade_active = True
            self.freq_changes += 1
        
        current_freq = self._apply_ramp(self._freq_target, dt)
        
        vol_diff = self._vol_target - self.current_volume
        if abs(vol_diff) > 0.001:
            self.current_volume += vol_diff * 0.1
        else:
            self.current_volume = self._vol_target
        
        new_buffer = self._generate_buffer(current_freq, self.current_volume)
        
        if self.crossfade_active and self.old_buffer is not None:
            old = self.old_buffer.astype(np.float64)
            new = new_buffer.astype(np.float64)
            fade_size = min(self.crossfade_size, len(new_buffer) // 4)
            fade_in = self.crossfade_in[:fade_size]
            fade_out = self.crossfade_out[:fade_size]
            old[-fade_size:] = old[-fade_size:] * fade_out
            new[:fade_size] = new[:fade_size] * fade_in
            mixed = old.copy()
            mixed[-fade_size:] += new[:fade_size]
            mixed[fade_size:] = new[fade_size:]
            new_buffer = mixed.astype(np.int16)
            self.crossfade_active = False
            self.old_buffer = None
        else:
            self.old_buffer = new_buffer.copy()
        
        np.copyto(self.sound_array, new_buffer)
        self.update_count += 1
    
    # ============================================
    # ГЕТТЕРЫ И ДИАГНОСТИКА
    # ============================================
    
    def set_frequency(self, freq):
        """Установка частоты"""
        self._freq_target = max(100, min(10000, freq))
    
    def update_interval_frequency(self, freq):
        """
        Обновление частоты интервала (для совместимости с ExerciseEngine).
        Просто вызывает set_frequency().
        """
        self.set_frequency(freq)
    
    def set_volume(self, vol):
        """
        Установка громкости с использованием микшера.
        
        Args:
            vol: float от 0 до 1.0
        """
        # Сохраняем целевую громкость для микшера
        self._volume = max(0, min(1.0, vol))
        # Микшер применит оптимальное значение
        mixer.apply_mix()
    def next_timbre(self):
        """Следующий тембр"""
        self.timbre_index = (self.timbre_index + 1) % len(self.timbre_names)
        self.timbre = Timbre(self.timbre_names[self.timbre_index])
        print(f"🔄 Тембр: {self.timbre.name}")
    
    def get_timbre_name(self):
        """Получение имени текущего тембра"""
        return self.timbre.name
    
    def get_sine_data(self):
        """Получение данных для осциллографа"""
        return self.sine_data
    
    def get_current_frequency(self):
        """Получение текущей частоты"""
        return self.current_frequency
    
    def get_current_volume(self):
        """Получение текущей громкости"""
        return self.current_volume
    
    def get_diagnostics(self):
        """Получение диагностической информации"""
        return {
            "freq": self.current_frequency,
            "target": self._freq_target,
            "phase": self.phase,
            "timbre": self.timbre.name,
            "sine_data": self.sine_data,
            "volume": self.current_volume,
            "updates": self.update_count,
            "oscilloscope_mode": self.oscilloscope_mode,
            "is_playing": self.is_playing
        }