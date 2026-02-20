from typing import Optional, List

from pydantic import BaseModel


class QueryRequest(BaseModel):
    input: str
    chat_history: Optional[List[dict]] = None

class QueryResponse(BaseModel):
    output: str