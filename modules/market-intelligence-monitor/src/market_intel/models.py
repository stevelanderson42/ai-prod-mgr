from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class EvidenceItem(BaseModel):
    id: str
    title: str
    url: HttpUrl
    source: str
    published_at: Optional[datetime] = None

    content_text: str = ""
    summary_text: str = ""

    tags: List[str] = Field(default_factory=list)
    credibility: int = 0
    relevance: int = 0
