# Project Setup

## 1. Clone the repository
```
git clone https://github.com/gmohmad/ylab_fastapi.git
```

<details>
    <summary>Setup for syncing with Google Sheets</summary>
    <h3>1. Create a project in Google Drive Console and connect Google Sheets API</h3>
        <details>
            <summary>Instructions</summary>
            <h4>Timestamp - 1:51-5:41</h4>
            <h4>Link - https://www.youtube.com/watch?v=zCEJurLGFRk</h4>
        </details>
            <h3>2. Rename the downloaded data file to creds.json and place it in the src/tasks/google_api_config directory</h3>
            <h3>3. In the same directory, create a .env file and fill it according to the .env.example file (put the id of your Google Sheet in SPREADSHEET_ID)</h3>
</details>
<br>

## 2. Create a .env file in the project directory and fill it according to the .env.example file

## 3. Running the application
```
docker-compose up -d --build
```

## 4. Running the tests

### Stop the previously running application for stable execution
```
docker-compose down -v
```

### And start the container for running the tests
```
docker-compose -f docker-compose.tests.yaml up --build
```

#### For running with log filtering, run
```
docker-compose -f docker-compose.tests.yaml up -d --build ; docker logs -f ylab_fastapi-web-1
```
