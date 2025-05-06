FROM python:3.12-slim

# Install Chrome for captcha solving
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Setup app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir .
RUN mkdir -p /root/.config/tbd-api

EXPOSE 5000
ENTRYPOINT ["tbd-api"] 