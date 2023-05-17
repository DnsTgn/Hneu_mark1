import logging
import os
from sqlalchemy import create_engine, Column, Integer, Text, BIGINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
def set_base():
    global Base
    Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(BIGINT, unique=True, nullable=False,primary_key=True)
    math = Column(Integer, nullable=True)
    ukr = Column(Integer, nullable=True)
    add_subj_mark = Column(Integer, nullable=True)
    additional_subj_name = Column(Text, nullable=True)


class SpecList(Base):
    __tablename__ = 'spec_list'

    spec_code = Column(Text, primary_key=True)
    amount = Column(Integer)


class database:
    instance = None
    session = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        #if self.session == None:
        logging.debug("Database instance created.")
        self.engine = create_engine(
            f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB")}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def add_user(self, user_id):# +
        try:
            user = User(user_id=user_id)
            self.session.merge(user)
            self.session.commit()
            logging.info(f"User with user_id {user_id} was added.")
        except:
            self.session.rollback()
            logging.error(f"User with user_id {user_id} was not added due to an error.")

    def add_additional_subj_name(self, additional_subj_name, user_id): #+
        try:
            self.session.query(User).filter(User.user_id == user_id).update({User.additional_subj_name: additional_subj_name})
            self.session.commit()
            logging.info(f"Additional subject name '{additional_subj_name}' was added for user with user_id {user_id}.")
        except:
            self.session.rollback()
            logging.error(f"Additional subject name for user with user_id {user_id} was not added due to an error.")

    def add_mark(self, subject, mark, user_id): #+
        try:
            self.session.query(User).filter(User.user_id == user_id).update({getattr(User, subject): mark})
            self.session.commit()
            logging.info(f"Mark {mark} for {subject} was added for user with user_id {user_id}.")
        except:
            self.session.rollback()
            logging.error(f"Mark {subject} for user with user_id {user_id} was not added due to an error.")

    def add_spec_amount(self, spec_code): #+?
        try:
            self.session.query(SpecList).filter(SpecList.spec_code == spec_code).update({SpecList.amount: SpecList.amount+1})
            self.session.commit()
            logging.info(f"1 was added to spec_code {spec_code}.")
        except:
            self.session.rollback()
            logging.warn(f"1 was not added to spec_code {spec_code}.")



    def get_user_info(self, user_id):#+?
        try:
            user_info = self.session.query(User).filter(User.user_id == user_id).one()
            logging.info(f"User info for user with user_id {user_id} was retrieved.")
            return user_info
        except:
            logging.error(f"No user info was retrieved for user with user_id {user_id}.")

    def get_all_users(self): #+?
        try:
            user_ids = [user[0] for user in self.session.query(User.user_id).all()]
            logging.info("All user IDs were retrieved.")
            return user_ids
        except:
            logging.error("No user IDs were retrieved.")

    def get_user_count(self):#+?
        try:
            user_count = self.session.query(User).count()
            logging.info("User count was retrieved.")
            return user_count
        except:
            logging.error("User count was not retrieved.")

    def get_stats(self):#+?
        try:
            stats = self.session.query(SpecList.spec_code, SpecList.amount).order_by(SpecList.amount.desc()).all()
            logging.info("Stats were retrieved.")
            return stats
        except:
            logging.error("Stats were not retrieved.")