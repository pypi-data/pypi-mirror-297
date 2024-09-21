from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional, Any


class ApiResponse(BaseModel):
    """
    Base API response model
    """
    result: bool
    message: str


class ErrorResponse(ApiResponse):
    """
    Base error API response model
    """
    exception_type: str
    validation_errors: Optional[List[Dict[str, Any]]] = None


class TokenRequest(BaseModel):
    """
    Token request model
    """
    username: str
    password: str

    @field_validator('username')
    def validate_username(cls, value):
        if not value:
            raise ValueError('El campo es requerido')
        # Verificar longitud del campo
        if not (4 <= len(value) <= 21):
            raise ValueError('El nombre de usuario debe tener de 5 a 20 caracteres')
        return value

    @field_validator('password')
    def validate_password(cls, value):
        if not value:
            raise ValueError('El campo es requerido')
        # Verificar longitud del campo
        if not (4 <= len(value) <= 21):
            raise ValueError('La contraseña debe tener de 5 a 20 caracteres')
        return value


class TokenResponse(ApiResponse):
    """
    Token response model
    """
    token: str
    token_type: str
