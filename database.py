import logging

import psycopg2
import json
from enum import IntEnum
import sqlalchemy
from sqlalchemy import create_engine, exists, desc, or_
from sqlalchemy import Column, String, Integer, Date, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class UniversityTypes(IntEnum):
    SPBSU = 0


base = declarative_base()


class User(base):
    __tablename__ = 'users'

    vk_id = Column(Integer, primary_key=True)
    state = Column(Integer)
    state_payload = Column(String)
    sending_time = Column(String)
    universities = Column(ARRAY(String))
    topics = Column(ARRAY(String))
    last_sending_date = Column(Date)


class News(base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    university = Column(String)
    title = Column(String)
    theme = Column(String)
    link = Column(String)
    photo_id = Column(String)


class Database:
    def __init__(self):
        self.engine = create_engine('postgresql://postgres:24682468@localhost/vk_bot')
        session = sessionmaker(self.engine)
        self.session = session()
        base.metadata.create_all(self.engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_user(self, vk_id, state, state_payload="{}", universities=None, sending_time=None,
                 last_sending_date=None, topics=None):
        if topics is None:
            topics = []
        if universities is None:
            universities = []
        new_user = User(vk_id=vk_id, state=state,
                        state_payload=state_payload,
                        universities=universities,
                        sending_time=sending_time,
                        last_sending_date=last_sending_date,
                        topics=topics)
        self.session.add(new_user)
        self.session.commit()

    def is_user_exist(self, user_id):
        return self.session.query(exists().where(User.vk_id == user_id)).scalar()

    def add_news(self, date, university, title, link, theme=None, photo_id=None):
        new_news = News(date=date, university=university, title=title, theme=theme, link=link, photo_id=photo_id)
        self.session.add(new_news)
        self.session.commit()

    def get_user(self, user_id):
        return self.session.query(User).filter(User.vk_id == user_id).one()

    def set_topics(self, user_id, topics):
        user = self.get_user(user_id)
        user.topics = topics
        self.session.commit()

    def get_topics(self, user_id):
        return self.get_user(user_id.user_id).topics

    def set_universities(self, user_id, universities):
        user = self.get_user(user_id)
        user.universities = universities
        self.session.commit()

    def set_sending_time(self, user_id, sending_time):
        user = self.get_user(user_id)
        user.sending_time = sending_time
        self.session.commit()

    def set_user_state(self, user_id, state, state_payload):
        user = self.get_user(user_id)
        user.state = state
        if state_payload is not None:
            user.state_payload = state_payload
        self.session.commit()

    def get_user_state(self, user_id):
        return self.get_user(user_id).state

    def get_user_state_payload(self, user_id):
        return self.get_user(user_id).state_payload

    def set_user_state_payload(self, user_id, state_payload):
        user = self.get_user(user_id)
        user.state_payload = state_payload
        self.session.commit()

    def get_subscribed_universities(self, user_id):
        return self.get_user(user_id).universities

    def get_news(self, universities, last_date=None, topics=None):
        news = self.session.query(News).filter(News.university.in_(universities))
        if last_date is not None:
            news = news.filter(News.date > last_date)
        if topics is not None and topics != []:
            news = news.filter(News.theme.in_(topics))
        return news.order_by(desc(News.date))

    def get_news_by_ids(self, list_with_ids):
        return self.session.query(News).filter(News.id.in_(list_with_ids)).order_by(
            desc(News.id))

    def get_subscribed_users_to_send_news(self, list_of_suitable_sending_dates, current_date):
        return self.session.query(User). \
            filter(User.sending_time.in_(list_of_suitable_sending_dates)). \
            filter(or_(User.last_sending_date.is_(None), User.last_sending_date < current_date)). \
            filter(User.universities != [])