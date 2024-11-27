from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.schema import json_scheme
from sqlalchemy import Column
from datetime import datetime

class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                'username': "rajiniyaz",
                'email': "rajiniyaz5@gmail.com",
                'password': "password12345",
            }
        }
    )

class Settings(BaseModel):  # Исправлено имя
    authjwt_secret_key: str = '4b4312209a72fcc5aa2c0a533b005a82f9b3492f118e0f71ce7a02d36aff92b6'

class LoginModel(BaseModel):
    username_or_email: str
    password: str

class DebtModel(BaseModel):
    id: Optional[int] = None
    debt_types: str
    first_name: str
    last_name: str
    quantity: int
    valuta: Optional[str] = 'UZS'
    description: Optional[str] = None
    data_incurred: str
    data_due: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "first_name": 'Ajiniyaz',
                "last_name": 'Reymov',
                "debt types": "OWED_TO",
                "quantity": 50000,
                "data_incurred": "2024-11-25T00:00:00"
            }
        }
    )


class DebtStatusModel(BaseModel):
    debt_types: Optional[str] = 'OWED_TO'

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                'debt_types': 'OWED_TO'
            }
        }
    )