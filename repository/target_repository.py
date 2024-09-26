from returns.result import Failure, Success, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from config.base import session_factory
from model.City import City
from model.Target import Target


def get_all_targets():
    with session_factory() as session:
        try:
            # Query all targets with joined relationships to city, country, target_type, and industry
            targets = session.query(Target).options(
                joinedload(Target.city).joinedload(City.country),  # Join city and country
                joinedload(Target.target_type),  # Join target type
                joinedload(Target.industry)  # Join industry
            ).all()

            # Convert targets to a list of dictionaries with full details
            target_list = []
            for target in targets:
                target_data = {
                    'target_id': target.target_id,
                    'priority': target.target_priority,
                    'coordinates': {
                        'latitude': target.latitude,
                        'longitude': target.longitude
                    },
                    'city': {
                        'city_id': target.city.city_id,
                        'city_name': target.city.name,
                        'country': {
                            'country_id': target.city.country.country_id,
                            'country_name': target.city.country.name
                        } if target.city and target.city.country else None
                    } if target.city else None,
                    'target_type': {
                        'target_type_id': target.target_type.target_type_id,
                        'type': target.target_type.type
                    } if target.target_type else None,
                    'industry': {
                        'industry_id': target.industry.industry_id,
                        'industry_name': target.industry.industry
                    } if target.industry else None
                }
                target_list.append(target_data)

            return Success(target_list)  # Return the Success object containing the list of target details
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))



def create_target(target_data: dict) -> Result[dict, str]:
    with session_factory() as session:
        try:
            # Extract data from the request payload
            priority = target_data.get('priority')
            latitude = target_data.get('latitude')
            longitude = target_data.get('longitude')
            city_id = target_data.get('city_id')
            target_type_id = target_data.get('target_type_id')
            industry_id = target_data.get('industry_id')

            # Create a new Target object
            new_target = Target(
                target_priority=priority,
                latitude=latitude,
                longitude=longitude,
                city_id=city_id,
                target_type_id=target_type_id,
                industry_id=industry_id
            )

            # Add and commit the new target
            session.add(new_target)
            session.commit()

            # Return the new target's ID and details
            return Success({'target_id': new_target.target_id, 'message': 'Target created successfully'})

        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))



def update_target(target_id: int, target_data: dict) -> Result[dict, str]:
    with session_factory() as session:
        try:
            # Find the target by ID
            target = session.query(Target).filter_by(target_id=target_id).one_or_none()

            if not target:
                return Failure(f"No target found with id {target_id}")

            # Update the target's fields with new data
            target.target_priority = target_data.get('priority', target.target_priority)
            target.latitude = target_data.get('latitude', target.latitude)
            target.longitude = target_data.get('longitude', target.longitude)
            target.city_id = target_data.get('city_id', target.city_id)
            target.target_type_id = target_data.get('target_type_id', target.target_type_id)
            target.industry_id = target_data.get('industry_id', target.industry_id)

            # Commit the changes
            session.commit()

            return Success({'target_id': target.target_id, 'message': 'Target updated successfully'})

        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))



def delete_target(target_id: int) -> Result[dict, str]:
    with session_factory() as session:
        try:
            # Find the target by ID
            target = session.query(Target).filter_by(target_id=target_id).one_or_none()

            if not target:
                return Failure(f"No target found with id {target_id}")

            # Delete the target
            session.delete(target)
            session.commit()

            return Success({'target_id': target_id, 'message': 'Target deleted successfully'})

        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))
