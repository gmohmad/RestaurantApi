# Запуск проекта

## 1. Склонируйте репозиторий
```
git clone https://github.com/gmohmad/Y_lab_FastAPI.git
```
## 2. Подготовьте базу данных (PostgreSQL)
```
создайте пользователя
создайте базу данных
```
## 3. Создайте файл .env в дериктории проекта и заполните его по примеру файла .env.example  

## 4. Создайте виртуальное окружение в дериктории проекта и активируйте его
```
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```
## 5. Установите все зависимости
```
pip intall -r requirements.txt
```
## 6. Примените миграцию
```
alembic upgrade a92e977974a8
```
## 7. Запустите сервер
```
uvicorn src.main:app --reload
```
# Готово
