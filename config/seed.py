import psycopg2
from sqlalchemy import create_engine
from model import City, Country, Target, TargetIndustry, TargetType

from config.base import Base


# Step 1: Create the normalized tables in the existing wwii_missions database
def create_normalized_tables():
    try:
        DATABASE_URI = 'postgresql://postgres:1234@localhost/wwii_missions'
        engine = create_engine(DATABASE_URI)

        # Create all normalized tables (excluding 'mission' because it already exists)
        Base.metadata.create_all(engine)
        print("Normalized tables created successfully in wwii_missions database.")

    except Exception as e:
        print(f"Error creating tables: {e}")


# Step 2: Transfer data from the unnormalized 'mission' table to the new normalized schema
def transfer_data():
    try:
        # Connect to both the source (existing wwii_missions) and the target (wwii_missions with normalized tables)
        source_conn = psycopg2.connect(dbname="wwii_missions", user="postgres", password="1234", host="localhost")

        source_cur = source_conn.cursor()

        # Fetch the relevant data from the source 'mission' table
        source_cur.execute("""
            SELECT DISTINCT target_country, target_city, target_type, target_industry, target_priority, target_latitude, target_longitude, mission_date
            FROM mission
        """)
        rows = source_cur.fetchall()

        # Insert the normalized data into the new database
        for row in rows:
            country, city, target_type, industry, priority, latitude, longitude, mission_date = row

            # Insert country only if it is not None
            if country:
                source_cur.execute(
                    "INSERT INTO country (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING country_id",
                    (country,))
                country_id = source_cur.fetchone()
            else:
                country_id = None

            # Insert city only if it is not None and country_id exists
            if city and country_id:
                source_cur.execute(
                    "INSERT INTO city (name, country_id) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING RETURNING city_id",
                    (city, country_id))
                city_id = source_cur.fetchone()
            else:
                city_id = None

            # Insert target type only if it is not None
            if target_type:
                source_cur.execute(
                    "INSERT INTO target_type (type) VALUES (%s) ON CONFLICT (type) DO NOTHING RETURNING target_type_id",
                    (target_type,))
                target_type_id = source_cur.fetchone()
            else:
                target_type_id = None

            # Insert industry only if it is not None
            if industry:
                source_cur.execute(
                    "INSERT INTO target_industry (industry) VALUES (%s) ON CONFLICT (industry) DO NOTHING RETURNING industry_id",
                    (industry,))
                industry_id = source_cur.fetchone()
            else:
                industry_id = None

            # Insert target only if latitude, longitude, and city_id are available
            if latitude and longitude and city_id:
                source_cur.execute("""
                    INSERT INTO target (target_priority, latitude, longitude, city_id, target_type_id, industry_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING target_id
                """, (priority, latitude, longitude, city_id, target_type_id, industry_id))
                target_id = source_cur.fetchone()
            else:
                target_id = None



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
