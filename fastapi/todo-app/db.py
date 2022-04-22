from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

# SQLALCHEMY_SQLITE_DATABASE_URL = 'sqlite:///./todos.db';
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/todos_db';
SQLALCHEMY_MYSQL_DATABASE_URL = 'mysql+pymysql://root:root@127.0.0.1:3006/todos_db';

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
