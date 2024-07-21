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
import os
import subprocess
app = FastAPI(title="FastAPI Json Processor",
              description="""Приложение, которое производит операции с json\n
                /get - получает все записи из БД \n
                /post - записывает json в БД \n
                /get_state/{id} - получает параметр state по id из БД \n
                /delete/{id} - удаляет запись из БД по id \n
                /put/{id} - меняет параметр state на один из допущенных \n
                /change_spec/{kind}/{id}/{configuration} - меняет значение congiguration внутри json_data \n
                /update_settings/{id} - меняет значение settings внутри json_data
              """)


def start_kafka_consumers():
    threading.Thread(target=consume_messages, args=("application_grabbed", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_posted", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_state_recieved", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_deleted", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_state_updated", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_specification_updated", ), daemon=True).start()
    threading.Thread(target=consume_messages, args=("application_settings_updated", ), daemon=True).start()



def create_json_schema():
    output_file = "./model.py"
    if os.path.getsize(output_file) == 0:
        command = r"datamodel-codegen --input ../schema.json --input-file-type jsonschema --output ./model.py"
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print("The exit code was: %d" % result.returncode)
        print("The output was:\n%s" % result.stdout)
    return None


@app.on_event('startup')
async def startup():
    db.Base.metadata.create_all(bind=engine)
    create_json_schema()


    

app.include_router(applications.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"])
