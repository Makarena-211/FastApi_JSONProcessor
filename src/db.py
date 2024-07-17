import psycopg2
from db_config import Base
from sqlalchemy import Column, String, Enum, JSON, Text
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType

class Applications(Base):
    __tablename__ = 'applications'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kind = Column(String(32))
    name = Column(String(128))
    version = Column(String(50))
    description = Column(Text)
    state = Column(Enum('NEW', 'INSTALLING', 'RUNNING', name='app_state'), default='NEW')
    json_data = Column(JSON)