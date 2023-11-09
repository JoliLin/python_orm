import pathlib
import sys

p = pathlib.Path(__file__).resolve().parent.parent
sys.path.append('{}/'.format(p))

from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from configs import get_settings

settings = get_settings('record')

class ORMObject():
    def __init__(self):
        record_host = settings.record_host
        record_user = settings.record_user
        record_password = settings.record_password
        record_name = settings.record_name
        Base = declarative_base()
    
        engine_url = 'mysql+pymysql://{}:{}@{}/{}'.format(record_user, record_password, record_host, record_name)
        self.engine = create_engine(engine_url, echo=True)

    def create_table(self, table=None):
        if table == None:
            Base.metadata.create_all(self.engine)
        else:
            table.__table__.create(bind=self.engine, checkfirst=True)

    def drop_table(self, table=None):
        if table == None:
            Base.metadata.drop_all(self.engine)
        else:
            table.__table__.drop(bind=self.engine, checkfirst=True)
    
    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def save_data(self, data):
        # ex: Test(id='5', name='Bob')
        session = self.create_session()
        session.add(data)
        session.commit()
        session.close()
    
    def query_all(self, table):
        session = self.create_session()
        res = session.query(table).all()  
        session.close()
        return res

if __name__ == '__main__':
    from orm import Test 

    orm = ORMObject()

    orm.create_table(Test)
