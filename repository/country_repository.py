# Create a new country
from model.Country import Country





def create_country(session, country_name):
    new_country = Country(name=country_name)
    session.add(new_country)
    session.commit()
    return new_country

def get_country_by_id(session, country_id):
    return session.query(Country).filter_by(country_id=country_id).first()

def get_country_by_name(session, country_name):
    return session.query(Country).filter_by(name=country_name).first()

# Update a country
def update_country(session, country_id, new_name):
    country = session.query(Country).filter_by(country_id=country_id).first()
    if country:
        country.name = new_name
        session.commit()
        return country
    return None

# Delete a country
def delete_country(session, country_id):
    country = session.query(Country).filter_by(country_id=country_id).first()
    if country:
        session.delete(country)
        session.commit()
        return True
    return False
