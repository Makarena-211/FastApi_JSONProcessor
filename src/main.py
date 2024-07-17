import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from fastapi import FastAPI
from db_config import engine
import db
import applications
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event('startup')
async def startup():
    db.Base.metadata.create_all(bind=engine)

app.include_router(applications.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"])
