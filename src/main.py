import aiohttp
import asyncio
import logging
import hubstaff_api
import logging.config

from yattag import Doc
from constants import LOG_PREFIX, LOG_CONFIG_PATH
from common import config, get_yesterday, format_time_spent


logging.config.fileConfig(LOG_CONFIG_PATH)
logger = logging.getLogger(__name__)


def render_html(employees, projects, activites):
    doc, tag, text = Doc().tagtext()
    with tag("html"):
        with tag("body"):
            with tag("table", border="1"):
                with tag("tr"):
                    with tag("th"):
                        text("Project / Employee")
                    for name in employees.values():
                        with tag("th"):
                            text(name)
                for project_id, project_name in projects.items():
                    with tag("tr"):
                        with tag("td"):
                            text(project_name)
                        for user_id in employees:
                            time_spent = sum(
                                activity["tracked"]
                                for activity in activites.get(
                                    (project_id, user_id), []
                                )
                            )
                            with tag("td"):
                                text(format_time_spent(time_spent))
    return doc.getvalue()


async def main():
    try:
        async with aiohttp.ClientSession() as session:
            organizations = await hubstaff_api.get_organizations(session)
            config_org_id = int(config["organization"]["id"])
            orgs = [org for org in organizations if org["id"] == config_org_id]

            if not orgs:
                logger.error(
                    f"{LOG_PREFIX} Configured Organization ID not found"
                )
                return

            org_id = orgs[0]["id"]
            projects = await hubstaff_api.get_projects(session, org_id)
            employees = await hubstaff_api.get_employees(session, org_id)
            yesterday = get_yesterday()
            activities = {}

            tasks = []
            for project_id in projects:
                for user_id in employees:
                    task = hubstaff_api.get_activities(
                        session, project_id, user_id, yesterday, yesterday
                    )
                    tasks.append((project_id, user_id, task))
            results = await asyncio.gather(*(task for _, _, task in tasks))
            activities = {
                (project_id, user_id): result
                for (project_id, user_id, _), result in zip(tasks, results)
            }

            html_output = render_html(employees, projects, activities)
            print(html_output)
    except Exception as e:
        logger.error(f"{LOG_PREFIX} Error in main function: {e}")


if __name__ == "__main__":
    asyncio.run(main())
