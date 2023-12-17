from sqlalchemy import create_engine, MetaData, Table, select, literal, union, cast, String
import pandas as pd
from new_database_structure import *
from sql_queues import *


old_engine = create_engine('postgresql://postgres:postgres@localhost/results_zno')
new_engine = create_engine('postgresql://postgres:postgres@localhost/results_zno_new')

Base.metadata.create_all(old_engine)

# Визначення метаданих та таблиці для старої бази даних
metadata_old = MetaData()
table_old = Table('Results_ZNO_2021', metadata_old, autoload_with=old_engine)

# Визначення метаданих та таблиці для нової бази даних
metadata_new = MetaData()
table_students_new = Table('Students', metadata_new, autoload_with=new_engine)
table_subjects = Table('Subjects', metadata_new, autoload_with=new_engine)
table_results_of_students = Table('Results_Of_Students', metadata_new, autoload_with=new_engine)
table_educational_institutions = Table('Educational_Institutions', metadata_new, autoload_with=new_engine)


select_info_students = (table_old
    .select()
    .with_only_columns([
        table_old.c.OUTID,
        table_old.c.BIRTH,
        table_old.c.SEXTYPENAME,
        table_old.c.REGNAME,
        table_old.c.AREANAME,
        table_old.c.TERNAME,
        table_old.c.REGTYPENAME,
        table_old.c.TERTYPENAME,
        table_old.c.CLASSPROFILENAME,
        table_old.c.CLASSLANGNAME,
    ])
)

subjects = [
    {'ID': 'UML', 'Name': 'Українська мова і література'},
    {'ID': 'Ukr', 'Name': 'Українська мова'},
    {'ID': 'Hist', 'Name': 'Історія України'},
    {'ID': 'Math', 'Name': 'Математика'},
    {'ID': 'MathSt', 'Name': 'Математика (завдання рівня стандарту)'},
    {'ID': 'Phys', 'Name': 'Фізика'},
    {'ID': 'Chem', 'Name': 'Хімія'},
    {'ID': 'Bio', 'Name': 'Біологія'},
    {'ID': 'Geo', 'Name': 'Географія'},
    {'ID': 'Eng', 'Name': 'Англійська мова'},
    {'ID': 'Fr', 'Name': 'Французька мова'},
    {'ID': 'Deu', 'Name': 'Німецька мова'},
    {'ID': 'Sp', 'Name': 'Іспанська мова'},
]

select_st_UML = select(
    [
        table_old.c.OUTID,
        literal('UML'),
        table_old.c.YEAR,
        None,
        table_old.c.UMLTESTSTATUS,
        None,
        None,
        table_old.c.UMLBALL100,
        table_old.c.UMLBALL12,
        table_old.c.UMLBALL,
        table_old.c.UMLADAPTSCALE
    ]
)

select_st_Ukr = select(
    [
        table_old.c.OUTID,
        literal('Ukr'),
        table_old.c.YEAR,
        None,
        table_old.c.UKRTESTSTATUS,
        table_old.c.UKRSUBTEST,
        None,
        table_old.c.UKRBALL100,
        table_old.c.UKRBALL12,
        table_old.c.UKRBALL,
        table_old.c.UKRADAPTSCALE
    ]
)

select_st_Hist = select(
    [
        table_old.c.OUTID,
        literal('Hist'),
        table_old.c.YEAR,
        table_old.c.HISTLANG,
        table_old.c.HISTTESTSTATUS,
        None,
        None,
        table_old.c.HISTBALL100,
        table_old.c.HISTBALL12,
        table_old.c.HISTBALL,
        0.0
    ]
)

select_st_Math = select(
    [
        table_old.c.OUTID,
        literal('Math'),
        table_old.c.YEAR,
        table_old.c.MATHLANG,
        table_old.c.MATHTESTSTATUS,
        None,
        table_old.c.MATHDPALEVEL,
        table_old.c.MATHBALL100,
        table_old.c.MATHBALL12,
        table_old.c.MATHBALL,
        0.0
    ]
)

select_st_MathSt = select(
    [
        table_old.c.OUTID,
        literal('MathSt'),
        table_old.c.YEAR,
        table_old.c.MATHSTLANG,
        table_old.c.MATHSTTESTSTATUS,
        None,
        None,
        None,
        table_old.c.MATHSTBALL12,
        table_old.c.MATHSTBALL,
        0.0
    ]
)

select_st_Phys = select(
    [
        table_old.c.OUTID,
        literal('Phys'),
        table_old.c.YEAR,
        table_old.c.PHYSLANG,
        table_old.c.PHYSTESTSTATUS,
        None,
        None,
        table_old.c.PHYSBALL100,
        table_old.c.PHYSBALL12,
        table_old.c.PHYSBALL,
        0.0
    ]
)

select_st_Chem = select(
    [
        table_old.c.OUTID,
        literal('Chem'),
        table_old.c.YEAR,
        table_old.c.CHEMLANG,
        table_old.c.CHEMTESTSTATUS,
        None,
        None,
        table_old.c.CHEMBALL100,
        table_old.c.CHEMBALL12,
        table_old.c.CHEMBALL,
        0.0
    ]
)

select_st_Bio = select(
    [
        table_old.c.OUTID,
        literal('Bio'),
        table_old.c.YEAR,
        table_old.c.BIOLANG,
        table_old.c.BIOTESTSTATUS,
        None,
        None,
        table_old.c.BIOBALL100,
        table_old.c.BIOBALL12,
        table_old.c.BIOBALL,
        0.0
    ]
)

select_st_Geo = select(
    [
        table_old.c.OUTID,
        literal('Geo'),
        table_old.c.YEAR,
        table_old.c.GEOLANG,
        table_old.c.GEOTESTSTATUS,
        None,
        None,
        table_old.c.GEOBALL100,
        table_old.c.GEOBALL12,
        table_old.c.GEOBALL,
        0.0
    ]
)

select_st_Eng = select(
    [
        table_old.c.OUTID,
        literal('Eng'),
        table_old.c.YEAR,
        None,
        table_old.c.ENGTESTSTATUS,
        None,
        table_old.c.ENGDPALEVEL,
        table_old.c.ENGBALL100,
        table_old.c.ENGBALL12,
        table_old.c.ENGBALL,
        0.0
    ]
)

select_st_Fr = select(
    [
        table_old.c.OUTID,
        literal('Fr'),
        table_old.c.YEAR,
        None,
        table_old.c.FRATESTSTATUS,
        None,
        table_old.c.FRADPALEVEL,
        table_old.c.FRABALL100,
        table_old.c.FRABALL12,
        table_old.c.FRABALL,
        0.0
    ]
)

select_st_Deu = select(
    [
        table_old.c.OUTID,
        literal('Deu'),
        table_old.c.YEAR,
        None,
        table_old.c.DEUTESTSTATUS,
        None,
        table_old.c.DEUDPALEVEL,
        table_old.c.DEUBALL100,
        table_old.c.DEUBALL12,
        table_old.c.DEUBALL,
        0.0
    ]
)

select_st_Sp = select(
    [
        table_old.c.OUTID,
        literal('Sp'),
        table_old.c.YEAR,
        None,
        table_old.c.SPATESTSTATUS,
        None,
        cast(table_old.c.SPADPALEVEL, String),
        table_old.c.SPABALL100,
        table_old.c.SPABALL12,
        table_old.c.SPABALL,
        0.0
    ]
)

select_results_of_students = union(
    select_st_UML,
    select_st_Ukr,
    select_st_Math,
    select_st_MathSt,
    select_st_Hist,
    select_st_Phys,
    select_st_Bio,
    select_st_Chem,
    select_st_Geo,
    select_st_Eng,
    select_st_Fr,
    select_st_Deu,
    select_st_Sp
)

def main():
    with old_engine.connect() as old_connection, new_engine.connect() as new_connection:
        info_students = old_connection.execute(select_info_students)
        info_students_rows = info_students.fetchall()

        for row in info_students_rows:
            insert_query = table_students_new.insert().values(
                ID=row.OUTID,
                Birth=row.BIRTH,
                SexTypeName=row.SEXTYPENAME,
                RegName=row.REGNAME,
                AreaName=row.AREANAME,
                TerName=row.TERNAME,
                RegTypeName=row.REGTYPENAME,
                TerTypeName=row.TERTYPENAME,
                ClassProfileName=row.CLASSPROFILENAME,
                ClassLangName=row.CLASSLANGNAME
            )
            new_connection.execute(insert_query)

        for row in subjects:
            insert_query = table_subjects.insert().values(row)
            new_connection.execute(insert_query)

        results_of_students = old_connection.execute(select_results_of_students)
        results_of_students_rows = results_of_students.fetchall()

        for row in results_of_students_rows:
            insert_query = table_results_of_students.insert().values(row)
            new_connection.execute(insert_query)

        old_connection.execute(insert_students)
        old_connection.execute(insert_subjects)
        
        old_connection.execute(insert_educational_institutions)
        query = 'SELECT * FROM "Educational_Institutions";'
        df = pd.read_sql_query(query, old_engine)
        df.to_sql('Educational_Institutions', new_engine, if_exists='append', index=False)

        old_connection.execute(insert_ei_of_students)
        query = 'SELECT * FROM "EI_of_Students";'
        df = pd.read_sql_query(query, old_engine)
        df.to_sql('EI_of_Students', new_engine, if_exists='append', index=False)

        old_connection.execute(insert_zno_places)
        query = 'SELECT * FROM "ZNO_Places";'
        df = pd.read_sql_query(query, old_engine)
        df.to_sql('ZNO_Places', new_engine, if_exists='append', index=False)

        old_connection.execute('DROP TABLE "ZNO_Places";')
        old_connection.execute('DROP TABLE "Results_Of_Students";')
        old_connection.execute('DROP TABLE "EI_of_Students";')
        old_connection.execute('DROP TABLE "Subjects";')
        old_connection.execute('DROP TABLE "Students";')
        old_connection.execute('DROP TABLE "Educational_Institutions";')


if __name__ == "__main__":
    main()