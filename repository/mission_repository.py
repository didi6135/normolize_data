# from typing import List
#
# from returns.result import Success, Failure, Result
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import joinedload
#
# from config.base import session_factory
#
# from model.City import City
# from model.Target import Target
#
#
# def get_all_missions() -> Result[List[dict], str]:
#     with session_factory() as session:
#         try:
#             missions = session.query(Mission).options(
#                 joinedload(Mission.target)
#                 .joinedload(Target.city)
#                 .joinedload(City.country)
#             ).all()
#
#             # Build the response list
#             mission_list = []
#             for mission in missions:
#                 mission_data = {
#                     'mission_id': mission.mission_id,
#                     'mission_date': mission.mission_date,
#                     'target': {
#                         'city': mission.target.city.name if mission.target and mission.target.city else None,
#                         'country': mission.target.city.country.name if mission.target and mission.target.city and mission.target.city.country else None,
#                         'type': mission.target.target_type.type if mission.target and mission.target.target_type else None,
#                         'industry': mission.target.industry.industry if mission.target and mission.target.industry else None,
#                         'priority': mission.target.target_priority if mission.target else None,
#                         'coordinates': {
#                             'latitude': mission.target.latitude if mission.target else None,
#                             'longitude': mission.target.longitude if mission.target else None
#                         }
#                     }
#                 }
#                 mission_list.append(mission_data)
#
#             return Success(mission_list)
#
#         except SQLAlchemyError as e:
#             session.rollback()
#             return Failure(str(e))