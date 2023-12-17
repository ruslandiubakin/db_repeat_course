import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_batch
import pandas as pd
import re
import time
import csv


FILE_PATHS = [
            ['my_app\data\Odata2021File.csv', 'UTF-8-SIG'],
]


TABLE_NAME = 'Results_ZNO_2021'


DATABASE_NAME = 'results_zno'
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'


# Визначення типів даних стовпців
def define_col_types(df):
    col_types = []
    for col_name, col_type in zip(df.columns, df.dtypes):
        if "int64" in str(col_type):
            col_types.append((sql.Identifier(col_name), sql.SQL("INTEGER")))
        elif "float64" in str(col_type):
            col_types.append((sql.Identifier(col_name), sql.SQL("FLOAT")))
        else:
            col_types.append((sql.Identifier(col_name), sql.SQL("VARCHAR(255)")))
    return col_types


def insert_to_table(conn, cursor, df, table_name, year, isTableExist = False, new_dataset=True):
    # Створити таблицю, якщо вона ще не існую в базі даних
    if isTableExist == False:
        col_types = define_col_types(df)

        # SQL-запит для створення таблиці
        create_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(",").join(sql.SQL("{} {}").format(*col_type) for col_type in col_types)
        )

        # Виконання SQL-запиту
        cursor.execute(create_query)
        conn.commit()

    # SQL-запит для заповнення таблиці
    columns = df.columns
    insert_query = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
        sql.Identifier(table_name),
        sql.SQL(',').join(map(sql.Identifier, columns)),
        sql.SQL(',').join(sql.Placeholder() * len(columns))
    )

    if new_dataset == False:
        # Відправка запиту на отримання кількості рядків в таблиці
        count_query = sql.SQL('SELECT COUNT(*) FROM {} WHERE "YEAR" = {};').format(sql.Identifier(table_name),
                                                                                   sql.Identifier(year))
        cursor.execute(count_query)
        count = cursor.fetchone()[0]

        # Перетворення датафрейму на список кортежів
        values = [tuple(getattr(row, col) for col in columns) for row in df.itertuples()]
        # print(values)
        values = values[count+1:]
    else:
        # Перетворення датафрейму на список кортежів
        values = [tuple(getattr(row, col) for col in columns) for row in df.itertuples()]

    # Виконання операції вставки значень
    execute_batch(cursor, insert_query, values)    


# Завантаження даних з файлів до бази даних
def load_to_database():
    isTableExist = False
    for file in FILE_PATHS:
        new_dataset = True
        match = re.search('\d\d\d\d', file[0]).group(0)
        year = int(match)
        specific_rows = [x for x in range(10000)]
        df = pd.read_csv(file[0], sep=';', encoding= file[1], skiprows= lambda x: x not in specific_rows)
        # df = pd.read_csv(file[0], sep=';', encoding= file[1])
        df = df.assign(year = year)
        df.columns = df.columns.str.upper()
        df = df.replace(regex=r'\b,\b', value='.')
        df[df.filter(like='BALL').columns] = df[df.filter(like='BALL').columns].astype('float64')
        print(df.info())

        conn = None
        tries = 0
        while conn is None:
            if tries < 5:
                try:
                    conn = psycopg2.connect(database=DATABASE_NAME,
                                            user=USERNAME, 
                                            password=PASSWORD,
                                            host = HOST,
                                            port = PORT)
                    cursor = conn.cursor()
                    conn.autocommit = False

                    print(f"Завантаження файлу {file} до бази даних...")

                    insert_to_table(conn, cursor, df, TABLE_NAME, year, isTableExist, new_dataset)
                    conn.commit()

                    print(f"Завантажено дані з файлу {file} .")
                    isTableExist = True

                    # Закриття з'єднання з базою даних
                    conn.close()
                except psycopg2.OperationalError:
                    print("Could not connect to database. Retrying in 5 seconds...")
                    tries += 1
                    new_dataset = False
                    time.sleep(5)
            else: 
                print("Could not connect to database.")
                break

# def exec_query_7():
#     # Запит варіанту 7. Порівняти  найкращий  бал  з  Математики  у  кожному  регіоні  у  2021  та  2019  роках  серед тих кому було зараховано тест.

#     query_7 = sql.SQL('''
#         SELECT "REGNAME", 
#             MAX(CASE WHEN "YEAR" = 2021 THEN "MATHBALL100" END) AS max_mathball_2021, 
#             MAX(CASE WHEN "YEAR" = 2019 THEN "MATHBALL100" END) AS max_mathball_2019
#         FROM "Results_ZNO"
#         WHERE "MATHTESTSTATUS" = 'Зараховано'
#         GROUP BY "REGNAME";
#     ''')

#     conn = psycopg2.connect(database=DATABASE_NAME,
#                             user=USERNAME, 
#                             password=PASSWORD,
#                             host = HOST,
#                             port = PORT)

#     # Виконання запиту №7
#     with conn.cursor() as cursor:
#         cursor.execute(query_7)

#         # Створення або відкриття файлу results.csv та записування до нього результату запиту №7.
#         with open('result.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow([i[0] for i in cursor.description]) # запис заголовку таблиці
#             writer.writerows(cursor.fetchall()) # запис даних таблиці
  

def main():
    start_time = time.time()
    load_to_database()
    end_time = time.time()

    execution_time = (end_time - start_time) / 60
    with open('lab1/execution_time.txt', 'w') as file:
        file.write(str(execution_time))

    # exec_query_7()


if __name__ == "__main__":
    main()