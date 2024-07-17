#routes

from fastapi import HTTPException, Depends, APIRouter, status
import db
from sqlalchemy.orm import session
from db_config import get_db
from uuid import UUID
import schema
from typing import Dict
import models
from pydantic import ValidationError
from sqlalchemy.orm.attributes import flag_modified
router = APIRouter()


@router.get('/get')
def get_from_db(database: session=Depends(get_db)):
    applications = database.query(db.Applications).all()
    return {'data':applications}

@router.post('/post', response_model=schema.ApplicationResponse)
def write_to_db(data: models.Application, database: session = Depends(get_db)):
    new_app = db.Applications(
        kind=data.kind,
        name=data.name,
        version=data.version,
        description=data.description,
        json_data=data.dict()
    )
    database.add(new_app)
    database.commit()
    database.refresh(new_app)
    
    return new_app

@router.get('/get_state/{id}')
def get_state_from_app(id: UUID, database: session=Depends(get_db)):
    application = database.query(db.Applications).filter(db.Applications.id == id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return {"state": application.state}

@router.delete('/delete/{id}')
def delete_app_from_db(id:UUID, database:session=Depends(get_db)):
    application = database.query(db.Applications).filter(db.Applications.id == id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    database.delete(application)
    database.commit()
    return database

@router.put('/put/{id}')
def change_app_state(id:UUID, state:str, database:session=Depends(get_db)):
    application = database.query(db.Applications).filter(db.Applications.id == id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    application.state = state
    database.commit()
    return {"Message": "State changed successfully!"}, database


@router.put('/change_spec/{kind}/{id}/{configuration}')
def change_specification(id: UUID, specification: Dict, database: session = Depends(get_db)):
    application = database.query(db.Applications).filter(db.Applications.id == id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    try:
        new_specification = models.Specification(**specification)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    application.json_data["configuration"]["specification"] = new_specification.dict()
    flag_modified(application, "json_data")
    database.commit()

    return application

@router.put("/update_settings/{id}", response_model=schema.ApplicationResponse)
def update_settings(id: UUID, settings:Dict, database: session = Depends(get_db)):
    application = database.query(db.Applications).filter(db.Applications.id == id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    try:
        new_settings = models.Settings(**settings)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    application.json_data["configuration"]["settings"] = new_settings.dict()
    flag_modified(application, "json_data")
    database.commit()
    
    return application



