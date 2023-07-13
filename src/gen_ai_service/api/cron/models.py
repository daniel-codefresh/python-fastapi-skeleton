from pydantic import BaseModel


class CronPrompt(BaseModel):
    text: str
