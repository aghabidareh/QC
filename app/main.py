from pathlib import Path

from fastapi import FastAPI, applications, Request, HTTPException, status
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware

from api.database.database import database
from api.v1_0.profiles.routes import profile_router
from api.v1_0.vendors.routes import vendor_router

from backbone_auth_sdk.auth_sdk import AsyncAuth
import time

token_cache = {}
DEFAULT_CACHE_TTL_IN_SECONDS = 365 * 24 * 60 * 60

auth = AsyncAuth(
    secret=os.getenv("BASALAM_AUTH_SECRET"),
)

app = FastAPI(title="QC",
              description="API for QC(q-commerce) project for basalam",
              version="1.0", )


@app.middleware("https")
async def auth_middleware(request: Request, call_next):
    public_paths = ["/", "/hello/", "/docs", "/redoc", "/openapi.json", "/static"]
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else auth_header
    cache_key = "who-am-i:" + token

    try:
        current_time = time.time()
        if cache_key in token_cache:
            cached_data = token_cache[cache_key]
            if cached_data["expiry"] > current_time:
                user = cached_data["user"]
            else:
                del token_cache[cache_key]
                user = None
        else:
            user = None

        if not user:
            user = await auth.who_am_i(token)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            token_cache[cache_key] = {
                "user": user,
                "expiry": current_time + DEFAULT_CACHE_TTL_IN_SECONDS
            }

        request.state.user = user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response = await call_next(request)
    return response


"Routes will be defined here"
app.include_router(vendor_router)
app.include_router(profile_router)

CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "QC"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name} from QC"}


BASE_DIR = Path(__file__).resolve().parent
static_path = os.path.join(BASE_DIR, 'resources')

app.mount("/static", StaticFiles(directory=static_path), name="static")


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )


applications.get_swagger_ui_html = swagger_monkey_patch
