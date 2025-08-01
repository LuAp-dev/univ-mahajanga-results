#app/schemas/chatbot.py
from pydantic import BaseModel, StringConstraints
from typing import Annotated

class MatriculeRequest(BaseModel):
    matricule: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=3,
            max_length=20,
            pattern=r'^[A-Za-z0-9\-]+$'
        )
    ]

class ChatbotLoginRequest(BaseModel):
    matricule: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=3,
            max_length=20,
            pattern=r'^[A-Za-z0-9\-]+$'
        )
    ]
    password: Annotated[
        str,
        StringConstraints(min_length=3, max_length=128)
    ]
