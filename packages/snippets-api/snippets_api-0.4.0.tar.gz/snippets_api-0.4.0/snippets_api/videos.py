from pydantic import BaseModel
from snippets_api.snippets import Snippet

class PendingVideo(BaseModel):
    title: str
    description: str
    url: str
    snippet: Snippet
