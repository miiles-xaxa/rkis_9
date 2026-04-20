import customtkinter as ctk
import random
import string
from typing import List, Dict, Any, Union

#asiogfajnsmgopasgojm

# --- Логика генерации рынка ---
def generate_new_coin_name() -> str:
    prefixes: List[str] = ['Crypto', 'Block', 'Chain', 'Digital', 'Smart', 'Meta', 'Web', 'NFT', 'FPI']
    suffixes: List[str] = ['Coin', 'Token', 'Cash', 'Gold', 'Dollar', 'Finance', 'FPI']
    return random.choice(prefixes) + random.choice(suffixes)


def generate_fixed_coins(amount: int = 10) -> List[Dict[str, Union[str, float]]]:
    coins: List[Dict[str, Union[str, float]]] = []
    for _ in range(amount):
        coin: Dict[str, Union[str, float]] = {
            "name": generate_new_coin_name(),
            "cost": round(random.uniform(0.01, 100), 3),
            "change": round(random.uniform(-0.5, 0.5), 2)
        }
        coins.append(coin)
    return coins


# ==========================================
# МОДУЛЬ 1: Обработка числовых данных
# ==========================================
def calculate_portfolio_value(wallet: Dict[str, float], market_data: List[Dict[str, Any]]) -> float:
    """Подсчет общей стоимости всех монет в кошельке на основе текущих цен рынка."""
    total_value: float = 0.0
    for coin in market_data:
        name: str = str(coin["name"])
        if name in wallet:
            total_value += wallet[name] * float(coin["cost"])
    return round(total_value, 2)


# ==========================================
# МОДУЛЬ 2: Поиск данных
# ==========================================
def search_coin(market_data: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """Поиск монеты по названию (регистронезависимый)."""
    if not query:
        return market_data
    query = query.lower()
    return [coin for coin in market_data if query in str(coin["name"]).lower()]


# ==========================================
# МОДУЛЬ 3: Обработка табличных данных
# ==========================================
def sort_coins(market_data: List[Dict[str, Any]], sort_key: str, reverse: bool = False) -> List[Dict[str, Any]]:
    """Сортировка списка монет по заданному ключу (name, cost, change)."""
    return sorted(market_data, key=lambda x: x[sort_key], reverse=reverse)


# ==========================================
# МОДУЛЬ 4: Генерация случайных символов
# ==========================================
def generate_transaction_id(length: int = 16) -> str:
    """Генерирует уникальный ID транзакции (например: TX-8F9A2B...)"""
    chars: str = string.ascii_uppercase + string.digits
    random_hash: str = ''.join(random.choices(chars, k=length))
    return f"TX-{random_hash}"


# --- Интерфейс пользователя ---
class MarketApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("ZZZ Trading - Market & Logic")
        self.geometry("900x800")
        self.minsize(600, 600)
        ctk.set_appearance_mode("dark")

        # Данные приложения
        self.full_market_data: List[Dict[str, Any]] = generate_fixed_coins()
        self.displayed_data: List[Dict[str, Any]] = self.full_market_data.copy()

        # Пример кошелька пользователя для демонстрации подсчета (Модуль 1)
        self.user_wallet: Dict[str, float] = {
            self.full_market_data[0]["name"]: 150.5,  # 150.5 монет первой крипты
            self.full_market_data[1]["name"]: 50.0  # 50.0 монет второй крипты
        }

        self._build_ui()

    def _build_ui(self) -> None:
        """Построение интерфейса"""
        # Главный заголовок
        self.label = ctk.CTkLabel(self, text="РЫНОК АКТИВОВ", font=("Arial", 28, "bold"))
        self.label.pack(pady=(20, 10))

        # Панель инструментов (Поиск и Сортировка)
        self.tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tools_frame.pack(padx=20, pady=5, fill="x")

        self.search_entry = ctk.CTkEntry(self.tools_frame, placeholder_text="Поиск монеты...", font=("Arial", 16))
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        # Привязка поиска к вводу текста
        self.search_entry.bind("<KeyRelease>", self._handle_search)

        self.btn_sort = ctk.CTkButton(self.tools_frame, text="Сортировать по цене", font=("Arial", 14),
                                      command=self._handle_sort)
        self.btn_sort.pack(side="right")

        # Контейнер для таблицы
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid_columnconfigure(1, weight=1)
        self.scroll_frame.grid_columnconfigure(2, weight=1)

        # Метка стоимости портфеля
        self.portfolio_label = ctk.CTkLabel(self, text="Оценка портфеля: Загрузка...", font=("Arial", 16, "italic"),
                                            text_color="#F39C12")
        self.portfolio_label.pack(pady=5)

        self.create_headers()
        self.refresh_table()
        self.update_portfolio_ui()

        # Кнопка кошелька внизу
        self.btn_wallet = ctk.CTkButton(
            self,
            text="ОТКРЫТЬ КОШЕЛЕК",
            font=("Arial", 18, "bold"),
            height=50,
            width=300
        )
        self.btn_wallet.pack(side="bottom", pady=20)

    def _handle_search(self, event: Any) -> None:
        """Обработчик события поиска"""
        query: str = self.search_entry.get()
        self.displayed_data = search_coin(self.full_market_data, query)
        self.refresh_table()

    def _handle_sort(self) -> None:
        """Обработчик события сортировки (переключатель)"""
        # Для простоты всегда сортируем по убыванию цены
        self.displayed_data = sort_coins(self.displayed_data, sort_key="cost", reverse=True)
        self.refresh_table()

    def update_portfolio_ui(self) -> None:
        """Обновление текста стоимости портфеля"""
        total: float = calculate_portfolio_value(self.user_wallet, self.full_market_data)
        self.portfolio_label.configure(text=f"Текущая оценка кошелька: {total} Z$")

    def create_headers(self) -> None:
        headers: List[str] = ["Название", "Цена (Z$)", "Изменение (%)"]
        for i, text in enumerate(headers):
            h_label = ctk.CTkLabel(
                self.scroll_frame,
                text=text,
                font=("Arial", 18, "bold"),
                text_color="#AAAAAA"
            )
            h_label.grid(row=0, column=i, pady=15, sticky="nsew")

    def refresh_table(self) -> None:
        """Очистка старых данных и отрисовка новых"""
        # Удаляем старые виджеты (кроме заголовков в нулевом ряду)
        for widget in self.scroll_frame.winfo_children():
            info = widget.grid_info()
            if int(info.get("row", 0)) > 0:
                widget.destroy()

        data_font = ("Arial", 20)
        for index, coin in enumerate(self.displayed_data):
            ctk.CTkLabel(self.scroll_frame, text=str(coin["name"]), font=data_font).grid(
                row=index + 1, column=0, pady=10, sticky="nsew"
            )
            ctk.CTkLabel(self.scroll_frame, text=f"{float(coin['cost']):.3f}", font=data_font).grid(
                row=index + 1, column=1, pady=10, sticky="nsew"
            )
            color: str = "#2ECC71" if float(coin["change"]) >= 0 else "#E74C3C"
            ctk.CTkLabel(self.scroll_frame, text=f"{float(coin['change'])}%", text_color=color, font=data_font).grid(
                row=index + 1, column=2, pady=10, sticky="nsew"
            )


if __name__ == "__main__":
    app = MarketApp()
    # Тестовая демонстрация модуля генерации символов в консоль
    print(f"[Система] Сгенерирован ID сессии: {generate_transaction_id()}")
    app.mainloop()