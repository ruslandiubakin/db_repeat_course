# Опис робіт
Репозиторій містить два проєкти:
- my_app: для локального запуску на комп'ютері
- my_app_docker: для запуску в Docker.
- Посиланна на датасет: https://drive.google.com/file/d/1aE73zhmWOPZySmrSFMhKeth_UwA7T1gR/view?usp=sharing
- Датасет помістити за шляхом: 
    db_repeat_course/my_app/data/
    db_reoeat_course/my_app_docker/

# Інструкція по запуску
## my_app
1. Створити базу даних в PostgreSQL з такими параметрами:
```
DATABASE_NAME = 'results_zno'
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'
TABLE_NAME = 'Results_ZNO_2021'
```

2. Запустити funnel.py, зачекати поки виконається програма.
3. Створити базу даних в PostgreSQL з такими параметрами:
```
DATABASE_NAME = 'results_zno_new'
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'
```

4. Виконати міграцію за допомогою alembic:
```
alembic upgrade head
```

5. Запустити service_worker.py, зачекати поки виконається програма.
6. Для виконання параметризованих запитів до БД запустити consumer.py.

## my_app_docker
1. Перейти у директорію docker і запустити команду:
```
docker-compose build    
```

2. Виконати команду:
```
docker-compose up --no-start
```

3. Запустити контейнер з базою даних PostgreSQL.
4. Для зручності та необхідності запустити контейнер з pgAdmin (Логін: noemail@noemail.com, пароль: root).
5. Запустити контейнер funnel.
6. Створити в PostgreSQL нову базу даних з такими параметрами:
```
DATABASE_NAME = 'results_zno_new'
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'postgres'
PORT = '5432'
```
7. Після виконання funnel запустити контейнер service_worker.
8. Після успішного виконання service_worker запустити funnel для виконання параметризованих запитів до БД через консоль за допомогою наступної команди:
```
docker exec -it ID_контейнера_consumer python consumer.py
```