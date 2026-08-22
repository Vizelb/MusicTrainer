"""
SETTINGS SCREEN - Экран настроек упражнения
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.metrics import dp, sp

from exercises.config.settings import ExerciseSettings
from exercises.config.settings_manager import SettingsManager


class SettingsScreen(Screen):
    """Экран настроек упражнения"""
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "exercise_settings"
        
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.load()
        
        self._build_ui()
    
    def _build_ui(self):
        """Построение интерфейса"""
        main_layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(5))
        
        # Заголовок
        main_layout.add_widget(Label(
            text="🎯 НАСТРОЙКИ УПРАЖНЕНИЯ",
            font_size=sp(24),
            size_hint=(1, None),
            height=dp(50),
            color=(0.3, 0.9, 0.3, 1),
            bold=True
        ))
        
        # Содержимое с прокруткой
        scroll = ScrollView(size_hint=(1, 0.82))
        content = BoxLayout(orientation="vertical", size_hint=(1, None), spacing=dp(8), padding=dp(10))
        content.bind(minimum_height=content.setter("height"))
        
        # ---------- 1. Музыкальный строй ----------
        tuning_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))
        tuning_layout.add_widget(Label(
            text="🎵 Строй:",
            font_size=sp(16),
            size_hint=(0.4, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        self.tuning_spinner = Spinner(
            text="Натуральный" if self.settings.tuning == "natural" else "Равномерно-темперированный",
            values=["Натуральный", "Равномерно-темперированный"],
            size_hint=(0.6, 1),
            font_size=sp(14),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.tuning_spinner.bind(text=self.on_tuning_change)
        tuning_layout.add_widget(self.tuning_spinner)
        content.add_widget(tuning_layout)
        
        # ---------- 2. Диапазон тоники ----------
        tonic_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))
        tonic_layout.add_widget(Label(
            text="🎵 Тоника:",
            font_size=sp(16),
            size_hint=(0.4, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        tonic_inner = BoxLayout(orientation="horizontal", size_hint=(0.6, 1), spacing=dp(5))
        
        self.tonic_min_spinner = Spinner(
            text=self.settings.tonic_range[0],
            values=self._get_note_names(),
            size_hint=(0.45, 1),
            font_size=sp(14),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.tonic_min_spinner.bind(text=self.on_tonic_min_change)
        tonic_inner.add_widget(self.tonic_min_spinner)
        
        tonic_inner.add_widget(Label(
            text="—",
            font_size=sp(18),
            size_hint=(0.1, 1),
            color=(0.6, 0.6, 0.6, 1),
            halign="center"
        ))
        
        self.tonic_max_spinner = Spinner(
            text=self.settings.tonic_range[1],
            values=self._get_note_names(),
            size_hint=(0.45, 1),
            font_size=sp(14),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.tonic_max_spinner.bind(text=self.on_tonic_max_change)
        tonic_inner.add_widget(self.tonic_max_spinner)
        
        tonic_layout.add_widget(tonic_inner)
        content.add_widget(tonic_layout)
        
        # ---------- 3. Частота Ля ----------
        a4_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))
        a4_layout.add_widget(Label(
            text="🎵 Ля (A4):",
            font_size=sp(16),
            size_hint=(0.4, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        a4_inner = BoxLayout(orientation="horizontal", size_hint=(0.6, 1), spacing=dp(5))
        
        self.a4_input = TextInput(
            text=str(self.settings.a4_frequency),
            font_size=sp(16),
            size_hint=(0.5, 1),
            multiline=False,
            input_filter="float",
            background_color=(0.2, 0.2, 0.3, 1),
            foreground_color=(0.9, 0.9, 0.9, 1)
        )
        self.a4_input.bind(text=self.on_a4_change)
        a4_inner.add_widget(self.a4_input)
        
        a4_inner.add_widget(Label(
            text="Гц",
            font_size=sp(16),
            size_hint=(0.3, 1),
            color=(0.6, 0.6, 0.6, 1)
        ))
        
        a4_layout.add_widget(a4_inner)
        content.add_widget(a4_layout)
        
        # ---------- 4. Интервалы ----------
        interval_header = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(35))
        interval_header.add_widget(Label(
            text="🎹 Интервалы:",
            font_size=sp(16),
            size_hint=(0.5, 1),
            color=(0.9, 0.9, 0.9, 1),
            halign="left"
        ))
        
        btn_layout = BoxLayout(orientation="horizontal", size_hint=(0.5, 1), spacing=dp(5))
        
        select_all_btn = Button(
            text="Выбрать всё",
            font_size=sp(11),
            size_hint=(0.5, 1),
            background_color=(0.2, 0.5, 0.2, 1),
            background_normal=""
        )
        select_all_btn.bind(on_press=self.select_all_intervals)
        btn_layout.add_widget(select_all_btn)
        
        deselect_all_btn = Button(
            text="Снять всё",
            font_size=sp(11),
            size_hint=(0.5, 1),
            background_color=(0.5, 0.2, 0.2, 1),
            background_normal=""
        )
        deselect_all_btn.bind(on_press=self.deselect_all_intervals)
        btn_layout.add_widget(deselect_all_btn)
        
        interval_header.add_widget(btn_layout)
        content.add_widget(interval_header)
        
        # Список интервалов
        self.intervals_grid = GridLayout(cols=3, size_hint=(1, None), spacing=dp(5))
        self.intervals_grid.bind(minimum_height=self.intervals_grid.setter("height"))
        
        self.interval_checkboxes = {}
        all_intervals = self.settings.get_all_interval_names()
        selected = self.settings.selected_intervals
        
        for interval in all_intervals:
            display_name = self.settings.get_interval_display_name(interval)
            is_selected = interval in selected
            
            row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(30))
            
            cb = CheckBox(active=is_selected, size_hint=(0.2, 1))
            cb.bind(active=lambda cb, val, name=interval: self.on_interval_change(name, cb.active))
            
            label = Label(
                text=display_name,
                font_size=sp(13),
                size_hint=(0.8, 1),
                color=(0.9, 0.9, 0.9, 1),
                halign="left"
            )
            
            row.add_widget(cb)
            row.add_widget(label)
            self.intervals_grid.add_widget(row)
            self.interval_checkboxes[interval] = cb
        
        content.add_widget(self.intervals_grid)
        
        # ---------- 5. Движение ----------
        direction_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))
        direction_layout.add_widget(Label(
            text="⬆⬇ Движение:",
            font_size=sp(16),
            size_hint=(0.4, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        direction_inner = BoxLayout(orientation="horizontal", size_hint=(0.6, 1), spacing=dp(10))
        
        self.up_btn = Button(
            text="Вверх",
            font_size=sp(16),
            size_hint=(0.5, 1),
            background_color=(0.3, 0.6, 0.3, 1) if self.settings.direction == "up" else (0.2, 0.2, 0.3, 1),
            background_normal=""
        )
        self.up_btn.bind(on_press=lambda x: self.set_direction("up"))
        direction_inner.add_widget(self.up_btn)
        
        self.down_btn = Button(
            text="Вниз",
            font_size=sp(16),
            size_hint=(0.5, 1),
            background_color=(0.3, 0.6, 0.3, 1) if self.settings.direction == "down" else (0.2, 0.2, 0.3, 1),
            background_normal=""
        )
        self.down_btn.bind(on_press=lambda x: self.set_direction("down"))
        direction_inner.add_widget(self.down_btn)
        
        direction_layout.add_widget(direction_inner)
        content.add_widget(direction_layout)
        
        # ---------- 6. Режим проведения ----------
        mode_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))
        mode_layout.add_widget(Label(
            text="🎵 Режим:",
            font_size=sp(16),
            size_hint=(0.4, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        self.mode_spinner = Spinner(
            text=self._get_mode_display(self.settings.mode),
            values=["Мелодический", "Гармонический", "Оба"],
            size_hint=(0.6, 1),
            font_size=sp(14),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.mode_spinner.bind(text=self.on_mode_change)
        mode_layout.add_widget(self.mode_spinner)
        content.add_widget(mode_layout)
        
        # ---------- 7. Скорость ----------
        speed_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50))
        speed_layout.add_widget(Label(
            text="⏱ Скорость:",
            font_size=sp(16),
            size_hint=(0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        speed_inner = BoxLayout(orientation="horizontal", size_hint=(0.7, 1), spacing=dp(10))
        
        self.speed_slider = Slider(
            min=1,
            max=100,
            value=self.settings.speed,
            size_hint=(0.7, 1)
        )
        self.speed_slider.bind(value=self.on_speed_change)
        speed_inner.add_widget(self.speed_slider)
        
        self.speed_label = Label(
            text=f"{self.settings.speed}%",
            font_size=sp(16),
            size_hint=(0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        speed_inner.add_widget(self.speed_label)
        
        speed_layout.add_widget(speed_inner)
        content.add_widget(speed_layout)
        
        # ---------- 8. Громкость тоники и эталона ----------
        tonic_volume_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50))
        tonic_volume_layout.add_widget(Label(
            text="🔊 Громкость тоники/эталона:",
            font_size=sp(14),
            size_hint=(0.4, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        tonic_volume_inner = BoxLayout(orientation="horizontal", size_hint=(0.6, 1), spacing=dp(10))
        
        self.tonic_volume_slider = Slider(
            min=1,
            max=100,
            value=self.settings.tonic_volume,
            size_hint=(0.7, 1)
        )
        self.tonic_volume_slider.bind(value=self.on_tonic_volume_change)
        tonic_volume_inner.add_widget(self.tonic_volume_slider)
        
        self.tonic_volume_label = Label(
            text=f"{self.settings.tonic_volume}%",
            font_size=sp(16),
            size_hint=(0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        tonic_volume_inner.add_widget(self.tonic_volume_label)
        
        tonic_volume_layout.add_widget(tonic_volume_inner)
        content.add_widget(tonic_volume_layout)
        
        # ---------- 9. Начальная громкость подбора ----------
        start_volume_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50))
        start_volume_layout.add_widget(Label(
            text="🔊 Начальная громкость подбора:",
            font_size=sp(14),
            size_hint=(0.4, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        start_volume_inner = BoxLayout(orientation="horizontal", size_hint=(0.6, 1), spacing=dp(10))
        
        self.start_volume_slider = Slider(
            min=1,
            max=100,
            value=self.settings.interval_start_volume,
            size_hint=(0.7, 1)
        )
        self.start_volume_slider.bind(value=self.on_start_volume_change)
        start_volume_inner.add_widget(self.start_volume_slider)
        
        self.start_volume_label = Label(
            text=f"{self.settings.interval_start_volume}%",
            font_size=sp(16),
            size_hint=(0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        start_volume_inner.add_widget(self.start_volume_label)
        
        start_volume_layout.add_widget(start_volume_inner)
        content.add_widget(start_volume_layout)
        
        # ---------- 9. Тембр ----------
        timbre_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))
        timbre_layout.add_widget(Label(
            text="🎹 Тембр:",
            font_size=sp(16),
            size_hint=(0.4, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        timbres = ["Синус", "Орган", "Скрипка", "Флейта", "Кларнет"]
        self.timbre_spinner = Spinner(
            text=self.settings.timbre,
            values=timbres,
            size_hint=(0.6, 1),
            font_size=sp(14),
            background_color=(0.2, 0.2, 0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        self.timbre_spinner.bind(text=self.on_timbre_change)
        timbre_layout.add_widget(self.timbre_spinner)
        content.add_widget(timbre_layout)
        
        # ---------- 10. Диапазон настройки ----------
        tuning_range_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50))
        tuning_range_layout.add_widget(Label(
            text="🎯 Диапазон настройки:",
            font_size=sp(14),
            size_hint=(0.35, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        tuning_range_inner = BoxLayout(orientation="horizontal", size_hint=(0.65, 1), spacing=dp(10))
        
        self.tuning_range_slider = Slider(
            min=50,
            max=1200,
            step=10,
            value=self.settings.tuning_range,
            size_hint=(0.7, 1)
        )
        self.tuning_range_slider.bind(value=self.on_tuning_range_change)
        tuning_range_inner.add_widget(self.tuning_range_slider)
        
        self.tuning_range_label = Label(
            text=f"{self.settings.tuning_range} центов",
            font_size=sp(14),
            size_hint=(0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        tuning_range_inner.add_widget(self.tuning_range_label)
        
        tuning_range_layout.add_widget(tuning_range_inner)
        content.add_widget(tuning_range_layout)
        
        # ---------- 11. Диапазон старта ----------
        start_range_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50))
        start_range_layout.add_widget(Label(
            text="🎯 Диапазон старта:",
            font_size=sp(14),
            size_hint=(0.35, 1),
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        start_range_inner = BoxLayout(orientation="horizontal", size_hint=(0.65, 1), spacing=dp(10))
        
        self.start_range_slider = Slider(
            min=50,
            max=1200,
            step=10,
            value=self.settings.start_range,
            size_hint=(0.7, 1)
        )
        self.start_range_slider.bind(value=self.on_start_range_change)
        start_range_inner.add_widget(self.start_range_slider)
        
        self.start_range_label = Label(
            text=f"{self.settings.start_range} центов",
            font_size=sp(14),
            size_hint=(0.3, 1),
            color=(0.9, 0.9, 0.9, 1)
        )
        start_range_inner.add_widget(self.start_range_label)
        
        start_range_layout.add_widget(start_range_inner)
        content.add_widget(start_range_layout)
        
        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        
        # ---------- Кнопки ----------
        btn_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(10))
        
        reset_btn = Button(
            text="↺ Сброс",
            font_size=sp(14),
            size_hint=(0.2, 1),
            background_color=(0.4, 0.3, 0.1, 1),
            background_normal=""
        )
        reset_btn.bind(on_press=self.reset_settings)
        btn_layout.add_widget(reset_btn)
        
        back_btn = Button(
            text="◀ НАЗАД",
            font_size=sp(16),
            size_hint=(0.35, 1),
            background_color=(0.3, 0.3, 0.5, 1),
            background_normal=""
        )
        back_btn.bind(on_press=self.go_back)
        btn_layout.add_widget(back_btn)
        
        self.start_btn = Button(
            text="▶ НАЧАТЬ",
            font_size=sp(16),
            size_hint=(0.45, 1),
            background_color=(0.2, 0.5, 0.2, 1),
            background_normal=""
        )
        self.start_btn.bind(on_press=self.start_exercise)
        btn_layout.add_widget(self.start_btn)
        
        main_layout.add_widget(btn_layout)
        
        self.add_widget(main_layout)
    
    def _get_note_names(self):
        return ["C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", 
                "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", 
                "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5"]
    
    def _get_mode_display(self, mode):
        modes = {"melodic": "Мелодический", "harmonic": "Гармонический", "both": "Оба"}
        return modes.get(mode, "Мелодический")
    
    def _get_mode_value(self, display):
        modes = {"Мелодический": "melodic", "Гармонический": "harmonic", "Оба": "both"}
        return modes.get(display, "melodic")
    
    # ==========================================
    # ОБРАБОТЧИКИ
    # ==========================================
    
    def on_tuning_change(self, spinner, text):
        self.settings.tuning = "natural" if text == "Натуральный" else "equal"
        self._save_settings()
    
    def on_tonic_min_change(self, spinner, text):
        self.settings.tonic_range = (text, self.settings.tonic_range[1])
        self._save_settings()
    
    def on_tonic_max_change(self, spinner, text):
        self.settings.tonic_range = (self.settings.tonic_range[0], text)
        self._save_settings()
    
    def on_a4_change(self, instance, text):
        try:
            value = float(text)
            if value > 0:
                self.settings.a4_frequency = value
                self._save_settings()
        except ValueError:
            pass
    
    def on_interval_change(self, interval_name, is_selected):
        if is_selected and interval_name not in self.settings.selected_intervals:
            self.settings.selected_intervals.append(interval_name)
        elif not is_selected and interval_name in self.settings.selected_intervals:
            self.settings.selected_intervals.remove(interval_name)
        self._save_settings()
    
    def select_all_intervals(self, instance):
        all_intervals = self.settings.get_all_interval_names()
        self.settings.selected_intervals = all_intervals.copy()
        for interval, cb in self.interval_checkboxes.items():
            cb.active = True
        self._save_settings()
    
    def deselect_all_intervals(self, instance):
        self.settings.selected_intervals = []
        for interval, cb in self.interval_checkboxes.items():
            cb.active = False
        self._save_settings()
    
    def set_direction(self, direction):
        self.settings.direction = direction
        self.up_btn.background_color = (0.3, 0.6, 0.3, 1) if direction == "up" else (0.2, 0.2, 0.3, 1)
        self.down_btn.background_color = (0.3, 0.6, 0.3, 1) if direction == "down" else (0.2, 0.2, 0.3, 1)
        self._save_settings()
    
    def on_mode_change(self, spinner, text):
        self.settings.mode = self._get_mode_value(text)
        self._save_settings()
    
    def on_speed_change(self, instance, value):
        self.settings.speed = int(value)
        self.speed_label.text = f"{int(value)}%"
        self._save_settings()
    
    def on_tonic_volume_change(self, instance, value):
        """Обработчик изменения громкости тоники/эталона"""
        self.settings.tonic_volume = int(value)
        self.tonic_volume_label.text = f"{int(value)}%"
        self._save_settings()
    
    def on_start_volume_change(self, instance, value):
        """Обработчик изменения начальной громкости подбора"""
        self.settings.interval_start_volume = int(value)
        self.start_volume_label.text = f"{int(value)}%"
        self._save_settings()
    
    def on_timbre_change(self, spinner, text):
        self.settings.timbre = text
        self._save_settings()
    
    def on_tuning_range_change(self, instance, value):
        """Обработчик изменения диапазона настройки"""
        value = int(value)
        # Используем метод set_tuning_range для автоматической корректировки
        self.settings.set_tuning_range(value)
        self.tuning_range_label.text = f"{self.settings.tuning_range} центов"
        # Синхронизируем слайдер с возможной корректировкой
        if self.tuning_range_slider.value != self.settings.tuning_range:
            self.tuning_range_slider.value = self.settings.tuning_range
        self._save_settings()
    
    def on_start_range_change(self, instance, value):
        """Обработчик изменения диапазона старта"""
        value = int(value)
        # Используем метод set_start_range для автоматической корректировки
        self.settings.set_start_range(value)
        self.start_range_label.text = f"{self.settings.start_range} центов"
        # Синхронизируем слайдеры после возможной корректировки
        if self.start_range_slider.value != self.settings.start_range:
            self.start_range_slider.value = self.settings.start_range
        if self.tuning_range_slider.value != self.settings.tuning_range:
            self.tuning_range_slider.value = self.settings.tuning_range
            self.tuning_range_label.text = f"{self.settings.tuning_range} центов"
        self._save_settings()
    
    def reset_settings(self, instance):
        self.settings = self.settings_manager.reset_to_default()
        self._update_ui_from_settings()
    
    def _save_settings(self):
        self.settings_manager.save(self.settings)
    
    def _update_ui_from_settings(self):
        self.tuning_spinner.text = "Натуральный" if self.settings.tuning == "natural" else "Равномерно-темперированный"
        self.tonic_min_spinner.text = self.settings.tonic_range[0]
        self.tonic_max_spinner.text = self.settings.tonic_range[1]
        self.a4_input.text = str(self.settings.a4_frequency)
        
        for interval, cb in self.interval_checkboxes.items():
            cb.active = interval in self.settings.selected_intervals
        
        self.up_btn.background_color = (0.3, 0.6, 0.3, 1) if self.settings.direction == "up" else (0.2, 0.2, 0.3, 1)
        self.down_btn.background_color = (0.3, 0.6, 0.3, 1) if self.settings.direction == "down" else (0.2, 0.2, 0.3, 1)
        
        self.mode_spinner.text = self._get_mode_display(self.settings.mode)
        self.speed_slider.value = self.settings.speed
        self.speed_label.text = f"{self.settings.speed}%"
        self.tonic_volume_slider.value = self.settings.tonic_volume
        self.tonic_volume_label.text = f"{self.settings.tonic_volume}%"
        self.start_volume_slider.value = self.settings.interval_start_volume
        self.start_volume_label.text = f"{self.settings.interval_start_volume}%"
        self.timbre_spinner.text = self.settings.timbre
        self.tuning_range_slider.value = self.settings.tuning_range
        self.tuning_range_label.text = f"{self.settings.tuning_range} центов"
        self.start_range_slider.value = self.settings.start_range
        self.start_range_label.text = f"{self.settings.start_range} центов"
    
    # ==========================================
    # НАВИГАЦИЯ
    # ==========================================
    
    def go_back(self, instance):
        if self.app:
            self.app.switch_to("menu")
    
    def start_exercise(self, instance):
        if not self.settings.selected_intervals:
            print("⚠️ Выберите хотя бы один интервал!")
            self.start_btn.text = "⚠️ ВЫБЕРИТЕ ИНТЕРВАЛ!"
            self.start_btn.background_color = (0.6, 0.2, 0.2, 1)
            Clock.schedule_once(lambda dt: self._reset_start_btn(), 2)
            return
        
        if self.app:
            self.app.switch_to("exercise")
            exercise_screen = self.app.screens.get("exercise")
            if exercise_screen:
                exercise_screen.start_exercise()
    
    def _reset_start_btn(self):
        self.start_btn.text = "▶ НАЧАТЬ"
        self.start_btn.background_color = (0.2, 0.5, 0.2, 1)
    
    def get_settings(self):
        """
        Получение текущих настроек из экрана настроек.
        
        Returns:
            ExerciseSettings: Объект с настройками
        """
        print("🔍 get_settings() вызван из SettingsScreen")
        
        # Создаем объект настроек
        from exercises.config.settings import ExerciseSettings
        settings = ExerciseSettings()
        
        # Заполняем из текущего состояния UI
        # Здесь нужно будет добавить чтение значений из виджетов
        # Пока возвращаем настройки из self.settings если есть
        if hasattr(self, 'settings'):
            settings = self.settings
            print(f"   📊 Режим из self.settings: {settings.mode}")
        else:
            print("   ⚠️ self.settings не найден, используются значения по умолчанию")
        
        return settings
