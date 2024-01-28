# Запуск проекта

## 1. Склонируйте репозиторий
```
git clone https://github.com/gmohmad/Y_lab_FastAPI.git
```
## 2. Создайте файл .env в дериктории проекта и заполните его по примеру файла .env.example
## 3. Запустите контейнер приложения
```
docker-compose up -d --build
```
## 4. Для запуска тестов
```
docker-compose down -v
docker-compose -f docker-compose.tests.yaml -d --build
```
### Путь к файлу с реализацией сложного orm запроса (3-ий пункт ДЗ) - ./src/utils.py 
### Имя функции - get_counts_for_menu
