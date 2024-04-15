# Используем официальный образ Python с уменьшенной версией (slim)
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt requirements.txt

# Устанавливаем virtualenv
RUN pip install --no-cache-dir virtualenv

# Создаем виртуальное окружение и активируем его
RUN python -m virtualenv venv
RUN /bin/bash -c "source venv/bin/activate"

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое локальной директории проекта в рабочую директорию контейнера
COPY . .

# Указываем команду для запуска приложения при старте контейнера
CMD ["python", "babki/app.py"]
