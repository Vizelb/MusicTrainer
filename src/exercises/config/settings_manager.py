"""
SETTINGS MANAGER - Управление сохранением настроек
"""

import json
from pathlib import Path
from .settings import ExerciseSettings


class SettingsManager:
    """Менеджер сохранения и загрузки настроек"""
    
    def __init__(self, settings_file="exercise_settings.json"):
        self.settings_file = Path(settings_file)
        self.default_settings = ExerciseSettings()
    
    def save(self, settings: ExerciseSettings):
        """Сохранение настроек в файл"""
        try:
            data = settings.to_dict()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"   💾 Настройки сохранены: {self.settings_file}")
            return True
        except Exception as e:
            print(f"⚠️ Ошибка сохранения настроек: {e}")
            return False
    
    def load(self) -> ExerciseSettings:
        """Загрузка настроек из файла"""
        settings = ExerciseSettings()
        
        if not self.settings_file.exists():
            print(f"   ℹ️ Файл настроек не найден, используются значения по умолчанию")
            return settings
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            settings.from_dict(data)
            print(f"   ✅ Настройки загружены: {self.settings_file}")
        except Exception as e:
            print(f"⚠️ Ошибка загрузки настроек: {e}")
        
        return settings
    
    def reset_to_default(self) -> ExerciseSettings:
        """Сброс к настройкам по умолчанию"""
        settings = ExerciseSettings()
        self.save(settings)
        return settings