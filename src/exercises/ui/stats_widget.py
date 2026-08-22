"""
stats_widget.py - Виджет графика тренда для статистики
"""

import math
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp


class StatsGraphWidget(Widget):
    """Виджет для отображения графика тренда"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self.filters = {}
        self.bg_color = (0.05, 0.05, 0.08, 1)
        self.grid_color = (0.2, 0.2, 0.3, 0.5)
        self.trend_color = (0.9, 0.9, 0.3, 0.6)
        
        self.point_colors = {
            "accurate": (0.3, 0.9, 0.3, 1),
            "over": (0.9, 0.3, 0.3, 1),
            "under": (0.3, 0.3, 0.9, 1)
        }
        
        self.bind(size=self.draw, pos=self.draw)
    
    def update(self, data, filters=None):
        """Обновление данных"""
        self.data = data
        if filters:
            self.filters = filters
        self.draw()
    
    def draw(self, *args):
        """Отрисовка графика"""
        self.canvas.clear()
        
        if not self.data:
            self._draw_empty()
            return
        
        deviations = [d["deviation"] for d in self.data]
        n = len(deviations)
        
        if n < 2:
            self._draw_empty("Недостаточно данных")
            return
        
        max_abs = max(abs(d) for d in deviations) if deviations else 10
        max_abs = max(max_abs, 5)
        
        if max_abs > 50:
            y_scale = math.ceil(max_abs / 10) * 10
        elif max_abs > 20:
            y_scale = math.ceil(max_abs / 5) * 5
        else:
            y_scale = math.ceil(max_abs / 2) * 2
        
        width = self.width or 400
        height = self.height or 250
        padding = dp(20)
        graph_width = width - padding * 2
        graph_height = height - padding * 2
        
        with self.canvas:
            Color(*self.bg_color)
            Rectangle(pos=self.pos, size=self.size)
            
            Color(*self.grid_color)
            for i in range(1, 5):
                y = self.y + padding + (i / 5) * graph_height
                Line(points=[self.x + padding, y, self.x + padding + graph_width, y], width=1)
            
            Color(0.3, 0.3, 0.4, 0.8)
            y_center = self.y + padding + graph_height / 2
            Line(points=[self.x + padding, y_center, self.x + padding + graph_width, y_center], width=1)
            Line(points=[self.x + padding, self.y + padding, self.x + padding, self.y + padding + graph_height], width=1)
            
            if n >= 3:
                self._draw_trend_line(deviations, width, height, padding, graph_width, graph_height, y_scale)
            
            self._draw_points(deviations, width, height, padding, graph_width, graph_height, y_scale)
    
    def _draw_points(self, deviations, width, height, padding, graph_width, graph_height, y_scale):
        n = len(deviations)
        display_width = min(graph_width, n * 8)
        
        for i in range(min(n, int(display_width / 8))):
            val = deviations[i]
            x = self.x + padding + (i / n) * display_width
            y = self.y + padding + graph_height / 2 - (val / y_scale) * (graph_height / 2)
            
            if abs(val) <= 5:
                color = self.point_colors["accurate"]
            elif val > 5:
                color = self.point_colors["over"]
            else:
                color = self.point_colors["under"]
            
            radius = dp(4)
            with self.canvas:
                Color(*color)
                Line(points=[x, y - radius, x, y + radius], width=2)
                Line(points=[x - radius, y, x + radius, y], width=2)
    
    def _draw_trend_line(self, deviations, width, height, padding, graph_width, graph_height, y_scale):
        n = len(deviations)
        if n < 3:
            return
        
        x = list(range(n))
        sum_x = sum(x)
        sum_y = sum(deviations)
        sum_xy = sum(x[i] * deviations[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2) if n > 1 else 0
        intercept = (sum_y - slope * sum_x) / n
        
        if abs(slope) < 0.05:
            return
        
        y_start = slope * 0 + intercept
        y_end = slope * (n - 1) + intercept
        
        x_start = self.x + padding
        x_end = self.x + padding + graph_width
        
        y_start_pos = self.y + padding + graph_height / 2 - (y_start / y_scale) * (graph_height / 2)
        y_end_pos = self.y + padding + graph_height / 2 - (y_end / y_scale) * (graph_height / 2)
        
        with self.canvas:
            Color(*self.trend_color)
            Line(points=[x_start, y_start_pos, x_end, y_end_pos], width=2, dash_length=4)
    
    def _draw_empty(self, message="Нет данных"):
        with self.canvas:
            Color(*self.bg_color)
            Rectangle(pos=self.pos, size=self.size)
