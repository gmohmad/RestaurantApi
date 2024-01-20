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

## 4. Установите все зависимости
```
pip intall -r requirements.txt
```
## 5. Запустите сервер
```
uvicorn src.main:app --reload
```
# Готово!
