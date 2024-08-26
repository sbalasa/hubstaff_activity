import os
import sys
import asyncio
import unittest
import configparser


# Add src to the path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from main import render_html
from unittest.mock import patch, MagicMock
from hubstaff_api import (
    get_organizations,
    get_projects,
    get_employees,
    get_activities,
)

# Load the config.ini file
CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config.ini")
)
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Mock the config object in common.py
import common

common.config = config


class TestHubstaffActivity(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    @patch("src.hubstaff_api.get_organizations")
    async def test_get_organizations(self, mock_get_organizations):
        mock_get_organizations.return_value = asyncio.Future()
        mock_get_organizations.return_value.set_result(
            [{"id": 1, "name": "Org 1"}, {"id": 2, "name": "Org 2"}]
        )
        organizations = await get_organizations(MagicMock())
        self.assertEqual(len(organizations), 2)
        self.assertEqual(organizations[0]["id"], 1)
        self.assertEqual(organizations[1]["id"], 2)

    @patch("src.hubstaff_api.get_projects")
    async def test_get_projects(self, mock_get_projects):
        mock_get_projects.return_value = asyncio.Future()
        mock_get_projects.return_value.set_result(
            {1: "Project A", 2: "Project B"}
        )
        projects = await get_projects(MagicMock(), 1)
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects[1], "Project A")
        self.assertEqual(projects[2], "Project B")

    @patch("src.hubstaff_api.get_employees")
    async def test_get_employees(self, mock_get_employees):
        mock_get_employees.return_value = asyncio.Future()
        mock_get_employees.return_value.set_result(
            {1: "Employee 1", 2: "Employee 2"}
        )
        employees = await get_employees(MagicMock(), 1)
        self.assertEqual(len(employees), 2)
        self.assertEqual(employees[1], "Employee 1")
        self.assertEqual(employees[2], "Employee 2")

    @patch("src.hubstaff_api.get_activities")
    async def test_get_activities(self, mock_get_activities):
        mock_get_activities.return_value = asyncio.Future()
        mock_get_activities.return_value.set_result(
            [{"tracked": 3600}, {"tracked": 1800}]
        )
        activities = await get_activities(
            MagicMock(), 1, 1, "2023-04-01", "2023-04-01"
        )
        self.assertEqual(len(activities), 2)
        self.assertEqual(activities[0]["tracked"], 3600)
        self.assertEqual(activities[1]["tracked"], 1800)

    def test_render_html(self):
        employees = {1: "Employee 1", 2: "Employee 2"}
        projects = {1: "Project A", 2: "Project B"}
        activities = {
            (1, 1): [{"tracked": 3600}],
            (1, 2): [{"tracked": 1800}],
            (2, 1): [{"tracked": 7200}],
            (2, 2): [{"tracked": 900}],
        }
        html_output = render_html(employees, projects, activities)
        self.assertIn("Project A", html_output)
        self.assertIn("Project B", html_output)
        self.assertIn("Employee 1", html_output)
        self.assertIn("Employee 2", html_output)
        self.assertIn("01:00:00", html_output)
        self.assertIn("00:30:00", html_output)
        self.assertIn("02:00:00", html_output)
        self.assertIn("00:15:00", html_output)


if __name__ == "__main__":
    unittest.main()
