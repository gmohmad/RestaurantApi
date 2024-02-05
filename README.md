# Запуск проекта

## 1. Склонируйте репозиторий

```
git clone https://github.com/gmohmad/Y_lab_FastAPI.git
```

## 2. Создайте файл .env в дериктории проекта и заполните его по примеру файла .env.example

## 3. Запуск приложения

```
docker-compose up -d --build
```

## 4. Запуск тестов

### для стабильного запуска остановите ранее запущенное приложение

```
docker-compose down -v
```

### и запустите контейнер для прогона тестов

```
docker-compose -f docker-compose.tests.yaml up --build
```

#### для запуска с фильтрацией логов запустите

```
docker-compose -f docker-compose.tests.yaml up -d --build ; docker logs -f ylab_fastapi-web-1
```
