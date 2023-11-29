from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from lab2.sql_queues import *

Base = declarative_base()

class Student(Base):
    __tablename__ = 'Students'
    ID = Column(String(300), primary_key=True)
    Birth = Column(Integer)
    SexTypeName = Column(String(300))
    RegName = Column(String(300))
    AreaName = Column(String(300))
    TerName = Column(String(300))
    RegTypeName = Column(String(300))
    TerTypeName = Column(String(300))
    ClassProfileName = Column(String(300))
    ClassLangName = Column(String(300))

class EducationalInstitution(Base):
    __tablename__ = 'Educational_Institutions'
    ID = Column(Integer, primary_key=True)
    Name = Column(String(300))
    TypeName = Column(String(300))
    RegName = Column(String(300))
    AreaName = Column(String(300))
    TerName = Column(String(300))
    Parent = Column(String(300))

class EIOfStudent(Base):
    __tablename__ = 'EI_of_Students'
    StudentID = Column(String(300), ForeignKey('Students.ID'), primary_key=True)
    EIID = Column(Integer, ForeignKey('Educational_Institutions.ID'), primary_key=True)
    student = relationship('Student')
    educational_institution = relationship('EducationalInstitution')

class Subject(Base):
    __tablename__ = 'Subjects'
    ID = Column(String(50), primary_key=True)
    Name = Column(String(300))

class ZNOPlace(Base):
    __tablename__ = 'ZNO_Places'
    StudentID = Column(String(300), ForeignKey('Students.ID'), primary_key=True)
    SubjectID = Column(String(50), ForeignKey('Subjects.ID'), primary_key=True)
    InsitutionID = Column(Integer, ForeignKey('Educational_Institutions.ID'), primary_key=True)
    student = relationship('Student')
    subject = relationship('Subject')
    educational_institution = relationship('EducationalInstitution')

class ResultsOfStudent(Base):
    __tablename__ = 'Results_Of_Students'
    StudentID = Column(String(300), ForeignKey('Students.ID'), primary_key=True)
    SubjectID = Column(String(50), ForeignKey('Subjects.ID'), primary_key=True)
    Year = Column(Integer)
    Lang = Column(String(100))
    TestStatus = Column(String(100))
    UkrSubTest = Column(String(100))
    DPALevel = Column(String(100))
    Ball100 = Column(Float)
    Ball12 = Column(Float)
    Ball = Column(Float)
    AdaptScale = Column(Float)
    student = relationship('Student')
    subject = relationship('Subject')