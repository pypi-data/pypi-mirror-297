from pydantic import BaseModel
from snippets_api.snippets import Snippet

class PendingVideo(BaseModel):
    id: str
    title: str
    description: str
    url: str
    snippet: Snippet
