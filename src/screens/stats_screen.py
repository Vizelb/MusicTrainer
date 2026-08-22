"""
stats_screen.py - Экран статистики
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp

from core.statistics import stats_manager
from exercises.ui.stats_widget import StatsGraphWidget


class StatsScreen(Screen):
    """Экран статистики"""
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "stats"
        self._initialized = False
        
        self.current_filters = {
            "interval_name": "all",
            "mode": "all",
            "direction": "all",
            "tuning": "all",
            "period": "all",
            "attempts": 0
        }
        
        # UI строится при первом входе
    
    def on_enter(self):
        print("🔍 StatsScreen: on_enter вызван")
        print(f"🔍 StatsScreen: _initialized = {self._initialized}")
        """Вызывается при переходе на экран"""
        if not self._initialized:
            self._build_ui()
            self._initialized = True
        self._load_data()
    
    def _build_ui(self):
        print("🔍 StatsScreen: _build_ui вызван")
        main_layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(5))
        
        main_layout.add_widget(Label(
            text="📊 СТАТИСТИКА",
            font_size=sp(24),
            size_hint=(1, None),
            height=dp(50),
            color=(0.3, 0.9, 0.3, 1),
            bold=True
        ))
        
        # Фильтры
        filter_layout = BoxLayout(orientation="vertical", size_hint=(1, None), height=dp(180), spacing=dp(5))
        
        # Ряд 1
        row1 = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(35), spacing=dp(10))
        row1.add_widget(Label(text="Интервал:", font_size=sp(14), size_hint=(0.2, 1), color=(0.8, 0.8, 0.8, 1)))
        self.interval_spinner = Spinner(
            text="Все",
            values=self._get_interval_list(),
            size_hint=(0.3, 1),
            font_size=sp(13),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.interval_spinner.bind(text=self.on_filter_change)
        row1.add_widget(self.interval_spinner)
        
        row1.add_widget(Label(text="Режим:", font_size=sp(14), size_hint=(0.2, 1), color=(0.8, 0.8, 0.8, 1)))
        self.mode_spinner = Spinner(
            text="Все",
            values=["Все", "Мелодический", "Гармонический"],
            size_hint=(0.3, 1),
            font_size=sp(13),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.mode_spinner.bind(text=self.on_filter_change)
        row1.add_widget(self.mode_spinner)
        filter_layout.add_widget(row1)
        
        # Ряд 2
        row2 = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(35), spacing=dp(10))
        row2.add_widget(Label(text="Движение:", font_size=sp(14), size_hint=(0.2, 1), color=(0.8, 0.8, 0.8, 1)))
        self.direction_spinner = Spinner(
            text="Все",
            values=["Все", "Вверх", "Вниз"],
            size_hint=(0.3, 1),
            font_size=sp(13),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.direction_spinner.bind(text=self.on_filter_change)
        row2.add_widget(self.direction_spinner)
        
        row2.add_widget(Label(text="Строй:", font_size=sp(14), size_hint=(0.2, 1), color=(0.8, 0.8, 0.8, 1)))
        self.tuning_spinner = Spinner(
            text="Все",
            values=["Все", "Натуральный", "Равномерный"],
            size_hint=(0.3, 1),
            font_size=sp(13),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.tuning_spinner.bind(text=self.on_filter_change)
        row2.add_widget(self.tuning_spinner)
        filter_layout.add_widget(row2)
        
        # Ряд 3
        row3 = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(35), spacing=dp(10))
        row3.add_widget(Label(text="Период:", font_size=sp(14), size_hint=(0.2, 1), color=(0.8, 0.8, 0.8, 1)))
        self.period_spinner = Spinner(
            text="Всё время",
            values=["Всё время", "Неделя", "Месяц", "Год"],
            size_hint=(0.3, 1),
            font_size=sp(13),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.period_spinner.bind(text=self.on_filter_change)
        row3.add_widget(self.period_spinner)
        
        row3.add_widget(Label(text="Попытки:", font_size=sp(14), size_hint=(0.2, 1), color=(0.8, 0.8, 0.8, 1)))
        self.attempts_spinner = Spinner(
            text="Все",
            values=["Все", "10", "20", "30", "50", "100"],
            size_hint=(0.3, 1),
            font_size=sp(13),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.attempts_spinner.bind(text=self.on_filter_change)
        row3.add_widget(self.attempts_spinner)
        filter_layout.add_widget(row3)
        
        main_layout.add_widget(filter_layout)
        
        # График
        self.graph_widget = StatsGraphWidget(size_hint=(1, 0.5))
        main_layout.add_widget(self.graph_widget)
        
        # Статистика
        stats_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(80), spacing=dp(10))
        
        self.stats_labels = {}
        stats_items = [
            ("attempts", "Попыток:"),
            ("mean", "Среднее:"),
            ("mean_abs", "|Bias|:"),
            ("trend", "Тренд:")
        ]
        
        for key, label in stats_items:
            item_layout = BoxLayout(orientation="vertical", size_hint=(0.25, 1))
            item_layout.add_widget(Label(
                text=label,
                font_size=sp(12),
                size_hint=(1, 0.4),
                color=(0.6, 0.6, 0.6, 1),
                halign="center"
            ))
            self.stats_labels[key] = Label(
                text="---",
                font_size=sp(16),
                size_hint=(1, 0.6),
                color=(0.9, 0.9, 0.9, 1),
                halign="center",
                bold=True
            )
            item_layout.add_widget(self.stats_labels[key])
            stats_layout.add_widget(item_layout)
        
        main_layout.add_widget(stats_layout)
        
        # Кнопки
        btn_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(10))
        btn_layout.add_widget(Widget(size_hint=(0.3, 1)))
        
        refresh_btn = Button(
            text="🔄 Обновить",
            font_size=sp(14),
            size_hint=(0.2, 1),
            background_color=(0.2, 0.5, 0.2, 1),
            background_normal=""
        )
        refresh_btn.bind(on_press=self.refresh)
        btn_layout.add_widget(refresh_btn)
        
        back_btn = Button(
            text="◀ НАЗАД",
            font_size=sp(16),
            size_hint=(0.25, 1),
            background_color=(0.3, 0.3, 0.5, 1),
            background_normal=""
        )
        back_btn.bind(on_press=self.go_back)
        btn_layout.add_widget(back_btn)
        
        main_layout.add_widget(btn_layout)
        self.add_widget(main_layout)
        print("🔍 StatsScreen: _build_ui завершён, виджетов:", len(self.children))
    
    def _get_interval_list(self):
        intervals = ["Все"]
        intervals.extend(stats_manager.get_all_intervals())
        return intervals
    
    def on_filter_change(self, spinner, text):
        mode_map = {"Все": "all", "Мелодический": "melodic", "Гармонический": "harmonic"}
        direction_map = {"Все": "all", "Вверх": "up", "Вниз": "down"}
        tuning_map = {"Все": "all", "Натуральный": "natural", "Равномерный": "equal"}
        period_map = {"Всё время": "all", "Неделя": "week", "Месяц": "month", "Год": "year"}
        attempts_map = {"Все": 0, "10": 10, "20": 20, "30": 30, "50": 50, "100": 100}
        
        self.current_filters = {
            "interval_name": "all" if self.interval_spinner.text == "Все" else self.interval_spinner.text,
            "mode": mode_map.get(self.mode_spinner.text, "all"),
            "direction": direction_map.get(self.direction_spinner.text, "all"),
            "tuning": tuning_map.get(self.tuning_spinner.text, "all"),
            "period": period_map.get(self.period_spinner.text, "all"),
            "attempts": attempts_map.get(self.attempts_spinner.text, 0)
        }
        self._load_data()
    
    def _load_data(self):
        print("🔍 StatsScreen: _load_data вызван")
        """Загрузка данных с обработкой ошибок"""
        try:
            interval = self.current_filters["interval_name"]
            
            if interval == "all":
                self._load_all_intervals_summary()
                return
            
            filters = {
                "mode": self.current_filters["mode"],
                "direction": self.current_filters["direction"],
                "tuning": self.current_filters["tuning"],
                "period": self.current_filters["period"],
                "attempts": self.current_filters["attempts"]
            }
            
            data = stats_manager.get_stats(interval, filters)
            
            if not data or not data.get("history"):
                self.graph_widget.update([])
                self._update_stats_labels({})
                return
            
            self.graph_widget.update(data["history"])
            self._update_stats_labels({
                "attempts": data.get("total_attempts", 0),
                "mean": data.get("summary", {}).get("mean", 0),
                "mean_abs": data.get("summary", {}).get("mean_abs", 0),
                "trend": data.get("trend", {}).get("slope", 0)
            })
            
        except Exception as e:
            print(f"   ❌ Ошибка загрузки данных: {e}")
            self.graph_widget.update([])
            self._update_stats_labels({})
    
    def _update_stats_labels(self, stats):
        if not stats:
            for key in self.stats_labels:
                self.stats_labels[key].text = "---"
            return
        
        self.stats_labels["attempts"].text = str(stats.get("attempts", 0))
        
        mean = stats.get("mean", 0)
        self.stats_labels["mean"].text = f"{mean:+.1f} центов"
        self.stats_labels["mean"].color = (0.3, 0.9, 0.3, 1) if abs(mean) <= 5 else (0.9, 0.3, 0.3, 1)
        
        self.stats_labels["mean_abs"].text = f"{stats.get('mean_abs', 0):.1f} центов"
        
        trend = stats.get("trend", 0)
        if trend < -0.1:
            self.stats_labels["trend"].text = "📈 Улучшение"
            self.stats_labels["trend"].color = (0.3, 0.9, 0.3, 1)
        elif trend > 0.1:
            self.stats_labels["trend"].text = "📉 Ухудшение"
            self.stats_labels["trend"].color = (0.9, 0.3, 0.3, 1)
        else:
            self.stats_labels["trend"].text = "➡️ Стабильно"
            self.stats_labels["trend"].color = (0.9, 0.9, 0.3, 1)
    
    def _load_all_intervals_summary(self):
        """Загрузка сводки по всем интервалам"""
        try:
            summary_table = stats_manager.get_summary_table()
            if not summary_table:
                self.graph_widget.update([])
                self._update_stats_labels({})
                return
            
            # Берём интервал с наибольшим количеством попыток
            best = summary_table[0]
            interval_name = best["interval_name"]
            
            # Применяем фильтры
            filters = {
                "mode": self.current_filters["mode"],
                "direction": self.current_filters["direction"],
                "tuning": self.current_filters["tuning"],
                "period": self.current_filters["period"],
                "attempts": self.current_filters["attempts"]
            }
            
            data = stats_manager.get_stats(interval_name, filters)
            
            if data and data.get("history"):
                self.graph_widget.update(data["history"])
                summary = data.get("summary", {})
                trend = data.get("trend", {})
                
                self._update_stats_labels({
                    "attempts": data.get("total_attempts", 0),
                    "mean": summary.get("mean", 0),
                    "mean_abs": summary.get("mean_abs", 0),
                    "trend": trend.get("slope", 0)
                })
            else:
                self.graph_widget.update([])
                self._update_stats_labels({})
                
        except Exception as e:
            print(f"   ❌ Ошибка загрузки сводки: {e}")
            self.graph_widget.update([])
            self._update_stats_labels({})
    
    def refresh(self, instance):
        self._load_data()
    
    def go_back(self, instance):
        if self.app:
            self.app.switch_to("menu")