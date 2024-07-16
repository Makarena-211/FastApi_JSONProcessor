# generated by datamodel-codegen:
#   filename:  schema.json
#   timestamp: 2024-07-16T13:47:57+00:00

from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, constr
import json

class ExposedPort(BaseModel):
    name: str
    port: int
    protocol: str
    sharedNamespace: bool


class Log(BaseModel):
    level: str


class Specification(BaseModel):
    jvmConfig: List[str]
    exposedPorts: List[ExposedPort]
    log: Log
    environmentVariables: List[str]


class Settings(BaseModel):
    settingAaa: Dict[str, Any]
    settingAab: Dict[str, Any]


class Configuration(BaseModel):
    specification: Specification
    settings: Settings


class Application(BaseModel):
    kind: str
    name: str
    version: constr(regex=r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')
    description: str
    configuration: Configuration

# with open('data.json') as f:
#     doc = json.load(f)
#     #print(doc)

#     app = Application(kind=doc['kind'], name=doc['name'], version=doc['version'], description=doc['description'], configuration=doc['configuration'])
#     print(app)