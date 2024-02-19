# Запуск проекта

## 1. Склонируйте репозиторий

```
git clone https://github.com/gmohmad/ylab_fastapi.git
```
<details>
    <summary><h1>$${\color{red}Настройка \space \color{red}для \space \color{red}синхронизации \space \color{red}с \space \color{red}google \space \color{red}таблицей}$$</h1></summary>
    <h3>1. Создайте проект в google drive console и подключите google sheets api</h3>
        <details>
            <summary><h2>$${\color{red}Инструкция}$$</h2></summary>
            <h4>Таймстемп - 1:51-5:41</h4>
            <h4>Ссылка - https://www.youtube.com/watch?v=zCEJurLGFRk</h4>
        </details>
            <h3>2. Загруженный файл с данными переименуйте в creds.json и поместите в дерикторию src/tasks/google_api_config</h3>
            <h3>3. В той же дериктории создайте файл .env и заполните его по примеру .env.example (в SPREADSHEET_ID запишите id вашей google таблицы)</h3>
</details>
<br>

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
