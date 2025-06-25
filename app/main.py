from pathlib import Path

from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import os

from api.v1_0.routes.vendors import vendor_router

app = FastAPI(title="QC",
              description="API for QC(q-commerce) project for basalam",
              version="1.0",)

app.include_router(vendor_router)

BASE_DIR = Path(__file__).resolve().parent
static_path = os.path.join(BASE_DIR, 'resources')

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}




app.mount("/static", StaticFiles(directory=static_path), name="static")


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )


applications.get_swagger_ui_html = swagger_monkey_patch