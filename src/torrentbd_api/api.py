import pathlib
from typing import Any

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .profile import get_user_profile
from .search import search_torrents
from .version import __version__

app = FastAPI(
    title="TorrentBD API",
    version=__version__,
    description="Unofficial API for TorrentBD",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount static files directory
static_dir = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage() -> FileResponse:
    """Serve the HTML homepage"""
    html_file = static_dir / "index.html"
    return FileResponse(html_file)


@app.get("/api")
def root() -> dict[str, Any]:
    return {
        "info": {
            "title": "TorrentBD API",
            "version": __version__,
            "description": "Unofficial API for TorrentBD",
        },
        "endpoints": {
            "search": {
                "path": "/search",
                "method": "GET",
                "description": "Search for torrents on TorrentBD",
            },
            "profile": {
                "path": "/profile",
                "method": "GET",
                "description": "Get user profile information",
            },
        },
        "documentation": {"swagger": "/docs", "redoc": "/redoc"},
    }


@app.get("/search")
def search(
    query: str = Query(..., description="Search term"), page: int = 1
) -> dict[str, Any]:
    """Search for torrents on TorrentBD."""
    result = search_torrents(query, page)
    return {"result": result}


@app.get("/profile")
def profile() -> dict[str, Any]:
    """Get user profile information."""
    result = get_user_profile()
    return {"result": result}
