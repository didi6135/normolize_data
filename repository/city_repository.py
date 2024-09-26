# Create a new city
from model.City import City


def create_city(session, city_name, country_id):
    new_city = City(name=city_name, country_id=country_id)
    session.add(new_city)
    session.commit()
    return new_city

# Read (get) a city by ID or name
def get_city_by_id(session, city_id):
    return session.query(City).filter_by(city_id=city_id).first()

def get_city_by_name(session, city_name):
    return session.query(City).filter_by(name=city_name).first()

# Update a city
def update_city(session, city_id, new_name, new_country_id=None):
    city = session.query(City).filter_by(city_id=city_id).first()
    if city:
        city.name = new_name
        if new_country_id:
            city.country_id = new_country_id
        session.commit()
        return city
    return None

# Delete a city
def delete_city(session, city_id):
    city = session.query(City).filter_by(city_id=city_id).first()
    if city:
        session.delete(city)
        session.commit()
        return True
    return False
