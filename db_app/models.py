from datetime import datetime
from sqlalchemy import ForeignKey, Float, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    students: Mapped[list["Student"]] = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    group: Mapped[Group] = relationship("Group", back_populates="students")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="student")


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", back_populates="teacher"
    )


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    teacher: Mapped[Teacher] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[list["Grade"]] = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    student: Mapped[Student] = relationship("Student", back_populates="grades")
    subject: Mapped[Subject] = relationship("Subject", back_populates="grades")
