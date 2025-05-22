from pydantic import BaseModel
from typing import List

class KeywordResponse(BaseModel):
    keywords: List[str]

class Relation(BaseModel):
    source: str
    relation: str
    target: str
    weight: float

class RelatedTermsResponse(BaseModel):
    term: str
    results: List[Relation]