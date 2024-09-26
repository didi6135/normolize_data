import logging

from config.base import Base, engine


def create_tables():
    Base.metadata.create_all(bind=engine)
    logging.info('table created')

def drop_tables():
    Base.metadata.drop_all(bind=engine)