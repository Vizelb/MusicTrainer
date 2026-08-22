"""
EXERCISE ENGINE - Движок упражнений
Управляет воспроизведением и логикой упражнений
"""

import random
import numpy as np
from typing import List, Tuple, Optional
from datetime import datetime
from kivy.clock import Clock

from core.engine import SoundEngine
from exercises.config.settings import ExerciseSettings
from core.timbre import Timbre
from core.statistics import stats_manager


# 🏷️ СТАРТ_БЛОКА: EXERCISEENGINE
# 🏷️ КОНЕЦ_БЛОКА: EXERCISEENGINE

class ExerciseEngine:
    """Движок для управления упражнениями"""
    
    def __init__(self, settings: ExerciseSettings):
        self.settings = settings
        self.sound_engine = None
        self.interval_engine = None
        self.tonic_engine = None
        self.current_task = None
        self.target_freq = None  # Эталонная частота (не меняется)
        self.is_active = False
        self.is_playing = False
        self.is_harmonic_mode = False  # Флаг гармонического режима
        self.interval_timer = None
        self.tonic_timer = None
        
        # Громкости (в долях от 1.0)
        self.tonic_volume_float = self.settings.tonic_volume / 100.0
        self.interval_start_volume_float = self.settings.interval_start_volume / 100.0
        
        # Статистика
        self.correct_count = 0
        self.wrong_count = 0
        self.total_deviation = 0.0
        self.deviation_count = 0
        
        # Устанавливаем тембр из настроек
        self._setup_timbre()
        
        print(f"🎵 ExerciseEngine создан. Тембр: {self.settings.timbre}")
    
    def _setup_timbre(self):
        """Настройка тембра из настроек (без создания SoundEngine)"""
        timbre_names = ["Синус", "Орган", "Скрипка", "Флейта", "Кларнет"]
        
        if self.settings.timbre in timbre_names:
            self.timbre_name = self.settings.timbre
        else:
            self.timbre_name = "Синус"
        
        print(f"   🎹 Тембр установлен: {self.timbre_name}")
    
    def _get_note_duration(self) -> float:
        """Получение длительности ноты на основе скорости"""
        speed = self.settings.speed
        return 0.5 + (speed / 100) * 9.5
    
    def _play_note(self, frequency: float, duration: float, callback=None):
        """Воспроизведение одной ноты с заданной длительностью"""
        if not self.sound_engine:
            return
        
        self.sound_engine.stop()
        self.sound_engine.set_frequency(frequency)
        self.sound_engine.set_volume(self.tonic_volume_float)
        self.sound_engine.timbre = Timbre(self.timbre_name)
        self.sound_engine.start()
        self.is_playing = True
        
        if callback:
            Clock.schedule_once(lambda dt: self._stop_note(callback), duration)
        else:
            Clock.schedule_once(lambda dt: self._stop_note(), duration)
        
        print(f"   🎵 Нота: {frequency:.1f} Гц, {duration:.1f} сек")
    def _play_note_without_stop(self, frequency: float, duration: float, callback=None):
        """
        Воспроизведение ноты БЕЗ остановки текущего звука.
        Используется для гармонического режима.
        """
        if not self.sound_engine:
            return
        
        self.sound_engine.set_frequency(frequency)
        self.sound_engine.set_volume(self.tonic_volume_float)
        self.sound_engine.timbre = Timbre(self.timbre_name)
        self.sound_engine.start()
        self.is_playing = True
        
        if callback:
            Clock.schedule_once(lambda dt: self._stop_note(callback), duration)
        else:
            Clock.schedule_once(lambda dt: self._stop_note(), duration)
        
        print(f"   🎵 Нота (поверх): {frequency:.1f} Гц, {duration:.1f} сек")
    
    def _start_harmonic_tonic(self):
        """Запуск постоянного звучания тоники (гармонический режим)"""
        print("🔍 _start_harmonic_tonic: ВЫЗВАН")
        
        if not self.current_task:
            print("   ⚠️ _start_harmonic_tonic: current_task is None")
            return
        
        tonic_freq = self.current_task["tonic_freq"]
        print(f"   🎵 ТОНИКА: {tonic_freq:.1f} Гц")
        
        # Создаем tonic_engine если нужно
        if self.tonic_engine is None:
            print("   🔧 СОЗДАЕМ tonic_engine")
            self.tonic_engine = SoundEngine()
            print("   ✅ tonic_engine создан")
        
        # Останавливаем предыдущий звук тоники
        self.tonic_engine.stop()
        
        # Настраиваем и запускаем тонику
        self.tonic_engine.set_frequency(tonic_freq)
        self.tonic_engine.set_volume(self.tonic_volume_float)
        self.tonic_engine.timbre = Timbre(self.timbre_name)
        self.tonic_engine.start()
        self.is_harmonic_mode = True
        self.is_playing = True
        
        print(f"   🎵 ТОНИКА (фон) ЗАПУЩЕНА: {tonic_freq:.1f} Гц")
    
    def _stop_harmonic_tonic(self):
        """Остановка постоянного звучания тоники"""
        print("🔍 _stop_harmonic_tonic: ВЫЗВАН")
        
        if self.tonic_engine:
            self.tonic_engine.stop()
            self.is_harmonic_mode = False
            self.is_playing = False
            print("   🔇 ТОНИКА (фон) остановлена")
        else:
            print("   ⚠️ tonic_engine is None")
    
    def _stop_note(self, callback=None):
        """Остановка звука и вызов колбэка"""
        if self.sound_engine and not self.is_harmonic_mode:
            self.sound_engine.stop()
        self.is_playing = False
        
        if callback:
            callback()
    
    def start_session(self):
        """Начало сессии упражнений"""
        self.is_active = True
        self.correct_count = 0
        self.wrong_count = 0
        self.total_deviation = 0.0
        self.deviation_count = 0
        
        self.sound_engine = SoundEngine()
        self.sound_engine.is_playing = False
        self.sound_engine.timbre = Timbre(self.timbre_name)
        
        # Начинаем сессию статистики
        stats_manager.start_session({
            "mode": self.settings.mode,
            "direction": self.settings.direction,
            "tuning": self.settings.tuning,
            "intervals": self.settings.selected_intervals
        })
        
        print(f"🎯 Сессия упражнений начата")
        print(f"   Тембр: {self.timbre_name}, Громкость тоники/эталона: {self.settings.tonic_volume}%")
    
    def generate_task(self) -> dict:
        """Генерация следующего задания"""
        if not self.is_active:
            return None
        
        intervals = self.settings.selected_intervals
        if not intervals:
            return None
        
        interval_name = random.choice(intervals)
        cents = self.settings.get_interval_cents(interval_name)
        
        direction = self.settings.direction
        if direction == "both":
            direction = random.choice(["up", "down"])
        
        mode = self.settings.mode
        if mode == "both":
            mode = random.choice(["melodic", "harmonic"])
        
        tonic_freq = self._get_random_tonic()
        interval_freq = self._calculate_interval_frequency(tonic_freq, cents, direction)
        
        task = {
            "interval_name": interval_name,
            "cents": cents,
            "direction": direction,
            "mode": mode,
            "tonic_freq": tonic_freq,
            "interval_freq": interval_freq,  # Эталонная частота (НЕ МЕНЯЕТСЯ!)
            "current_freq": interval_freq,   # Текущая частота (меняется пользователем)
            "display_name": self.settings.get_interval_display_name(interval_name),
            "user_freq": None,
            "deviation": None,
            "is_correct": None,
            "completed": False
        }
        
        self.current_task = task
        self.target_freq = interval_freq  # Сохраняем эталон
        return task
    
    def _get_random_tonic(self) -> float:
        """Получение случайной тоники из диапазона"""
        frequencies = self.settings.get_tonic_frequencies()
        if not frequencies:
            return 440.0
        return random.choice(frequencies)
    
    def _calculate_interval_frequency(self, tonic: float, cents: int, direction: str) -> float:
        """Расчет частоты интервала от тоники"""
        if direction == "up":
            return tonic * (2 ** (cents / 1200))
        else:
            return tonic * (2 ** (-cents / 1200))
    
    def _play_melodic(self, tonic_freq: float, interval_freq: float, callback=None):
        """Воспроизведение в мелодическом режиме (последовательно)"""
        duration = self._get_note_duration()
        
        print(f"   🎵 Мелодический режим: тоника → интервал")
        
        def play_interval_part():
            self._play_note(interval_freq, duration, callback)
        
        self._play_note(tonic_freq, duration, play_interval_part)
    
    def _play_harmonic(self, tonic_freq: float, interval_freq: float, callback=None):
        """
        Воспроизведение в гармоническом режиме (одновременно).
        Тоника звучит как фон, интервал поверх.
        """
        duration = self._get_note_duration()
        
        print(f"   🎵 Гармонический режим: тоника + интервал (ОДНОВРЕМЕННО)")
        print(f"   🔍 ТОНИКА: {tonic_freq:.1f} Гц, ИНТЕРВАЛ: {interval_freq:.1f} Гц")
        
        if self.current_task:
            self.current_task["tonic_freq"] = tonic_freq
        
        # Останавливаем все звуки перед воспроизведением
        self.stop_sound()
        
        # Запускаем тонику на отдельном движке
        self._start_harmonic_tonic()
        
        # Создаем движок для интервала если нужно
        if self.interval_engine is None:
            print("   🔧 СОЗДАЕМ interval_engine")
            self.interval_engine = SoundEngine()
            print("   ✅ interval_engine создан")
        
        # Запускаем интервал
        self.interval_engine.stop()
        self.interval_engine.set_frequency(interval_freq)
        self.interval_engine.set_volume(self.tonic_volume_float)
        self.interval_engine.timbre = Timbre(self.timbre_name)
        self.interval_engine.start()
        self.is_playing = True
        
        print(f"   🎵 ИНТЕРВАЛ ЗАПУЩЕН: {interval_freq:.1f} Гц")
        
        # Планируем остановку через duration секунд
        def stop_harmonic():
            print("   🔇 Остановка гармонического режима")
            if self.interval_engine:
                self.interval_engine.stop()
            self._stop_harmonic_tonic()
            self.is_playing = False
            if callback:
                callback()
            print("   ✅ Гармонический режим остановлен")
        
        Clock.schedule_once(lambda dt: stop_harmonic(), duration + 0.1)
    
    def play_interval_full(self, callback=None):
        """Полное воспроизведение интервала (тоника + интервал)"""
        if not self.current_task:
            return
        
        tonic_freq = self.current_task["tonic_freq"]
        interval_freq = self.current_task["interval_freq"]
        mode = self.current_task["mode"]
        
        if mode == "melodic":
            self._play_melodic(tonic_freq, interval_freq, callback)
        else:
            self._play_harmonic(tonic_freq, interval_freq, callback)
    
    # 🏷️ СТАРТ_БЛОКА: PUBLIC_PLAYBACK
    def start_adjustment(self):
        """
        Начало настройки.
        
        Для гармонического режима: тоника звучит как фон, интервал настраивается.
        Для мелодического режима: непрерывный звук для настройки.
        """
        print("🔍 start_adjustment: ВЫЗВАН")
        
        if not self.current_task:
            print("   ⚠️ start_adjustment: current_task is None")
            return
        
        mode = self.current_task["mode"]
        tonic_freq = self.current_task["tonic_freq"]
        interval_freq = self.current_task["interval_freq"]
        
        print(f"   📊 mode: {mode}, tonic: {tonic_freq:.1f}, interval: {interval_freq:.1f}")
        
        # Останавливаем текущий звук
        self.stop_sound()
        
        if mode == "harmonic":
            # Запускаем тонику как фон
            print("   🔄 Вызов _start_harmonic_tonic()")
            self._start_harmonic_tonic()
            print("   ✅ _start_harmonic_tonic() завершен")
            print("   🎵 ГАРМОНИЧЕСКИЙ РЕЖИМ: тоника звучит (фон)")
            
            # Запускаем интервал для настройки
            if self.interval_engine is None:
                print("   🔧 СОЗДАЕМ interval_engine")
                self.interval_engine = SoundEngine()
                print("   ✅ interval_engine создан")
            
            # Останавливаем предыдущий звук интервала
            self.interval_engine.stop()
            
            # Генерируем случайную начальную частоту
            start_range = self.settings.start_range  # Диапазон старта в центах
            
            # Рассчитываем границы для случайной частоты
            start_min = self.target_freq * (2 ** (-start_range / 1200))
            start_max = self.target_freq * (2 ** (start_range / 1200))
            
            # Ограничиваем глобальными границами (100-3500 Гц)
            start_min = max(start_min, 100.0)
            start_max = min(start_max, 3500.0)
            
            # Генерируем случайную частоту
            import random
            initial_freq = random.uniform(start_min, start_max)
            
            # Сохраняем начальную частоту
            if self.current_task:
                self.current_task["current_freq"] = initial_freq
            
            print(f"   🎲 Случайная частота: {initial_freq:.1f} Гц (диапазон: {start_min:.1f}-{start_max:.1f} Гц)")
            
            # Настраиваем и запускаем интервал
            self.interval_engine.set_frequency(initial_freq)
            self.interval_engine.set_volume(self.tonic_volume_float)
            self.interval_engine.timbre = Timbre(self.timbre_name)
            self.interval_engine.start()
            self.is_playing = True
            print(f"   🎵 Интервал для настройки: {initial_freq:.1f} Гц (эталон: {self.target_freq:.1f} Гц)")
            
            # Уведомляем UI об обновлении частоты
            if hasattr(self, 'on_frequency_updated'):
                self.on_frequency_updated(initial_freq)
        else:
            # Мелодический режим
            # Создаём движок для интервала
            if self.interval_engine is None:
                print("   🔧 СОЗДАЕМ interval_engine для мелодического")
                self.interval_engine = SoundEngine()
                print("   ✅ interval_engine создан")
            
            # Останавливаем предыдущий звук интервала
            self.interval_engine.stop()
            
            # Генерируем случайную начальную частоту для мелодического режима
            start_range = self.settings.start_range  # Диапазон старта в центах
            
            # Рассчитываем границы для случайной частоты
            start_min = self.target_freq * (2 ** (-start_range / 1200))
            start_max = self.target_freq * (2 ** (start_range / 1200))
            
            # Ограничиваем глобальными границами (100-3500 Гц)
            start_min = max(start_min, 100.0)
            start_max = min(start_max, 3500.0)
            
            # Генерируем случайную частоту
            import random
            initial_freq = random.uniform(start_min, start_max)
            
            # Сохраняем начальную частоту
            if self.current_task:
                self.current_task["current_freq"] = initial_freq
            
            print(f"   🎲 Случайная частота: {initial_freq:.1f} Гц (диапазон: {start_min:.1f}-{start_max:.1f} Гц)")
            
            # Настраиваем и запускаем интервал
            self.interval_engine.set_frequency(initial_freq)
            self.interval_engine.set_volume(self.interval_start_volume_float)
            self.interval_engine.timbre = Timbre(self.timbre_name)
            self.interval_engine.start()
            self.is_playing = True
            print(f"   🎵 МЕЛОДИЧЕСКИЙ РЕЖИМ: звучит только интервал {initial_freq:.1f} Гц (эталон: {self.target_freq:.1f} Гц)")
    
    def update_interval_frequency(self, freq: float):
        """
        Обновление частоты интервала в реальном времени.
        Используется во время настройки.
        """
        print(f"   🔄 update_interval_frequency: {freq:.1f} Гц")
        
        # Для гармонического режима обновляем интервал
        if self.is_harmonic_mode and self.interval_engine:
            self.interval_engine.set_frequency(freq)
            if self.current_task:
                # Обновляем ТОЛЬКО текущую частоту, эталон не трогаем!
                self.current_task["current_freq"] = freq
            print(f"   ✅ interval_engine обновлен (гармонический): {freq:.1f} Гц (эталон: {self.target_freq:.1f} Гц)")
        # Для мелодического режима обновляем интервал
        elif self.interval_engine and self.is_playing:
            self.interval_engine.set_frequency(freq)
            if self.current_task:
                self.current_task["current_freq"] = freq
            print(f"   ✅ interval_engine обновлен (мелодический): {freq:.1f} Гц")
        else:
            print(f"   ⚠️ Не удалось обновить частоту: is_harmonic_mode={self.is_harmonic_mode}, interval_engine={self.interval_engine is not None}")
    
    def stop_adjustment(self):
        """Остановка настройки (выключение звука)"""
        self._stop_harmonic_tonic()
        self.stop_sound()
    # 🏷️ КОНЕЦ_БЛОКА: PUBLIC_PLAYBACK
    
    def play_etalon(self, callback=None):
        """Воспроизведение эталонного интервала"""
        return self.play_interval_full(callback)
    
    def stop_sound(self):
        """Остановка звука"""
        print("🔍 stop_sound: ВЫЗВАН")
        
        self._stop_harmonic_tonic()
        if self.sound_engine:
            self.sound_engine.stop()
        if self.interval_engine:
            self.interval_engine.stop()
        if self.tonic_engine:
            self.tonic_engine.stop()
        self.is_playing = False
        
        if self.interval_timer:
            self.interval_timer.cancel()
            self.interval_timer = None
        if self.tonic_timer:
            self.tonic_timer.cancel()
            self.tonic_timer = None
        
        print("   ✅ Звук остановлен")
    
    def check_answer(self, user_freq: float) -> dict:
        """Проверка ответа пользователя"""
        if not self.current_task:
            return None
        
        target_freq = self.current_task["interval_freq"]
        
        if user_freq > 0 and target_freq > 0:
            deviation = 1200 * np.log2(user_freq / target_freq)
        else:
            deviation = 9999
        
        is_correct = abs(deviation) <= 10
        
        if is_correct:
            self.correct_count += 1
        else:
            self.wrong_count += 1
        
        self.total_deviation += abs(deviation)
        self.deviation_count += 1
        
        self.current_task["user_freq"] = user_freq
        self.current_task["deviation"] = deviation
        self.current_task["is_correct"] = is_correct
        self.current_task["completed"] = True
        
        # Сохраняем параметры для статистики
        interval_name = self.current_task["interval_name"]
        cents = self.current_task["cents"]
        mode = self.current_task["mode"]
        direction = self.current_task["direction"]
        
        # Записываем в статистику
        stats_manager.record_attempt(
            interval_name=interval_name,
            deviation=deviation,
            size_cents=cents,
            mode=mode,
            direction=direction,
            tuning=self.settings.tuning,
            is_correct=is_correct
        )
        
        return {
            "correct": is_correct,
            "deviation": deviation,
            "target_freq": target_freq,
            "user_freq": user_freq,
            "score": 10 if is_correct else 0,
            "message": f"Отклонение: {deviation:.1f} центов"
        }
    
    def get_average_deviation(self) -> float:
        """Получение среднего отклонения"""
        if self.deviation_count == 0:
            return 0.0
        return self.total_deviation / self.deviation_count
    
    def get_progress(self) -> dict:
        """Получение прогресса"""
        total_attempts = self.correct_count + self.wrong_count
        return {
            "correct": self.correct_count,
            "wrong": self.wrong_count,
            "accuracy": (self.correct_count / total_attempts * 100) if total_attempts > 0 else 0
        }
    
    
    def get_current_frequency(self) -> float:
        """
        Получение текущей частоты из движка.
        Для гармонического режима - частота интервала.
        Для мелодического - частота основного движка.
        """
        if self.is_harmonic_mode and self.interval_engine:
            return self.interval_engine.current_frequency
        elif self.interval_engine:
            return self.interval_engine.current_frequency
        elif self.sound_engine:
            return self.sound_engine.current_frequency
        else:
            return 0.0

    def get_sine_data(self):
        """
        Получение данных для осциллографа.
        Для гармонического режима - данные интервала.
        Для мелодического - данные основного движка.
        """
        if self.is_harmonic_mode and self.interval_engine:
            return self.interval_engine.get_sine_data()
        elif self.interval_engine:
            return self.interval_engine.get_sine_data()
        elif self.sound_engine:
            return self.sound_engine.get_sine_data()
        else:
            return np.zeros(1000)

    def _print_state(self):
        """Диагностика состояния движков"""
        print(f"   📊 Состояние:")
        print(f"      is_harmonic_mode: {self.is_harmonic_mode}")
        print(f"      is_playing: {self.is_playing}")
        print(f"      sound_engine: {self.sound_engine is not None}")
        if self.sound_engine:
            print(f"         sound_engine freq: {self.sound_engine.current_frequency:.1f} Гц")
        print(f"      tonic_engine: {self.tonic_engine is not None}")
        if self.tonic_engine:
            print(f"         tonic_engine freq: {self.tonic_engine.current_frequency:.1f} Гц")
        print(f"      interval_engine: {self.interval_engine is not None}")
        if self.interval_engine:
            print(f"         interval_engine freq: {self.interval_engine.current_frequency:.1f} Гц")

    def close(self):
        """Закрытие движка"""
        print("🔍 close: ВЫЗВАН")
        
        # Завершаем сессию статистики
        stats_manager.end_session()
        
        self.stop_sound()
        if self.sound_engine:
            self.sound_engine.full_stop()
            self.sound_engine = None
        if self.tonic_engine:
            self.tonic_engine.full_stop()
            self.tonic_engine = None
        if self.interval_engine:
            self.interval_engine.full_stop()
            self.interval_engine = None
        self.is_active = False
        print("🔇 ExerciseEngine закрыт")
# 🏷️ КОНЕЦ_БЛОКА: EXERCISEENGINE