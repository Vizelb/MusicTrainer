"""
STATISTICS - Сбор и хранение статистики упражнений
Поддерживает непрерывный режим и запись после каждой попытки
"""

import json
import re
import os
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple


class StatisticsManager:
    """
    Управление статистикой упражнений.
    
    Особенности:
    - Непрерывный сбор данных (без ограничения на количество заданий)
    - Запись после каждой попытки
    - Глобальная статистика по интервалам
    - Текущая сессия в памяти
    - Фильтрация данных для анализа
    """
    
    # Карта нормализации имён интервалов
    INTERVAL_NAME_MAP = {
        "малая терция": "малая_терция",
        "большая терция": "большая_терция",
        "чистая кварта": "чистая_кварта",
        "чистая квинта": "чистая_квинта",
        "малая секста": "малая_секста",
        "большая секста": "большая_секста",
        "малая септима": "малая_септима",
        "большая септима": "большая_септима",
        "малая секунда": "малая_секунда",
        "большая секунда": "большая_секунда",
        "увеличенная кварта": "тритон",
        "уменьшенная квинта": "тритон"
    }
    
    def __init__(self, stats_file: str = "statistics.json"):
        """
        Инициализация менеджера статистики.
        
        Args:
            stats_file: путь к файлу для хранения статистики
        """
        self.stats_file = stats_file
        
        # СОЗДАЁМ ДИРЕКТОРИЮ ДЛЯ ФАЙЛА
        stats_dir = os.path.dirname(stats_file)
        if stats_dir and not os.path.exists(stats_dir):
            os.makedirs(stats_dir, exist_ok=True)
            print(f"   📁 Создана директория: {stats_dir}")
        
        self.data = self._load()
        
        # Текущая сессия (в памяти)
        self._reset_session()
        
        # Кэш для быстрых вычислений
        self._cache = {}
        
        # Счётчик записей для отладки
        self._save_counter = 0
        
        print(f"📊 StatisticsManager инициализирован")
        print(f"   Файл: {stats_file}")
        print(f"   Интервалов в статистике: {len(self.data)}")
    
    # ============================================
    # ЗАГРУЗКА / СОХРАНЕНИЕ
    # ============================================
    
    def _normalize_interval_name(self, name: str) -> str:
        """Нормализация имени интервала для использования как ключа"""
        if not name:
            return "unknown"
        
        # Очищаем от лишних пробелов
        name = name.strip().lower()
        
        # Проверяем маппинг
        if name in self.INTERVAL_NAME_MAP:
            return self.INTERVAL_NAME_MAP[name]
        
        # Заменяем пробелы на подчёркивания
        name = re.sub(r'\s+', '_', name)
        
        # Удаляем недопустимые символы
        name = re.sub(r'[^a-zA-Zа-яА-Я0-9_]', '', name)
        
        return name
    
    def _load(self) -> Dict:
        """Загрузка статистики из файла с улучшенной обработкой ошибок"""
        if not os.path.exists(self.stats_file):
            print(f"   📄 Файл статистики не найден, создаём новый")
            return {}
        
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Проверка на пустой файл
                if not content or not content.strip():
                    print(f"   ⚠️ Файл пуст, создаём новый")
                    return {}
                
                # Парсим JSON
                data = json.loads(content)
                
                # Проверка структуры
                if not isinstance(data, dict):
                    print(f"   ⚠️ Неверный формат данных (ожидался dict), создаём новый")
                    return {}
                
                # Проверка и нормализация данных
                normalized_data = {}
                for key, value in data.items():
                    # Пропускаем метаданные если есть
                    if key.startswith('_'):
                        continue
                    
                    # Проверяем структуру интервала
                    if isinstance(value, dict) and "history" in value:
                        # Убеждаемся, что history это список
                        if not isinstance(value["history"], list):
                            value["history"] = []
                        
                        # Нормализуем каждую запись
                        normalized_history = []
                        for record in value["history"]:
                            if isinstance(record, dict):
                                # Проверяем обязательные поля
                                normalized_record = {
                                    "deviation": float(record.get("deviation", 0)),
                                    "abs_deviation": float(record.get("abs_deviation", 0)),
                                    "timestamp": record.get("timestamp", datetime.now().isoformat()),
                                    "mode": record.get("mode", "harmonic"),
                                    "direction": record.get("direction", "up"),
                                    "tuning": record.get("tuning", "natural"),
                                    "is_correct": record.get("is_correct", None)
                                }
                                normalized_history.append(normalized_record)
                        
                        value["history"] = normalized_history
                        value["total_attempts"] = len(normalized_history)
                        
                        # Убеждаемся, что size_cents есть
                        if "size_cents" not in value:
                            value["size_cents"] = 0
                        
                        normalized_data[key] = value
                    elif isinstance(value, list):
                        # Если это просто список, конвертируем в правильную структуру
                        normalized_data[key] = {
                            "size_cents": 0,
                            "history": [],
                            "total_attempts": 0
                        }
                        for record in value:
                            if isinstance(record, dict):
                                normalized_record = {
                                    "deviation": float(record.get("deviation", 0)),
                                    "abs_deviation": float(record.get("abs_deviation", 0)),
                                    "timestamp": record.get("timestamp", datetime.now().isoformat()),
                                    "mode": record.get("mode", "harmonic"),
                                    "direction": record.get("direction", "up"),
                                    "tuning": record.get("tuning", "natural"),
                                    "is_correct": record.get("is_correct", None)
                                }
                                normalized_data[key]["history"].append(normalized_record)
                        normalized_data[key]["total_attempts"] = len(normalized_data[key]["history"])
                
                print(f"   ✅ Загружено {len(normalized_data)} интервалов")
                return normalized_data
                
        except json.JSONDecodeError as e:
            print(f"   ❌ Ошибка парсинга JSON: {e}")
            # Создаём резервную копию повреждённого файла
            self._backup_corrupted_file()
            return {}
            
        except Exception as e:
            print(f"   ❌ Ошибка загрузки: {e}")
            import traceback
            traceback.print_exc()
            return {}
    
    def _backup_corrupted_file(self):
        """Создание бэкапа повреждённого файла"""
        try:
            if os.path.exists(self.stats_file):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_file = f"{self.stats_file}.corrupted_{timestamp}"
                os.rename(self.stats_file, backup_file)
                print(f"   💾 Повреждённый файл сохранён как: {backup_file}")
        except Exception as e:
            print(f"   ⚠️ Не удалось сохранить повреждённый файл: {e}")
    
    def _save(self) -> bool:
        """
        Сохранение статистики в файл с атомарной записью
        
        Returns:
            bool: True если сохранение успешно
        """
        self._save_counter += 1
        
        try:
            # Проверяем данные перед сохранением
            if not isinstance(self.data, dict):
                print(f"   ❌ Ошибка: данные не являются словарём")
                return False
            
            # УБЕЖДАЕМСЯ, ЧТО ДИРЕКТОРИЯ СУЩЕСТВУЕТ
            stats_dir = os.path.dirname(self.stats_file)
            if stats_dir and not os.path.exists(stats_dir):
                os.makedirs(stats_dir, exist_ok=True)
                print(f"   📁 Создана директория: {stats_dir}")
            
            # Создаём временный файл
            temp_file = f"{self.stats_file}.tmp"
            
            # Сериализуем с проверкой
            try:
                json_string = json.dumps(
                    self.data, 
                    indent=2, 
                    ensure_ascii=False,
                    default=str
                )
            except Exception as e:
                print(f"   ❌ Ошибка сериализации: {e}")
                return False
            
            # Проверяем, что получилась валидная строка
            if not json_string or len(json_string) < 10:
                print(f"   ⚠️ Предупреждение: слишком маленький JSON")
            
            # Записываем во временный файл
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(json_string)
                f.flush()
                os.fsync(f.fileno())
            
            # Проверяем, что временный файл создан
            if not os.path.exists(temp_file) or os.path.getsize(temp_file) == 0:
                print(f"   ❌ Ошибка: временный файл не создан или пуст")
                return False
            
            # Переименовываем (атомарная операция)
            if os.path.exists(self.stats_file):
                # Создаём бэкап
                backup_file = f"{self.stats_file}.bak"
                try:
                    os.rename(self.stats_file, backup_file)
                except:
                    pass
            
            os.rename(temp_file, self.stats_file)
            
            # Проверяем, что файл создан
            if os.path.exists(self.stats_file) and os.path.getsize(self.stats_file) > 0:
                if self._save_counter % 10 == 0:  # Логируем каждые 10 сохранений
                    print(f"   ✅ Статистика сохранена (№{self._save_counter})")
                return True
            else:
                print(f"   ❌ Ошибка: файл не создан или пуст после сохранения")
                return False
            
        except Exception as e:
            print(f"   ❌ Ошибка сохранения: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _reset_session(self):
        """Сброс текущей сессии"""
        self.session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "settings": {},
            "attempts": [],
            "summary": {
                "total": 0,
                "correct": 0,
                "wrong": 0,
                "total_deviation": 0,
                "avg_deviation": 0
            }
        }
    
    # ============================================
    # ЗАПИСЬ ПОПЫТКИ
    # ============================================
    
    def record_attempt(
        self,
        interval_name: str,
        deviation: float,
        size_cents: int,
        mode: str = "melodic",
        direction: str = "up",
        tuning: str = "natural",
        is_correct: bool = None
    ) -> Dict:
        """
        Запись попытки в статистику с улучшенной обработкой.
        
        Args:
            interval_name: название интервала
            deviation: отклонение в центах (со знаком)
            size_cents: размер интервала в центах
            mode: "melodic" или "harmonic"
            direction: "up" или "down"
            tuning: "natural" или "equal"
            is_correct: правильный ли ответ (опционально)
        
        Returns:
            Dict: запись о попытке
        """
        try:
            timestamp = datetime.now().isoformat()
            abs_deviation = abs(deviation)
            
            # Нормализуем имя интервала
            normalized_name = self._normalize_interval_name(interval_name)
            
            # Если имя изменилось, логируем
            if normalized_name != interval_name:
                print(f"   ℹ️ Нормализация имени: '{interval_name}' -> '{normalized_name}'")
            
            # ===== 1. Глобальная статистика =====
            if normalized_name not in self.data:
                self.data[normalized_name] = {
                    "size_cents": size_cents,
                    "history": [],
                    "total_attempts": 0,
                    "last_updated": timestamp
                }
            
            entry = {
                "deviation": float(deviation),
                "abs_deviation": float(abs_deviation),
                "timestamp": str(timestamp),
                "mode": str(mode),
                "direction": str(direction),
                "tuning": str(tuning),
                "is_correct": bool(is_correct) if is_correct is not None else None
            }
            
            self.data[normalized_name]["history"].append(entry)
            self.data[normalized_name]["total_attempts"] = len(self.data[normalized_name]["history"])
            self.data[normalized_name]["last_updated"] = timestamp
            
            # Ограничиваем историю (последние 5000 записей)
            if len(self.data[normalized_name]["history"]) > 5000:
                self.data[normalized_name]["history"] = self.data[normalized_name]["history"][-5000:]
            
            # ===== 2. Текущая сессия =====
            self.session["attempts"].append({
                "interval_name": normalized_name,
                "deviation": float(deviation),
                "abs_deviation": float(abs_deviation),
                "timestamp": str(timestamp),
                "is_correct": bool(is_correct) if is_correct is not None else None
            })
            
            # ===== 3. Обновляем сводку сессии =====
            summary = self.session["summary"]
            summary["total"] += 1
            
            if is_correct is not None:
                if is_correct:
                    summary["correct"] += 1
                else:
                    summary["wrong"] += 1
            
            summary["total_deviation"] += deviation
            summary["avg_deviation"] = summary["total_deviation"] / summary["total"]
            
            # ===== 4. Сохраняем (с проверкой) =====
            save_success = self._save()
            
            if not save_success:
                print(f"   ⚠️ Ошибка сохранения после записи попытки!")
                # Пробуем сохранить ещё раз
                print(f"   🔄 Повторная попытка сохранения...")
                save_success = self._save()
                if not save_success:
                    print(f"   ❌ Критическая ошибка: не удалось сохранить данные!")
            
            # ===== 5. Инвалидируем кэш =====
            self._cache = {}
            
            return entry
            
        except Exception as e:
            print(f"   ❌ Ошибка записи попытки: {e}")
            import traceback
            traceback.print_exc()
            
            # Возвращаем частичную запись
            return {
                "deviation": float(deviation),
                "abs_deviation": abs(float(deviation)),
                "timestamp": datetime.now().isoformat(),
                "mode": str(mode),
                "direction": str(direction),
                "tuning": str(tuning),
                "is_correct": is_correct,
                "error": str(e)
            }
    
    # ============================================
    # УПРАВЛЕНИЕ СЕССИЕЙ
    # ============================================
    
    def start_session(self, settings: Dict = None):
        """Начало новой сессии"""
        self._reset_session()
        if settings:
            self.session["settings"] = settings
        print(f"   📊 Новая сессия: {self.session['session_id']}")
        return self.session["session_id"]  # ВОЗВРАЩАЕМ ID
    
    def end_session(self) -> Dict:
        """Завершение текущей сессии"""
        if not self.session["attempts"]:
            return self.session
        
        self.session["end_time"] = datetime.now().isoformat()
        
        # Сохраняем сессию в отдельный файл
        self._save_session()
        
        print(f"   📊 Сессия завершена: {self.session['session_id']}")
        if self.session["summary"]["total"] > 0:
            accuracy = self.session["summary"]["correct"] / self.session["summary"]["total"] * 100
            print(f"      Попыток: {self.session['summary']['total']}")
            print(f"      Точность: {accuracy:.1f}%")
        
        return self.session
    
    def _save_session(self):
        """Сохранение сессии в отдельный файл"""
        if not self.session["attempts"]:
            return
        
        session_dir = "data/sessions"
        # СОЗДАЁМ ДИРЕКТОРИЮ ДЛЯ СЕССИЙ
        if not os.path.exists(session_dir):
            os.makedirs(session_dir, exist_ok=True)
        
        session_file = f"{session_dir}/{self.session['session_id']}.json"
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(self.session, f, indent=2, ensure_ascii=False, default=str)
            print(f"   💾 Сессия сохранена: {session_file}")
        except Exception as e:
            print(f"   ⚠️ Ошибка сохранения сессии: {e}")
    
    def get_session_summary(self) -> Dict:
        """Получение сводки текущей сессии"""
        return self.session["summary"]
    
    def get_session_attempts(self) -> List:
        """Получение всех попыток текущей сессии"""
        return self.session["attempts"]
    
    def get_session_duration(self) -> float:
        """Получение длительности сессии в минутах"""
        if not self.session["start_time"]:
            return 0
        
        start = datetime.fromisoformat(self.session["start_time"])
        end = datetime.now()
        if self.session["end_time"]:
            end = datetime.fromisoformat(self.session["end_time"])
        
        return (end - start).total_seconds() / 60
    
    # ============================================
    # ПОЛУЧЕНИЕ СТАТИСТИКИ
    # ============================================
    
    def get_stats(
        self,
        interval_name: str,
        filters: Dict = None
    ) -> Dict:
        """
        Получение статистики по интервалу с фильтрацией.
        
        Args:
            interval_name: название интервала
            filters: фильтры для данных
                - mode: "melodic" | "harmonic" | "all"
                - direction: "up" | "down" | "all"
                - tuning: "natural" | "equal" | "all"
                - period: "week" | "month" | "year" | "all"
                - attempts: число (последние N попыток) или 0
        
        Returns:
            Dict: статистика по интервалу
        """
        if interval_name not in self.data:
            return {
                "interval_name": interval_name,
                "size_cents": 0,
                "history": [],
                "total_attempts": 0,
                "summary": {},
                "bias": {},
                "trend": {}
            }
        
        history = self.data[interval_name]["history"]
        
        # Применяем фильтры
        if filters:
            history = self._filter_history(history, filters)
        
        if not history:
            return {
                "interval_name": interval_name,
                "size_cents": self.data[interval_name]["size_cents"],
                "history": [],
                "total_attempts": 0,
                "summary": {},
                "bias": {},
                "trend": {}
            }
        
        deviations = [h["deviation"] for h in history]
        
        return {
            "interval_name": interval_name,
            "size_cents": self.data[interval_name]["size_cents"],
            "history": history,
            "total_attempts": len(history),
            "summary": self._calculate_summary(deviations),
            "bias": self._calculate_bias(deviations),
            "trend": self._calculate_trend(deviations)
        }
    
    def _filter_history(self, history: List, filters: Dict) -> List:
        """Фильтрация истории по критериям"""
        filtered = history.copy()
        
        if filters.get("mode") and filters["mode"] != "all":
            filtered = [h for h in filtered if h.get("mode") == filters["mode"]]
        
        if filters.get("direction") and filters["direction"] != "all":
            filtered = [h for h in filtered if h.get("direction") == filters["direction"]]
        
        if filters.get("tuning") and filters["tuning"] != "all":
            filtered = [h for h in filtered if h.get("tuning") == filters["tuning"]]
        
        if filters.get("period") and filters["period"] != "all":
            now = datetime.now()
            cutoff = {
                "week": now - timedelta(days=7),
                "month": now - timedelta(days=30),
                "year": now - timedelta(days=365)
            }.get(filters["period"])
            
            if cutoff:
                filtered = [
                    h for h in filtered 
                    if datetime.fromisoformat(h["timestamp"]) >= cutoff
                ]
        
        if filters.get("attempts", 0) > 0:
            filtered = filtered[-filters["attempts"]:]
        
        return filtered
    
    # ============================================
    # РАСЧЁТ СТАТИСТИКИ
    # ============================================
    
    def _calculate_summary(self, deviations: List[float]) -> Dict:
        """Расчёт сводной статистики"""
        n = len(deviations)
        if n == 0:
            return {
                "count": 0,
                "mean": 0,
                "mean_abs": 0,
                "median": 0,
                "std": 0,
                "min": 0,
                "max": 0
            }
        
        mean = sum(deviations) / n
        mean_abs = sum(abs(d) for d in deviations) / n
        sorted_d = sorted(deviations)
        median = sorted_d[n//2] if n > 0 else 0
        std = math.sqrt(sum((d - mean) ** 2 for d in deviations) / n) if n > 1 else 0
        
        return {
            "count": n,
            "mean": mean,
            "mean_abs": mean_abs,
            "median": median,
            "std": std,
            "min": min(deviations) if n > 0 else 0,
            "max": max(deviations) if n > 0 else 0
        }
    
    def _calculate_bias(self, deviations: List[float]) -> Dict:
        """Расчёт систематической ошибки (Bias)"""
        n = len(deviations)
        if n == 0:
            return {}
        
        mean = sum(deviations) / n
        over = len([d for d in deviations if d > 5])
        under = len([d for d in deviations if d < -5])
        neutral = len([d for d in deviations if -5 <= d <= 5])
        
        return {
            "mean": mean,
            "over_count": over,
            "under_count": under,
            "neutral_count": neutral,
            "over_ratio": over / n if n > 0 else 0,
            "under_ratio": under / n if n > 0 else 0
        }
    
    def _calculate_trend(self, deviations: List[float]) -> Dict:
        """Расчёт тренда (линейная регрессия)"""
        n = len(deviations)
        if n < 3:
            return {"slope": 0, "intercept": 0, "r_squared": 0}
        
        x = list(range(n))
        sum_x = sum(x)
        sum_y = sum(deviations)
        sum_xy = sum(x[i] * deviations[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2) if n > 1 else 0
        intercept = (sum_y - slope * sum_x) / n
        
        mean_y = sum_y / n
        ss_total = sum((d - mean_y) ** 2 for d in deviations)
        ss_residual = sum((deviations[i] - (slope * x[i] + intercept)) ** 2 for i in range(n))
        r_squared = 1 - (ss_residual / ss_total) if ss_total > 0 else 0
        
        return {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared
        }
    
    # ============================================
    # ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ
    # ============================================
    
    def get_all_intervals(self) -> List[str]:
        """Получение списка всех интервалов со статистикой"""
        return list(self.data.keys())
    
    def get_summary_table(self) -> List[Dict]:
        """
        Получение сводной таблицы по всем интервалам.
        Сортировка по количеству попыток (убывание).
        """
        result = []
        for interval_name, data in self.data.items():
            if not data["history"]:
                continue
            
            deviations = [h["deviation"] for h in data["history"]]
            summary = self._calculate_summary(deviations)
            bias = self._calculate_bias(deviations)
            trend = self._calculate_trend(deviations)
            
            result.append({
                "interval_name": interval_name,
                "size_cents": data["size_cents"],
                "attempts": len(deviations),
                "mean": summary["mean"],
                "mean_abs": summary["mean_abs"],
                "median": summary["median"],
                "std": summary["std"],
                "bias_mean": bias.get("mean", 0),
                "trend_slope": trend.get("slope", 0),
                "over_ratio": bias.get("over_ratio", 0),
                "under_ratio": bias.get("under_ratio", 0),
                "last_updated": data.get("last_updated", "")
            })
        
        return sorted(result, key=lambda x: x["attempts"], reverse=True)
    
    def get_total_attempts(self) -> int:
        """Получение общего количества попыток"""
        total = 0
        for data in self.data.values():
            total += data.get("total_attempts", 0)
        return total
    
    def reset(self):
        """Полный сброс статистики (с подтверждением)"""
        self.data = {}
        self._reset_session()
        self._save()
        print("   🔄 Статистика сброшена")
    
    def validate_data(self) -> Dict[str, Any]:
        """
        Проверка целостности данных
        
        Returns:
            Dict: результаты проверки
        """
        result = {
            "is_valid": True,
            "issues": [],
            "stats": {
                "intervals": len(self.data),
                "total_attempts": 0,
                "corrupted_records": 0
            }
        }
        
        for interval_name, interval_data in self.data.items():
            if not isinstance(interval_data, dict):
                result["is_valid"] = False
                result["issues"].append(f"Интервал '{interval_name}' не является словарём")
                continue
            
            if "history" not in interval_data:
                result["is_valid"] = False
                result["issues"].append(f"Интервал '{interval_name}' не имеет поля 'history'")
                continue
            
            if not isinstance(interval_data["history"], list):
                result["is_valid"] = False
                result["issues"].append(f"History для '{interval_name}' не является списком")
                continue
            
            # Проверяем записи
            for i, record in enumerate(interval_data["history"]):
                if not isinstance(record, dict):
                    result["is_valid"] = False
                    result["issues"].append(f"Запись {i} в '{interval_name}' не является словарём")
                    result["stats"]["corrupted_records"] += 1
                    continue
                
                required_fields = ["deviation", "timestamp"]
                for field in required_fields:
                    if field not in record:
                        result["is_valid"] = False
                        result["issues"].append(f"Запись {i} в '{interval_name}' не имеет поля '{field}'")
            
            result["stats"]["total_attempts"] += len(interval_data["history"])
        
        return result
    
    def get_diagnostics(self) -> Dict:
        """Получение диагностической информации"""
        return {
            "stats_file": self.stats_file,
            "intervals": len(self.data),
            "total_attempts": self.get_total_attempts(),
            "session_active": len(self.session["attempts"]) > 0,
            "session_attempts": self.session["summary"]["total"],
            "session_duration": self.get_session_duration(),
            "last_update": datetime.now().isoformat()
        }


# Глобальный экземпляр для использования во всём приложении
# Используем путь в data директории
stats_manager = StatisticsManager("data/statistics.json")