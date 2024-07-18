import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from fastapi import FastAPI
from db_config import engine
import db
import applications
from fastapi.middleware.cors import CORSMiddleware
import threading
from kafka.kafka_consumer import consume_messages
app = FastAPI()

def start_kafka_consumers():
    threading.Thread(target=consume_messages, args=("application_grabbed", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_posted", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_state_recieved", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_deleted", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_state_updated", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_specification_updated", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_settings_updated", ), daemon=True).start()

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
