FROM python:3.12-slim

# Install Chrome for captcha solving
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Setup app
WORKDIR /app
COPY . /app
COPY --from=ghcr.io/astral-sh/uv:0.8.8 /uv /uvx /bin/
RUN uv sync --locked
RUN mkdir -p /root/.config/tbd-api

EXPOSE 5000
ENTRYPOINT ["uv", "run", "tbd-api"]
