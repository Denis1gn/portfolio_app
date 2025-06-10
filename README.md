# Анализ и оптимизация инвестиционного портфеля на MOEX

_Интерактивное приложение на Streamlit для построения, анализа и оптимизации инвестиционного портфеля на основе исторических данных Московской биржи (MOEX)._

---

##  Функциональность

- Загрузка котировок акций с MOEX (через **ISS API**)
- Расчет доходности, стандартного отклонения и **Sharpe Ratio**
- Визуализация:
  - доходности портфеля
  - распределения доходностей
  - корреляционной матрицы активов
- Интерактивная настройка весов активов
- Оптимизация структуры портфеля (минимизация волатильности)
- Отображение процесса оптимизации
- Расчет **Value-at-Risk (VaR)** и биномиальная проверка нарушений

---

##  Используемые технологии

- Python 3.10+
- Streamlit
- Plotly
- SciPy
- Pandas, NumPy
- MOEX ISS API

---

##  Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Denis1gn/portfolio_app.git
cd portfolio_app
```

2. Установите зависимости

```bash
pip install -r requirements.txt
```

3. Запуск
   
```bash
streamlit run streamlit_app/app.py
```
Приложение откроется по адресу: http://localhost:8501

⸻

```bash

Если используете Docker:

docker-compose up --build
```

Откройте в браузере: http://localhost:8051

⸻

Структура проекта

```
portfolio_app/
├── streamlit_app/
│   ├── app.py                  # Точка входа (Streamlit-приложение)
│   ├── ui.py                   # Интерфейс и графики
│
├── loaders/
│   ├── moex_loader.py          # Загрузка данных с MOEX
│   └── risk_free_rate.py       # Получение безрисковой ставки
│
├── portfolio/
│   ├── constructor.py          # Сборка портфеля
│   ├── risk_return.py          # Метрики доходности и риска
│   ├── optimizer.py            # Оптимизация портфеля
│   └── var_analysis.py         # Расчет и проверка VaR
│
├── requirements.txt            # Зависимости проекта
└── README.md                   # Описание
```

⸻

⚠️ Ограничения
	•	Поддерживаются только акции из режима торгов TQBR (MOEX)
	•	Данные загружаются с шагом 100 дней (ограничение API)
	•	Не работает в оффлайне (все данные берутся из MOEX API)

⸻

Как использовать
1. Выберите тикеры (например: SBER, GAZP)
2. Укажите период анализа и веса активов
3. Нажмите Загрузить и проанализировать
<img width="1570" alt="image" src="https://github.com/user-attachments/assets/692a34ce-2a27-4ca3-9113-22f6f0c5a7e8" /> 	
4. Изучите метрики, графики, корреляции, VAR
<img width="1570" alt="image" src="https://github.com/user-attachments/assets/55b45f1c-5c27-419c-ad40-8e36bb52ebfd" />

<img width="1570" alt="image" src="https://github.com/user-attachments/assets/508a11ad-4795-459d-b07e-aaaa61a7e70d" />

5. Для оптимизации доходность / риск, выберите годовое значение волатильности и нажмите Оптимизировать

<img width="1595" alt="image" src="https://github.com/user-attachments/assets/f5e3e59f-9cca-42e8-9f6c-ed191ef0f332" />

