from sqlalchemy import create_engine, Column, Integer, String, Float, Numeric, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base








# Initialize the database connection
DATABASE_URI = 'postgresql+psycopg2://user:password@localhost:5432/your_db'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Create all tables in the database
Base.metadata.create_all(engine)

if __name__ == '__main__':
    print('hi')


