import logging

from sqlalchemy import Column, JSON, String, DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine("sqlite://", echo=True, future=True)

Base = declarative_base()


class Resource(Base):
    __tablename__ = 'Resource'

    resource = Column(String, primary_key=True)
    last_data = Column(JSON)
    date = Column(DateTime)

    def __init__(self, resource, data, date):
        self.resource = resource
        self.last_data = data
        self.date = date


class DBHelper:
    def __init__(self, sqlite_filepath: str):
        self.engine = create_engine(f"sqlite:///{sqlite_filepath}")
        Base.metadata.create_all(self.engine, checkfirst=True)
        print(Base.metadata.tables.keys())

    def update_info(self, resource, data, date):
        try:
            with sessionmaker(self.engine)() as session:
                db_item = session.query(Resource).filter_by(resource=resource).first()
                if db_item:
                    db_item.last_data = data
                    db_item.date = date
                else:
                    session.add(Resource(resource=resource, data=data, date=date))

                session.commit()
                return True

        except SQLAlchemyError as e:
            logging.error(e.args)
            session.rollback()
            return False

    def get_info(self, resource):
        try:
            with sessionmaker(self.engine)() as session:
                return session.query(Resource).filter_by(resource=resource).all()

        except SQLAlchemyError as e:
            logging.error(e.args)
            return False

