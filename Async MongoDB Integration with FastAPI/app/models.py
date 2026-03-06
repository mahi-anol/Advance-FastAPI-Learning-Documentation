from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime

class NoteCreate(BaseModel):
    title: str=Field(...,min_length=1,max_lengrh=200,description="Note title")
    content: str=Field(...,min_length=1,description="Note content")
    tags: 