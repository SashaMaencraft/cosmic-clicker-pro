import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from datetime import datetime
import json
import os
import platform
import sys


class ModernClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Cosmic Clicker Pro")

        # Определяем тип устройства
        self.device_type = self.detect_device_type()
        self.setup_window_size()

        self.root.configure(bg='#0f0f23')
        self.root.resizable(True, True)

        # Современная цветовая схема
        self.colors = {
            'bg': '#0f0f23',
            'card_bg': '#1a1a2e',
            'accent': '#4cc9f0',
            'accent2': '#4361ee',
            'success': '#4ade80',
            'danger': '#ef4444',
            'warning': '#fbbf24',
            'text': '#ffffff',
            'text_secondary': '#94a3b8',
            'profit': '#10b981',
            'loss': '#ef4444',
            'bitcoin': '#f7931a'
        }

        # Настройки шрифтов в зависимости от устройства
        self.setup_fonts()

        # Загрузка сохранения
        self.save_file = "clicker_save.json"
        self.load_game()

        # Убедимся что stock_history_length установлен
        if not hasattr(self, 'stock_history_length'):
            self.stock_history_length = 10

        self.create_modern_ui()
        self.update_stock_prices()
        self.start_passive_income()

        # Бинды для мобильных устройств
        self.setup_mobile_bindings()

    def detect_device_type(self):
        """Определяет тип устройства"""
        try:
            if platform.system() == "Android" or platform.system() == "iOS":
                return "mobile"
            elif self.is_tablet():
                return "tablet"
            else:
                return "desktop"
        except:
            return "desktop"

    def is_tablet(self):
        """Проверяет, является ли устройство планшетом"""
        try:
            root = tk.Tk()
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            root.destroy()

            diagonal = math.sqrt(width ** 2 + height ** 2) / 96
            return 7 <= diagonal <= 12
        except:
            return False

    def setup_window_size(self):
        """Настраивает размер окна в зависимости от устройства"""
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            if self.device_type == "mobile":
                self.root.attributes('-fullscreen', True)
                self.window_width = screen_width
                self.window_height = screen_height
            elif self.device_type == "tablet":
                self.window_width = min(800, screen_width - 100)
                self.window_height = min(1000, screen_height - 100)
                self.root.geometry(f"{self.window_width}x{self.window_height}")
            else:
                self.window_width = 600
                self.window_height = 750
                self.root.geometry(f"{self.window_width}x{self.window_height}")
        except:
            self.root.geometry("600x750")

    def setup_fonts(self):
        """Настраивает шрифты в зависимости от устройства"""
        if self.device_type == "mobile":
            self.fonts = {
                'title': ("Arial", 16, "bold"),
                'subtitle': ("Arial", 10),
                'button_large': ("Arial", 14, "bold"),
                'button_medium': ("Arial", 12, "bold"),
                'button_small': ("Arial", 10, "bold"),
                'card_title': ("Arial", 12, "bold"),
                'card_text': ("Arial", 9),
                'stats_large': ("Arial", 14, "bold"),
                'stats_medium': ("Arial", 11, "bold"),
                'stats_small': ("Arial", 9),
                'tab': ("Arial", 8, "bold")
            }
        elif self.device_type == "tablet":
            self.fonts = {
                'title': ("Arial", 18, "bold"),
                'subtitle': ("Arial", 11),
                'button_large': ("Arial", 16, "bold"),
                'button_medium': ("Arial", 13, "bold"),
                'button_small': ("Arial", 11, "bold"),
                'card_title': ("Arial", 13, "bold"),
                'card_text': ("Arial", 10),
                'stats_large': ("Arial", 16, "bold"),
                'stats_medium': ("Arial", 12, "bold"),
                'stats_small': ("Arial", 10),
                'tab': ("Arial", 9, "bold")
            }
        else:
            self.fonts = {
                'title': ("Arial", 18, "bold"),
                'subtitle': ("Arial", 10),
                'button_large': ("Arial", 16, "bold"),
                'button_medium': ("Arial", 12, "bold"),
                'button_small': ("Arial", 9, "bold"),
                'card_title': ("Arial", 12, "bold"),
                'card_text': ("Arial", 9),
                'stats_large': ("Arial", 14, "bold"),
                'stats_medium': ("Arial", 11, "bold"),
                'stats_small': ("Arial", 9),
                'tab': ("Arial", 9, "bold")
            }

    def setup_mobile_bindings(self):
        """Настройка жестов для мобильных устройств"""
        if self.device_type == "mobile":
            self.root.bind('<Left>', self.previous_tab)
            self.root.bind('<Right>', self.next_tab)
            self.root.bind('<ButtonPress-1>', self.start_long_press)
            self.root.bind('<ButtonRelease-1>', self.end_long_press)
            self.root.bind('<Double-Button-1>', self.double_tap)

    def previous_tab(self, event=None):
        """Переход к предыдущей вкладке"""
        current = self.notebook.index(self.notebook.select())
        if current > 0:
            self.notebook.select(current - 1)

    def next_tab(self, event=None):
        """Переход к следующей вкладке"""
        current = self.notebook.index(self.notebook.select())
        if current < len(self.notebook.tabs()) - 1:
            self.notebook.select(current + 1)

    def start_long_press(self, event):
        """Начало долгого нажатия"""
        self.long_press_time = datetime.now()
        self.long_press_job = self.root.after(1000, self.execute_long_press, event.widget)

    def end_long_press(self, event):
        """Конец долгого нажатия"""
        if hasattr(self, 'long_press_job'):
            self.root.after_cancel(self.long_press_job)

    def execute_long_press(self, widget):
        """Выполнение действия при долгом нажатии"""
        if hasattr(widget, 'long_press_action'):
            widget.long_press_action()

    def double_tap(self, event):
        """Обработка двойного нажатия"""
        widget = event.widget
        if hasattr(widget, 'double_tap_action'):
            widget.double_tap_action()

    def initialize_new_game(self):
        """Инициализация новой игры"""
        self.money = 0
        self.bitcoins = 0
        self.total_clicks = 0
        self.click_power = 1
        self.auto_click_power = 0
        self.passive_income = 0
        self.initialized = True
        self.stock_history_length = 10
        self.last_update = datetime.now()

        # Биржевые активы
        self.stocks = {
            "🚀 TechCorp": {"price": 100, "owned": 0, "volatility": 0.1, "history": [100]},
            "💎 CryptoCoin": {"price": 50, "owned": 0, "volatility": 0.15, "history": [50]},
            "🛢️ OilGlobal": {"price": 80, "owned": 0, "volatility": 0.08, "history": [80]},
            "🏦 BankGroup": {"price": 120, "owned": 0, "volatility": 0.06, "history": [120]},
            "₿ Bitcoin": {"price": 50000, "owned": 0, "volatility": 0.2, "history": [50000]}
        }

        # Недвижимость - реалистичные цены и доходы
        self.real_estate = {
            "🏠 Домик": {
                "bitcoin_cost": 0.001,
                "income": 5,
                "owned": 0,
                "emoji": "🏠",
                "description": "Сдача в аренду"
            },
            "🏡 Дача": {
                "bitcoin_cost": 0.005,
                "income": 25,
                "owned": 0,
                "emoji": "🏡",
                "description": "Сезонная аренда"
            },
            "🏘️ Таунхаус": {
                "bitcoin_cost": 0.01,
                "income": 50,
                "owned": 0,
                "emoji": "🏘️",
                "description": "Аренда семьям"
            },
            "🏢 Квартира": {
                "bitcoin_cost": 0.02,
                "income": 100,
                "owned": 0,
                "emoji": "🏢",
                "description": "Долгосрочная аренда"
            },
            "🏬 Офис": {
                "bitcoin_cost": 0.05,
                "income": 200,
                "owned": 0,
                "emoji": "🏬",
                "description": "Аренда бизнесу"
            },
            "🏨 Отель": {
                "bitcoin_cost": 0.1,
                "income": 500,
                "owned": 0,
                "emoji": "🏨",
                "description": "Гостиничный бизнес"
            },
            "🏰 Вилла": {
                "bitcoin_cost": 0.2,
                "income": 1000,
                "owned": 0,
                "emoji": "🏰",
                "description": "Элитная аренда"
            },
            "🏛️ Дворец": {
                "bitcoin_cost": 0.5,
                "income": 2500,
                "owned": 0,
                "emoji": "🏛️",
                "description": "Роскошная недвижимость"
            },
            "🗼 Небоскреб": {
                "bitcoin_cost": 1.0,
                "income": 5000,
                "owned": 0,
                "emoji": "🗼",
                "description": "Коммерческая недвижимость"
            },
            "🏝️ Остров": {
                "bitcoin_cost": 2.0,
                "income": 10000,
                "owned": 0,
                "emoji": "🏝️",
                "description": "Эксклюзивная собственность"
            }
        }

        # Транспорт - реалистичные бонусы к доходу
        self.transport = {
            "🚲 Велосипед": {
                "bitcoin_cost": 0.0005,
                "bonus": 1.02,
                "owned": 0,
                "emoji": "🚲",
                "description": "Увеличивает эффективность"
            },
            "🛵 Мопед": {
                "bitcoin_cost": 0.001,
                "bonus": 1.05,
                "owned": 0,
                "emoji": "🛵",
                "description": "Быстрая доставка"
            },
            "🏍️ Мотоцикл": {
                "bitcoin_cost": 0.002,
                "bonus": 1.08,
                "owned": 0,
                "emoji": "🏍️",
                "description": "Мобильность бизнеса"
            },
            "🚗 Седан": {
                "bitcoin_cost": 0.005,
                "bonus": 1.12,
                "owned": 0,
                "emoji": "🚗",
                "description": "Комфортные поездки"
            },
            "🚙 Внедорожник": {
                "bitcoin_cost": 0.01,
                "bonus": 1.18,
                "owned": 0,
                "emoji": "🚙",
                "description": "Доступ к новым рынкам"
            },
            "🏎️ Спорткар": {
                "bitcoin_cost": 0.02,
                "bonus": 1.25,
                "owned": 0,
                "emoji": "🏎️",
                "description": "Престиж и скорость"
            },
            "🚁 Вертолет": {
                "bitcoin_cost": 0.05,
                "bonus": 1.35,
                "owned": 0,
                "emoji": "🚁",
                "description": "Быстрые деловые поездки"
            },
            "✈️ Самолет": {
                "bitcoin_cost": 0.1,
                "bonus": 1.5,
                "owned": 0,
                "emoji": "✈️",
                "description": "Международный бизнес"
            },
            "🛥️ Яхта": {
                "bitcoin_cost": 0.2,
                "bonus": 1.7,
                "owned": 0,
                "emoji": "🛥️",
                "description": "Элитные переговоры"
            },
            "🚀 Ракета": {
                "bitcoin_cost": 0.5,
                "bonus": 2.0,
                "owned": 0,
                "emoji": "🚀",
                "description": "Космический бизнес"
            }
        }

        self.upgrades = {
            "🚀 Улучшение клика": {"cost": 10, "power": 1, "count": 0, "emoji": "🚀", "description": "+1 к силе клика"},
            "💎 Усилитель клика": {"cost": 200, "power": 5, "count": 0, "emoji": "💎", "description": "+5 к силе клика"},
            "🌟 Супер клик": {"cost": 500, "power": 10, "count": 0, "emoji": "🌟", "description": "+10 к силе клика"},
            "⚡ Множитель x2": {"cost": 1000, "power": 2, "count": 0, "emoji": "⚡", "multiplier": True,
                               "description": "x2 к доходу с клика"}
        }

    def save_game(self):
        """Сохранение игры"""
        save_data = {
            'money': self.money,
            'bitcoins': self.bitcoins,
            'total_clicks': self.total_clicks,
            'click_power': self.click_power,
            'auto_click_power': self.auto_click_power,
            'passive_income': self.passive_income,
            'stocks': self.stocks,
            'real_estate': self.real_estate,
            'transport': self.transport,
            'upgrades': self.upgrades,
            'stock_history_length': self.stock_history_length,
            'initialized': True
        }

        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_game(self):
        """Загрузка игры"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)

                for key, value in save_data.items():
                    setattr(self, key, value)
                print("Игра загружена!")
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.initialize_new_game()
        else:
            self.initialize_new_game()

    def start_passive_income(self):
        """Запуск пассивного дохода от недвижимости"""
        self.update_passive_income()

    def update_passive_income(self):
        """Обновление пассивного дохода"""
        income = self.get_real_estate_income()
        if income > 0:
            self.money += income
            self.update_display()
            self.save_game()

        self.root.after(1000, self.update_passive_income)

    def get_real_estate_income(self):
        """Рассчитывает общий доход от недвижимости"""
        total = 0
        for estate in self.real_estate.values():
            total += estate['income'] * estate['owned']
        return total

    def get_transport_bonus(self):
        """Рассчитывает общий бонус от транспорта"""
        bonus = 1.0
        for transport in self.transport.values():
            if transport['owned'] > 0:
                bonus *= transport['bonus']
        return bonus

    def create_modern_ui(self):
        # Создаем Notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Настройка стиля вкладок для мобильных устройств
        self.setup_notebook_style()

        # Вкладки
        self.clicker_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.stock_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.bitcoin_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.estate_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.transport_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.portfolio_tab = tk.Frame(self.notebook, bg=self.colors['bg'])

        self.notebook.add(self.clicker_tab, text="🎮 Кликер")
        self.notebook.add(self.bitcoin_tab, text="₿ Биткоины")
        self.notebook.add(self.stock_tab, text="📈 Биржа")
        self.notebook.add(self.estate_tab, text="🏠 Недвижимость")
        self.notebook.add(self.transport_tab, text="🚗 Транспорт")
        self.notebook.add(self.portfolio_tab, text="💼 Портфель")

        self.create_clicker_ui()
        self.create_bitcoin_ui()
        self.create_stock_ui()
        self.create_estate_ui()
        self.create_transport_ui()
        self.create_portfolio_ui()

        # Кнопка сохранения внизу
        self.create_bottom_controls()

    def setup_notebook_style(self):
        """Настройка стиля Notebook для разных устройств"""
        style = ttk.Style()

        if self.device_type == "mobile":
            tab_padding = [10, 5]
            font = self.fonts['tab']
        elif self.device_type == "tablet":
            tab_padding = [15, 8]
            font = self.fonts['tab']
        else:
            tab_padding = [15, 5]
            font = self.fonts['tab']

        style.configure("TNotebook", background=self.colors['bg'], borderwidth=0)
        style.configure("TNotebook.Tab",
                        background='#1a1a2e',
                        foreground='#94a3b8',
                        padding=tab_padding,
                        font=font)
        style.map("TNotebook.Tab",
                  background=[("selected", self.colors['accent'])],
                  foreground=[("selected", 'white')])

    def create_bottom_controls(self):
        """Создание нижней панели управления"""
        bottom_frame = tk.Frame(self.root, bg=self.colors['bg'])
        bottom_frame.pack(fill='x', pady=5)

        if self.device_type == "mobile":
            button_height = 3
            font = self.fonts['button_medium']
        else:
            button_height = 2
            font = self.fonts['button_small']

        # Кнопка сохранения
        save_btn = tk.Button(bottom_frame, text="💾 Сохранить",
                             font=font,
                             bg=self.colors['accent2'],
                             fg='white',
                             command=self.save_game,
                             height=button_height)
        save_btn.pack(side='left', fill='x', expand=True, padx=2)

        # Кнопка сброса
        reset_btn = tk.Button(bottom_frame, text="🔄 Сброс",
                              font=font,
                              bg=self.colors['warning'],
                              fg='white',
                              command=self.reset_game,
                              height=button_height)
        reset_btn.pack(side='left', fill='x', expand=True, padx=2)

        # Кнопка выхода на мобильных
        if self.device_type == "mobile":
            exit_btn = tk.Button(bottom_frame, text="🚪 Выход",
                                 font=font,
                                 bg=self.colors['danger'],
                                 fg='white',
                                 command=self.root.quit,
                                 height=button_height)
            exit_btn.pack(side='left', fill='x', expand=True, padx=2)

    def create_clicker_ui(self):
        if self.device_type == "mobile":
            self.create_mobile_clicker_ui()
        else:
            self.create_desktop_clicker_ui()

    def create_mobile_clicker_ui(self):
        """Создание интерфейса кликера для мобильных устройств"""
        main_frame = tk.Frame(self.clicker_tab, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Заголовок
        title_label = tk.Label(main_frame, text="🌌 Cosmic Clicker",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        # Основная кнопка кликера
        self.create_mobile_main_button(main_frame)

        # Статистика под кнопкой
        self.create_mobile_stats_card(main_frame)

        # Улучшения с вертикальным скроллингом
        self.create_mobile_upgrades_section(main_frame)

    def create_desktop_clicker_ui(self):
        """Создание интерфейса кликера для десктопов"""
        canvas = tk.Canvas(self.clicker_tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.clicker_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = scrollable_frame

        title_label = tk.Label(main_frame, text="🌌 Cosmic Clicker",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        subtitle_label = tk.Label(main_frame, text="Кликай по кнопке чтобы зарабатывать деньги!",
                                  font=self.fonts['subtitle'],
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg'])
        subtitle_label.pack(pady=(0, 10))

        self.create_stats_card(main_frame)
        self.create_main_button(main_frame)
        self.create_upgrades_section(main_frame)

    def create_stats_card(self, parent):
        stats_card = tk.Frame(parent, bg=self.colors['card_bg'],
                              relief='flat', bd=1, highlightthickness=1,
                              highlightbackground=self.colors['accent2'])
        stats_card.pack(fill='x', pady=5, padx=10)

        # Верхняя строка - основные валюты
        top_frame = tk.Frame(stats_card, bg=self.colors['card_bg'])
        top_frame.pack(fill='x', padx=10, pady=5)

        self.money_label = tk.Label(top_frame, text=f"💰 {self.money:,}₽",
                                    font=self.fonts['stats_large'],
                                    fg=self.colors['success'],
                                    bg=self.colors['card_bg'])
        self.money_label.pack(side='left')

        self.bitcoin_label = tk.Label(top_frame, text=f"₿ {self.bitcoins:.4f}",
                                      font=self.fonts['stats_medium'],
                                      fg=self.colors['bitcoin'],
                                      bg=self.colors['card_bg'])
        self.bitcoin_label.pack(side='right')

        # Нижняя строка - статистика
        bottom_frame = tk.Frame(stats_card, bg=self.colors['card_bg'])
        bottom_frame.pack(fill='x', padx=10, pady=5)

        self.power_label = tk.Label(bottom_frame,
                                    text=f"⚡{self.click_power}/клик",
                                    font=self.fonts['stats_small'],
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['card_bg'])
        self.power_label.pack(side='left')

        passive_income = self.get_real_estate_income() * self.get_transport_bonus()
        self.passive_label = tk.Label(bottom_frame,
                                      text=f"🔄{passive_income:.0f}/сек",
                                      font=self.fonts['stats_small'],
                                      fg=self.colors['text_secondary'],
                                      bg=self.colors['card_bg'])
        self.passive_label.pack(side='left', padx=10)

        self.clicks_label = tk.Label(bottom_frame,
                                     text=f"👆{self.total_clicks}",
                                     font=self.fonts['stats_small'],
                                     fg=self.colors['text_secondary'],
                                     bg=self.colors['card_bg'])
        self.clicks_label.pack(side='right')

    def create_mobile_stats_card(self, parent):
        """Создание карточки статистики для мобильных"""
        stats_card = tk.Frame(parent, bg=self.colors['card_bg'],
                              relief='flat', bd=1, highlightthickness=1,
                              highlightbackground=self.colors['accent2'])
        stats_card.pack(fill='x', pady=10, padx=5)

        content_frame = tk.Frame(stats_card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=10, pady=8)

        # Деньги
        self.money_label = tk.Label(content_frame, text=f"💰 {self.money:,}₽",
                                    font=self.fonts['stats_large'],
                                    fg=self.colors['success'],
                                    bg=self.colors['card_bg'])
        self.money_label.pack(anchor='w', pady=2)

        # Биткоины
        self.bitcoin_label = tk.Label(content_frame, text=f"₿ {self.bitcoins:.4f}",
                                      font=self.fonts['stats_medium'],
                                      fg=self.colors['bitcoin'],
                                      bg=self.colors['card_bg'])
        self.bitcoin_label.pack(anchor='w', pady=2)

        # Статистика в строку
        stats_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        stats_frame.pack(fill='x', pady=5)

        self.power_label = tk.Label(stats_frame,
                                    text=f"⚡{self.click_power}/клик",
                                    font=self.fonts['stats_small'],
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['card_bg'])
        self.power_label.pack(side='left')

        passive_income = self.get_real_estate_income() * self.get_transport_bonus()
        self.passive_label = tk.Label(stats_frame,
                                      text=f"🔄{passive_income:.0f}/сек",
                                      font=self.fonts['stats_small'],
                                      fg=self.colors['text_secondary'],
                                      bg=self.colors['card_bg'])
        self.passive_label.pack(side='left', padx=20)

        self.clicks_label = tk.Label(stats_frame,
                                     text=f"👆{self.total_clicks}",
                                     font=self.fonts['stats_small'],
                                     fg=self.colors['text_secondary'],
                                     bg=self.colors['card_bg'])
        self.clicks_label.pack(side='right')

    def create_main_button(self, parent):
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(pady=10)

        self.click_button = tk.Button(button_frame,
                                      text="🚀\nКЛИКАЙ!\n🚀",
                                      font=self.fonts['button_large'],
                                      bg=self.colors['accent2'],
                                      fg='white',
                                      command=self.click,
                                      width=15,
                                      height=4,
                                      relief='flat',
                                      bd=0,
                                      cursor='hand2')
        self.click_button.pack()

        def on_enter(e):
            self.click_button.configure(bg=self.colors['accent'])

        def on_leave(e):
            self.click_button.configure(bg=self.colors['accent2'])

        self.click_button.bind("<Enter>", on_enter)
        self.click_button.bind("<Leave>", on_leave)

    def create_mobile_main_button(self, parent):
        """Создание основной кнопки для мобильных"""
        button_frame = tk.Frame(parent, bg=self.colors['bg'])
        button_frame.pack(pady=20, fill='x')

        self.click_button = tk.Button(button_frame,
                                      text="🚀\nКЛИКАЙ!\n🚀",
                                      font=self.fonts['button_large'],
                                      bg=self.colors['accent2'],
                                      fg='white',
                                      command=self.click,
                                      height=6 if self.device_type == "mobile" else 4,
                                      relief='flat',
                                      bd=0,
                                      cursor='hand2')
        self.click_button.pack(fill='both', expand=True)

        # Добавляем поддержку жестов
        self.click_button.long_press_action = self.start_auto_click
        self.click_button.double_tap_action = self.mega_click

        def on_enter(e):
            self.click_button.configure(bg=self.colors['accent'])

        def on_leave(e):
            self.click_button.configure(bg=self.colors['accent2'])

        self.click_button.bind("<Enter>", on_enter)
        self.click_button.bind("<Leave>", on_leave)

    def create_upgrades_section(self, parent):
        upgrades_frame = tk.Frame(parent, bg=self.colors['bg'])
        upgrades_frame.pack(fill='both', expand=True, pady=5)

        section_label = tk.Label(upgrades_frame, text="🛠️ УЛУЧШЕНИЯ КЛИКОВ",
                                 font=self.fonts['card_title'],
                                 fg=self.colors['text'],
                                 bg=self.colors['bg'])
        section_label.pack(anchor='w', pady=(0, 10), padx=10)

        self.upgrades_container = tk.Frame(upgrades_frame, bg=self.colors['bg'])
        self.upgrades_container.pack(fill='both', expand=True, padx=10)

        self.upgrade_cards = {}

        for i, (upgrade_name, upgrade_info) in enumerate(self.upgrades.items()):
            frame = tk.Frame(self.upgrades_container, bg=self.colors['bg'])
            frame.pack(fill='x', pady=5)

            self.create_compact_upgrade_card(frame, upgrade_name, upgrade_info)

    def create_mobile_upgrades_section(self, parent):
        """Создание секции улучшений для мобильных"""
        upgrades_frame = tk.Frame(parent, bg=self.colors['bg'])
        upgrades_frame.pack(fill='both', expand=True, pady=5)

        section_label = tk.Label(upgrades_frame, text="🛠️ УЛУЧШЕНИЯ КЛИКОВ",
                                 font=self.fonts['card_title'],
                                 fg=self.colors['text'],
                                 bg=self.colors['bg'])
        section_label.pack(anchor='w', pady=(0, 10), padx=5)

        upgrades_container = tk.Frame(upgrades_frame, bg=self.colors['bg'])
        upgrades_container.pack(fill='both', expand=True)

        canvas = tk.Canvas(upgrades_container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(upgrades_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.upgrade_cards = {}
        for upgrade_name, upgrade_info in self.upgrades.items():
            self.create_mobile_upgrade_card(scrollable_frame, upgrade_name, upgrade_info)

    def create_compact_upgrade_card(self, parent, upgrade_name, upgrade_info):
        card = tk.Frame(parent,
                        bg=self.colors['card_bg'],
                        relief='flat',
                        bd=1,
                        highlightthickness=1,
                        highlightbackground='#2d3748')
        card.pack(fill='x', pady=3)

        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=10, pady=8)

        # Верхняя строка - название и количество
        top_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        top_frame.pack(fill='x', pady=2)

        name_label = tk.Label(top_frame,
                              text=f"{upgrade_info['emoji']} {upgrade_name}",
                              font=self.fonts['card_title'],
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        name_label.pack(side='left')

        count_label = tk.Label(top_frame,
                               text=f"Куплено: {upgrade_info['count']}",
                               font=self.fonts['card_text'],
                               fg=self.colors['warning'],
                               bg=self.colors['card_bg'])
        count_label.pack(side='right')

        # Описание улучшения
        desc_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        desc_frame.pack(fill='x', pady=2)

        desc_label = tk.Label(desc_frame,
                              text=upgrade_info['description'],
                              font=self.fonts['card_text'],
                              fg=self.colors['text_secondary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        desc_label.pack(fill='x')

        # Нижняя строка - цена и кнопка
        bottom_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        bottom_frame.pack(fill='x', pady=2)

        price_label = tk.Label(bottom_frame,
                               text=f"Цена: {upgrade_info['cost']}₽",
                               font=self.fonts['card_text'],
                               fg=self.colors['success'],
                               bg=self.colors['card_bg'])
        price_label.pack(side='left')

        buy_btn = tk.Button(bottom_frame,
                            text="КУПИТЬ УЛУЧШЕНИЕ",
                            font=self.fonts['button_small'],
                            bg=self.colors['accent2'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=lambda name=upgrade_name: self.buy_upgrade(name))
        buy_btn.pack(side='right')

        self.upgrade_cards[upgrade_name] = {
            'card': card,
            'count_label': count_label,
            'price_label': price_label,
            'button': buy_btn
        }

        self.update_upgrade_button_state(upgrade_name)

    def create_mobile_upgrade_card(self, parent, upgrade_name, upgrade_info):
        """Создание карточки улучшения для мобильных"""
        card = tk.Frame(parent,
                        bg=self.colors['card_bg'],
                        relief='flat',
                        bd=1,
                        highlightthickness=1,
                        highlightbackground='#2d3748')
        card.pack(fill='x', pady=3, padx=5)

        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=8, pady=6)

        name_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        name_frame.pack(fill='x', pady=2)

        name_label = tk.Label(name_frame,
                              text=f"{upgrade_info['emoji']} {upgrade_name}",
                              font=self.fonts['card_title'],
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        name_label.pack(side='left')

        count_label = tk.Label(name_frame,
                               text=f"{upgrade_info['count']} шт",
                               font=self.fonts['card_text'],
                               fg=self.colors['warning'],
                               bg=self.colors['card_bg'])
        count_label.pack(side='right')

        desc_label = tk.Label(content_frame,
                              text=upgrade_info['description'],
                              font=self.fonts['card_text'],
                              fg=self.colors['text_secondary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        desc_label.pack(fill='x', pady=2)

        action_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        action_frame.pack(fill='x', pady=2)

        price_label = tk.Label(action_frame,
                               text=f"{upgrade_info['cost']}₽",
                               font=self.fonts['card_text'],
                               fg=self.colors['success'],
                               bg=self.colors['card_bg'])
        price_label.pack(side='left')

        buy_btn = tk.Button(action_frame,
                            text="КУПИТЬ",
                            font=self.fonts['button_small'],
                            bg=self.colors['accent2'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=lambda name=upgrade_name: self.buy_upgrade(name))
        buy_btn.pack(side='right')

        self.upgrade_cards[upgrade_name] = {
            'card': card,
            'count_label': count_label,
            'price_label': price_label,
            'button': buy_btn
        }

        self.update_upgrade_button_state(upgrade_name)

    def update_upgrade_button_state(self, upgrade_name):
        """Обновляет состояние конкретной кнопки улучшения"""
        if upgrade_name in self.upgrade_cards:
            upgrade_info = self.upgrades[upgrade_name]
            card_data = self.upgrade_cards[upgrade_name]

            if self.money >= upgrade_info['cost']:
                card_data['button'].configure(bg=self.colors['accent2'], state='normal')
            else:
                card_data['button'].configure(bg='#475569', state='disabled')

    def update_upgrade_buttons(self):
        """Обновляет состояние ВСЕХ кнопок улучшений"""
        for upgrade_name in self.upgrades:
            self.update_upgrade_button_state(upgrade_name)

    # БИТКОИНЫ UI
    def create_bitcoin_ui(self):
        if self.device_type == "mobile":
            self.create_mobile_bitcoin_ui()
        else:
            self.create_desktop_bitcoin_ui()

    def create_desktop_bitcoin_ui(self):
        canvas = tk.Canvas(self.bitcoin_tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.bitcoin_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = scrollable_frame

        title_label = tk.Label(main_frame, text="₿ Покупка Биткоинов",
                               font=self.fonts['title'],
                               fg=self.colors['bitcoin'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        info_frame = tk.Frame(main_frame, bg=self.colors['card_bg'],
                              relief='flat', bd=1, highlightthickness=1,
                              highlightbackground=self.colors['bitcoin'])
        info_frame.pack(fill='x', pady=5, padx=10)

        rate_label = tk.Label(info_frame,
                              text="💰 1 Биткоин = 500,000 рублей",
                              font=self.fonts['card_title'],
                              fg=self.colors['bitcoin'],
                              bg=self.colors['card_bg'])
        rate_label.pack(pady=10)

        buy_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        buy_frame.pack(fill='x', pady=10, padx=10)

        input_frame = tk.Frame(buy_frame, bg=self.colors['bg'])
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Количество биткоинов:",
                 font=self.fonts['card_text'],
                 fg=self.colors['text'],
                 bg=self.colors['bg']).pack(side='left')

        self.bitcoin_qty_var = tk.StringVar(value="0.01")
        bitcoin_entry = tk.Entry(input_frame, textvariable=self.bitcoin_qty_var,
                                 width=10, font=self.fonts['card_text'],
                                 bg='#2d3748', fg='white', relief='flat')
        bitcoin_entry.pack(side='left', padx=5)

        buy_btn = tk.Button(buy_frame,
                            text="🛒 КУПИТЬ БИТКОИНЫ",
                            font=self.fonts['button_medium'],
                            bg=self.colors['bitcoin'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=self.buy_bitcoins,
                            height=2)
        buy_btn.pack(fill='x', pady=10)

        self.bitcoin_cost_label = tk.Label(buy_frame,
                                           text="Стоимость: 5,000 рублей",
                                           font=self.fonts['card_text'],
                                           fg=self.colors['text_secondary'],
                                           bg=self.colors['bg'])
        self.bitcoin_cost_label.pack()

        def update_cost(*args):
            try:
                qty = float(self.bitcoin_qty_var.get())
                cost = qty * 500000
                self.bitcoin_cost_label.config(text=f"Стоимость: {cost:,.0f} рублей")
            except:
                self.bitcoin_cost_label.config(text="Стоимость: -")

        if hasattr(self.bitcoin_qty_var, 'trace_add'):
            self.bitcoin_qty_var.trace_add('write', update_cost)
        else:
            self.bitcoin_qty_var.trace('w', update_cost)

        update_cost()

    def create_mobile_bitcoin_ui(self):
        main_frame = tk.Frame(self.bitcoin_tab, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        title_label = tk.Label(main_frame, text="₿ Покупка Биткоинов",
                               font=self.fonts['title'],
                               fg=self.colors['bitcoin'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        # Карточка курса
        rate_card = tk.Frame(main_frame, bg=self.colors['card_bg'],
                             relief='flat', bd=1, highlightthickness=1,
                             highlightbackground=self.colors['bitcoin'])
        rate_card.pack(fill='x', pady=5)

        rate_label = tk.Label(rate_card,
                              text="💰 1 Биткоин = 500,000 рублей",
                              font=self.fonts['card_title'],
                              fg=self.colors['bitcoin'],
                              bg=self.colors['card_bg'])
        rate_label.pack(pady=10)

        # Карточка покупки
        buy_card = tk.Frame(main_frame, bg=self.colors['card_bg'],
                            relief='flat', bd=1, highlightthickness=1,
                            highlightbackground='#2d3748')
        buy_card.pack(fill='x', pady=5)

        content_frame = tk.Frame(buy_card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=10, pady=10)

        input_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        input_frame.pack(fill='x', pady=5)

        tk.Label(input_frame, text="Количество BTC:",
                 font=self.fonts['card_text'],
                 fg=self.colors['text'],
                 bg=self.colors['card_bg']).pack(side='left')

        self.bitcoin_qty_var = tk.StringVar(value="0.01")
        bitcoin_entry = tk.Entry(input_frame, textvariable=self.bitcoin_qty_var,
                                 width=8, font=self.fonts['card_text'],
                                 bg='#2d3748', fg='white', relief='flat')
        bitcoin_entry.pack(side='left', padx=5)

        self.bitcoin_cost_label = tk.Label(content_frame,
                                           text="Стоимость: 5,000 рублей",
                                           font=self.fonts['card_text'],
                                           fg=self.colors['text_secondary'],
                                           bg=self.colors['card_bg'])
        self.bitcoin_cost_label.pack(pady=2)

        buy_btn = tk.Button(content_frame,
                            text="🛒 КУПИТЬ БИТКОИНЫ",
                            font=self.fonts['button_medium'],
                            bg=self.colors['bitcoin'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=self.buy_bitcoins)
        buy_btn.pack(fill='x', pady=10)

        def update_cost(*args):
            try:
                qty = float(self.bitcoin_qty_var.get())
                cost = qty * 500000
                self.bitcoin_cost_label.config(text=f"Стоимость: {cost:,.0f} рублей")
            except:
                self.bitcoin_cost_label.config(text="Стоимость: -")

        if hasattr(self.bitcoin_qty_var, 'trace_add'):
            self.bitcoin_qty_var.trace_add('write', update_cost)
        else:
            self.bitcoin_qty_var.trace('w', update_cost)

        update_cost()

    # БИРЖА UI
    def create_stock_ui(self):
        if self.device_type == "mobile":
            self.create_mobile_stock_ui()
        else:
            self.create_desktop_stock_ui()

    def create_desktop_stock_ui(self):
        canvas = tk.Canvas(self.stock_tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.stock_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = scrollable_frame

        title_label = tk.Label(main_frame, text="📈 Биржевые Активы",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        subtitle_label = tk.Label(main_frame,
                                  text="Покупайте и продавайте акции для получения прибыли",
                                  font=self.fonts['subtitle'],
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg'])
        subtitle_label.pack(pady=(0, 10))

        # Создаем карточки для каждого актива
        self.stock_cards = {}
        for stock_name, stock_info in self.stocks.items():
            self.create_stock_card(main_frame, stock_name, stock_info)

    def create_mobile_stock_ui(self):
        main_frame = tk.Frame(self.stock_tab, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        title_label = tk.Label(main_frame, text="📈 Биржевые Активы",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        # Контейнер для акций с скроллингом
        container = tk.Frame(main_frame, bg=self.colors['bg'])
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.stock_cards = {}
        for stock_name, stock_info in self.stocks.items():
            self.create_mobile_stock_card(scrollable_frame, stock_name, stock_info)

    def create_stock_card(self, parent, stock_name, stock_info):
        """Создание карточки акции для десктопа"""
        card = tk.Frame(parent,
                        bg=self.colors['card_bg'],
                        relief='flat',
                        bd=1,
                        highlightthickness=1,
                        highlightbackground='#2d3748')
        card.pack(fill='x', pady=3, padx=10)

        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=8, pady=6)

        # Верхняя строка - название и цена
        top_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        top_frame.pack(fill='x', pady=2)

        name_label = tk.Label(top_frame,
                              text=f"{stock_name}",
                              font=self.fonts['card_title'],
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        name_label.pack(side='left')

        price_label = tk.Label(top_frame,
                               text=f"Цена: {stock_info['price']:,.0f}₽",
                               font=self.fonts['card_text'],
                               fg=self.colors['success'],
                               bg=self.colors['card_bg'])
        price_label.pack(side='right')

        # Средняя строка - владение и изменение цены
        middle_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        middle_frame.pack(fill='x', pady=2)

        owned_label = tk.Label(middle_frame,
                               text=f"Владеете: {stock_info['owned']} акций",
                               font=self.fonts['card_text'],
                               fg=self.colors['warning'],
                               bg=self.colors['card_bg'],
                               anchor='w')
        owned_label.pack(side='left')

        # Нижняя строка - кнопки покупки/продажи
        bottom_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        bottom_frame.pack(fill='x', pady=2)

        buy_btn = tk.Button(bottom_frame,
                            text="КУПИТЬ 1",
                            font=self.fonts['button_small'],
                            bg=self.colors['success'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=lambda: self.buy_stock(stock_name, 1))
        buy_btn.pack(side='left', padx=(0, 5))

        sell_btn = tk.Button(bottom_frame,
                             text="ПРОДАТЬ 1",
                             font=self.fonts['button_small'],
                             bg=self.colors['danger'],
                             fg='white',
                             relief='flat',
                             cursor='hand2',
                             command=lambda: self.sell_stock(stock_name, 1))
        sell_btn.pack(side='left')

        self.stock_cards[stock_name] = {
            'card': card,
            'price_label': price_label,
            'owned_label': owned_label,
            'buy_button': buy_btn,
            'sell_button': sell_btn
        }

    def create_mobile_stock_card(self, parent, stock_name, stock_info):
        """Создание карточки акции для мобильных"""
        card = tk.Frame(parent,
                        bg=self.colors['card_bg'],
                        relief='flat',
                        bd=1,
                        highlightthickness=1,
                        highlightbackground='#2d3748')
        card.pack(fill='x', pady=3, padx=5)

        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=8, pady=6)

        # Заголовок
        name_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        name_frame.pack(fill='x', pady=2)

        name_label = tk.Label(name_frame,
                              text=f"{stock_name}",
                              font=self.fonts['card_title'],
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        name_label.pack(side='left')

        price_label = tk.Label(name_frame,
                               text=f"{stock_info['price']:,.0f}₽",
                               font=self.fonts['card_text'],
                               fg=self.colors['success'],
                               bg=self.colors['card_bg'])
        price_label.pack(side='right')

        # Информация
        info_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        info_frame.pack(fill='x', pady=2)

        owned_label = tk.Label(info_frame,
                               text=f"Владеете: {stock_info['owned']}",
                               font=self.fonts['card_text'],
                               fg=self.colors['warning'],
                               bg=self.colors['card_bg'])
        owned_label.pack(side='left')

        # Кнопки
        button_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        button_frame.pack(fill='x', pady=2)

        buy_btn = tk.Button(button_frame,
                            text="КУПИТЬ",
                            font=self.fonts['button_small'],
                            bg=self.colors['success'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=lambda: self.buy_stock(stock_name, 1))
        buy_btn.pack(side='left', fill='x', expand=True, padx=(0, 2))

        sell_btn = tk.Button(button_frame,
                             text="ПРОДАТЬ",
                             font=self.fonts['button_small'],
                             bg=self.colors['danger'],
                             fg='white',
                             relief='flat',
                             cursor='hand2',
                             command=lambda: self.sell_stock(stock_name, 1))
        sell_btn.pack(side='left', fill='x', expand=True, padx=(2, 0))

        self.stock_cards[stock_name] = {
            'card': card,
            'price_label': price_label,
            'owned_label': owned_label,
            'buy_button': buy_btn,
            'sell_button': sell_btn
        }

    # НЕДВИЖИМОСТЬ UI
    def create_estate_ui(self):
        if self.device_type == "mobile":
            self.create_mobile_estate_ui()
        else:
            self.create_desktop_estate_ui()

    def create_desktop_estate_ui(self):
        canvas = tk.Canvas(self.estate_tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.estate_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = scrollable_frame

        title_label = tk.Label(main_frame, text="🏠 Недвижимость за Биткоины",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        subtitle_label = tk.Label(main_frame,
                                  text="Покупайте недвижимость чтобы получать пассивный доход каждую секунду",
                                  font=self.fonts['subtitle'],
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg'])
        subtitle_label.pack(pady=(0, 10))

        # Компактные карточки недвижимости
        self.estate_cards = {}
        for estate_name, estate_info in self.real_estate.items():
            self.create_compact_estate_card(main_frame, estate_name, estate_info)

    def create_mobile_estate_ui(self):
        main_frame = tk.Frame(self.estate_tab, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        title_label = tk.Label(main_frame, text="🏠 Недвижимость",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        # Контейнер с скроллингом
        container = tk.Frame(main_frame, bg=self.colors['bg'])
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.estate_cards = {}
        for estate_name, estate_info in self.real_estate.items():
            self.create_mobile_estate_card(scrollable_frame, estate_name, estate_info)

    def create_compact_estate_card(self, parent, estate_name, estate_info):
        card = tk.Frame(parent,
                        bg=self.colors['card_bg'],
                        relief='flat',
                        bd=1,
                        highlightthickness=1,
                        highlightbackground='#2d3748')
        card.pack(fill='x', pady=3, padx=10)

        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=8, pady=6)

        # Левая часть - информация
        left_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        left_frame.pack(side='left', fill='x', expand=True)

        name_label = tk.Label(left_frame,
                              text=f"{estate_info['emoji']} {estate_name}",
                              font=self.fonts['card_title'],
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        name_label.pack(fill='x')

        info_label = tk.Label(left_frame,
                              text=f"Доход: +{estate_info['income']}₽/сек • {estate_info['description']}",
                              font=self.fonts['card_text'],
                              fg=self.colors['text_secondary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        info_label.pack(fill='x')

        owned_label = tk.Label(left_frame,
                               text=f"Куплено: {estate_info['owned']}",
                               font=self.fonts['card_text'],
                               fg=self.colors['warning'],
                               bg=self.colors['card_bg'],
                               anchor='w')
        owned_label.pack(fill='x')

        # Правая часть - цена и кнопка
        right_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        right_frame.pack(side='right')

        price_label = tk.Label(right_frame,
                               text=f"₿{estate_info['bitcoin_cost']:.3f}",
                               font=self.fonts['card_title'],
                               fg=self.colors['bitcoin'],
                               bg=self.colors['card_bg'])
        price_label.pack()

        buy_btn = tk.Button(right_frame,
                            text="КУПИТЬ",
                            font=self.fonts['button_small'],
                            bg=self.colors['bitcoin'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=lambda: self.buy_real_estate(estate_name))
        buy_btn.pack(fill='x')

        self.estate_cards[estate_name] = {
            'card': card,
            'info_label': info_label,
            'owned_label': owned_label,
            'button': buy_btn
        }

    def create_mobile_estate_card(self, parent, estate_name, estate_info):
        """Создание карточки недвижимости для мобильных"""
        card = tk.Frame(parent,
                        bg=self.colors['card_bg'],
                        relief='flat',
                        bd=1,
                        highlightthickness=1,
                        highlightbackground='#2d3748')
        card.pack(fill='x', pady=3, padx=5)

        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=8, pady=6)

        # Заголовок
        name_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        name_frame.pack(fill='x', pady=2)

        name_label = tk.Label(name_frame,
                              text=f"{estate_info['emoji']} {estate_name}",
                              font=self.fonts['card_title'],
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'])
        name_label.pack(side='left')

        price_label = tk.Label(name_frame,
                               text=f"₿{estate_info['bitcoin_cost']:.3f}",
                               font=self.fonts['card_text'],
                               fg=self.colors['bitcoin'],
                               bg=self.colors['card_bg'])
        price_label.pack(side='right')

        # Информация
        info_label = tk.Label(content_frame,
                              text=f"Доход: +{estate_info['income']}₽/сек",
                              font=self.fonts['card_text'],
                              fg=self.colors['text_secondary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        info_label.pack(fill='x', pady=1)

        desc_label = tk.Label(content_frame,
                              text=estate_info['description'],
                              font=self.fonts['card_text'],
                              fg=self.colors['text_secondary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        desc_label.pack(fill='x', pady=1)

        # Владение и кнопка
        action_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        action_frame.pack(fill='x', pady=2)

        owned_label = tk.Label(action_frame,
                               text=f"Куплено: {estate_info['owned']}",
                               font=self.fonts['card_text'],
                               fg=self.colors['warning'],
                               bg=self.colors['card_bg'])
        owned_label.pack(side='left')

        buy_btn = tk.Button(action_frame,
                            text="КУПИТЬ",
                            font=self.fonts['button_small'],
                            bg=self.colors['bitcoin'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=lambda: self.buy_real_estate(estate_name))
        buy_btn.pack(side='right')

        self.estate_cards[estate_name] = {
            'card': card,
            'info_label': info_label,
            'owned_label': owned_label,
            'button': buy_btn
        }

    # ТРАНСПОРТ UI
    def create_transport_ui(self):
        if self.device_type == "mobile":
            self.create_mobile_transport_ui()
        else:
            self.create_desktop_transport_ui()

    def create_desktop_transport_ui(self):
        canvas = tk.Canvas(self.transport_tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.transport_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = scrollable_frame

        title_label = tk.Label(main_frame, text="🚗 Транспорт за Биткоины",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        subtitle_label = tk.Label(main_frame,
                                  text="Покупайте транспорт чтобы увеличивать эффективность бизнеса",
                                  font=self.fonts['subtitle'],
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg'])
        subtitle_label.pack(pady=(0, 10))

        bonus_label = tk.Label(main_frame,
                               text=f"Общий бонус эффективности: x{self.get_transport_bonus():.2f}",
                               font=self.fonts['card_title'],
                               fg=self.colors['success'],
                               bg=self.colors['bg'])
        bonus_label.pack(pady=(0, 10))

        # Компактные карточки транспорта
        self.transport_cards = {}
        for transport_name, transport_info in self.transport.items():
            self.create_compact_transport_card(main_frame, transport_name, transport_info)

    def create_mobile_transport_ui(self):
        main_frame = tk.Frame(self.transport_tab, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        title_label = tk.Label(main_frame, text="🚗 Транспорт",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        # Бонус эффективности
        bonus_card = tk.Frame(main_frame, bg=self.colors['card_bg'],
                              relief='flat', bd=1, highlightthickness=1,
                              highlightbackground=self.colors['success'])
        bonus_card.pack(fill='x', pady=5)

        bonus_label = tk.Label(bonus_card,
                               text=f"Общий бонус эффективности: x{self.get_transport_bonus():.2f}",
                               font=self.fonts['card_title'],
                               fg=self.colors['success'],
                               bg=self.colors['card_bg'])
        bonus_label.pack(pady=10)

        # Контейнер с скроллингом
        container = tk.Frame(main_frame, bg=self.colors['bg'])
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.transport_cards = {}
        for transport_name, transport_info in self.transport.items():
            self.create_mobile_transport_card(scrollable_frame, transport_name, transport_info)

    def create_compact_transport_card(self, parent, transport_name, transport_info):
        card = tk.Frame(parent,
                        bg=self.colors['card_bg'],
                        relief='flat',
                        bd=1,
                        highlightthickness=1,
                        highlightbackground='#2d3748')
        card.pack(fill='x', pady=3, padx=10)

        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=8, pady=6)

        # Левая часть - информация
        left_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        left_frame.pack(side='left', fill='x', expand=True)

        name_label = tk.Label(left_frame,
                              text=f"{transport_info['emoji']} {transport_name}",
                              font=self.fonts['card_title'],
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        name_label.pack(fill='x')

        info_label = tk.Label(left_frame,
                              text=f"Бонус: x{transport_info['bonus']} • {transport_info['description']}",
                              font=self.fonts['card_text'],
                              fg=self.colors['text_secondary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        info_label.pack(fill='x')

        owned_label = tk.Label(left_frame,
                               text=f"Куплено: {transport_info['owned']}",
                               font=self.fonts['card_text'],
                               fg=self.colors['warning'],
                               bg=self.colors['card_bg'],
                               anchor='w')
        owned_label.pack(fill='x')

        # Правая часть - цена и кнопка
        right_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        right_frame.pack(side='right')

        price_label = tk.Label(right_frame,
                               text=f"₿{transport_info['bitcoin_cost']:.3f}",
                               font=self.fonts['card_title'],
                               fg=self.colors['bitcoin'],
                               bg=self.colors['card_bg'])
        price_label.pack()

        buy_btn = tk.Button(right_frame,
                            text="КУПИТЬ",
                            font=self.fonts['button_small'],
                            bg=self.colors['bitcoin'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=lambda: self.buy_transport(transport_name))
        buy_btn.pack(fill='x')

        self.transport_cards[transport_name] = {
            'card': card,
            'info_label': info_label,
            'owned_label': owned_label,
            'button': buy_btn
        }

    def create_mobile_transport_card(self, parent, transport_name, transport_info):
        """Создание карточки транспорта для мобильных"""
        card = tk.Frame(parent,
                        bg=self.colors['card_bg'],
                        relief='flat',
                        bd=1,
                        highlightthickness=1,
                        highlightbackground='#2d3748')
        card.pack(fill='x', pady=3, padx=5)

        content_frame = tk.Frame(card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=8, pady=6)

        # Заголовок
        name_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        name_frame.pack(fill='x', pady=2)

        name_label = tk.Label(name_frame,
                              text=f"{transport_info['emoji']} {transport_name}",
                              font=self.fonts['card_title'],
                              fg=self.colors['text'],
                              bg=self.colors['card_bg'])
        name_label.pack(side='left')

        price_label = tk.Label(name_frame,
                               text=f"₿{transport_info['bitcoin_cost']:.3f}",
                               font=self.fonts['card_text'],
                               fg=self.colors['bitcoin'],
                               bg=self.colors['card_bg'])
        price_label.pack(side='right')

        # Информация
        info_label = tk.Label(content_frame,
                              text=f"Бонус: x{transport_info['bonus']}",
                              font=self.fonts['card_text'],
                              fg=self.colors['text_secondary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        info_label.pack(fill='x', pady=1)

        desc_label = tk.Label(content_frame,
                              text=transport_info['description'],
                              font=self.fonts['card_text'],
                              fg=self.colors['text_secondary'],
                              bg=self.colors['card_bg'],
                              anchor='w')
        desc_label.pack(fill='x', pady=1)

        # Владение и кнопка
        action_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
        action_frame.pack(fill='x', pady=2)

        owned_label = tk.Label(action_frame,
                               text=f"Куплено: {transport_info['owned']}",
                               font=self.fonts['card_text'],
                               fg=self.colors['warning'],
                               bg=self.colors['card_bg'])
        owned_label.pack(side='left')

        buy_btn = tk.Button(action_frame,
                            text="КУПИТЬ",
                            font=self.fonts['button_small'],
                            bg=self.colors['bitcoin'],
                            fg='white',
                            relief='flat',
                            cursor='hand2',
                            command=lambda: self.buy_transport(transport_name))
        buy_btn.pack(side='right')

        self.transport_cards[transport_name] = {
            'card': card,
            'info_label': info_label,
            'owned_label': owned_label,
            'button': buy_btn
        }

    # ПОРТФЕЛЬ UI
    def create_portfolio_ui(self):
        if self.device_type == "mobile":
            self.create_mobile_portfolio_ui()
        else:
            self.create_desktop_portfolio_ui()

    def create_desktop_portfolio_ui(self):
        canvas = tk.Canvas(self.portfolio_tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.portfolio_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = scrollable_frame

        title_label = tk.Label(main_frame, text="💼 Ваш Портфель",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        # Общая статистика
        self.create_portfolio_stats(main_frame)

        # Детали портфеля
        self.create_portfolio_details(main_frame)

    def create_mobile_portfolio_ui(self):
        main_frame = tk.Frame(self.portfolio_tab, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        title_label = tk.Label(main_frame, text="💼 Портфель",
                               font=self.fonts['title'],
                               fg=self.colors['accent'],
                               bg=self.colors['bg'])
        title_label.pack(pady=10)

        # Контейнер с скроллингом
        container = tk.Frame(main_frame, bg=self.colors['bg'])
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_mobile_portfolio_stats(scrollable_frame)
        self.create_mobile_portfolio_details(scrollable_frame)

    def create_portfolio_stats(self, parent):
        """Создание статистики портфеля для десктопа"""
        stats_card = tk.Frame(parent, bg=self.colors['card_bg'],
                              relief='flat', bd=1, highlightthickness=1,
                              highlightbackground=self.colors['accent2'])
        stats_card.pack(fill='x', pady=5, padx=10)

        content_frame = tk.Frame(stats_card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=10, pady=10)

        # Общая стоимость
        total_value = self.calculate_total_assets()
        total_label = tk.Label(content_frame,
                               text=f"💰 Общая стоимость активов: {total_value:,.0f} рублей",
                               font=self.fonts['card_title'],
                               fg=self.colors['success'],
                               bg=self.colors['card_bg'])
        total_label.pack(anchor='w', pady=2)

        # Деньги
        money_label = tk.Label(content_frame,
                               text=f"💵 Наличные: {self.money:,.0f} рублей",
                               font=self.fonts['card_text'],
                               fg=self.colors['text'],
                               bg=self.colors['card_bg'])
        money_label.pack(anchor='w', pady=1)

        # Биткоины
        bitcoin_value = self.bitcoins * 500000
        bitcoin_label = tk.Label(content_frame,
                                 text=f"₿ Биткоины: {self.bitcoins:.4f} BTC ({bitcoin_value:,.0f} рублей)",
                                 font=self.fonts['card_text'],
                                 fg=self.colors['bitcoin'],
                                 bg=self.colors['card_bg'])
        bitcoin_label.pack(anchor='w', pady=1)

        # Пассивный доход
        passive_income = self.get_real_estate_income() * self.get_transport_bonus()
        passive_label = tk.Label(content_frame,
                                 text=f"🔄 Пассивный доход: {passive_income:.0f} рублей/сек",
                                 font=self.fonts['card_text'],
                                 fg=self.colors['warning'],
                                 bg=self.colors['card_bg'])
        passive_label.pack(anchor='w', pady=1)

    def create_mobile_portfolio_stats(self, parent):
        """Создание статистики портфеля для мобильных"""
        stats_card = tk.Frame(parent, bg=self.colors['card_bg'],
                              relief='flat', bd=1, highlightthickness=1,
                              highlightbackground=self.colors['accent2'])
        stats_card.pack(fill='x', pady=5, padx=5)

        content_frame = tk.Frame(stats_card, bg=self.colors['card_bg'])
        content_frame.pack(fill='x', padx=10, pady=8)

        total_value = self.calculate_total_assets()
        total_label = tk.Label(content_frame,
                               text=f"💰 Общая стоимость: {total_value:,.0f}₽",
                               font=self.fonts['card_title'],
                               fg=self.colors['success'],
                               bg=self.colors['card_bg'])
        total_label.pack(anchor='w', pady=2)

        money_label = tk.Label(content_frame,
                               text=f"💵 Наличные: {self.money:,.0f}₽",
                               font=self.fonts['card_text'],
                               fg=self.colors['text'],
                               bg=self.colors['card_bg'])
        money_label.pack(anchor='w', pady=1)

        bitcoin_value = self.bitcoins * 500000
        bitcoin_label = tk.Label(content_frame,
                                 text=f"₿ Биткоины: {bitcoin_value:,.0f}₽",
                                 font=self.fonts['card_text'],
                                 fg=self.colors['bitcoin'],
                                 bg=self.colors['card_bg'])
        bitcoin_label.pack(anchor='w', pady=1)

        passive_income = self.get_real_estate_income() * self.get_transport_bonus()
        passive_label = tk.Label(content_frame,
                                 text=f"🔄 Пассивный доход: {passive_income:.0f}₽/сек",
                                 font=self.fonts['card_text'],
                                 fg=self.colors['warning'],
                                 bg=self.colors['card_bg'])
        passive_label.pack(anchor='w', pady=1)

    def create_portfolio_details(self, parent):
        """Детали портфеля для десктопа"""
        # Акции
        stocks_card = tk.Frame(parent, bg=self.colors['card_bg'],
                               relief='flat', bd=1, highlightthickness=1,
                               highlightbackground='#2d3748')
        stocks_card.pack(fill='x', pady=5, padx=10)

        stocks_title = tk.Label(stocks_card, text="📈 Акции",
                                font=self.fonts['card_title'],
                                fg=self.colors['text'],
                                bg=self.colors['card_bg'])
        stocks_title.pack(anchor='w', padx=10, pady=5)

        stocks_content = tk.Frame(stocks_card, bg=self.colors['card_bg'])
        stocks_content.pack(fill='x', padx=10, pady=5)

        for stock_name, stock_info in self.stocks.items():
            if stock_info['owned'] > 0:
                stock_value = stock_info['price'] * stock_info['owned']
                stock_label = tk.Label(stocks_content,
                                       text=f"{stock_name}: {stock_info['owned']} акций ({stock_value:,.0f} рублей)",
                                       font=self.fonts['card_text'],
                                       fg=self.colors['text_secondary'],
                                       bg=self.colors['card_bg'])
                stock_label.pack(anchor='w', pady=1)

    def create_mobile_portfolio_details(self, parent):
        """Детали портфеля для мобильных"""
        # Акции
        stocks_card = tk.Frame(parent, bg=self.colors['card_bg'],
                               relief='flat', bd=1, highlightthickness=1,
                               highlightbackground='#2d3748')
        stocks_card.pack(fill='x', pady=5, padx=5)

        stocks_title = tk.Label(stocks_card, text="📈 Акции",
                                font=self.fonts['card_title'],
                                fg=self.colors['text'],
                                bg=self.colors['card_bg'])
        stocks_title.pack(anchor='w', padx=10, pady=5)

        stocks_content = tk.Frame(stocks_card, bg=self.colors['card_bg'])
        stocks_content.pack(fill='x', padx=10, pady=5)

        for stock_name, stock_info in self.stocks.items():
            if stock_info['owned'] > 0:
                stock_value = stock_info['price'] * stock_info['owned']
                stock_label = tk.Label(stocks_content,
                                       text=f"{stock_name}: {stock_info['owned']} акций",
                                       font=self.fonts['card_text'],
                                       fg=self.colors['text_secondary'],
                                       bg=self.colors['card_bg'])
                stock_label.pack(anchor='w', pady=1)

                value_label = tk.Label(stocks_content,
                                       text=f"{stock_value:,.0f} рублей",
                                       font=self.fonts['card_text'],
                                       fg=self.colors['success'],
                                       bg=self.colors['card_bg'])
                value_label.pack(anchor='w', pady=(0, 2))

    def calculate_total_assets(self):
        """Рассчитывает общую стоимость активов"""
        total = self.money
        total += self.bitcoins * 500000  # Стоимость биткоинов

        # Стоимость акций
        for stock_info in self.stocks.values():
            total += stock_info['price'] * stock_info['owned']

        return total

    # ОСНОВНЫЕ МЕТОДЫ ИГРЫ
    def click(self):
        """Обработка клика"""
        base_income = self.click_power

        multiplier = 1.0
        for upgrade_name, upgrade_info in self.upgrades.items():
            if upgrade_info.get('multiplier') and upgrade_info['count'] > 0:
                multiplier *= upgrade_info['power']

        total_income = base_income * multiplier

        self.money += total_income
        self.total_clicks += 1
        self.animate_click()
        self.update_display()
        self.update_upgrade_buttons()
        self.save_game()

    def buy_upgrade(self, upgrade_name):
        """Покупка улучшения"""
        upgrade = self.upgrades[upgrade_name]

        if self.money >= upgrade["cost"]:
            self.money -= upgrade["cost"]
            upgrade["count"] += 1
            upgrade["cost"] = int(upgrade["cost"] * 1.8)

            if upgrade.get('multiplier'):
                pass
            else:
                self.click_power += upgrade["power"]

            self.animate_purchase(upgrade_name)
            self.update_display()
            self.update_upgrade_cards()
            self.update_upgrade_buttons()
            self.save_game()

            self.show_message(f"✅ Куплено улучшение: {upgrade_name}")
        else:
            self.animate_insufficient_funds()
            self.show_message("❌ Недостаточно денег для покупки улучшения!")

    def update_upgrade_cards(self):
        """Обновление карточек улучшений"""
        for upgrade_name, upgrade_info in self.upgrades.items():
            if upgrade_name in self.upgrade_cards:
                card_data = self.upgrade_cards[upgrade_name]
                card_data['count_label'].config(text=f"Куплено: {upgrade_info['count']}")
                card_data['price_label'].config(text=f"Цена: {upgrade_info['cost']}₽")

    def buy_bitcoins(self):
        """Покупка биткоинов за рубли"""
        try:
            qty = float(self.bitcoin_qty_var.get())
            cost = qty * 500000

            if cost <= 0:
                self.show_message("❌ Введите положительное количество!")
                return

            if self.money >= cost:
                self.money -= cost
                self.bitcoins += qty
                self.update_display()
                self.update_upgrade_buttons()
                self.save_game()
                self.show_message(f"✅ Куплено {qty:.4f} BTC за {cost:,.0f} рублей!")
            else:
                self.show_message("❌ Недостаточно рублей для покупки!")
        except ValueError:
            self.show_message("❌ Введите корректное число!")

    def buy_stock(self, stock_name, quantity):
        """Покупка акций"""
        stock = self.stocks[stock_name]
        cost = stock['price'] * quantity

        if self.money >= cost:
            self.money -= cost
            stock['owned'] += quantity
            self.update_display()
            self.update_stock_cards()
            self.save_game()
            self.show_message(f"✅ Куплено {quantity} акций {stock_name} за {cost:,.0f} рублей!")
        else:
            self.show_message("❌ Недостаточно денег для покупки акций!")

    def sell_stock(self, stock_name, quantity):
        """Продажа акций"""
        stock = self.stocks[stock_name]

        if stock['owned'] >= quantity:
            income = stock['price'] * quantity
            self.money += income
            stock['owned'] -= quantity
            self.update_display()
            self.update_stock_cards()
            self.save_game()
            self.show_message(f"💰 Продано {quantity} акций {stock_name} за {income:,.0f} рублей!")
        else:
            self.show_message("❌ Недостаточно акций для продажи!")

    def update_stock_prices(self):
        """Обновление цен акций"""
        for stock_name, stock_info in self.stocks.items():
            change_percent = random.uniform(-stock_info['volatility'], stock_info['volatility'])
            new_price = stock_info['price'] * (1 + change_percent)
            stock_info['price'] = max(new_price, 1)

            stock_info['history'].append(stock_info['price'])
            if len(stock_info['history']) > self.stock_history_length:
                stock_info['history'].pop(0)

        self.update_stock_cards()
        self.root.after(5000, self.update_stock_prices)

    def update_stock_cards(self):
        """Обновление карточек акций"""
        for stock_name, stock_info in self.stocks.items():
            if stock_name in self.stock_cards:
                card_data = self.stock_cards[stock_name]
                card_data['price_label'].config(text=f"Цена: {stock_info['price']:,.0f}₽")
                card_data['owned_label'].config(text=f"Владеете: {stock_info['owned']} акций")

    def buy_real_estate(self, estate_name):
        """Покупка недвижимости за биткоины"""
        estate = self.real_estate[estate_name]

        if self.bitcoins >= estate['bitcoin_cost']:
            self.bitcoins -= estate['bitcoin_cost']
            estate['owned'] += 1
            self.update_display()
            self.update_estate_cards()
            self.save_game()
            self.show_message(f"✅ Куплена {estate_name}! Доход: +{estate['income']}₽/сек")
        else:
            self.show_message("❌ Недостаточно биткоинов!")

    def update_estate_cards(self):
        """Обновление карточек недвижимости"""
        for estate_name, estate_info in self.real_estate.items():
            if estate_name in self.estate_cards:
                card_data = self.estate_cards[estate_name]
                card_data['owned_label'].config(text=f"Куплено: {estate_info['owned']}")

    def buy_transport(self, transport_name):
        """Покупка транспорта за биткоины"""
        transport = self.transport[transport_name]

        if self.bitcoins >= transport['bitcoin_cost']:
            self.bitcoins -= transport['bitcoin_cost']
            transport['owned'] += 1
            self.update_display()
            self.update_transport_cards()
            self.save_game()
            self.show_message(f"✅ Куплен {transport_name}! Бонус эффективности: x{transport['bonus']}")
        else:
            self.show_message("❌ Недостаточно биткоинов!")

    def update_transport_cards(self):
        """Обновление карточек транспорта"""
        for transport_name, transport_info in self.transport.items():
            if transport_name in self.transport_cards:
                card_data = self.transport_cards[transport_name]
                card_data['owned_label'].config(text=f"Куплено: {transport_info['owned']}")

    def update_display(self):
        """Обновление отображения"""
        self.money_label.config(text=f"💰 {self.money:,}₽")
        self.bitcoin_label.config(text=f"₿ {self.bitcoins:.4f}")

        total_power = self.click_power
        for upgrade_name, upgrade_info in self.upgrades.items():
            if upgrade_info.get('multiplier') and upgrade_info['count'] > 0:
                total_power *= upgrade_info['power']

        self.power_label.config(text=f"⚡{total_power}/клик")

        passive_income = self.get_real_estate_income() * self.get_transport_bonus()
        self.passive_label.config(text=f"🔄{passive_income:.0f}/сек")

        self.clicks_label.config(text=f"👆{self.total_clicks}")

    def animate_click(self):
        """Анимация клика"""
        original_bg = self.click_button.cget('bg')
        self.click_button.configure(bg=self.colors['success'])
        self.root.after(100, lambda: self.click_button.configure(bg=original_bg))

    def animate_purchase(self, upgrade_name):
        """Анимация покупки"""
        if upgrade_name in self.upgrade_cards:
            card = self.upgrade_cards[upgrade_name]['card']
            original_bg = card.cget('bg')
            card.configure(bg=self.colors['success'])
            self.root.after(200, lambda: card.configure(bg=original_bg))

    def animate_insufficient_funds(self):
        """Анимация недостатка средств"""
        original_bg = self.money_label.cget('fg')
        self.money_label.configure(fg=self.colors['warning'])
        self.root.after(300, lambda: self.money_label.configure(fg=self.colors['success']))

    def start_auto_click(self):
        """Запуск автоматических кликов при долгом нажатии"""
        if not hasattr(self, 'auto_clicking') or not self.auto_clicking:
            self.auto_clicking = True
            self.auto_click_count = 0
            self.auto_click()

    def stop_auto_click(self):
        """Остановка автоматических кликов"""
        self.auto_clicking = False

    def auto_click(self):
        """Автоматический клик"""
        if hasattr(self, 'auto_clicking') and self.auto_clicking:
            self.click()
            self.auto_click_count += 1
            if self.auto_click_count < 50:
                self.root.after(100, self.auto_click)
            else:
                self.stop_auto_click()

    def mega_click(self):
        """Мега-клик при двойном нажатии"""
        bonus = self.click_power * 10
        self.money += bonus
        self.total_clicks += 1
        self.animate_mega_click()
        self.update_display()
        self.save_game()
        self.show_message(f"🌟 МЕГА-КЛИК! +{bonus}₽")

    def animate_mega_click(self):
        """Анимация мега-клика"""
        original_text = self.click_button.cget('text')
        original_bg = self.click_button.cget('bg')

        self.click_button.configure(
            text="🌟\nМЕГА!\n🌟",
            bg=self.colors['warning']
        )

        self.root.after(300, lambda: self.click_button.configure(
            text=original_text,
            bg=original_bg
        ))

    def reset_game(self):
        """Сброс игры"""
        if messagebox.askyesno("Сброс игры", "Вы уверены что хотите сбросить прогресс?"):
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
            self.initialize_new_game()
            self.update_display()
            self.show_message("🔄 Игра сброшена!")

    def show_message(self, message):
        """Показ сообщения"""
        print(f"Игра: {message}")


def main():
    root = tk.Tk()

    style = ttk.Style()
    style.theme_use('clam')

    game = ModernClickerGame(root)

    if game.device_type == "mobile":
        style.configure("TProgressbar",
                        troughcolor='#1e293b',
                        background='#4cc9f0',
                        bordercolor='#1e293b',
                        lightcolor='#4cc9f0',
                        darkcolor='#4cc9f0',
                        thickness=20)
    else:
        style.configure("TProgressbar",
                        troughcolor='#1e293b',
                        background='#4cc9f0',
                        bordercolor='#1e293b',
                        lightcolor='#4cc9f0',
                        darkcolor='#4cc9f0')

    root.mainloop()


if __name__ == "__main__":
    main()