from typing import List

from returns.maybe import Maybe
from returns.result import Success, Failure, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from config.base import session_factory
from model.Mission import Mission
from model.Target import Target
from model.City import City

def get_all_missions() -> Result[List[dict], str]:
    with session_factory() as session:
        try:
            # Query all targets with their associated mission, city, country, and target_type
            targets = session.query(Target).options(
                joinedload(Target.mission),
                joinedload(Target.city)
                .joinedload(City.country),
                joinedload(Target.target_type),
                joinedload(Target.industry)
            ).all()

            # Build the response list
            target_list = []
            for target in targets:
                if target.mission:
                    mission_data = {
                        'mission_id': target.mission.mission_id,
                        'mission_date': target.mission.mission_date,
                        'air_force': target.mission.air_force
                    }
                else:
                    mission_data = None

                target_data = {
                    'target_id': target.target_id,
                    'priority': target.target_priority,
                    'coordinates': {
                        'latitude': target.latitude,
                        'longitude': target.longitude
                    },
                    'city': target.city.name if target.city else None,
                    'country': target.city.country.name if target.city and target.city.country else None,
                    'type': target.target_type.type if target.target_type else None,  # Target type
                    'industry': target.industry.industry if target.industry else None,
                    'mission': mission_data
                }

                target_list.append(target_data)

            return Success(target_list)

        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))



def get_mission_by_id(mission_id: int) -> Maybe[dict, str]:
    with session_factory() as session:
        try:
            # Query for the specific mission with its associated target, city, and country
            mission = session.query(Mission).options(
                joinedload(Mission.target)
                .joinedload(Target.city)
                .joinedload(City.country),
                joinedload(Target.target_type),
                joinedload(Target.industry)
            ).filter(Mission.mission_id == mission_id).one_or_none()

            if mission:
                mission_data = {
                    'mission_id': mission.mission_id,
                    'mission_date': mission.mission_date,
                    'air_force': mission.air_force,
                    'target': {
                        'city': mission.target.city.name if mission.target and mission.target.city else None,
                        'country': mission.target.city.country.name if mission.target and mission.target.city and mission.target.city.country else None,
                        'type': mission.target.target_type.type if mission.target and mission.target.target_type else None,
                        'industry': mission.target.industry.industry if mission.target and mission.target.industry else None,
                        'priority': mission.target.target_priority if mission.target else None,
                        'coordinates': {
                            'latitude': mission.target.latitude if mission.target else None,
                            'longitude': mission.target.longitude if mission.target else None
                        }
                    }
                }
                return Success(mission_data)
            else:
                return Failure(f"No mission found with id {mission_id}")

        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))
