"""
AUDIO MIXER - Умное микширование звуковых движков
"""

import math
from typing import List, Optional
from threading import Lock


class AudioMixer:
    """
    Централизованный микшер для всех звуковых движков.
    
    Особенности:
    - Пропорциональное уменьшение при перегрузке
    - Защита от клиппинга
    - Поддержка любого количества движков
    - Автоматическое обновление при добавлении/удалении
    - Синглтон — один экземпляр на всё приложение
    """
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        """Синглтон — один микшер на всё приложение"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._engines = []  # Все зарегистрированные движки
        self._active_engines = []  # Только активные
        self._master_volume = 0.9  # Глобальный лимитер (страховка)
        self._mix_mode = "sum"  # "sum", "rms", "peak", "adaptive"
        
        print("🎛️ AudioMixer инициализирован")
        print(f"   Режим: {self._mix_mode}")
        print(f"   Лимитер: {self._master_volume * 100:.0f}%")
    
    # ============================================
    # УПРАВЛЕНИЕ ДВИЖКАМИ
    # ============================================
    
    def register_engine(self, engine):
        """
        Регистрация звукового движка в микшере.
        
        Args:
            engine: SoundEngine или его наследник
        """
        if engine not in self._engines:
            self._engines.append(engine)
            print(f"   🔌 Движок зарегистрирован: {engine.__class__.__name__}")
            self._update_active()
    
    def unregister_engine(self, engine):
        """Удаление движка из микшера"""
        if engine in self._engines:
            self._engines.remove(engine)
            print(f"   🔌 Движок удалён: {engine.__class__.__name__}")
            self._update_active()
    
    def _update_active(self):
        """Обновление списка активных движков"""
        self._active_engines = [
            e for e in self._engines 
            if hasattr(e, 'is_playing') and e.is_playing
        ]
    
    # ============================================
    # ОСНОВНАЯ ЛОГИКА МИКШИРОВАНИЯ
    # ============================================
    
    def apply_mix(self):
        """
        Применение умного микширования ко всем активным движкам.
        Вызывается при изменении громкости или состояния.
        """
        self._update_active()
        
        if len(self._active_engines) == 0:
            return
        
        # Собираем целевые громкости
        volumes = []
        for engine in self._active_engines:
            if hasattr(engine, '_volume'):
                volumes.append(engine._volume)
            else:
                volumes.append(0.5)
        
        # Применяем микширование
        if len(volumes) == 1:
            # Один движок — просто применяем громкость с лимитером
            self._apply_single(volumes[0])
        else:
            # Несколько движков — умное суммирование
            if self._mix_mode == "sum":
                self._apply_mix_sum(volumes)
            elif self._mix_mode == "rms":
                self._apply_mix_rms(volumes)
            elif self._mix_mode == "peak":
                self._apply_mix_peak(volumes)
            elif self._mix_mode == "adaptive":
                self._apply_mix_adaptive(volumes)
            else:
                self._apply_mix_sum(volumes)  # fallback
    
    def _apply_single(self, volume):
        """Применение громкости для одного движка"""
        engine = self._active_engines[0]
        if hasattr(engine, '_vol_target'):
            engine._vol_target = min(volume, self._master_volume)
    
    def _apply_mix_sum(self, volumes):
        """
        Суммарное микширование — пропорциональное уменьшение при перегрузке.
        Формула: если sum(v) > 1.0, уменьшаем все сигналы пропорционально.
        Это самый простой и надёжный способ.
        """
        total = sum(volumes)
        
        if total > 1.0:
            # Пропорциональное уменьшение всех сигналов
            scale = 1.0 / total
            # Дополнительно ограничиваем мастер-лимитером
            scale = min(scale, self._master_volume)
        else:
            scale = self._master_volume
        
        for i, engine in enumerate(self._active_engines):
            if hasattr(engine, '_vol_target'):
                scaled_vol = volumes[i] * scale
                engine._vol_target = min(scaled_vol, self._master_volume)
    
    def _apply_mix_rms(self, volumes):
        """
        RMS-микширование для нескольких движков.
        Формула: combined = sqrt(sum(v²))
        """
        total_power = math.sqrt(sum(v**2 for v in volumes))
        
        if total_power > 1.0:
            scale = 1.0 / total_power
            scale = min(scale, self._master_volume)
        else:
            scale = self._master_volume
        
        for i, engine in enumerate(self._active_engines):
            if hasattr(engine, '_vol_target'):
                scaled_vol = volumes[i] * scale
                engine._vol_target = min(scaled_vol, self._master_volume)
    
    def _apply_mix_peak(self, volumes):
        """
        Пиковое микширование (максимальное значение).
        Формула: combined = max(v)
        """
        max_vol = max(volumes)
        limited_vol = min(max_vol, self._master_volume)
        for engine in self._active_engines:
            if hasattr(engine, '_vol_target'):
                engine._vol_target = limited_vol
    
    def _apply_mix_adaptive(self, volumes):
        """
        Адаптивное микширование — комбинация суммарного и RMS.
        """
        total = sum(volumes)
        rms = math.sqrt(sum(v**2 for v in volumes)) / math.sqrt(len(volumes))
        
        # Используем суммарный подход как основной
        if total > 1.0:
            scale = 1.0 / total
        else:
            scale = 1.0
        
        # Смешиваем с RMS для плавности
        rms_scale = 1.0 / rms if rms > 1.0 else 1.0
        scale = min(scale, rms_scale, self._master_volume)
        
        for i, engine in enumerate(self._active_engines):
            if hasattr(engine, '_vol_target'):
                scaled_vol = volumes[i] * scale
                engine._vol_target = min(scaled_vol, self._master_volume)
    
    # ============================================
    # УПРАВЛЕНИЕ МАСТЕР-ЛИМИТЕРОМ
    # ============================================
    
    def set_master_volume(self, volume: float):
        """
        Установка мастер-громкости (лимитера).
        
        Args:
            volume: float от 0 до 1.0 (0.9 = 90%)
        """
        self._master_volume = max(0, min(1.0, volume))
        print(f"   🎛️ Мастер-громкость: {self._master_volume * 100:.0f}%")
        self.apply_mix()
    
    def set_mix_mode(self, mode: str):
        """
        Установка режима микширования.
        
        Args:
            mode: "sum", "rms", "peak", "adaptive"
        """
        if mode in ["sum", "rms", "peak", "adaptive"]:
            self._mix_mode = mode
            print(f"   🔄 Режим микширования: {mode}")
            self.apply_mix()
        else:
            print(f"   ⚠️ Неизвестный режим: {mode}. Доступны: sum, rms, peak, adaptive")
    
    # ============================================
    # ДИАГНОСТИКА
    # ============================================
    
    def get_state(self) -> dict:
        """Получение состояния микшера"""
        self._update_active()
        return {
            "engines_total": len(self._engines),
            "engines_active": len(self._active_engines),
            "master_volume": self._master_volume,
            "mix_mode": self._mix_mode,
            "active_volumes": [
                e._volume if hasattr(e, '_volume') else 0.5 
                for e in self._active_engines
            ]
        }
    
    def get_diagnostics(self) -> str:
        """Получение диагностической информации"""
        state = self.get_state()
        lines = [
            "=" * 40,
            "🎛️ AUDIO MIXER DIAGNOSTICS",
            "=" * 40,
            f"  Движков всего: {state['engines_total']}",
            f"  Движков активно: {state['engines_active']}",
            f"  Мастер-громкость: {state['master_volume'] * 100:.0f}%",
            f"  Режим: {state['mix_mode']}",
            f"  Активные громкости: {[round(v, 2) for v in state['active_volumes']]}",
            "=" * 40,
        ]
        return "\n".join(lines)


# Глобальный экземпляр для простого доступа
mixer = AudioMixer()