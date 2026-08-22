"""
EXERCISE SCREEN - Экран выполнения упражнения
"""

import numpy as np
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle

from ui.widgets import InfoLayout
from ui.controls import ControlsLayout
from exercises.ui.exercise_oscilloscope import ExerciseOscilloscope
from exercises.config.settings_manager import SettingsManager
from exercises.engine.exercise_engine import ExerciseEngine
from core.statistics import stats_manager


class ExerciseScreen(Screen):
    """Экран выполнения упражнения"""
    
    def __init__(self, app=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.name = "exercise"
        
        self.settings = None
        self.engine = None
        self.current_task = None
        self.is_listening = False
        self.is_adjusting = False
        self.is_completed = False
        self.result_shown = False
        self.session_completed = False
        
        # Таймер обновления статистики
        self.stats_update_timer = None
        
        self._build_ui()
    

    def _build_ui(self):
        """Построение интерфейса"""
        main_layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(5))
        
        # ---------- Верхняя панель ----------
        top_panel = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(10))
        
        self.title_label = Label(
            text="🎯 УПРАЖНЕНИЕ",
            font_size=sp(20),
            size_hint=(0.3, 1),
            color=(0.3, 0.9, 0.3, 1),
            halign="left",
            bold=True
        )
        top_panel.add_widget(self.title_label)
        
        self.task_info_label = Label(
            text="🎯 интервал",
            font_size=sp(16),
            size_hint=(0.35, 1),
            color=(0.8, 0.8, 0.8, 1),
            halign="center"
        )
        top_panel.add_widget(self.task_info_label)
        
        self.mode_label = Label(
            text="Мелодический ↑",
            font_size=sp(14),
            size_hint=(0.35, 1),
            color=(0.6, 0.8, 0.6, 1),
            halign="right"
        )
        top_panel.add_widget(self.mode_label)
        
        main_layout.add_widget(top_panel)
        
        # ---------- Панель статистики ----------
        stats_panel = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40), spacing=dp(10))
        
        self.session_attempts_label = Label(
            text="📊 0",
            font_size=sp(14),
            size_hint=(0.25, 1),
            color=(0.8, 0.8, 0.8, 1),
            halign="center"
        )
        stats_panel.add_widget(self.session_attempts_label)
        
        self.accuracy_label = Label(
            text="🎯 0%",
            font_size=sp(14),
            size_hint=(0.25, 1),
            color=(0.3, 0.9, 0.3, 1),
            halign="center"
        )
        stats_panel.add_widget(self.accuracy_label)
        
        self.avg_deviation_label = Label(
            text="📈 0.0¢",
            font_size=sp(14),
            size_hint=(0.25, 1),
            color=(0.9, 0.9, 0.3, 1),
            halign="center"
        )
        stats_panel.add_widget(self.avg_deviation_label)
        
        self.total_attempts_label = Label(
            text="🌍 0",
            font_size=sp(14),
            size_hint=(0.25, 1),
            color=(0.6, 0.6, 0.8, 1),
            halign="center"
        )
        stats_panel.add_widget(self.total_attempts_label)
        
        main_layout.add_widget(stats_panel)
        
        # ---------- Осциллограф ----------
        self.oscilloscope_container = BoxLayout(
            orientation="vertical",
            size_hint=(1, 0.4),
            padding=dp(5)
        )
        
        self.osc_placeholder = Label(
            text="Осциллограф будет здесь",
            font_size=sp(18),
            color=(0.5, 0.5, 0.5, 1),
            halign="center"
        )
        self.oscilloscope_container.add_widget(self.osc_placeholder)
        main_layout.add_widget(self.oscilloscope_container)
        
        # ---------- Информация о частоте ----------
        freq_panel = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(30), spacing=dp(20))
        
        freq_panel.add_widget(Label(
            text="Текущая:",
            font_size=sp(14),
            size_hint=(0.2, 1),
            color=(0.7, 0.7, 0.7, 1),
            halign="right"
        ))
        
        self.freq_label = Label(
            text="--- Гц",
            font_size=sp(16),
            size_hint=(0.3, 1),
            color=(0.9, 0.9, 0.9, 1),
            halign="center"
        )
        # Добавляем обработчик касания для переключения частоты
        self.freq_label.bind(on_touch_down=self.on_frequency_touch)
        freq_panel.add_widget(self.freq_label)
        
        freq_panel.add_widget(Label(
            text="Отклонение:",
            font_size=sp(14),
            size_hint=(0.2, 1),
            color=(0.7, 0.7, 0.7, 1),
            halign="right"
        ))
        
        self.deviation_label = Label(
            text="0.0 центов",
            font_size=sp(16),
            size_hint=(0.3, 1),
            color=(0.9, 0.9, 0.9, 1),
            halign="center"
        )
        # Добавляем обработчик касания для переключения отклонения
        self.deviation_label.bind(on_touch_down=self.on_deviation_touch)
        freq_panel.add_widget(self.deviation_label)
        
        main_layout.add_widget(freq_panel)
        
        # ---------- Информация об интервале ----------
        self.interval_info_label = Label(
            text="",
            font_size=sp(16),
            size_hint=(1, None),
            height=dp(30),
            color=(0.9, 0.9, 0.9, 1),
            halign="center"
        )
        main_layout.add_widget(self.interval_info_label)
        
        # ---------- Статус ----------
        self.status_label = Label(
            text="",
            font_size=sp(14),
            size_hint=(1, None),
            height=dp(30),
            color=(0.6, 0.8, 0.6, 1),
            halign="center"
        )
        main_layout.add_widget(self.status_label)
        
        # ---------- Кнопки управления ----------
        control_panel = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(50), spacing=dp(10))
        
        self.repeat_btn = Button(
            text="🔄 ПОВТОРИТЬ",
            font_size=sp(14),
            size_hint=(0.25, 1),
            background_color=(0.3, 0.3, 0.5, 1),
            background_normal=""
        )
        self.repeat_btn.bind(on_press=self.repeat_interval)
        control_panel.add_widget(self.repeat_btn)
        
        self.start_btn = Button(
            text="▶ НАЧАТЬ ПОДБОР",
            font_size=sp(14),
            size_hint=(0.35, 1),
            background_color=(0.2, 0.5, 0.2, 1),
            background_normal=""
        )
        self.start_btn.bind(on_press=self.start_adjustment)
        control_panel.add_widget(self.start_btn)
        
        self.submit_btn = Button(
            text="✅ ПОДОБРАНО",
            font_size=sp(14),
            size_hint=(0.25, 1),
            background_color=(0.2, 0.4, 0.6, 1),
            background_normal=""
        )
        self.submit_btn.bind(on_press=self.submit_answer)
        self.submit_btn.disabled = True
        self.submit_btn.opacity = 0.5
        control_panel.add_widget(self.submit_btn)
        
        self.finish_btn = Button(
            text="🔚 ЗАВЕРШИТЬ СЕССИЮ",
            font_size=sp(12),
            size_hint=(0.2, 1),
            background_color=(0.3, 0.2, 0.1, 1),
            background_normal=""
        )
        self.finish_btn.bind(on_press=self.finish_session)
        control_panel.add_widget(self.finish_btn)
        
        self.exit_btn = Button(
            text="🚪 ВЫЙТИ",
            font_size=sp(14),
            size_hint=(0.15, 1),
            background_color=(0.5, 0.2, 0.2, 1),
            background_normal=""
        )
        self.exit_btn.bind(on_press=self.exit_exercise)
        control_panel.add_widget(self.exit_btn)
        
        main_layout.add_widget(control_panel)
        
        # ---------- Результат ----------
        self.result_panel = BoxLayout(orientation="vertical", size_hint=(1, None), height=dp(100), spacing=dp(5))
        
        self.result_container = BoxLayout(orientation="vertical", size_hint=(1, 1))
        
        self.result_label = Label(
            text="",
            font_size=sp(18),
            size_hint=(1, 0.6),
            color=(1, 1, 1, 1),
            halign="center",
            bold=True
        )
        self.result_container.add_widget(self.result_label)
        
        self.result_detail_label = Label(
            text="",
            font_size=sp(14),
            size_hint=(1, 0.4),
            color=(0.8, 0.8, 0.8, 1),
            halign="center"
        )
        self.result_container.add_widget(self.result_detail_label)
        
        self.result_panel.add_widget(self.result_container)
        
        result_buttons = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40), spacing=dp(10))
        
        self.play_again_btn = Button(
            text="🔊 ЭТАЛОН",
            font_size=sp(12),
            size_hint=(0.35, 1),
            background_color=(0.3, 0.3, 0.5, 1),
            background_normal=""
        )
        self.play_again_btn.bind(on_press=self.play_etalon)
        result_buttons.add_widget(self.play_again_btn)
        
        self.next_btn = Button(
            text="➡ СЛЕДУЮЩЕЕ",
            font_size=sp(12),
            size_hint=(0.35, 1),
            background_color=(0.2, 0.5, 0.2, 1),
            background_normal=""
        )
        self.next_btn.bind(on_press=self.next_task)
        result_buttons.add_widget(self.next_btn)
        
        result_buttons.add_widget(Label(size_hint=(0.3, 1)))
        
        self.result_panel.add_widget(result_buttons)
        
        self.result_panel.opacity = 0
        self.result_panel.disabled = True
        
        main_layout.add_widget(self.result_panel)
        
        self.add_widget(main_layout)
        
        Clock.schedule_interval(self._update_frequency_display, 0.1)
    

    def _update_frequency_display(self, dt):
        """Обновление отображения частоты и отклонения"""
        if not self.engine:
            return
        
        freq = self.engine.get_current_frequency()
        
        # Проверяем, нужно ли показывать частоту
        if self.settings and self.settings.show_frequency and freq > 0:
            self.freq_label.text = f"{freq:.1f} Гц"
            self.freq_label.color = (0.9, 0.9, 0.9, 1)
        else:
            self.freq_label.text = "---"
            self.freq_label.color = (0.5, 0.5, 0.5, 1)
        
        if self.current_task and not self.is_completed:
            # Используем current_freq (текущая) и interval_freq (эталон)
            target = self.current_task["interval_freq"]  # Эталон
            current = self.current_task.get("current_freq", target)  # Текущая
            if target > 0 and current > 0:
                deviation = 1200 * np.log2(current / target)
                
                # ОТЛАДКА: подробный вывод
                print(f"🔴🔴🔴 ОТКЛОНЕНИЕ:")
                print(f"   freq (текущая частота): {freq:.3f} Гц")
                print(f"   target (эталон): {target:.3f} Гц")
                print(f"   deviation: {deviation:.3f} центов")
                print(f"   режим: {'гармонический' if self.engine.is_harmonic_mode else 'мелодический'}")
                print(f"   interval_engine: {self.engine.interval_engine is not None}")
                print("=" * 40)
                sign = "+" if deviation > 0 else ""
                
                # Проверяем, нужно ли показывать отклонение
                if self.settings and self.settings.show_deviation:
                    self.deviation_label.text = f"{sign}{deviation:.1f} центов"
                    
                    if abs(deviation) <= 5:
                        self.deviation_label.color = (0.3, 0.9, 0.3, 1)
                    elif abs(deviation) <= 10:
                        self.deviation_label.color = (0.9, 0.9, 0.3, 1)
                    elif abs(deviation) <= 20:
                        self.deviation_label.color = (0.9, 0.6, 0.3, 1)
                    else:
                        self.deviation_label.color = (0.9, 0.3, 0.3, 1)
                else:
                    self.deviation_label.text = "---"
                    self.deviation_label.color = (0.5, 0.5, 0.5, 1)
    

    
    def on_deviation_touch(self, instance, touch):
        """Обработка касания на индикаторе отклонения для переключения отображения"""
        if not self.settings:
            return False
        
        # Проверяем, что касание произошло в пределах deviation_label
        if self.deviation_label.collide_point(touch.x, touch.y):
            # Переключаем состояние
            self.settings.show_deviation = not self.settings.show_deviation
            # Сохраняем настройки
            manager = SettingsManager()
            manager.save(self.settings)
            # Обновляем отображение
            self._update_frequency_display(0)
            return True
        return False
    
    def on_frequency_touch(self, instance, touch):
        """Обработка касания на индикаторе текущей частоты для переключения отображения"""
        if not self.settings:
            return False
        
        # Проверяем, что касание произошло в пределах freq_label
        if self.freq_label.collide_point(touch.x, touch.y):
            # Переключаем состояние
            self.settings.show_frequency = not self.settings.show_frequency
            # Сохраняем настройки
            manager = SettingsManager()
            manager.save(self.settings)
            # Обновляем отображение
            self._update_frequency_display(0)
            return True
        return False
    
    def start_exercise(self):
        """Запуск упражнения"""
        print("🎯 start_exercise вызван")
        
        manager = SettingsManager()
        self.settings = manager.load()
        
        print(f"   Настройки загружены")
        
        # В непрерывном режиме всегда начинаем новую сессию
        self._start_new_session()
    

    def _start_new_session(self):
        """Начало новой сессии"""
        self.session_completed = False
        
        self.engine = ExerciseEngine(self.settings)
        self.engine.start_session()
        
        self._load_next_task()
        
        # Обновляем статистику
        self._update_stats_display(0)
        
        print("✅ Новая сессия начата")
    


    

    def _load_next_task(self):
        """Загрузка следующего задания"""
        if not self.engine:
            return
        
        self.current_task = self.engine.generate_task()
        if not self.current_task:
            return
        
        self._update_task_info()
        self._create_oscilloscope()
        
        self.is_listening = False
        self.is_adjusting = False
        self.is_completed = False
        self.result_shown = False
        
        self.repeat_btn.disabled = False
        self.start_btn.disabled = False
        self.start_btn.text = "▶ НАЧАТЬ ПОДБОР"
        self.start_btn.background_color = (0.2, 0.5, 0.2, 1)
        self.submit_btn.disabled = True
        self.submit_btn.opacity = 0.5
        
        self.result_panel.opacity = 0
        self.result_panel.disabled = True
        self.result_label.text = ""
        self.result_detail_label.text = ""
        
        
        self._play_interval()
        
        print(f"   Новое задание: {self.current_task['interval_name']}")
    

    def _create_oscilloscope(self):
        """Создание осциллографа для текущего задания"""
        if not self.current_task:
            return
        
        self.oscilloscope_container.clear_widgets()
        
        target_freq = self.current_task["interval_freq"]
        range_cents = self.settings.tuning_range
        
        # Для осциллографа используем interval_engine (активный звук для обоих режимов)
        if self.engine.interval_engine:
            engine = self.engine.interval_engine
        else:
            engine = self.engine.sound_engine
        
        self.exercise_osc = ExerciseOscilloscope(
            engine=engine,                    # правильный движок для визуализации
            exercise_engine=self.engine,      # ExerciseEngine для управления
            target_freq=target_freq,
            range_cents=range_cents,
            size_hint=(1, 1)
        )
        
        self.oscilloscope_container.add_widget(self.exercise_osc)
        print(f"   Осциллограф создан: target={target_freq:.1f} Гц")
        
        # Сохраняем ссылку на осциллограф для обновления диапазона
        self.exercise_osc_ref = self.exercise_osc
        
        # Включаем режим упражнения для осциллографа
        if hasattr(self.exercise_osc, 'set_exercise_mode'):
            self.exercise_osc.set_exercise_mode(True)
    

    def _update_task_info(self):
        """Обновление информации о задании"""
        if not self.current_task:
            print("⚠️ _update_task_info(): current_task is None")
            return

        task = self.current_task
        print(f"🔍 _update_task_info(): mode = {task.get('mode', 'NO MODE')}")

        self.task_info_label.text = f"🎯 {task['display_name']}"

        mode_display = "Мелодический" if task["mode"] == "melodic" else "Гармонический"
        direction_display = "↑" if task["direction"] == "up" else "↓"
        self.mode_label.text = f"{mode_display} {direction_display}"

        print(f"🔍 _update_task_info(): mode_display = {mode_display}")
        print(f"🔍 _update_task_info(): mode_label.text = {self.mode_label.text}")

        if self.settings and self.settings.show_interval_name:
            self.interval_info_label.text = f"🎯 Интервал: {task['display_name']}"
        else:
            self.interval_info_label.text = ""

        if task["mode"] == "harmonic":
            self.status_label.text = "🎵 Гармонический режим: тоника будет звучать как фон"
        else:
            self.status_label.text = "🎵 Мелодический режим: тоника и интервал последовательно"
    

    def _play_interval(self):
        """Воспроизведение интервала"""
        if not self.engine or not self.current_task:
            return
        
        self.is_listening = True
        self.status_label.text = "🎵 Воспроизведение..."
        
        self.engine.stop_sound()
        
        # Отключаем режим упражнения для осциллографа (эталон)
        if hasattr(self, 'exercise_osc') and hasattr(self.exercise_osc, 'set_exercise_mode'):
            self.exercise_osc.set_exercise_mode(False)
        
        def on_play_complete():
            self.is_listening = False
            self.status_label.text = "🎵 Готово! Нажмите 'НАЧАТЬ ПОДБОР'"
            # Включаем режим упражнения после завершения эталона
            if hasattr(self, 'exercise_osc') and hasattr(self.exercise_osc, 'set_exercise_mode'):
                self.exercise_osc.set_exercise_mode(True)
        
        self.engine.play_interval_full(on_play_complete)
    

    def repeat_interval(self, instance):
        """Повторное воспроизведение интервала"""
        if not self.engine or not self.current_task or self.is_completed:
            return
        
        if self.is_adjusting:
            self.engine.stop_adjustment()
            self.is_adjusting = False
            self.start_btn.disabled = False
            self.start_btn.text = "▶ НАЧАТЬ ПОДБОР"
            self.start_btn.background_color = (0.2, 0.5, 0.2, 1)
            self.submit_btn.disabled = True
            self.submit_btn.opacity = 0.5
        
        # Отключаем режим упражнения для эталона
        if hasattr(self, 'exercise_osc') and hasattr(self.exercise_osc, 'set_exercise_mode'):
            self.exercise_osc.set_exercise_mode(False)
        
        self._play_interval()
    

    def start_adjustment(self, instance):
        """Начало настройки частоты"""
        if not self.engine or not self.current_task or self.is_completed:
            return
        
        self.is_adjusting = True
        self.start_btn.disabled = True
        self.start_btn.text = "🔊 НАСТРОЙКА..."
        self.start_btn.background_color = (0.5, 0.3, 0.1, 1)
        
        self.engine.start_adjustment()
        
        # Синхронизируем осциллограф с движком после старта
        if hasattr(self, "exercise_osc"):
            if hasattr(self.exercise_osc, "sync_frequency_from_engine"):
                self.exercise_osc.sync_frequency_from_engine()
        
        # Включаем режим упражнения для осциллографа
        if hasattr(self, 'exercise_osc') and hasattr(self.exercise_osc, 'set_exercise_mode'):
            self.exercise_osc.set_exercise_mode(True)
        
        # Принудительно обновляем отображение частоты и отклонения
        Clock.schedule_once(lambda dt: self._update_frequency_display(0), 0.1)
        
        self.submit_btn.disabled = False
        self.submit_btn.opacity = 1.0
        
        mode = self.current_task["mode"]
        if mode == "harmonic":
            self.status_label.text = "🔊 Настройка частоты (тоника звучит как фон)"
        else:
            self.status_label.text = "🔊 Настройка частоты"
        
        print("🎵 Начало настройки частоты")
    

    def submit_answer(self, instance):
        """Отправка ответа"""
        if not self.engine or not self.current_task or not self.is_adjusting:
            return
        
        current_freq = self.engine.get_current_frequency()
        
        result = self.engine.check_answer(current_freq)
        if not result:
            return
        
        self.engine.stop_adjustment()
        self.is_adjusting = False
        self.is_completed = True
        self.result_shown = True
        
        self.submit_btn.disabled = True
        self.submit_btn.opacity = 0.5
        self.start_btn.disabled = True
        self.repeat_btn.disabled = True
        
        
        self._show_result(result)
        
        # Обновляем статистику
        self._update_stats_display(0)
        
        print(f"   Ответ: {current_freq:.1f} Гц, отклонение: {result['deviation']:.1f} центов")
    

    def _show_result(self, result):
        """Отображение результата с цветовой индикацией"""
        deviation = result["deviation"]
        is_correct = abs(deviation) <= 5
        
        if is_correct:
            status = "✅ ОТЛИЧНО!"
            color = (0.2, 0.7, 0.2, 1)
            detail = "Отклонение в пределах ±5 центов"
        elif abs(deviation) <= 10:
            status = "👍 ХОРОШО!"
            color = (0.7, 0.7, 0.2, 1)
            detail = "Отклонение в пределах ±10 центов"
        elif abs(deviation) <= 20:
            status = "📖 УЧИТЕСЬ!"
            color = (0.7, 0.5, 0.2, 1)
            detail = "Отклонение в пределах ±20 центов"
        else:
            status = "💪 ТРЕНИРУЙТЕСЬ!"
            color = (0.7, 0.2, 0.2, 1)
            detail = "Отклонение более ±20 центов"
        
        self.result_container.canvas.before.clear()
        with self.result_container.canvas.before:
            Color(*color, 0.3)
            Rectangle(pos=self.result_container.pos, size=self.result_container.size)
        
        sign = "+" if deviation > 0 else ""
        self.result_label.text = f"{status}"
        self.result_label.color = (1, 1, 1, 1)
        
        self.result_detail_label.text = f"Отклонение: {sign}{deviation:.1f} центов  |  Целевая частота: {result['target_freq']:.1f} Гц"
        self.result_detail_label.color = (0.9, 0.9, 0.9, 1)
        
        self.result_panel.opacity = 1
        self.result_panel.disabled = False
        
        self.status_label.text = f"✅ Задание завершено (отклонение {sign}{deviation:.1f} центов)"
        
        if abs(deviation) <= 5:
            self.deviation_label.color = (0.3, 0.9, 0.3, 1)
        elif abs(deviation) <= 10:
            self.deviation_label.color = (0.9, 0.9, 0.3, 1)
        elif abs(deviation) <= 20:
            self.deviation_label.color = (0.9, 0.6, 0.3, 1)
        else:
            self.deviation_label.color = (0.9, 0.3, 0.3, 1)
    

    def play_etalon(self, instance):
        """Проигрывание эталонного интервала"""
        if not self.engine or not self.current_task:
            return
        
        self.engine.stop_sound()
        
        def on_play_complete():
            self.status_label.text = "🎵 Эталон воспроизведен"
        
        self.engine.play_etalon(on_play_complete)
    

    def next_task(self, instance):
        """Переход к следующему заданию"""
        if not self.engine:
            return
        
        # В непрерывном режиме всегда переходим к следующему заданию
        self._load_next_task()
        self._update_stats_display(0)
    

    def finish_session(self, instance):
        """Завершение сессии по желанию пользователя"""
        if not self.engine:
            return
        
        summary = stats_manager.get_session_summary()
        
        if summary["total"] == 0:
            self.status_label.text = "⚠️ Нет попыток в этой сессии"
            return
        
        # Показываем итоги сессии
        self.result_container.canvas.before.clear()
        with self.result_container.canvas.before:
            Color(0.2, 0.4, 0.2, 0.3)
            Rectangle(pos=self.result_container.pos, size=self.result_container.size)
        
        self.result_label.text = "📊 СЕССИЯ ЗАВЕРШЕНА!"
        self.result_label.color = (0.3, 0.9, 0.3, 1)
        self.result_detail_label.text = f"Попыток: {summary['total']}  |  Точность: {summary['correct']/summary['total']*100:.1f}%  |  Среднее отклонение: {summary['avg_deviation']:.1f} центов"
        self.result_detail_label.color = (0.9, 0.9, 0.9, 1)
        
        self.result_panel.opacity = 1
        self.result_panel.disabled = False
        
        self.repeat_btn.disabled = True
        self.start_btn.disabled = True
        self.submit_btn.disabled = True
        self.finish_btn.disabled = True
        
        self.exit_btn.text = "🏠 В МЕНЮ"
        self.exit_btn.background_color = (0.2, 0.5, 0.2, 1)
        
        stats_manager.end_session()
        
        self.status_label.text = f"✅ Сессия завершена! ({summary['total']} попыток)"
        
        # Обновляем статистику
        self._update_stats_display(0)
        
        print(f"📊 Сессия завершена! Попыток: {summary['total']}, Точность: {summary['correct']/summary['total']*100:.1f}%")
    

    def exit_exercise(self, instance):
        """Выход из упражнения с сохранением прогресса"""
        print("🚪 Выход из упражнения")
        
        if self.engine:
            self.engine.close()
            self.engine = None
        
        # Останавливаем таймер обновления статистики
        if self.stats_update_timer:
            self.stats_update_timer.cancel()
            self.stats_update_timer = None
        
        if self.app:
            self.app.switch_to("exercise_settings")
    
    
    def update_oscilloscope_range(self):
        """Обновление диапазона осциллографа из настроек"""
        if hasattr(self, 'exercise_osc_ref') and self.exercise_osc_ref:
            tuning_range = self.settings.tuning_range
            self.exercise_osc_ref.update_range(tuning_range)
            print(f"   🔄 Диапазон осциллографа обновлен: {tuning_range} центов")
    
    def load_settings(self, settings):
        """
        Загрузка настроек в ExerciseScreen.
        
        Args:
            settings: Объект ExerciseSettings с настройками
        """
        print("🔍 load_settings() вызван в ExerciseScreen")
        print(f"   📊 Получен режим: {settings.mode}")
        print(f"   📊 Интервалы: {settings.selected_intervals}")
        
        self.settings = settings
        print("   ✅ Настройки загружены")
        
        # Обновляем UI если нужно
        if hasattr(self, '_update_settings_display'):
            self._update_settings_display()
    
    def _start_stats_updates(self):
        """Запуск обновления статистики"""
        if self.stats_update_timer:
            self.stats_update_timer.cancel()
        self.stats_update_timer = Clock.schedule_interval(self._update_stats_display, 1.0)
    
    def _update_stats_display(self, dt):
        """Обновление отображения статистики"""
        try:
            session_summary = stats_manager.get_session_summary()
            total = session_summary.get("total", 0)
            
            self.session_attempts_label.text = f"📊 {total}"
            
            if total > 0:
                correct = session_summary.get("correct", 0)
                accuracy = (correct / total) * 100
                avg_dev = session_summary.get("avg_deviation", 0)
                
                self.accuracy_label.text = f"🎯 {accuracy:.0f}%"
                if accuracy >= 80:
                    self.accuracy_label.color = (0.3, 0.9, 0.3, 1)
                elif accuracy >= 50:
                    self.accuracy_label.color = (0.9, 0.9, 0.3, 1)
                else:
                    self.accuracy_label.color = (0.9, 0.3, 0.3, 1)
                
                self.avg_deviation_label.text = f"📈 {avg_dev:.1f}¢"
                if abs(avg_dev) <= 5:
                    self.avg_deviation_label.color = (0.3, 0.9, 0.3, 1)
                elif abs(avg_dev) <= 10:
                    self.avg_deviation_label.color = (0.9, 0.9, 0.3, 1)
                elif abs(avg_dev) <= 20:
                    self.avg_deviation_label.color = (0.9, 0.6, 0.3, 1)
                else:
                    self.avg_deviation_label.color = (0.9, 0.3, 0.3, 1)
            else:
                self.accuracy_label.text = "🎯 0%"
                self.accuracy_label.color = (0.8, 0.8, 0.8, 1)
                self.avg_deviation_label.text = "📈 0.0¢"
                self.avg_deviation_label.color = (0.8, 0.8, 0.8, 1)
            
            self.total_attempts_label.text = f"🌍 {stats_manager.get_total_attempts()}"
            
        except Exception as e:
            pass
    
    def on_enter(self, *args):
        """При входе на экран"""
        self._start_stats_updates()
        self._update_stats_display(0)
        return super().on_enter(*args)
    
    def on_leave(self, *args):
        """При выходе с экрана"""
        if self.stats_update_timer:
            self.stats_update_timer.cancel()
            self.stats_update_timer = None
        return super().on_leave(*args)
