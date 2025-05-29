FROM python:3.10-slim

# Рабочая директория
WORKDIR /app

# Установим переменную окружения для импорта модулей
ENV PYTHONPATH=/app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Streamlit порт
EXPOSE 8501

# Запуск Streamlit
CMD ["streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]