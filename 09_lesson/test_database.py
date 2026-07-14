import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:Venom2906@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer)


@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_student(db_session):
    student_name = "Тестовый Студент Создание"
    new_student = Student(name=student_name, age=20)
    db_session.add(new_student)
    db_session.commit()
    queried_student = db_session.query(
        Student).filter_by(name=student_name).first()
    assert queried_student is not None
    assert queried_student.age == 20

    db_session.delete(queried_student)
    db_session.commit()


def test_update_student(db_session):
    student_name = "Тестовый Студент Изменение"
    test_student = Student(name=student_name, age=21)
    db_session.add(test_student)
    db_session.commit()

    test_student.age = 25
    db_session.commit()

    updated_student = db_session.query(
        Student).filter_by(name=student_name).first()
    assert updated_student.age == 25

    db_session.delete(updated_student)
    db_session.commit()


def test_delete_student(db_session):
    student_name = "Тестовый Студент Удаление"
    test_student = Student(name=student_name, age=22)
    db_session.add(test_student)
    db_session.commit()
    assert db_session.query(
        Student).filter_by(
            name=student_name).first() is not None

    db_session.delete(test_student)
    db_session.commit()

    deleted_student = db_session.query(
        Student).filter_by(
            name=student_name).first()
    assert deleted_student is None
