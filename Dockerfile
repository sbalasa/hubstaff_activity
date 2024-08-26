FROM python:3.10-slim
WORKDIR /app
COPY . /app

# Install cron
RUN apt-get update && apt-get install -y cron

# Add the cron job
COPY crontab /etc/cron.d/hubstaff-cron
RUN chmod 0644 /etc/cron.d/hubstaff-cron
RUN crontab /etc/cron.d/hubstaff-cron

RUN pip install --no-cache-dir -r requirements.txt --disable-pip-version-check --root-user-action=ignore

# Start cron and keep the container running
CMD ["/bin/sh", "-c", "cron && python src/main.py && tail -f /dev/null"]
