from pydantic import BaseModel
from typing import List

class Idea(BaseModel):
    idea: str
    tags: List[str]
    inspiration: str

IdeaList = List[Idea] 