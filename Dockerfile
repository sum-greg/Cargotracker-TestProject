# Используем базовый образ Python
FROM python:3.9

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
RUN mkdir /testcargotracker
WORKDIR /testcargotracker

# Устанавливаем зависимости
COPY requirements.txt /testcargotracker/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта внутрь контейнера
COPY . /testcargotracker/

# Загружаем данные в базу данных
RUN python load_data.py

# Открываем порт 8000
EXPOSE 8000

# Запускаем сервер Django
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
