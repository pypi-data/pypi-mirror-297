# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi import status as st
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import OperationalError

from .__about__ import __version__
from .auth import api_auth, auth
from .backend import OAuth2Backend, OAuth2Middleware
from .conf import config
from .db import sessionmanager
from .routes import api_router, workflow
from .utils import get_logger

logger = get_logger("ddeutil.observe")

# NOTE: Initial sqlalchemy session maker object that create instance of current
#   database pointer from `OBSERVE_SQLALCHEMY_DB_ASYNC_URL` env var.
sessionmanager.init(config.OBSERVE_SQLALCHEMY_DB_ASYNC_URL)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan context function that make sure the session maker instance
    already close after respond the incoming request to the client.
    """
    async with sessionmanager.connect() as conn:
        await sessionmanager.create_all(conn)

    from .init import create_admin

    async with sessionmanager.session() as session:
        await create_admin(session)

    # NOTE: Start release application.
    yield

    if sessionmanager.is_opened():
        await sessionmanager.close()


app = FastAPI(
    titile="Observe Web Application",
    version=__version__,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# NOTE: Add oauth2 backend middleware.
app.add_middleware(OAuth2Middleware, backend=OAuth2Backend())


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Custom process time middleware."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(OperationalError)
async def sqlalchemy_exception_handler(_: Request, exc) -> PlainTextResponse:
    """Exception handler for SQLAlchemy package that get the error from the
    backend database.
    """
    return PlainTextResponse(
        str(exc.detail),
        status_code=st.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# NOTE: Authentication
app.include_router(api_auth, prefix=config.API_PREFIX)
app.include_router(auth)

# NOTE: Any routers
app.include_router(api_router, prefix=config.API_PREFIX)
app.include_router(workflow)

# NOTE: Start mount all static files from /static path to this application.
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home(request: Request):
    """The home page that redirect to main page."""
    return RedirectResponse(
        request.url_for("read_workflows"),
        status_code=st.HTTP_307_TEMPORARY_REDIRECT,
    )
