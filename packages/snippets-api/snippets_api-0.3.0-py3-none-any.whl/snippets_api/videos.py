from pydantic import BaseModel

class PendingVideo(BaseModel):
    title: str
    description: str
    url: str
