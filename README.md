# TorrentBD API

Unofficial API for TorrentBD that provides search and profile endpoints.

## Disclaimer

This project is an unofficial API and is not affiliated with, endorsed by, or connected to TorrentBD. Use at your own risk and responsibility. The developers are not responsible for any misuse of this software.

## Installation

```bash
pip install tbd-api
```

## Usage

```bash
tbd-api
```

API available at http://localhost:5000

## Endpoints

- `/search?query=term&page=1` - Search torrents
- `/profile` - Get user profile

## Docker

```bash
docker build -t tbd-api .
docker run --env-file .env -p 5000:5000 tbd-api
```
