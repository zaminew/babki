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

# Устанавливаем Git
RUN apt-get update && apt-get install -y git

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

# Устанавливаем Git
RUN apt-get update && apt-get install -y git

# Настраиваем Git (замените 'your_name' и 'your_email' на свои данные)
RUN git config --global user.name "your_name"
RUN git config --global user.email "your_email"

# Настраиваем стандартное имя для автоматических коммитов
RUN git config --global commit.defaultName "main"

# Копируем содержимое локальной директории проекта в рабочую директорию контейнера
COPY . .

# Указываем команду для запуска приложения при старте контейнера
CMD ["python", "app.py"]


# Копируем содержимое локальной директории проекта в рабочую директорию контейнера
COPY . .

# Указываем команду для запуска приложения при старте контейнера
CMD ["python", "app.py"]
