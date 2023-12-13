

insert_students = """
    INSERT INTO "Students" ("ID", "Birth", "SexTypeName", "RegName", "AreaName", "TerName", "RegTypeName", "TerTypeName", "ClassProfileName", "ClassLangName")
    SELECT TRIM("OUTID"), "BIRTH", TRIM("SEXTYPENAME"), TRIM("REGNAME"), TRIM("AREANAME"), TRIM("TERNAME"), TRIM("REGTYPENAME"), TRIM("TERTYPENAME"), TRIM("CLASSPROFILENAME"), TRIM("CLASSLANGNAME")
    FROM "Results_ZNO_2021";
"""

insert_subjects = """
    INSERT INTO "Subjects" ("ID", "Name")
    VALUES ('UML', 'Українська мова і література'),
    ('Ukr', 'Українська мова'),
    ('Hist', 'Історія України'),
    ('Math', 'Математика'),
    ('MathSt', 'Математика (завдання рівня стандарту)'),
    ('Phys', 'Фізика'),
    ('Chem', 'Хімія'),
    ('Bio', 'Біологія'),
    ('Geo', 'Географія'),
    ('Eng', 'Англійська мова'),
    ('Fr', 'Французька мова'),
    ('Deu', 'Німецька мова'),
    ('Sp', 'Іспанська мова');
"""

insert_educational_institutions = """
    INSERT INTO "Educational_Institutions" ("Name", "TypeName", "RegName", "AreaName", "TerName", "Parent")
SELECT DISTINCT "EONAME" as "Name",
	"EOTYPENAME" as "TypeName",
	"EOREGNAME" as "RegName",
	"EOAREANAME" as "AreaName",
	"EOTERNAME" as "TerName",
	"EOPARENT" as "Parent"
FROM "Results_ZNO_2021" FULL OUTER JOIN
	(SELECT DISTINCT *
	FROM
		(
			SELECT "UMLPTNAME" as "Name",
			"UMLPTREGNAME" as "RegName",
			"UMLPTAREANAME" as "AreaName",
			"UMLPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "UKRPTNAME" as "Name",
				"UKRPTREGNAME" as "RegName",
				"UKRPTAREANAME" as "AreaName",
				"UKRPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "HISTPTNAME" as "Name",
				"HISTPTREGNAME" as "RegName",
				"HISTPTAREANAME" as "AreaName",
				"HISTPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "MATHPTNAME" as "Name",
				"MATHPTREGNAME" as "RegName",
				"MATHPTAREANAME" as "AreaName",
				"MATHPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "MATHSTPTNAME" as "Name",
				"MATHSTPTREGNAME" as "RegName",
				"MATHSTPTAREANAME" as "AreaName",
				"MATHSTPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "PHYSPTNAME" as "Name",
				"PHYSPTREGNAME" as "RegName",
				"PHYSPTAREANAME" as "AreaName",
				"PHYSPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "CHEMPTNAME" as "Name",
				"CHEMPTREGNAME" as "RegName",
				"CHEMPTAREANAME" as "AreaName",
				"CHEMPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "BIOPTNAME" as "Name",
				"BIOPTREGNAME" as "RegName",
				"BIOPTAREANAME" as "AreaName",
				"BIOPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "GEOPTNAME" as "Name",
				"GEOPTREGNAME" as "RegName",
				"GEOPTAREANAME" as "AreaName",
				"GEOPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "GEOPTNAME" as "Name",
				"GEOPTREGNAME" as "RegName",
				"GEOPTAREANAME" as "AreaName",
				"GEOPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "FRAPTNAME" as "Name",
				"FRAPTREGNAME" as "RegName",
				"FRAPTAREANAME" as "AreaName",
				"FRAPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "DEUPTNAME" as "Name",
				"DEUPTREGNAME" as "RegName",
				"DEUPTAREANAME" as "AreaName",
				"DEUPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
			UNION
			SELECT "SPAPTNAME" as "Name",
				"SPAPTREGNAME" as "RegName",
				"SPAPTAREANAME" as "AreaName",
				"SPAPTTERNAME" as "TerName"
			FROM "Results_ZNO_2021"
		) as "TestLocations"
	 ) as "tmp"
	ON "Results_ZNO_2021"."EONAME" = "tmp"."Name" AND
		"Results_ZNO_2021"."EOREGNAME" = "tmp"."RegName" AND
		"Results_ZNO_2021"."EOAREANAME" = "tmp"."AreaName" AND
		"Results_ZNO_2021"."EOTERNAME" = "tmp"."TerName";
"""

insert_ei_of_students = """
    INSERT INTO "EI_of_Students" ("StudentID", "EIID")
    SELECT "RZ"."OUTID", "EI"."ID"
    FROM "Results_ZNO_2021" AS "RZ"
    JOIN "Educational_Institutions" AS "EI"
    ON "RZ"."EONAME" = "EI"."Name";
"""

insert_zno_places = """
    INSERT INTO "ZNO_Places" ("StudentID", "SubjectID", "InsitutionID")
	SELECT "RZ"."OUTID", 'UML', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."UMLPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Ukr', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."UKRPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Hist', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."HISTPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Math', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."MATHPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'MathSt', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."MATHSTPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Phys', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."PHYSPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Chem', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."CHEMPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Bio', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."BIOPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Geo', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."GEOPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Eng', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."ENGPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Fr', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."FRAPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Deu', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."DEUPTNAME" = "EI"."Name"
	UNION
	SELECT "RZ"."OUTID", 'Sp', "EI"."ID"
	FROM "Results_ZNO_2021" as "RZ"
	JOIN "Educational_Institutions" AS "EI"
	ON "RZ"."SPAPTNAME" = "EI"."Name";
"""