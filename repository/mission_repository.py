from typing import List

from returns.result import Success, Failure, Result
from sqlalchemy.exc import SQLAlchemyError
from config.base import session_factory
from model.Mission import Mission



def get_all_missions() -> Result[List[Mission], str]:
    with session_factory() as session:
        try:
            # Query all missions
            missions = session.query(Mission).all()
            missions_list = [
                {
                    "mission_id": mission.mission_id,
                    "mission_date": mission.mission_date,
                    "theater_of_operations": mission.theater_of_operations,
                    "air_force": mission.air_force,
                    "mission_type": mission.mission_type,
                    "target_country": mission.target_country,
                    "target_city": mission.target_city,
                    "target_type": mission.target_type,
                    "airborne_aircraft": mission.airborne_aircraft,
                    "bomb_damage_assessment": mission.bomb_damage_assessment,
                }
                for mission in missions
            ]
            return Success(missions_list)
        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))



def get_mission_by_id(mission_id: int) -> Result[dict, str]:
    with session_factory() as session:
        try:
            # Query the mission with the given mission_id
            mission = session.query(Mission).filter(Mission.mission_id == mission_id).one_or_none()

            if mission:
                mission_data = {
                    "mission_id": mission.mission_id,
                    "mission_date": mission.mission_date,
                    "theater_of_operations": mission.theater_of_operations,
                    "air_force": mission.air_force,
                    "mission_type": mission.mission_type,
                    "target_country": mission.target_country,
                    "target_city": mission.target_city,
                    "target_type": mission.target_type,
                    "airborne_aircraft": mission.airborne_aircraft,
                    "bomb_damage_assessment": mission.bomb_damage_assessment,
                }
                return Success(mission_data)
            else:
                return Failure(f"Mission with id {mission_id} not found")

        except SQLAlchemyError as e:
            session.rollback()
            return Failure(str(e))
