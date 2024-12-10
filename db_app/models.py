from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    value = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
