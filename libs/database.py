from config.conf import dbconf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base() #create Base lei
engine = create_engine('mysql://%(db_user)s:%(db_pass)s@%(host)s/%(db_name)s?charset=utf8&autocommit=true' % dbconf,
                 encoding='utf-8', echo=False,
                   pool_size=100, pool_recycle=3600)
DB_Session = sessionmaker(bind=engine)
