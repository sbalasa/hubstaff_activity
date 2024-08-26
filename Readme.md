# Hubstaff Activity Report

This project generates a daily (1am) activity report for Hubstaff Employees using Python and Docker.

## Prerequisites

- Docker
- Docker Compose

## Organization of interest

To generate a report for a specific organization, update the `org id` in the `config.ini` file with the desired organization's identifier.

## Running the Project

1. **Build and run the project using Docker Compose:**

   ```sh
   docker-compose up --build
   ```

2. **To check the cron output:**

   ```sh
   docker ps
   docker exec -it <container_id> cat /app/cron.log
   ```
