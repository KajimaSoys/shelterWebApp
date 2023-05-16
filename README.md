# shelterWebApp
<br>

## Get started

### 1. Установите git cli

`для x64` https://github.com/git-for-windows/git/releases/download/v2.40.1.windows.1/Git-2.40.1-64-bit.exe

`для x32` https://github.com/git-for-windows/git/releases/download/v2.40.1.windows.1/Git-2.40.1-32-bit.exe

### 2. Клонируйте репозиторий
```shell
git clone https://github.com/KajimaSoys/shelterWebApp.git
```

### 3. Перейдите в репозиторий
```shell
cd ./shelterWebApp
```
<br>

## Быстрое развертывание с помощью Docker 

**Скачать:** https://www.docker.com/products/docker-desktop/

### 1. Соберите образы Docker:
```sh
docker-compose build
```

### 2. Запустите контейнеры:
```shell
docker-compose up -d
```

Откройте браузер по адресу http://localhost/ для доступа к фронтенду. Административная панель находится по адресу http://localhost/admin/, логин:пароль - `admin:12345`

### 3. Удаление контейнеров (необязательно)
```shell
docker-compose down
```
<br>

## Установка проекта для разработки

### 1. Скачайте и установите python:3.8+


`для x64` https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe

`для x32` https://www.python.org/ftp/python/3.8.0/python-3.8.0.exe


### 2. Скачайте и установите Node.js:16+
`для x64` https://nodejs.org/dist/v18.16.0/node-v18.16.0-x64.msi

`для x32` https://nodejs.org/dist/v18.16.0/node-v18.16.0-x86.msi

### 3. Скачайте и установите PostgreSQL:12+

https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

### 4. Создайте в PostgreSQL базу данных `shelter`

### 5. Запустите бэкенд

#### 1. В корневой директории создайте виртуальное окружение
```shell
python -m venv venv
```

#### 2. Активируйте окружение
```shell
./venv/Scripts/activate
```

#### 3. Установите все зависимости
```shell
pip install -r req.txt
```

#### 4. Проведите миграции в БД
```shell
python manage.py migrate
```

#### 5. Создайте суперюзера
```shell
python manage.py createsuperuser
```

#### 6. Запустите сервер
```shell
python manage.py runserver
```

Административная панель находится по адресу http://127.0.0.1:8000/admin/

### 6. Запустите фронтенд

#### 1. Перейдите в папку фронтенда
```shell
cd client/
```

#### 2. Установите зависимости
```shell
npm install
```
#### 3. Запустите сервер разработки (Hot-Reload)
```shell
npm run dev
```

Откройте браузер по адресу http://localhost:5173/ для доступа к фронтенду.

<br>

#### 4. Скомпилируйте и минифицируйте файлы для продакшена (необязательно)
```shell
npm run build
```
#### 5. Запустите сервер из скомпилированных файлов (необязательно)
```shell
npm run preview
```
**Заметка:** Скомпилированные файлы находятся в папке `dist`

Откройте браузер по адресу http://localhost:4173/ для доступа к фронтенду.