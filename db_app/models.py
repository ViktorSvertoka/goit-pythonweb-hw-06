from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    group_name = Column(String(50), nullable=False)
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    student_name = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String(100), nullable=False)
    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column(DateTime, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
