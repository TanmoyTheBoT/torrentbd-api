FROM python:3.12-slim

# Basic environment setup for v3cap
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV DISPLAY=:99

# Install Chrome and essential dependencies only for v3cap
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy files and install package
COPY . /app
RUN pip install --no-cache-dir .

EXPOSE 5000

CMD ["tbd-api"] 