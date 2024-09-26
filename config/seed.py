import psycopg2
from sqlalchemy import create_engine, MetaData
from config.base import Base
from model.City import City
from model.Country import Country
from model.Target import Target
from model.TargetIndustry import TargetIndustry
from model.TargetType import TargetType
from model.Mission import Mission


# Step 1: Create the normalized tables in the existing wwii_missions database
def create_normalized_tables():
    try:
        DATABASE_URI = 'postgresql://postgres:1234@localhost/wwii_missions'
        engine = create_engine(DATABASE_URI)

        # Get the current metadata and reflect it to get existing table information
        metadata = MetaData()
        metadata.reflect(bind=engine)

        # Drop all tables except 'mission'
        tables_to_drop = [table for table in metadata.sorted_tables if table.name != 'mission']
        Base.metadata.drop_all(engine, tables=tables_to_drop)
        print(f"Dropped tables: {', '.join([table.name for table in tables_to_drop])}")

        # Recreate the normalized tables (this won't recreate 'mission')
        Base.metadata.create_all(engine)
        print("Normalized tables created successfully in wwii_missions database.")

    except Exception as e:
        print(f"Error creating tables: {e}")


# Step 2: Transfer data from the unnormalized 'mission' table to the new normalized schema
def transfer_data():
    try:
        # Connect to the source database
        source_conn = psycopg2.connect(dbname="wwii_missions", user="postgres", password="1234", host="localhost")
        source_cur = source_conn.cursor()

        # Fetch the relevant data from the 'mission' table, including mission_id
        source_cur.execute("""
            SELECT DISTINCT mission_id, target_country, target_city, target_type, target_industry, target_priority, target_latitude, target_longitude, mission_date
            FROM mission
        """)
        rows = source_cur.fetchall()

        # Insert the normalized data into the new database
        for row in rows:
            mission_id, country, city, target_type, industry, priority, latitude, longitude, mission_date = row

            # Insert country if not None
            if country:
                source_cur.execute(
                    "INSERT INTO country (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING country_id",
                    (country,))
                result = source_cur.fetchone()
                country_id = result[0] if result else None
            else:
                country_id = None

            # Insert city if not None and country_id exists
            if city and country_id:
                source_cur.execute(
                    "INSERT INTO city (name, country_id) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING RETURNING city_id",
                    (city, country_id))
                result = source_cur.fetchone()
                city_id = result[0] if result else None
            else:
                city_id = None

            # Insert target type if not None
            if target_type:
                source_cur.execute(
                    "INSERT INTO target_type (type) VALUES (%s) ON CONFLICT (type) DO NOTHING RETURNING target_type_id",
                    (target_type,))
                result = source_cur.fetchone()
                target_type_id = result[0] if result else None
            else:
                target_type_id = None

            # Insert industry if not None
            if industry:
                source_cur.execute(
                    "INSERT INTO target_industry (industry) VALUES (%s) ON CONFLICT (industry) DO NOTHING RETURNING industry_id",
                    (industry,))
                result = source_cur.fetchone()
                industry_id = result[0] if result else None
            else:
                industry_id = None

            # Insert target with mission_id if latitude, longitude, and city_id are available
            if latitude and longitude and city_id:
                source_cur.execute("""
                    INSERT INTO target (target_priority, latitude, longitude, city_id, target_type_id, industry_id, mission_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING target_id
                """, (priority, latitude, longitude, city_id, target_type_id, industry_id, mission_id))
                target_id = source_cur.fetchone()[0]

        # Commit the transaction
        source_conn.commit()
        print("Data transferred and updated successfully in wwii_missions database.")

        # Close connections
        source_cur.close()
        source_conn.close()

    except Exception as e:
        print(f"Error transferring data: {e}")


def main_seed():
    # Step 1: Create the normalized tables
    create_normalized_tables()

    # Step 2: Transfer data from the existing 'mission' table to the new normalized tables
    transfer_data()
