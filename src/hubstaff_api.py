import logging
import logging.config

from common import get_headers
from constants import LOG_PREFIX, LOG_CONFIG_PATH


logging.config.fileConfig(LOG_CONFIG_PATH)
logger = logging.getLogger(__name__)


async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        return await response.json()


async def get_organizations(session):
    try:
        url = "https://mutator.reef.pl/v442/institution"
        headers = get_headers()
        response = await fetch(session, url, headers)
        return response["organizations"]
    except Exception as e:
        logger.error(f"{LOG_PREFIX} Error fetching organizations: {e}")
        return []


async def get_projects(session, org_id):
    try:
        url = f"https://mutator.reef.pl/v442/institution/{org_id}/subproject"
        headers = get_headers()
        response = await fetch(session, url, headers)
        return {
            project["id"]: project["name"] for project in response["projects"]
        }
    except Exception as e:
        logger.error(
            f"{LOG_PREFIX} Error fetching projects for organization {org_id}: {e}"
        )
        return {}


async def get_employee_name(session, user_id):
    try:
        url = f"https://mutator.reef.pl/v442/employee/{user_id}"
        headers = get_headers()
        response = await fetch(session, url, headers)
        return response["user"]["name"]
    except Exception as e:
        logger.error(
            f"{LOG_PREFIX} Error fetching employee name for user_id {user_id}: {e}"
        )
        return {}


async def get_employees(session, org_id):
    try:
        url = f"https://mutator.reef.pl/v442/institution/594481/staff_members"
        headers = get_headers()
        response = await fetch(session, url, headers)
        return {
            member["user_id"]: await get_employee_name(
                session, member["user_id"]
            )
            for member in response["members"]
        }
    except Exception as e:
        logger.error(
            f"{LOG_PREFIX} Error fetching employees for organization {org_id}: {e}"
        )
        return {}


async def get_activities(session, project_id, user_id, date_start, date_stop):
    try:
        headers = get_headers()
        headers["DateStart"] = date_start
        url = f"https://mutator.reef.pl/v442/subproject/{project_id}/operations/daily?date[stop]={date_stop}"
        headers = headers
        response = await fetch(session, url, headers)
        return response["daily_activities"]
    except Exception as e:
        logger.error(
            f"{LOG_PREFIX} Error fetching activites for project {project_id} and user {user_id} from {date_start} to {date_stop}: {e}"
        )
        return {}
