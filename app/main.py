from pathlib import Path

from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import os
from fastapi.middleware.cors import CORSMiddleware

from api.database.database import database
from api.v1_0.UI.vendors.routes import vendor_ui_router
from api.v1_0.main.profiles.routes import profile_main_router
from api.v1_0.main.vendors.routes import vendor_main_router

app = FastAPI(title="QC",
              description="API for QC(q-commerce) project for basalam",
              version="1.0", )

### UI Rotes
app.include_router(vendor_ui_router)


### Main Routes
app.include_router(vendor_main_router)
app.include_router(profile_main_router)

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
