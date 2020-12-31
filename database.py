import json
from enum import IntEnum
from sqlalchemy import create_engine, exists, desc, or_
from sqlalchemy import Column, String, Integer, Date, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


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


class DbSession(object):
    def __init__(self, Session, with_commit=False):
        self.Session = Session
        self.with_commit = with_commit

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.with_commit:
            self.session.commit()
        self.session.close()


class Database:
    def __init__(self):
        with open('config.json') as config_file:
            config = json.loads(config_file.read())['db']
        self.engine = create_engine('postgresql://{}:{}@{}/{}'.format(config['user'], config['password'],
                                                                      config['host'], config['db_name']))
        session_factory = sessionmaker(self.engine)
        self.Session = scoped_session(session_factory)
        base.metadata.create_all(self.engine)

    def add_user(self, vk_id, state, state_payload="{}", universities=None, sending_time=None,
                 last_sending_date=None, topics=None):
        with DbSession(self.Session, with_commit=True) as session:
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
            session.add(new_user)
            session.add(new_user)

    def is_user_exist(self, user_id):
        with DbSession(self.Session) as session:
            return session.query(exists().where(User.vk_id == user_id)).scalar()

    def add_news(self, date, university, title, link, theme=None, photo_id=None):
        with DbSession(self.Session, with_commit=True) as session:
            if session.query(News).filter(News.link == link).count() == 0:
                new_news = News(date=date, university=university, title=title, theme=theme, link=link,
                                photo_id=photo_id)
                session.add(new_news)

    def get_user(self, user_id, session=None):
        if session is None:
            with DbSession(self.Session) as new_session:
                return new_session.query(User).filter(User.vk_id == user_id).one()
        else:
            return session.query(User).filter(User.vk_id == user_id).one()

    def set_topics(self, user_id, topics):
        with DbSession(self.Session, with_commit=True) as session:
            self.get_user(user_id, session).topics = topics

    def set_universities(self, user_id, universities):
        with DbSession(self.Session, with_commit=True) as session:
            self.get_user(user_id, session).universities = universities

    def set_sending_time(self, user_id, sending_time):
        with DbSession(self.Session, with_commit=True) as session:
            self.get_user(user_id, session).sending_time = sending_time

    def set_user_state(self, user_id, state, state_payload):
        with DbSession(self.Session, with_commit=True) as session:
            user = self.get_user(user_id, session)
            user.state = state
            if state_payload is not None:
                user.state_payload = state_payload

    def set_user_state_payload(self, user_id, state_payload):
        with DbSession(self.Session, with_commit=True) as session:
            user = self.get_user(user_id, session)
            user.state_payload = state_payload

    def get_news(self, universities, last_date=None, topics=None):
        with DbSession(self.Session) as session:
            news = session.query(News).filter(News.university.in_(universities))
            if last_date is not None:
                news = news.filter(News.date > last_date)
            if topics is not None and topics != []:
                news = news.filter(News.theme.in_(topics))
            return news.order_by(desc(News.date))

    def get_news_by_ids(self, list_with_ids):
        with DbSession(self.Session) as session:
            return session.query(News).filter(News.id.in_(list_with_ids)).order_by(
                desc(News.id))

    def get_subscribed_users_to_send_news(self, list_of_suitable_sending_dates, current_date):
        with DbSession(self.Session) as session:
            return session.query(User). \
                filter(User.sending_time.in_(list_of_suitable_sending_dates)). \
                filter(or_(User.last_sending_date.is_(None), User.last_sending_date < current_date)). \
                filter(User.universities != [])
