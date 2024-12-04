from datetime import datetime
from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field, model_validator
from model.objectId_str import ObjectIdStr


class Status(Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    DELETED = 'DELETED'


class Audit(BaseModel):
    id: ObjectIdStr = Field(default_factory=ObjectId, alias="_id")
    createdAt: datetime = Field(default_factory=datetime.now)
    modifiedAt: datetime
    version: int = Field(default=1)
    status: str = Field(default=Status.ACTIVE.value)

    @model_validator(mode='before')
    def handle_datetime_and_string(cls, values):
        for field in ['createdAt', 'modifiedAt']:
            if field in values:
                value = values[field]
                if isinstance(value, str):
                    try:
                        values[field] = datetime.fromisoformat(value)
                    except ValueError:
                        raise ValueError(f"Invalid ISO 8601 date string: {value}")
        return values

    @model_validator(mode='before')
    def update_fields(cls, values):
        values['modifiedAt'] = datetime.now()
        if 'version' in values:
            values['version'] += 1
        return values

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True


class AuditBasic(BaseModel):
    createdAt: datetime = Field(default_factory=datetime.now)
    modifiedAt: datetime = Field(default_factory=datetime.now)
    version: int = Field(default=1)

    @model_validator(mode='before')
    def update_fields(cls, values):
        if 'version' in values:
            values['version'] += 1
        return values

    @model_validator(mode='before')
    def handle_datetime_and_string(cls, values):
        for field in ['createdAt', 'modifiedAt']:
            if field in values:
                value = values[field]
                if isinstance(value, str):
                    try:
                        values[field] = datetime.fromisoformat(value)
                    except ValueError:
                        raise ValueError(f"Invalid ISO 8601 date string: {value}")
        return values

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True
