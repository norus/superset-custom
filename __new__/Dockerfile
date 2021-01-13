FROM apache/incubator-superset

# Switching to root to install the required packages
USER root

# Install any extra database drivers and other deps
COPY ./requirements.txt /app
RUN pip install -r /app/requirements.txt
#RUN pip install sqlalchemy-clickhouse

# Install Geckodriver for Email Dashboard reports
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
        firefox-esr \
        libgtk-3-0 \
        xvfb \
    && rm -rf /var/lib/apt/lists/*
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.28.0/geckodriver-v0.28.0-linux64.tar.gz
RUN tar -x geckodriver -zf geckodriver-v0.28.0-linux64.tar.gz -O > /usr/bin/geckodriver
RUN chmod +x /usr/bin/geckodriver

# Switching back to using the `superset` user
#USER superset
# Needed for Geckodriver
RUN Xvfb :10 -ac &
RUN export DISPLAY=:10
