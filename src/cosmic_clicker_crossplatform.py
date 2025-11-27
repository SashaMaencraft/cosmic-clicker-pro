import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from datetime import datetime
import json
import os
import platform
import sys
from pathlib import Path

# Проверка платформы
IS_ANDROID = platform.system() == "Android"
IS_IOS = platform.system() == "Darwin" and "iOS" in platform.platform()
IS_WEB = hasattr(sys, 'getandroidapilevel')  # Pyodide environment
IS_MOBILE = IS_ANDROID or IS_IOS


class CosmicClickerPro:
    def __init__(self, root=None):
        # Для веб-версии создаем свой root
        if root is None:
            if not IS_WEB:
                self.root = tk.Tk()
            else:
                # Для веб-версии используем специальную инициализацию
                self.init_web_version()
                return
        else:
            self.root = root

        self.setup_app()

    def setup_app(self):
        """Настройка приложения"""
        self.root.title("💰 Cosmic Clicker Pro")

        # Определяем тип устройства
        self.device_type = self.detect_device_type()
        self.setup_window_size()

        self.root.configure(bg='#0f0f23')

        # Цветовая схема
        self.colors = {
            'bg': '#0f0f23', 'card_bg': '#1a1a2e', 'accent': '#4cc9f0',
            'accent2': '#4361ee', 'success': '#4ade80', 'danger': '#ef4444',
            'warning': '#fbbf24', 'text': '#ffffff', 'text_secondary': '#94a3b8',
            'profit': '#10b981', 'loss': '#ef4444', 'bitcoin': '#f7931a'
        }

        # Настройки для разных платформ
        self.setup_platform_specific()
        self.setup_fonts()

        # Инициализация игры
        self.save_file = self.get_save_path()
        self.load_game()

        if not hasattr(self, 'stock_history_length'):
            self.stock_history_length = 10

        self.create_modern_ui()
        self.update_stock_prices()
        self.start_passive_income()
        self.setup_mobile_bindings()

    def get_save_path(self):
        """Получение пути для сохранения в зависимости от платформы"""
        if IS_ANDROID:
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), "clicker_save.json")
        elif IS_IOS:
            from ios.storage import documents_path
            return os.path.join(documents_path(), "clicker_save.json")
        else:
            return "clicker_save.json"

    def setup_platform_specific(self):
        """Настройки для конкретных платформ"""
        if IS_ANDROID:
            # Настройки для Android
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            except ImportError:
                pass

        elif IS_IOS:
            # Настройки для iOS
            try:
                from ios.utils import set_idle_timer_disabled
                set_idle_timer_disabled(True)  # Предотвращаем сон экрана
            except ImportError:
                pass

    def detect_device_type(self):
        """Определение типа устройства"""
        if IS_MOBILE:
            return "mobile"
        elif self.is_tablet():
            return "tablet"
        else:
            return "desktop"

    def is_tablet(self):
        """Проверка на планшет"""
        try:
            if IS_MOBILE:
                return False  # На мобильных считаем все телефонами

            root = tk.Tk()
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            root.destroy()

            diagonal = math.sqrt(width ** 2 + height ** 2) / 96
            return 7 <= diagonal <= 12
        except:
            return False

    def setup_window_size(self):
        """Настройка размера окна"""
        try:
            if IS_MOBILE:
                # На мобильных - полноэкранный режим
                self.root.attributes('-fullscreen', True)
            else:
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()

                if self.device_type == "tablet":
                    self.window_width = min(800, screen_width - 100)
                    self.window_height = min(1000, screen_height - 100)
                    self.root.geometry(f"{self.window_width}x{self.window_height}")
                else:
                    self.window_width = 600
                    self.window_height = 750
                    self.root.geometry(f"{self.window_width}x{self.window_height}")

                self.root.resizable(True, True)
        except:
            if not IS_MOBILE:
                self.root.geometry("600x750")

    def setup_fonts(self):
        """Настройка шрифтов"""
        if self.device_type == "mobile":
            self.fonts = {
                'title': ("Arial", 16, "bold"), 'subtitle': ("Arial", 10),
                'button_large': ("Arial", 14, "bold"), 'button_medium': ("Arial", 12, "bold"),
                'button_small': ("Arial", 10, "bold"), 'card_title': ("Arial", 12, "bold"),
                'card_text': ("Arial", 9), 'stats_large': ("Arial", 14, "bold"),
                'stats_medium': ("Arial", 11, "bold"), 'stats_small': ("Arial", 9),
                'tab': ("Arial", 8, "bold")
            }
        elif self.device_type == "tablet":
            self.fonts = {
                'title': ("Arial", 18, "bold"), 'subtitle': ("Arial", 11),
                'button_large': ("Arial", 16, "bold"), 'button_medium': ("Arial", 13, "bold"),
                'button_small': ("Arial", 11, "bold"), 'card_title': ("Arial", 13, "bold"),
                'card_text': ("Arial", 10), 'stats_large': ("Arial", 16, "bold"),
                'stats_medium': ("Arial", 12, "bold"), 'stats_small': ("Arial", 10),
                'tab': ("Arial", 9, "bold")
            }
        else:
            self.fonts = {
                'title': ("Arial", 18, "bold"), 'subtitle': ("Arial", 10),
                'button_large': ("Arial", 16, "bold"), 'button_medium': ("Arial", 12, "bold"),
                'button_small': ("Arial", 9, "bold"), 'card_title': ("Arial", 12, "bold"),
                'card_text': ("Arial", 9), 'stats_large': ("Arial", 14, "bold"),
                'stats_medium': ("Arial", 11, "bold"), 'stats_small': ("Arial", 9),
                'tab': ("Arial", 9, "bold")
            }

    def setup_mobile_bindings(self):
        """Настройка жестов для мобильных"""
        if self.device_type == "mobile":
            self.root.bind('<Left>', self.previous_tab)
            self.root.bind('<Right>', self.next_tab)
            self.root.bind('<ButtonPress-1>', self.start_long_press)
            self.root.bind('<ButtonRelease-1>', self.end_long_press)
            self.root.bind('<Double-Button-1>', self.double_tap)

    def init_web_version(self):
        """Инициализация для веб-версии"""
        # Для веб-версии создаем виртуальный интерфейс
        print("Cosmic Clicker Pro - Web Version")
        print("Для веб-версии требуется специальная сборка")

    # ОСТАЛЬНЫЕ МЕТОДЫ ИГРЫ (такие же как в предыдущей версии)
    # initialize_new_game, save_game, load_game, create_modern_ui, и т.д.

    def previous_tab(self, event=None):
        current = self.notebook.index(self.notebook.select())
        if current > 0:
            self.notebook.select(current - 1)

    def next_tab(self, event=None):
        current = self.notebook.index(self.notebook.select())
        if current < len(self.notebook.tabs()) - 1:
            self.notebook.select(current + 1)

    def start_long_press(self, event):
        self.long_press_time = datetime.now()
        self.long_press_job = self.root.after(1000, self.execute_long_press, event.widget)

    def end_long_press(self, event):
        if hasattr(self, 'long_press_job'):
            self.root.after_cancel(self.long_press_job)

    def execute_long_press(self, widget):
        if hasattr(widget, 'long_press_action'):
            widget.long_press_action()

    def double_tap(self, event):
        widget = event.widget
        if hasattr(widget, 'double_tap_action'):
            widget.double_tap_action()

    # ... (все остальные методы игры из предыдущей версии)


def run_app():
    """Запуск приложения"""
    root = tk.Tk()

    # Настройка стилей
    style = ttk.Style()
    style.theme_use('clam')

    app = CosmicClickerPro(root)

    # Настройка прогресс-бара в зависимости от устройства
    if app.device_type == "mobile":
        style.configure("TProgressbar",
                        troughcolor='#1e293b',
                        background='#4cc9f0',
                        thickness=20)
    else:
        style.configure("TProgressbar",
                        troughcolor='#1e293b',
                        background='#4cc9f0')

    root.mainloop()


# Для Android запуск через Kivy Launcher
if __name__ == '__main__':
    run_app()