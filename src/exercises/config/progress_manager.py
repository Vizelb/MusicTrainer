"""
PROGRESS MANAGER - Управление сохранением прогресса упражнений
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class ProgressManager:
    """Менеджер сохранения и загрузки прогресса"""
    
    def __init__(self, progress_file="exercise_progress.json"):
        self.progress_file = Path(progress_file)
        self.progress_data = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Загрузка прогресса из файла"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Ошибка загрузки прогресса: {e}")
                return self._get_default()
        return self._get_default()
    
    def _get_default(self) -> Dict[str, Any]:
        """Получение прогресса по умолчанию"""
        return {
            "current_task": 0,
            "total_tasks": 10,
            "correct": 0,
            "wrong": 0,
            "total_deviation": 0.0,
            "deviation_count": 0,
            "task_history": [],
            "last_updated": datetime.now().isoformat(),
            "is_active": False
        }
    
    def save(self):
        """Сохранение прогресса в файл"""
        self.progress_data["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(self.progress_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️ Ошибка сохранения прогресса: {e}")
            return False
    
    def update_from_engine(self, engine):
        """Обновление прогресса из движка упражнений"""
        if not engine:
            return
        
        progress = engine.get_progress()
        self.progress_data["current_task"] = progress["current"]
        self.progress_data["total_tasks"] = progress["total"]
        self.progress_data["correct"] = progress["correct"]
        self.progress_data["wrong"] = progress["wrong"]
        self.progress_data["is_active"] = engine.is_active
        
        # Сохраняем отклонения
        if hasattr(engine, 'total_deviation') and hasattr(engine, 'deviation_count'):
            self.progress_data["total_deviation"] = engine.total_deviation
            self.progress_data["deviation_count"] = engine.deviation_count
        
        # Добавляем историю если есть текущее задание
        if engine.current_task and engine.current_task.get("completed"):
            task = engine.current_task
            self.progress_data["task_history"].append({
                "interval": task.get("interval_name", ""),
                "direction": task.get("direction", ""),
                "mode": task.get("mode", ""),
                "deviation": task.get("deviation", 0),
                "is_correct": task.get("is_correct", False),
                "timestamp": datetime.now().isoformat()
            })
        
        self.save()
    
    def get_summary(self) -> Dict[str, Any]:
        """Получение сводки прогресса"""
        total = self.progress_data["correct"] + self.progress_data["wrong"]
        accuracy = (self.progress_data["correct"] / total * 100) if total > 0 else 0
        
        avg_deviation = 0
        if self.progress_data["deviation_count"] > 0:
            avg_deviation = self.progress_data["total_deviation"] / self.progress_data["deviation_count"]
        
        return {
            "current": self.progress_data["current_task"],
            "total": self.progress_data["total_tasks"],
            "correct": self.progress_data["correct"],
            "wrong": self.progress_data["wrong"],
            "accuracy": accuracy,
            "avg_deviation": avg_deviation,
            "is_active": self.progress_data["is_active"],
            "last_updated": self.progress_data["last_updated"]
        }
    
    def reset(self):
        """Сброс прогресса"""
        self.progress_data = self._get_default()
        self.save()
    
    def get_task_history(self, limit=10) -> list:
        """Получение истории заданий"""
        history = self.progress_data.get("task_history", [])
        return history[-limit:] if history else []
