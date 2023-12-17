from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from prettytable import PrettyTable
from my_app.new_database_structure import Base, Student, EducationalInstitution, EIOfStudent, Subject, ZNOPlace, ResultsOfStudent


# Підключення до бази даних
engine = create_engine('postgresql://postgres:postgres@localhost/results_zno_new')
Base.metadata.create_all(engine)


def paginate_results(results, page_size=10):
    # Розділення результатів на сторінки
    for i in range(0, len(results), page_size):
        yield results[i:i + page_size]


def display_page(results, page_number, num_pages):
    # Створення PrettyTable для виведення результатів
    table = PrettyTable()
    table.field_names = ['Student ID', 'Subject ID', 'Ball100']

    # Додавання рядків з результатами до таблиці
    for result in results:
        table.add_row(result)

    # Виведення таблиці в консоль
    print(f"\nСтраниця {page_number} з {num_pages}:\n")
    print(table)


def display_page_educational_institutions(results, page_number, num_pages):
    # Створення PrettyTable для виведення результатів
    table = PrettyTable()
    table.field_names = ['ID', 'Name']

    # Додавання рядків з результатами до таблиці
    for result in results:
        table.add_row(result)

    # Виведення таблиці в консоль
    print(f"\nСтраниця {page_number} з {num_pages}:\n")
    print(table)


def add_student(student_data):
    # Створення сесії
    with Session(engine) as session:
        try:
            # Створення об'єкта Student
            new_student = Student(**student_data)
            
            # Додавання студента до бази даних
            session.add(new_student)
            session.commit()

            print("Студент успішно доданий до бази даних.")
        except Exception as e:
            print(f"Помилка при додаванні студента: {e}")
            session.rollback()


def add_results_of_student(results_data):
    # Створення сесії
    with Session(engine) as session:
        try:
            # Створення об'єкта ResultsOfStudent та встановлення зв'язків із студентом
            new_results = ResultsOfStudent(**results_data)

            # Додавання результатів до бази даних
            session.add(new_results)
            session.commit()

            print("Результат студента успішно доданий до бази даних.")
            return True
        except Exception as e:
            print(f"Помилка при додаванні результату студента: {e}")
            session.rollback()
            return False


def delete_student(student_id):
    with Session(engine) as session:
        try:
            student_to_delete = session.query(Student).filter_by(ID=student_id).first()

            if student_to_delete:
                # Також видалення результатів студента (якщо не використовується каскадне видалення)
                results_to_delete = session.query(ResultsOfStudent).filter_by(StudentID=student_id).all()
                for result in results_to_delete:
                    session.delete(result)
                    
                # Видалення студента
                session.delete(student_to_delete)
                session.commit()
                print(f"Студент з ID {student_id} та його результати видалені з бази даних.")
            else:
                print(f"Студент з ID {student_id} не знайдений.")
        except Exception as e:
            print(f"Помилка при видаленні студента та результатів: {e}")
            session.rollback()


def delete_result_by_subject(result_data):
    with Session(engine) as session:
        try:
            results_to_delete = session.query(ResultsOfStudent).filter_by(StudentID=result_data.StudentID, SubjectID=result_data.SubjectID, Year=result_data.Year).all()
            for result in results_to_delete:
                session.delete(result)
                
            session.commit()
            print(f"Результат студента {result_data.StudentID} з предмету {result_data.SubjectID} за {result_data.Year} рік видалені з бази даних.")
        except Exception as e:
            print(f"Помилка при видаленні студента та результатів: {e}")
            session.rollback()


def add_educational_institution(educational_institutions_data):
    with Session(engine) as session:
        try:
            
            new_educational_institutions = EducationalInstitution(**educational_institutions_data)

            session.add(new_educational_institutions)
            session.commit()

            print("Навчальний заклад успішно доданий.")
        except Exception as e:
            print(f"Помилка при додаванні навчального закладу: {e}")
            session.rollback()


def add_zno_place(zno_place_data):
    with Session(engine) as session:
        try:
            
            new_zno_place = ZNOPlace(**zno_place_data)

            session.add(new_zno_place)
            session.commit()

            print("Навчальний заклад, де учень проходив тест, успішно доданий.")
            return True
        except Exception as e:
            print(f"Помилка при додаванні навчального закладу проходження іспиту: {e}")
            session.rollback()
            return False


def delete_result_of_students(result_data):
    with Session(engine) as session:
        try:
            result_of_student_to_delete = session.query(ResultsOfStudent).filter_by(StudentID=result_data.StudentID, SubjectID=result_data.SubjectID, Year=result_data.Year).first()

            if result_of_student_to_delete:
                session.delete(result_of_student_to_delete)
                session.commit()
                print(f"Результат студента з ID {result_data.StudentID} з предмету {result_data.SubjectID} {result_data.Year} року видалено з бази даних.")
            else:
                print(f"Резульат студента з ID {result_data.StudentID} з предмету {result_data.SubjectID} {result_data.Year} року  не знайдений.")
        except Exception as e:
            print(f"Помилка при видаленні результату: {e}")
            session.rollback()


def search_institution_by_name(name, page_size=10):
    with Session(engine) as session:
        try:
            # Пошук навчального закладу за назвою
            institutions = (
                session.query(EducationalInstitution)
                .filter(EducationalInstitution.Name.ilike(f'%{name}%'))
                .all()
            )

            formatted_results = [
                [
                    institution.ID,
                    institution.Name
                ]
                for institution in institutions
            ]

            # Розділення результатів на сторінки
            paginated_results = list(paginate_results(formatted_results, page_size))
            num_pages = len(paginated_results)

            if num_pages == 0:
                print("Немає результатів для відображення.")
                return

            # Виведення першої сторінки
            current_page = 1
            display_page_educational_institutions(paginated_results[current_page - 1], current_page, num_pages)

            # Запит на відображення інших сторінок
            while True:
                user_input = input("\nВведіть 'n' для наступної сторінки, 'p' для попередньої, або 'q' для виходу: ").lower()

                if user_input == 'n' and current_page < num_pages:
                    current_page += 1
                    display_page_educational_institutions(paginated_results[current_page - 1], current_page, num_pages)
                elif user_input == 'p' and current_page > 1:
                    current_page -= 1
                    display_page_educational_institutions(paginated_results[current_page - 1], current_page, num_pages)
                elif user_input == 'q':
                    break
                else:
                    print("Невірна команда. Будь ласка, введіть 'n', 'p', або 'q'.")
                
        except Exception as e:
            print(f"Помилка при виконанні пошуку: {e}")


def delete_educational_institution(educational_institution_id):
    with Session(engine) as session:
        try:
            educational_institution_to_delete = session.query(EducationalInstitution).filter_by(ID=educational_institution_id).first()

            if educational_institution_to_delete:
                # Видалення студента
                session.delete(educational_institution_to_delete)
                session.commit()
                print(f"Навчальний заклад з ID {educational_institution_id} видалено з бази даних.")
            else:
                print(f"Навчальний заклад з ID {educational_institution_id} не знайдений.")
        except Exception as e:
            print(f"Помилка при видаленні навчального закладу: {e}")
            session.rollback()


def add_subject(subject_data):
    with Session(engine) as session:
        try:
            
            new_subject = Subject(**subject_data)

            session.add(new_subject)
            session.commit()

            print("Предмет успішно додано.")
        except Exception as e:
            print(f"Помилка при додаванні предмету: {e}")
            session.rollback()


def delete_subject(subject_id):
    with Session(engine) as session:
        try:
            subject_to_delete = session.query(Subject).filter_by(ID=subject_id).first()

            if subject_to_delete:
                session.delete(subject_to_delete)
                session.commit()
                print(f"Предмет з ID {subject_id} видалено з бази даних.")
            else:
                print(f"Предмет з ID {subject_id} не знайдений.")
        except Exception as e:
            print(f"Помилка при видаленні предмету: {e}")
            session.rollback()


def get_student_results(student_id):

    # Створення сесії SQLAlchemy
    with Session(engine) as session:
        try:
            # Отримання студента за його ідентифікатором
            student = session.query(Student).filter_by(ID=student_id).first()

            if not student:
                print(f"Студент з ID {student_id} не знайдений.")
                return

            # Отримання результатів студента
            results = session.query(ResultsOfStudent).filter_by(StudentID=student_id).all()

            # Створення таблиці для виведення результатів
            table = PrettyTable()
            table.field_names = ['SubjectID', 'Year', 'Lang', 'TestStatus', 'UkrSubTest', 'DPALevel', 'Ball100', 'Ball12', 'Ball', 'AdaptScale']

            # Додавання рядків з результатами до таблиці
            for result in results:
                table.add_row([
                    result.SubjectID,
                    result.Year,
                    result.Lang,
                    result.TestStatus,
                    result.UkrSubTest,
                    result.DPALevel,
                    result.Ball100,
                    result.Ball12,
                    result.Ball,
                    result.AdaptScale
                ])

            # Виведення таблиці в консоль
            print(f"Результати студента з ID {student_id}:")
            print(table)

        except Exception as e:
            print(f"Помилка при отриманні та виведенні результатів: {e}")


def get_students_above_score_paginated(subject_id, min_score, page_size=10):
    # Створення сесії SQLAlchemy
    with Session(engine) as session:
        try:
            # Отримання результатів студентів за вказаним предметом та балом
            results = (
                session.query(ResultsOfStudent)
                .filter(ResultsOfStudent.SubjectID == subject_id, ResultsOfStudent.Ball100 > min_score, ResultsOfStudent.Ball100 != 'NaN')
                .all()
            )

            # Створення списку для виведення результатів у вигляді PrettyTable
            formatted_results = [
                [
                    result.StudentID,
                    result.SubjectID,
                    result.Ball100
                ]
                for result in results
            ]

            # Розділення результатів на сторінки
            paginated_results = list(paginate_results(formatted_results, page_size))
            num_pages = len(paginated_results)

            if num_pages == 0:
                print("Немає результатів для відображення.")
                return

            # Виведення першої сторінки
            current_page = 1
            display_page(paginated_results[current_page - 1], current_page, num_pages)

            # Запит на відображення інших сторінок
            while True:
                user_input = input("\nВведіть 'n' для наступної сторінки, 'p' для попередньої, або 'q' для виходу: ").lower()

                if user_input == 'n' and current_page < num_pages:
                    current_page += 1
                    display_page(paginated_results[current_page - 1], current_page, num_pages)
                elif user_input == 'p' and current_page > 1:
                    current_page -= 1
                    display_page(paginated_results[current_page - 1], current_page, num_pages)
                elif user_input == 'q':
                    break
                else:
                    print("Невірна команда. Будь ласка, введіть 'n', 'p', або 'q'.")

        except Exception as e:
            print(f"Помилка при отриманні та виведенні результатів: {e}")


def get_students_below_score_paginated(subject_id, max_score, page_size=10):
    with Session(engine) as session:
        try:
            # Отримання результатів студентів за вказаним предметом та оцінкою
            results = (
                session.query(ResultsOfStudent)
                .filter(ResultsOfStudent.SubjectID == subject_id, ResultsOfStudent.Ball100 < max_score, ResultsOfStudent.Ball100 != 'NaN')
                .all()
            )

            # Створення списку для виведення результатів у вигляді PrettyTable
            formatted_results = [
                [
                    result.StudentID,
                    result.SubjectID,
                    result.Ball100
                ]
                for result in results
            ]

            # Розділення результатів на сторінки
            paginated_results = list(paginate_results(formatted_results, page_size))
            num_pages = len(paginated_results)

            if num_pages == 0:
                print("Немає результатів для відображення.")
                return

            # Виведення першої сторінки
            current_page = 1
            display_page(paginated_results[current_page - 1], current_page, num_pages)

            # Запит на відображення інших сторінок
            while True:
                user_input = input("\nВведіть 'n' для наступної сторінки, 'p' для попередньої, або 'q' для виходу: ").lower()

                if user_input == 'n' and current_page < num_pages:
                    current_page += 1
                    display_page(paginated_results[current_page - 1], current_page, num_pages)
                elif user_input == 'p' and current_page > 1:
                    current_page -= 1
                    display_page(paginated_results[current_page - 1], current_page, num_pages)
                elif user_input == 'q':
                    break
                else:
                    print("Невірна команда. Будь ласка, введіть 'n', 'p', або 'q'.")

        except Exception as e:
            print(f"Помилка при отриманні та виведенні результатів: {e}")


def app():

    while True:
        menu_text = """
        ---------------------------Меню програми---------------------------
            1. Додати нового студента
            2. Додати результати певного студента з предмету
            3. Видалити студента та всі його результати
            4. Додати новий навчальний заклад
            5. Видалити навчальний заклад
            6. Додати новий предмет
            7. Видалити предмет
            8. Вивести результати студента
            9. Вивести результати студентів з вказаного предмету, бал яких вищий за вказаний
            10. Вивести результати студентів з вказаного предмету, бал яких нищий за вказаний
            11. Пошук навчального закладу
            12. Видалити результати студента з обраного предмету
            0. Вийти
        --------------------------------------------------------------------
    """
        print(menu_text)

        user_input = input("Оберіть опцію: ")

        if user_input == '1':
            student_id = input("Уведіть ID студента: ")

            while True:    
                birth = input("Уведіть рік народження студента: ")
                try:
                    birth = int(birth)
                except Exception as e:
                    print(f"Уведіть числове значення року народження: {e}")
                    continue
                break

            while True:
                sexTypeName = input("Уведіть 1 - якщо студент чоловічої статі, 2 - якщо жіночої статі: ")
                    
                if sexTypeName == '1':
                    sexTypeName = 'чоловіча'
                elif sexTypeName == '2':
                    sexTypeName = 'жіноча'
                else:
                    print("Вказано некоректне значення. Спробуйте ще")
                    continue
                break

            regName = input("Регіон/проживання учасника: ")
            areaName = input("Район/Місто реєстрації/проживання учасника: ")
            terName = input("Населений пункт реєстрації/проживання учасника: ")
            regTypeName = input("Статус учасника: ")
            terTypeName = input("Тип території: ")
            classProfileName = input("Профіль навчання учасника/ОКР, який учасник здобуває: ")
            classLangName = input("Мова навчання учасника: ")

            student_data = {
                'ID': student_id,
                'Birth': birth,
                'SexTypeName': sexTypeName,
                'RegName': regName,
                'AreaName': areaName,
                'TerName': terName,
                'RegTypeName': regTypeName,
                'TerTypeName': terTypeName,
                'ClassProfileName': classProfileName,
                'ClassLangName': classLangName
            }

            add_student(student_data)

        elif user_input == '2':
            studentID = input("Укажіть ID учасника: ")
            subjectID = input("Назва навчального предмета: ")

            while True:
                year = input("Рік складання тесту: ")
                try:
                    year = int(year)

                    if year < 2021 or year > 2023:
                        print("Уведіть рік 2021 - 2023")
                        continue

                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue
                break

            lang = input("Мова складання тесту: ")
            
            while True:
                testStatus = input(
    """
    Результат складання тесту:
        1. Зараховано
        2. Не з'явився
        3. Не подолав поріг
    """)
                if testStatus == "1":
                    testStatus = "Зараховано"
                elif testStatus == "2":
                    testStatus = "Не з'явився"
                elif testStatus == "3":
                    testStatus = "Не подолав поріг"
                else:
                    print("Уведіть номер запропонованого варіанту!")
                    continue
                break
            
            if subjectID == "Ukr" or subjectID == "UML":
                while True:
                    ukrSubTest = input(
"""
Оберіть номер запропонованого варіанту:
    1. учасник проходив ЗНО з української мови  і літератури, отримав результат з української мови за підсумками  виконання завдань субтесту "Атестаційні завдання з української мови"
    2. учасник проходив ЗНО з української мови 
""")

                    if ukrSubTest == "1":
                        ukrSubTest = "Так"
                    elif ukrSubTest == "2":
                        ukrSubTest = "Ні"
                    else:
                        print("Уведіть номер запропонованого варіанту!")
                        continue
                    break
            else:
                ukrSubTest = None

            while True:
                dpaLevel = input(
"""
Рівень складності завдань ДПА: 
    1. стандарт(академічний)
    2. профільний
""")

                if dpaLevel == "1":
                    dpaLevel = "стандарт(академічний)"
                elif dpaLevel == "2":
                    dpaLevel = "профільний"
                else:
                    print("Уведіть номер запропонованого варіанту!")
                    continue
                break

            while True:    
                ball100 = input("Оцінка за шкалою 100-200: ")
                try:
                    ball100 = int(ball100)
                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue
                if ball100 < 100 or ball100 > 200:
                    print("Уведіть значення у межах від 100 до 200!")
                    continue
                break

            while True:    
                ball12 = input("Оцінка за шкалою 1-12: ")
                try:
                    ball12 = int(ball12)
                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue
                if ball12 < 1 or ball12 > 12:
                    print("Уведіть значення у межах від 1 до 12!")
                    continue
                break

            while True:    
                ball = input("Тестовий бал: ")
                try:
                    ball = int(ball)
                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue
                break
            
            while True:
                adaptScale = input(
"""
Установлення адаптивного порога:
    0 - не потребує
    3 - потребує (угорська мова навчання)
    4 - потребує (молдовська мова навчання)
    7 - потребує (румунська мова навчання)
""")
                
                if adaptScale == '0':
                    adaptScale = 0
                elif adaptScale == '3':
                    adaptScale = 3
                elif adaptScale == '4':
                    adaptScale = 4
                elif adaptScale == '7':
                    adaptScale = 7
                else:
                    print("Уведіть запропоноване число!")
                    continue
                break

            while True:
                institutionID = input("Укажіть ID навчального закладу, де учасник складав іспит: ")
                try:
                    institutionID = int(institutionID)
                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue
                break

            results_data = {
                'StudentID': studentID,
                'SubjectID': subjectID,
                'Year': year,
                'Lang': lang,
                'TestStatus': testStatus,
                'UkrSubTest': ukrSubTest,
                'DPALevel': dpaLevel,
                'Ball100': ball100,
                'Ball12': ball12,
                'Ball': ball,
                'AdaptScale': adaptScale
            }

            zno_place_data = {
                'StudentID': studentID,
                'SubjectID': subjectID,
                'InstitutionID': institutionID
            }

            add_results_of_student(results_data)
            if add_results_of_student:
                if not add_zno_place(zno_place_data):
                    delete_result_of_students(results_data)
        
        elif user_input == '3':
            studentID = input("Укажіть ID учасника: ")
            delete_student(studentID)

        elif user_input == '4':
            with Session(engine) as session:
                latest_record = session.query(EducationalInstitution).order_by(EducationalInstitution.created_at.desc()).first()

            eiID = latest_record.ID + 1
            name = input("Заклад освіти: ")
            typeName = input("Тип закладу освіти: ")
            regName = input("Регіон, де розташований заклад освіти: ")
            areaName = input("Район/Місто, де розташований заклад освіти: ")
            terName = input("Населений пункт, де розташований заклад освіти: ")
            parent = input("Орган, якому підпорядковується заклад освіти: ")

            educational_institutions_data = {
                'ID': eiID,
                'Name': name,
                'TypeName': typeName,
                'RegName': regName, 
                'AreaName': areaName,
                'TerName': terName,
                'Parent': parent
            }

            add_educational_institution(educational_institutions_data)

        elif user_input == '5':
            while True:    
                eiID = input("Укажіть ID навчального закладу: ")
                try:
                    eiID = int(eiID)
                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue
                break

            delete_educational_institution(eiID)
        
        elif user_input == '6':
            subjectID = input("Уведіть ID для нового предмету: ")
            name = input("Назва навчального предмета: ")

            subject_data = {
                'ID': subjectID,
                'Name': name
            }

            add_subject(subject_data)

        elif user_input == '7':
            subjectID = input("Уведіть ID предмету: ")
            delete_subject(subjectID)
        
        elif user_input == '8':
            studentID = input("Укажіть ID учасника: ")
            get_student_results(studentID)

        elif user_input == '9':
            subjectID = input("Уведіть ID предмету: ")

            while True:    
                minScore = input("Уведіть мінімальний бал: ")
                try:
                    minScore = int(minScore)
                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue

                if minScore < 100 or minScore > 200:
                    print("Уведіть значення у межах від 100 до 200!")
                    continue

                break
            
            get_students_above_score_paginated(subjectID, minScore)

        elif user_input == '10':
            subjectID = input("Уведіть ID предмету: ")

            while True:    
                maxScore = input("Уведіть максимальний бал: ")
                try:
                    maxScore = int(maxScore)
                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue

                if maxScore < 100 or maxScore > 200:
                    print("Уведіть значення у межах від 100 до 200!")
                    continue

                break

            get_students_below_score_paginated(subjectID, maxScore)

        elif user_input == '11':
            search_name = input("Введіть назву навчального закладу для пошуку: ")
            search_institution_by_name(search_name)

        elif user_input == '12':
            studentID = input("Укажіть ID учасника: ")
            subjectID = input("Уведіть ID предмету: ")

            while True:
                year = input("Рік складання тесту: ")
                try:
                    year = int(year)

                    if year < 2021 or year > 2023:
                        print("Уведіть рік 2021 - 2023")
                        continue

                except Exception as e:
                    print(f"Уведіть числове ціле значення: {e}")
                    continue
                break

            result_data = {
                'StudentID': studentID,
                'SubjectID': subjectID,
                'Year': year
            }

            delete_result_by_subject(result_data)

        elif user_input == '0':
            break


app()